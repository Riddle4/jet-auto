# Robot JetAuto / Jetson - 192.168.100.50

Date d'observation: 2026-06-04, depuis le reseau Cosmo-Robotics.

## Resume

Le robot repond a l'adresse `192.168.100.50`. Il s'agit d'un JetAuto base sur NVIDIA Jetson Orin Nano 8GB, avec Ubuntu 22.04.5 LTS, L4T R36.4.3, ROS 2 Humble, controleur moteur/servo, LiDAR 2D, IMU, odometrie, camera USB, camera RGB-D Orbbec/depth, bras et gripper.

L'acces SSH par cle fonctionne avec l'utilisateur `ubuntu`.

## Identite reseau

| Element | Valeur observee |
| --- | --- |
| IP | `192.168.100.50` |
| MAC | `48:8f:4c:de:bf:0` |
| Latence ping | environ 16 a 42 ms |
| SSH | `OpenSSH_8.9p1 Ubuntu-3ubuntu0.10` |
| ROS | ROS 2 `humble`, via `/rosapi/get_ros_version` |

## Inventaire systeme

| Element | Valeur observee |
| --- | --- |
| Utilisateur SSH | `ubuntu` |
| Hostname | `ubuntu` |
| OS | Ubuntu `22.04.5 LTS` |
| Kernel | `5.15.148-tegra` |
| Architecture | `aarch64` |
| Plateforme | `NVIDIA Jetson Orin Nano Engineering Reference Developer Kit Super` |
| Module | `NVIDIA Jetson Orin Nano (8GB ram)` d'apres l'environnement |
| L4T | `R36.4.3`, date NVIDIA `2025-01-08` |
| CUDA | `12.6` d'apres `nvidia-smi` |
| GPU | `Orin (nvgpu)` |
| CPU | 6 coeurs Cortex-A78AE |
| RAM | 7.4 GiB, environ 4.0 GiB disponibles pendant l'observation |
| Swap | 11 GiB, non utilise pendant l'observation |
| Disque systeme | NVMe, `/dev/nvme0n1p1`, 116G dont 52G utilises |
| Temperature observee | environ 52 a 54 degC via `tegrastats` |

Le rapport brut complet est sauvegarde dans `system-inventory-2026-06-04.txt`.

## Sauvegardes ajoutees

- `system-inventory-2026-06-04.txt`: inventaire brut collecte par SSH.
- `ros2-config-snapshot/`: snapshot des `package.xml`, `*.launch.py`, `*.yaml` et `*.xacro` de `/home/ubuntu/ros2_ws/src`.
- `systemd/start_app_node.service.txt`: unite systemd qui demarre le bringup ROS.
- `systemd/x11vnc.service.txt`: unite systemd qui demarre VNC.
- `assets/`: snapshots camera captures via `web_video_server`.
- `../../scripts/collect_robot_info.sh`: script de collecte reutilisable depuis le poste local.

## Ports ouverts

| Port | Service | Observation |
| --- | --- | --- |
| `22/tcp` | SSH | Ouvert, authentification requise. |
| `111/tcp/udp` | rpcbind | Seulement `rpcbind` annonce via `rpcinfo`. |
| `631/tcp` | CUPS | Interface web CUPS `2.4.19`. Une imprimante Brother est configuree. |
| `5900/tcp` | VNC/RFB | Banniere `RFB 003.008`. |
| `8080/tcp` | `web_video_server` | Liste et snapshots des topics image ROS. |
| `9090/tcp` | `rosbridge_websocket` | API WebSocket ROS 2, serveur Tornado 6.1. |

Interfaces supplementaires observees sur le robot:

- `wlan0`: `192.168.100.50/24`, MAC `48:8f:4c:de:bf:00`, reseau Cosmo-Robotics.
- `eth0`: `192.168.1.18/24`, route par defaut prioritaire via `192.168.1.1`.
- `l4tbr0`: `192.168.55.1/24`, bridge USB Jetson, lien down au moment de l'observation.
- `docker0`: `172.17.0.1/16`, lien down au moment de l'observation.
- `can0`: present mais down.

## Interfaces Web utiles

