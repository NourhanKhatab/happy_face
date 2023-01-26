import rclpy
from rclpy.node import Node

from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.listener_callback, 10)
        self.subscription
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0
        msg.linear.y = 0.0
        msg.angular.z = 1.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%f"' % msg.linear.x)
        self.i += 1
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%f"' % msg.x)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

