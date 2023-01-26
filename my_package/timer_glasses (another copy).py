import rclpy
from rclpy.node import Node

from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, floor


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.listener_callback, 10)
        self.subscription
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.circle_pose = Pose()
        self.goal_pose = Pose()
        self.flag = 1
        self.set_goal = 0
        self.hamada = 0
        self.counter = 0
        self.i = 0
        
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))
    	
    def timer_callback(self):

        msg =Twist()
        
        if self.i == 0:
        	self.circle_pose = self.pose
        	print("circle_pose ", self.circle_pose)

        if self.flag == 1:
        	
        	if self.counter == 0:
        		msg.linear.x = 0.5
        		msg.linear.y = 0.0
        		msg.angular.z = 0.5
        	elif not (self.counter%2):
        		msg.linear.x = 0.5
        		msg.linear.y = 0.0
        		msg.angular.z = -0.5
        	else:
        		msg.linear.x = 0.5
        		msg.linear.y = 0.0
        		msg.angular.z = 0.5        		
        	print("circling")
        
        #print("Difference poses = ", round(self.euclidean_distance(self.circle_pose), 1))
        
        if ((round(self.euclidean_distance(self.circle_pose), 1) <= 0.2) and (self.i != 0) and self.hamada != self.i) or self.flag == 0:	    
		    
        	if self.set_goal == 0:
        		if self.counter%2 != 0:
        			self.goal_pose.x = 5.8
        			self.goal_pose.y = 5.8
        			self.counter += 1

        		else:
        			self.goal_pose.x = 8.54
        			self.goal_pose.y = 8.54
        			self.counter += 1
        		
        		self.set_goal = 1
        		print("GOAL SET", self.goal_pose) 	

        	#print("Heading to goal, error = ", self.euclidean_distance(self.goal_pose))
        	print("Heading to goal")
        	if self.euclidean_distance(self.goal_pose) >= 0.01:
        	        	
        		self.flag = 0
        		msg.linear.x = 0.5 * self.euclidean_distance(self.goal_pose)
        		msg.linear.y = 0.0
        		msg.linear.z = 0.0
        		
        		msg.angular.x = 0.0
        		msg.angular.y = 0.0
        		msg.angular.z = 1 * (atan2(self.goal_pose.y - self.pose.y, self.goal_pose.x - self.pose.x) - self.pose.theta)
        		
        	
        	if self.euclidean_distance(self.goal_pose) <= 0.01:
        		self.flag = 1
        		self.set_goal = 0
        		msg.linear.x = 0.0
        		msg.linear.y = 0.0
        		print("stopping after line")
        		self.circle_pose = self.pose
        		print("circle_pose ", self.circle_pose)
        		self.hamada = self.i + 1
        		  
        		
        self.publisher_.publish(msg) 
        #self.get_logger().info('Publishing: "%f"' % msg.linear.x)
        self.i += 1        	
        
    def listener_callback(self, msg):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = msg
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)


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