- Video ROS: `http://192.168.100.50:8080/`
- Snapshot camera RGB-D RGB: `http://192.168.100.50:8080/snapshot?topic=/depth_cam/rgb/image_raw`
- Snapshot camera USB: `http://192.168.100.50:8080/snapshot?topic=/usb_cam/image_raw`
- Rosbridge WebSocket: `ws://192.168.100.50:9090/`
- CUPS: `http://192.168.100.50:631/`

## Snapshots camera

Deux snapshots ont ete captures:

- `assets/_depth_cam_rgb_image_raw.jpg`: image JPEG 640x480 de `/depth_cam/rgb/image_raw`.
- `assets/_usb_cam_image_raw.jpg`: image JPEG 640x480 de `/usb_cam/image_raw`.

Les snapshots suivants n'ont pas donne d'image pendant l'observation, probablement parce que les applications ne publiaient pas activement: `/line_following/image_result`, `/object_tracking/image_result`, `/ar_app/image_result`.

## ROS 2

Le demarrage ROS principal est gere par l'unite systemd `start_app_node.service`, qui lance:

```bash
ros2 launch bringup bringup.launch.py
```

Le launch principal sauvegarde dans `ros2-config-snapshot/bringup/launch/bringup.launch.py` inclut:

- le controleur robot et odometrie,
- la camera de profondeur,
- le LiDAR,
- `rosbridge_websocket`,
- `web_video_server`,
- les applications prechargees,
- le controle joystick,
- l'initialisation de pose.

L'environnement ROS expose `ROS_DISTRO=humble`, `ROS_VERSION=2`, `ROS_LOCALHOST_ONLY=0`.

### Nodes detectes

Nodes principaux visibles via `/rosapi/nodes`:

- `/ros_robot_controller`
- `/controller_manager`
- `/servo_manager`
- `/arm_controller`
- `/gripper_controller`
- `/odom_publisher`
- `/ekf_filter_node`
- `/imu_calib`
- `/imu_filter`
- `/sllidar_node`
- `/scan_to_scan_filter_chain`
- `/depth_cam/camera_container`
- `/depth_cam/depth_cam`
- `/usb_cam/usb_cam`
- `/usb_cam/undistort_node`
- `/robot_state_publisher`
- `/joint_state_publisher`
- `/joystick_control`
- `/line_following`
- `/object_tracking`
- `/ar_app`
- `/lidar_app`
- `/patrol_app`
- `/web_video_server`
- `/rosbridge_websocket`
- `/rosapi`

### Workspaces et packages

Le workspace principal est `/home/ubuntu/ros2_ws`. Il contient notamment:

- `bringup`
- `driver/controller`
- `driver/ros_robot_controller`
- `driver/servo_controller`
- `peripherals`
- `app`
- `navigation`
- `slam`
- `simulations/jetauto_description`
- `xf_mic_asr_offline`
- `large_models`
- `large_models_examples`

Workspaces tiers detectes:

- `/home/ubuntu/third_party/third_party_ws`
- `/home/ubuntu/third_party/orbbec_ws`
- `/home/ubuntu/third_party/rtabmap_ws`
- `/home/ubuntu/third_party/YDLidar-SDK`

### Topics importants

Mobilite:

- `/cmd_vel` - `geometry_msgs/msg/Twist`
- `/controller/cmd_vel` - `geometry_msgs/msg/Twist`
- `/odom` - `nav_msgs/msg/Odometry`
- `/odom_raw` - `nav_msgs/msg/Odometry`
- `/set_odom` - `geometry_msgs/msg/Pose2D`
- `/set_pose` - `geometry_msgs/msg/PoseWithCovarianceStamped`
- `/tf`, `/tf_static` - `tf2_msgs/msg/TFMessage`

Capteurs:

- `/imu` - `sensor_msgs/msg/Imu`
- `/imu_corrected` - `sensor_msgs/msg/Imu`
- `/ros_robot_controller/imu_raw` - `sensor_msgs/msg/Imu`
- `/scan` - `sensor_msgs/msg/LaserScan`
- `/scan_raw` - `sensor_msgs/msg/LaserScan`
- `/depth_cam/depth/points` - `sensor_msgs/msg/PointCloud2`
- `/depth_cam/rgb/image_raw` - `sensor_msgs/msg/Image`
- `/depth_cam/depth/image_raw` - `sensor_msgs/msg/Image`
- `/usb_cam/image_raw` - `sensor_msgs/msg/Image`
- `/usb_cam/image` - `sensor_msgs/msg/Image`

