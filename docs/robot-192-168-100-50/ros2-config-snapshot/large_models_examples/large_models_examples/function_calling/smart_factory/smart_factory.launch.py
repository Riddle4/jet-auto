import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription, LaunchService
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction, ExecuteProcess
from launch.conditions import IfCondition, UnlessCondition

def launch_setup(context, *args, **kwargs):
    function = LaunchConfiguration('function', default='default')
    function_arg = DeclareLaunchArgument('function', default_value=function)

    conf = LaunchConfiguration('conf', default='0.45')
    conf_arg = DeclareLaunchArgument('conf', default_value=conf)

    mode = LaunchConfiguration('mode', default='1')
    mode_arg = DeclareLaunchArgument('mode', default_value=mode)

    interruption = LaunchConfiguration('interruption', default='false')
    interruption_arg = DeclareLaunchArgument('interruption', default_value=interruption)

    camera_topic = LaunchConfiguration('camera_topic', default='usb_cam/image')
    camera_topic_arg = DeclareLaunchArgument('camera_topic', default_value=camera_topic)

    use_depth_cam = LaunchConfiguration('use_depth_cam', default='false')
    use_depth_cam_arg = DeclareLaunchArgument('use_depth_cam', default_value=use_depth_cam)

    debug = LaunchConfiguration('debug', default='false')
    debug_arg = DeclareLaunchArgument('debug', default_value=debug)

    map_name = LaunchConfiguration('map', default='map_01')
    map_arg = DeclareLaunchArgument('map', default_value=map_name)

    robot_name = LaunchConfiguration('robot_name', default=os.environ.get('HOST', 'robot'))
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value=robot_name)

    master_name = LaunchConfiguration('master_name', default=os.environ.get('MASTER', 'master'))
    master_name_arg = DeclareLaunchArgument('master_name', default_value=master_name)

    controller_package_path = get_package_share_directory('controller')
    kinematics_package_path = get_package_share_directory('kinematics')
    navigation_package_path = get_package_share_directory('navigation')
    large_models_examples_path = get_package_share_directory('large_models_examples')


    peripherals_package_path = get_package_share_directory('peripherals')

    depth_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(peripherals_package_path, 'launch/depth_camera.launch.py')),
        condition=IfCondition(debug)
    )


    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(controller_package_path, 'launch/controller.launch.py')),
        condition=IfCondition(debug)
    )

    kinematics_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(kinematics_package_path, 'launch/kinematics_node.launch.py')),
    )

    tf_transform_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name="usb_to_color_frame_link",
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
            '--frame-id', 'usb_link',
            '--child-frame-id', 'depth_cam_color_frame'
        ],
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(navigation_package_path, 'launch/navigation.launch.py')),
        launch_arguments={
            'sim': 'false',
            'map': map_name,
            'robot_name': robot_name,
            'master_name': master_name,
            'use_teb': 'true',
        }.items(),
        condition=UnlessCondition(debug)
    )

    navigation_controller_node = Node(
        package='large_models_examples',
        executable='navigation_controller',
        output='screen',
        parameters=[{'map_frame': 'map', 'nav_goal': '/nav_goal'}],
        condition=UnlessCondition(debug)
    )

    rviz_node = ExecuteProcess(
        cmd=['rviz2', '-d', os.path.join(navigation_package_path, 'rviz/navigation_controller.rviz')],
        output='screen',
        condition=UnlessCondition(debug)
    )

    smart_factory_transport_node = Node(
        package='large_models_examples',
        executable='smart_factory_transport_node',
        output='screen',
        parameters=[{'start': 'false'}],
        condition=UnlessCondition(debug)
    )
    smart_factory_transport_debug_node = Node(
        package='large_models_examples',
        executable='smart_factory_transport_node',
        output='screen',
        parameters=[{'start': 'true'}],
        condition=IfCondition(debug)
    )

    llm_agent_progress_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(large_models_examples_path, 'large_models_examples/function_calling/llm_agent_progress.launch.py')),
        launch_arguments={
            'camera_topic': camera_topic,
            'function': 'smart_factory'
        }.items(),
        condition=UnlessCondition(debug)
    )

    return [
        function_arg,
        conf_arg,
        mode_arg,
        interruption_arg,
        camera_topic_arg,
        use_depth_cam_arg,
        debug_arg,
        map_arg,
        robot_name_arg,
        master_name_arg,

        depth_camera_launch,
        controller_launch,
        smart_factory_transport_debug_node,

        tf_transform_node,
        kinematics_launch,

        navigation_launch,
        navigation_controller_node,

        smart_factory_transport_node,
        llm_agent_progress_launch,
        
        rviz_node
    ]


def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])


if __name__ == '__main__':
    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
