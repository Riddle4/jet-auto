import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node  # noqa: E402
from launch import LaunchDescription, LaunchService  # noqa: E402

def generate_launch_description():
    compiled = os.environ['need_compile']
    if compiled == 'True':
        peripherals_package_path = get_package_share_directory('peripherals')
    else:
        peripherals_package_path = '/home/ubuntu/ros2_ws/src/peripherals'
    ns = 'usb_cam'
    camera_nodes = Node(
            package='usb_cam', 
            executable='usb_cam_node_exe', 
            output='screen',
            name='usb_cam',
            namespace=ns,
            parameters=[os.path.join(peripherals_package_path, 'config', 'usb_cam_param.yaml')],
            remappings = [
                # ('image_raw', '/usb_cam/image_raw'),
                # ('image_raw/compressed', '/usb_cam/image_compressed'),
                # ('image_raw/compressedDepth', '/usb_cam/compressedDepth'),
                # ('image_raw/theora', '/usb_cam/image_raw/theora'),
                # ('camera_info', '/usb_cam/camera_info'),
                ('camera_info', 'camera_info'),      # 相对名，落在本命名空间
                ('image_raw',  'image_raw'),  

            ]
        )

    undistort_node = Node(
        package='peripherals',
        executable='undistort_node',   
        name='undistort_node',
        namespace=ns,
        output='screen',       
    )

    return LaunchDescription([
        camera_nodes,
        undistort_node
        ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()

