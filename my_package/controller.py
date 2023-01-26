import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot(Node):

    def __init__(self):
        
        super().__init__('turtlebot')

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
        self.pose_subscriber
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.move2goal)
        self.i = 0
    
    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        #print("updated pose: ",self.pose)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        print("Are you here?")
        goal_pose = Pose()

        goal_pose.x = 2.0
        goal_pose.y = 2.0
        distance_tolerance = 0.01

        vel_msg = Twist()

        if self.euclidean_distance(goal_pose) >= distance_tolerance:

            # Porportional controller
            print("Or here?")

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            self.i += 1
            
            print("distance from goal: ", self.euclidean_distance(goal_pose))

        # Stopping our robot after the movement is over.
        print("OR there?")
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.0
        self.velocity_publisher.publish(vel_msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    turtlebot = TurtleBot()
    
    rclpy.spin(turtlebot)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtlebot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    