Controle robot:

- `/ros_robot_controller/battery` - `std_msgs/msg/UInt16`
- `/ros_robot_controller/set_motor` - `ros_robot_controller_msgs/msg/MotorsState`
- `/ros_robot_controller/set_led` - `ros_robot_controller_msgs/msg/LedState`
- `/ros_robot_controller/set_buzzer` - `ros_robot_controller_msgs/msg/BuzzerState`
- `/ros_robot_controller/set_oled` - `ros_robot_controller_msgs/msg/OLEDState`
- `/ros_robot_controller/button` - `ros_robot_controller_msgs/msg/ButtonState`
- `/ros_robot_controller/joy` - `sensor_msgs/msg/Joy`
- `/ros_robot_controller/bus_servo/set_position` - `ros_robot_controller_msgs/msg/ServosPosition`
- `/ros_robot_controller/pwm_servo/set_state` - `ros_robot_controller_msgs/msg/SetPWMServoState`

Bras et joints:

- `/joint_states` - `sensor_msgs/msg/JointState`
- `/controller_manager/joint_states` - `sensor_msgs/msg/JointState`
- `/controller_manager/servo_states` - `servo_controller_msgs/msg/ServoStateList`
- `/joint_controller` - `sensor_msgs/msg/JointState`
- `/servo_controller` - `servo_controller_msgs/msg/ServosPosition`

Applications:

- `/line_following/image_result` - `sensor_msgs/msg/Image`
- `/object_tracking/image_result` - `sensor_msgs/msg/Image`
- `/ar_app/image_result` - `sensor_msgs/msg/Image`
- Services dedies pour `enter`, `exit`, `heartbeat`, `set_running`, `set_target_color`, `set_threshold` selon l'application.

## Echantillons d'etat

### Batterie

Topic: `/ros_robot_controller/battery`

Valeur observee via rosbridge: `11369`, interpretable comme environ `11.369 V` si l'unite du firmware est le millivolt. L'echantillon via `ros2 topic echo` n'a pas publie pendant le timeout court de l'inventaire SSH.

### IMU

Topic: `/imu`, frame `imu_link`.

- Orientation quaternion observee: `x=0.0453`, `y=-0.0153`, `z=0.4108`, `w=0.9105`
- Acceleration lineaire: environ `x=0.529`, `y=0.564`, `z=8.202`
- Vitesse angulaire proche de zero, robot immobile.

### Odometrie

Topic: `/odom`, frames `odom` -> `base_footprint`.

- Position observee: `x=0.0`, `y=0.0`, `z=0.0`
- Vitesse lineaire observee: `0.0`
- Vitesse angulaire `z`: environ `5.8e-06`, donc quasi nulle.

### LiDAR

Topic: `/scan`, frame `lidar_frame`.

- Plage angulaire: `-pi` a `+pi`
- `range_min`: environ `0.05 m`
- `range_max`: `12.0 m`
- `scan_time`: environ `0.0747 s`, soit environ 13.4 Hz
- Nombre de mesures: environ 1080 valeurs
- Premiers ranges observes: autour de `1.67 m`, avec quelques valeurs invalides/nulles.

### Joints

Topic: `/joint_states`.

Joints observes: `joint1`, `joint2`, `joint3`, `joint4`, `joint5`, `r_joint`, `l_joint`, `l_in_joint`, `l_out_joint`, `r_in_joint`, etc. Cela confirme la presence d'un bras articule et d'un gripper.

### Diagnostics

Topic: `/diagnostics`.

Le diagnostic de `ekf_filter_node: odometry/filtered topic status` etait en niveau `2` avec le message `No events recorded.` et une frequence observee `0.0 Hz` pour `odometry/filtered`, attendue entre environ `25.2` et `35.2 Hz`. A verifier si l'EKF doit publier une odometrie filtree dans la configuration active.

## Services applicatifs et controle

Services notables:

