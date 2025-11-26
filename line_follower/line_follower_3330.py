import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import TwistStamped, Twist, Vector3
from std_msgs.msg import Header

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        
        self.subscription = self.create_subscription(Range,'ps7',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.subscription = self.create_subscription(Range, 'ps6', self.listener_callback, 10)
        self.subscription

        self.publisher_ = self.create_publisher(TwistStamped, 'cmd_vel', 10)
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.ahaha)


    def listener_callback(self, msg):
        sensor_range = float(msg.range)
        self.get_logger().info(f"{msg.range}")

        twist_stamped_msg = TwistStamped()

        # Create Header
        twist_stamped_msg.header = Header()
        twist_stamped_msg.header.stamp = self.get_clock().now().to_msg()
        twist_stamped_msg.header.frame_id = 'base_link'

        # Create Twist message
        twist_msg = Twist()
        twist_msg.linear = Vector3(x=0.1, y=0.0, z=0.0)
        twist_msg.angular = Vector3(x=0.0, y=0.0, z=0.0)

        if sensor_range <= 0.0675:
            twist_msg.linear = Vector3(x=0.001, y=0.0, z=0.0)
            twist_msg.angular = Vector3(x = 0.0, y = 0.0, z = -0.9)

        twist_stamped_msg.twist = twist_msg
        self.publisher_.publish(twist_stamped_msg)
        self.get_logger().info(f'Publishing: Linear x={twist_stamped_msg.twist.linear.x}, Angular z={twist_stamped_msg.twist.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()