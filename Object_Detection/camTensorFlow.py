######################################################
#              CAMERA TENSOR FLOW SCRIPT             #
######################################################
# Version: 1.00                                      #                    
# Date: 25 April 2020                                #
# Author: Arsalan                                    #
#----------------------------------------------------#
## Parts of the code is copied from:                ##
## https://github.com/EdjeElectronics/              ##
######################################################

# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import sys
import datetime

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Set up camera constants
IM_WIDTH = 640 # 1280   #  Use smaller resolution for
IM_HEIGHT =480 # 720   #  faster framerate
frameRate = 30 # fps

def startObjectDetect(frame_rate_calc, classes_Share, scores_Share, stopFlag , lock):

	currentDT = datetime.datetime.now()
	currentDT = currentDT.strftime("%Y-%m-%d_%H-%M-%S")
	FILE_OUTPUT = '/home/pi/Gripper_Control/Object_Detection/videos/cameraTFOutput_%s.mp4' %(currentDT)

	# Define the codec and create VideoWriter object
	out = cv2.VideoWriter(FILE_OUTPUT,cv2.VideoWriter_fourcc('m','p','4','v'), frameRate, (IM_WIDTH,IM_HEIGHT))

	# This is needed since the working directory is the object_detection folder.
    #sys.path.append('..')

	# Name of the directory containing the object detection module we're using
	MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
	#MODEL_NAME = 'custom_models'

	# Path to frozen detection graph .pb file, which contains the model that is used
	# for object detection.
	PATH_TO_CKPT = os.path.join('/home/pi/Gripper_Control/Object_Detection/',MODEL_NAME,'frozen_inference_graph.pb')
	#PATH_TO_CKPT = os.path.join('/home/pi/Gripper_Control/Object_Detection/',MODEL_NAME,'frozen_inference_graph_windTurbine.pb')

	# Path to label map file
	PATH_TO_LABELS = os.path.join('/home/pi/Gripper_Control/Object_Detection/','data','mscoco_label_map.pbtxt')
	#PATH_TO_LABELS = os.path.join('/home/pi/Gripper_Control/Object_Detection/','data','label_map_windTurbine.pbtxt')

	# Number of classes the object detector can identify
	NUM_CLASSES = 90
	#NUM_CLASSES = 1

	## Load the label map.
	# Label maps map indices to category names, so that when the convolution
	# network predicts `5`, we know that this corresponds to `airplane`.
	# Here we use internal utility functions, but anything that returns a
	# dictionary mapping integers to appropriate string labels would be fine
	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)

	# Load the Tensorflow model into memory.
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	#    od_graph_def = tf.GraphDef()
		od_graph_def = tf.compat.v1.GraphDef()
	#    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')

	#    sess = tf.Session(graph=detection_graph)
		sess = tf.compat.v1.Session(graph=detection_graph)

	# Define input and output tensors (i.e. data) for the object detection classifier

	# Input tensor is the image
	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

	# Output tensors are the detection boxes, scores, and classes
	# Each box represents a part of the image where a particular object was detected
	detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

	# Each score represents level of confidence for each of the objects.
	# The score is shown on the result image, together with the class label.
	detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
	detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

	# Number of objects detected
	num_detections = detection_graph.get_tensor_by_name('num_detections:0')

	# Initialize frame rate calculation
	#frame_rate_calc = 1
	freq = cv2.getTickFrequency()
	font = cv2.FONT_HERSHEY_SIMPLEX

	# Initialize camera and perform object detection.
	# The camera has to be set up and used differently depending on if it's a
	# Picamera or USB webcam.

	# Initialize Picamera and grab reference to the raw capture
	camera = PiCamera()
	camera.resolution = (IM_WIDTH,IM_HEIGHT)
	camera.framerate = frameRate
	rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
	rawCapture.truncate(0)

	for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

		t1 = cv2.getTickCount()
		
		# Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
		# i.e. a single-column array, where each item in the column has the pixel RGB value
		frame = np.copy(frame1.array)
		frame.setflags(write=1)
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame_expanded = np.expand_dims(frame_rgb, axis=0)

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: frame_expanded})
		
		# Writing to SHARED variables
		classes_Share[0:4] = classes[0][0:4]
		scores_Share[0:4] = scores[0][0:4]
		
		# Draw the results of the detection (aka 'visulaize the results')
		vis_util.visualize_boxes_and_labels_on_image_array(
			frame,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			category_index,
			use_normalized_coordinates=True,
			line_thickness=8,
			min_score_thresh=0.40)

		cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc.value),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

		# All the results have been drawn on the frame, so it's time to display it.
		cv2.imshow('TF Object detector', frame)
		
		# Write final frame
		out.write(frame)

		t2 = cv2.getTickCount()
		time1 = (t2-t1)/freq
		frame_rate_calc.value = 1/time1

		# Press 'q' to quit
		if (cv2.waitKey(1) == ord('q')) or (stopFlag.value==1):
			break

		rawCapture.truncate(0)

	camera.close()
	out.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':  # Program entrance
    startObjectDetect(1,0,0)
    # WARNING! In order to run this script in main '.value' needs to be removed from 
    # the following variables in the script above: frame_rate_calc and stopFlag.
    # But remember to put them back if you want to run the script in Main_B.py with
    # multi-processing and shared variables
