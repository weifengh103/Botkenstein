import rospy
from sensor_msgs.msg import Image 
import cv2 
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

def callback(data):
  br = CvBridge()

  rospy.loginfo("receiving video frame")
  current_frame = br.imgmsg_to_cv2(data)
#   cv_image_array = np.array(current_frame, dtype = np.dtype('f8'))
#   cv_image_norm = cv2.normalize(cv_image_norm, cv_image_array, 0, 1, cv2.NORM_MINMAX)
#   cv2.imshow("camera", cv2.cvtColor(current_frame,cv2.COLOR_BGR2RGB))
  cv2.imshow("Image window", current_frame)
#   print(cv_image_norm.shape)
  cv2.waitKey(1)

def receive_message():
  rospy.init_node('video_sub_py', anonymous=True)
#   rospy.Subscriber('/camera/depth/image_rect_raw', Image, callback) # check name by rostopic list
  rospy.Subscriber('/camera/color/image_raw', Image, callback) # check name by rostopic list

  rospy.spin()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  receive_message()