import rospy
import math
import numpy as np
from fbl_control.msg import plant_msg

from std_msgs.msg import Float32MultiArray

if __name__ == '__main__':
	rospy.init_node('tracker', anonymous=True)
	tracker_pub = rospy.Publisher('tracking', plant_msg, queue_size=10)

	msg = plant_msg()
	freq = 100;
	rate = rospy.Rate(freq)
		
	while not rospy.is_shutdown():
		file = open("data.txt", "r")
		content  = file.read()

		points = content.split(",");
		if content != "":
			x = np.array(points)
			y = x.astype(np.float)
			# msg state values
			print y[0:3]
			msg.x = y[0:3].tolist()
			# msg vel values
			msg.velx = y[3:5].tolist()
			# also need setpts

			tracker_pub.publish(msg)
		
		rate.sleep()