- `/start_motor`, `/stop_motor`, `/enable`, `/toggle`
- `/controller/load_calibrate_param`
- `/ros_robot_controller/bus_servo/get_state`
- `/ros_robot_controller/pwm_servo/get_state`
- `/depth_cam/get_device_info`
- `/depth_cam/get_sdk_version`
- `/depth_cam/save_images`
- `/depth_cam/save_point_cloud`
- `/depth_cam/reboot_device`
- `/line_following/enter`, `/line_following/exit`, `/line_following/set_running`
- `/object_tracking/enter`, `/object_tracking/exit`, `/object_tracking/set_running`
- `/lidar_app/enter`, `/lidar_app/exit`, `/lidar_app/set_running`
- `/patrol_app/enter`, `/patrol_app/exit`, `/patrol_app/set_running`

Attention: plusieurs de ces services peuvent modifier l'etat du robot. Les observations ci-dessus ont ete faites avec des appels de lecture et des abonnements uniquement, sans envoyer de commande de mouvement.

## Services systemd

Services importants actifs:

- `start_app_node.service`: demarrage du stack ROS JetAuto.
- `ssh.service`: acces SSH par cle, utilisateur `ubuntu`.
- `x11vnc.service`: VNC sur `:0`, authentification par `/home/ubuntu/.vnc/passwd`.
- `docker.service` et `containerd.service`: installes et actifs, mais l'utilisateur `ubuntu` n'a pas l'acces au socket Docker pendant l'observation.
- `snap.cups.cupsd.service`: CUPS via snap.
- `nvargus-daemon.service`, `nvfancontrol.service`, services NVIDIA Jetson.
- `nxserver.service`: NoMachine Server actif.

Un seul service en echec a ete observe:

- `apport-autoreport.service`: failed, lie au reporting d'erreurs Ubuntu.

## Processus ROS principaux

Le process parent ROS observe est:

```bash
/usr/bin/python3 /opt/ros/humble/bin/ros2 launch bringup bringup.launch.py
```

Processus notables:

- `component_container` en namespace `/depth_cam`, node `camera_container`.
- `ros_robot_controller`.
- `odom_publisher`.
- `ekf_node`, node `ekf_filter_node`.
- `servo_controller`.
- `usb_cam_node_exe`.
- `undistort_node`.
- `sllidar_node`.
- `scan_to_scan_filter_chain`.
- `web_video_server`.
- `rosbridge_websocket` et `rosapi_node`.
- apps `lidar_controller`, `line_following`, `object_tracking`, `ar_app`, `patrol`.
- `joystick_control`.
- `robot_state_publisher` avec `/home/ubuntu/ros2_ws/src/simulations/jetauto_description/urdf/jetauto.xacro`.

## CUPS

CUPS `2.4.19` est expose sur le port `631`. Une imprimante est configuree:

| Queue | Modele | Etat |
| --- | --- | --- |
| `Brother_DCP_L3560CDW_series` | Brother Printer, driverless, 2.1.1 | Idle |

## Limites de l'analyse

- Les commandes ont ete limitees a de la lecture et a de l'inventaire. Aucun ordre de mouvement, de redemarrage materiel ou de controle moteur n'a ete envoye.
- L'inventaire Docker n'a pas pu lister les conteneurs car `ubuntu` n'a pas acces a `/var/run/docker.sock`.
- Les topics ROS publies sporadiquement ou uniquement quand une application est active peuvent ne pas apparaitre dans les echantillons.
- Le snapshot de configuration ROS ne contient pas tout le code source: il sauvegarde les manifestes, launch files, YAML et Xacro utiles a l'analyse.

## Prochaine etape recommandee

Ajouter un alias SSH local:

```sshconfig
Host jetauto
  HostName 192.168.100.50
  User ubuntu
  IdentityFile ~/.ssh/id_ed25519
```

Puis utiliser:

```bash
ssh jetauto
```

Ensuite, les prochaines actions utiles sont:

- securiser VNC, rosbridge et CUPS si le robot sort du reseau de labo;
- tester les commandes de mouvement uniquement roues levees ou dans un espace degage;
- sauvegarder les sources complets de `/home/ubuntu/ros2_ws/src` si le robot doit etre reproductible a l'identique;
- documenter une procedure de restauration de l'environnement ROS.
