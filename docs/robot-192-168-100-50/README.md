# Robot JetAuto / Jetson - 192.168.100.50

Date d'observation: 2026-06-04, depuis le reseau Cosmo-Robotics.

## Resume

Le robot repond a l'adresse `192.168.100.50`. Il expose un systeme ROS 2 Humble accessible via `rosbridge_websocket` et `web_video_server`. La signature generale correspond a un robot mobile 4 roues avec Jetson, controleur moteur/servo, LiDAR 2D, IMU, odometrie, camera USB, camera RGB-D Orbbec/depth, bras et gripper.

L'acces SSH est ouvert mais necessite un mot de passe ou une cle autorisee. Les comptes courants testes en mode non interactif (`jetson`, `ubuntu`, `nvidia`, `pi`, `root`, `cosmo`, `jetauto`, `hiwonder`) n'acceptent pas les cles locales.

## Identite reseau

| Element | Valeur observee |
| --- | --- |
| IP | `192.168.100.50` |
| MAC | `48:8f:4c:de:bf:0` |
| Latence ping | environ 16 a 42 ms |
| SSH | `OpenSSH_8.9p1 Ubuntu-3ubuntu0.10` |
| ROS | ROS 2 `humble`, via `/rosapi/get_ros_version` |

## Ports ouverts

| Port | Service | Observation |
| --- | --- | --- |
| `22/tcp` | SSH | Ouvert, authentification requise. |
| `111/tcp/udp` | rpcbind | Seulement `rpcbind` annonce via `rpcinfo`. |
| `631/tcp` | CUPS | Interface web CUPS `2.4.19`. Une imprimante Brother est configuree. |
| `5900/tcp` | VNC/RFB | Banniere `RFB 003.008`. |
| `8080/tcp` | `web_video_server` | Liste et snapshots des topics image ROS. |
| `9090/tcp` | `rosbridge_websocket` | API WebSocket ROS 2, serveur Tornado 6.1. |

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

Valeur observee: `11369`, interpretable comme environ `11.369 V` si l'unite du firmware est le millivolt.

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

## CUPS

CUPS `2.4.19` est expose sur le port `631`. Une imprimante est configuree:

| Queue | Modele | Etat |
| --- | --- | --- |
| `Brother_DCP_L3560CDW_series` | Brother Printer, driverless, 2.1.1 | Idle |

## Limites de l'analyse

- Pas d'acces shell obtenu: SSH repond mais demande une authentification non disponible localement.
- Sans SSH, les informations internes comme `uname -a`, version JetPack/L4T, packages installes, services systemd, espace disque, temperature, GPU, Docker et configuration reseau complete n'ont pas pu etre verifies.
- Les topics ROS publies sporadiquement ou uniquement quand une application est active peuvent ne pas apparaitre dans les echantillons.

## Prochaine etape recommandee

Fournir un compte SSH ou installer une cle publique sur le robot, puis relancer une inspection systeme complete:

```bash
ssh <user>@192.168.100.50
```

Une fois connecte, verifier au minimum:

```bash
hostnamectl
uname -a
cat /etc/os-release
dpkg -l | grep -E 'ros-|nvidia|jetpack|l4t'
systemctl --type=service --state=running
ip addr
df -h
free -h
tegrastats
ros2 node list
ros2 topic list -t
ros2 service list -t
```
