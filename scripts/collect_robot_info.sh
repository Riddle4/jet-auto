#!/usr/bin/env bash
set -u

section() {
  printf '\n===== %s =====\n' "$1"
}

run() {
  printf '\n$ %s\n' "$*"
  "$@" 2>&1 || true
}

run_shell() {
  printf '\n$ %s\n' "$1"
  bash -lc "$1" 2>&1 || true
}

section "Collection metadata"
run date -Is
run whoami
run hostname
run pwd

section "OS and kernel"
run hostnamectl
run uname -a
run cat /etc/os-release
run_shell 'cat /etc/nv_tegra_release 2>/dev/null || true'
run_shell 'dpkg-query -W "nvidia-l4t*" "nvidia-jetpack" 2>/dev/null || true'

section "Hardware"
run_shell 'cat /proc/device-tree/model 2>/dev/null | tr "\0" "\n" || true'
run_shell 'cat /proc/meminfo | sed -n "1,12p"'
run free -h
run lscpu
run lsblk -f
run df -h
run_shell 'command -v tegrastats >/dev/null && timeout 5 tegrastats || true'

section "NVIDIA and accelerators"
run_shell 'command -v nvidia-smi >/dev/null && nvidia-smi || true'
run_shell 'ls -la /dev/nv* /dev/video* /dev/ttyUSB* /dev/ttyACM* /dev/i2c-* 2>/dev/null || true'

section "Network"
run ip addr
run ip route
run resolvectl status
run_shell 'ss -tulpn 2>/dev/null || ss -tuln'

section "Users and SSH"
run_shell 'getent passwd | awk -F: '\''$3 >= 1000 && $3 < 65534 {print $1 ":" $3 ":" $6 ":" $7}'\'''
run_shell 'ls -la ~/.ssh 2>/dev/null || true'
run systemctl status ssh --no-pager

section "Services"
run systemctl --type=service --state=running --no-pager
run systemctl --type=service --state=failed --no-pager
run_shell 'systemctl list-unit-files --no-pager | grep -Ei "ros|robot|jet|vnc|cups|docker|container|ssh|lidar|camera|joy|bringup|start" || true'

section "Processes"
run_shell 'ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | sed -n "1,80p"'

section "Packages of interest"
run_shell 'dpkg-query -W "ros-*" 2>/dev/null | sed -n "1,240p"'
run_shell 'dpkg-query -W "*orbbec*" "*realsense*" "*opencv*" "*cuda*" "*cudnn*" "*tensorrt*" "*docker*" 2>/dev/null | sed -n "1,240p"'

section "Workspaces and source trees"
run_shell 'find "$HOME" -maxdepth 4 \( -name "install" -o -name "src" -o -name "*.launch.py" -o -name "package.xml" \) 2>/dev/null | sed -n "1,240p"'
run_shell 'find /home -maxdepth 5 \( -name "*.launch.py" -o -name "package.xml" -o -name "*.yaml" \) 2>/dev/null | sed -n "1,320p"'

section "Environment"
run_shell 'env | sort'
run_shell 'ls -la ~'
run_shell 'sed -n "1,220p" ~/.bashrc 2>/dev/null || true'

section "ROS environment"
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; env | grep -E "^(ROS|RMW|AMENT|COLCON)" | sort'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; ros2 doctor --report 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; ros2 node list 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; ros2 topic list -t 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; ros2 service list -t 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; ros2 action list -t 2>/dev/null || true'

section "ROS samples"
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; timeout 4 ros2 topic echo /ros_robot_controller/battery --once 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; timeout 4 ros2 topic echo /imu --once 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; timeout 4 ros2 topic echo /odom --once 2>/dev/null || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; timeout 4 ros2 topic echo /scan --once 2>/dev/null | sed -n "1,180p" || true'
run_shell 'source /opt/ros/humble/setup.bash 2>/dev/null; timeout 4 ros2 topic echo /joint_states --once 2>/dev/null || true'

section "Containers"
run_shell 'command -v docker >/dev/null && docker ps -a || true'

section "Cron"
run_shell 'crontab -l 2>/dev/null || true'
run_shell 'ls -la /etc/cron* 2>/dev/null || true'
