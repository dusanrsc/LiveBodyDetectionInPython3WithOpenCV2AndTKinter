# importing modules
import cv2
import numpy
import os

# importing sub-modules
from tkinter import *
from PIL import Image, ImageTk
from cvzone.PoseModule import PoseDetector
from time import strftime

# variable section
# special metadata variables
__version__ = "v1.0.0-beta"
__updated__ = "29.07.2024"
__by__ = "Dusan Rosic"

# classic variable
# body shape detection initialization
body_detector = PoseDetector()

# image storage path
image_path = "detected_images\\body_detection_images\\"

# switch variables for on/off settings
displaying_rectangle = False
displaying_detection_skeleton = False
auto_save_frame_when_detected = False
displaying_on_screen_data = True

# function section for button functionalities
# displaying rectangle on/off by button click
def switch_displaying_rectangle():
	global displaying_rectangle

	if displaying_rectangle:
		displaying_rectangle = False 
	else:
		displaying_rectangle = True

# displaying rectangle on/off by button click
def switch_displaying_detection_skeleton():
	global displaying_detection_skeleton

	if displaying_detection_skeleton:
		displaying_detection_skeleton = False 
	else:
		displaying_detection_skeleton = True

# auto save frame on/off by button click
def switch_auto_save_frame_when_detected():
	global auto_save_frame_when_detected

	if auto_save_frame_when_detected:
		auto_save_frame_when_detected = False
	else:
		auto_save_frame_when_detected = True

# displaying on screen data on/off by button click
def switch_displaying_on_screen_data():
	global displaying_on_screen_data

	if displaying_on_screen_data:
		displaying_on_screen_data = False
	else:
		displaying_on_screen_data = True

# constants section
# standard opencv2 constatns color tuple (BGR)
BGR_BLUE = (255, 0, 0)
BGR_GREEN = (0, 255, 0)
BGR_RED = (0, 0, 255)

BGR_ALPHA = BGR_GREEN

BGR_BACKGROUND_BLUE = (130, 30, 30)

# constatns color tuple (RGB)
RGB_BLUE = (0, 0, 255)
RGB_GREEN = (0, 255, 0)
RGB_RED = (255, 0, 0)

RGB_ALPHA = RGB_GREEN

RGB_BACKGROUND_BLUE = (30, 30, 130)

# RGB and BGR constant color tuple 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# creating directory for image storage
os.system(f"mkdir {image_path}")

# class section
# main app class
class BodyDetectionApp:
	def __init__(self, window, window_title=None):
		self.window = window
		self.window.title(f"{window_title} | {__version__}")
		self.window.resizable(False, False)

		# menubar section
		self.menubar = Menu(self.window)
		self.window.config(menu=self.menubar)

		# create a menu
		self.options_menu = Menu(self.menubar, tearoff=0)
		self.help_menu = Menu(self.menubar, tearoff=0)

		# options menu settings
		self.options_menu.add_command(label="Body Detection Rectangle", command=switch_displaying_rectangle)
		self.options_menu.add_command(label="Body Detection Skeleton", command=switch_displaying_detection_skeleton)
		self.options_menu.add_separator()
		self.options_menu.add_command(label="Auto Save Frames", command=switch_auto_save_frame_when_detected)
		self.options_menu.add_separator()
		self.options_menu.add_command(label="Show Screen Data", command=switch_displaying_on_screen_data)
		self.options_menu.add_separator()
		self.options_menu.add_command(label="Quit", command=lambda: self.window.destroy())

		# adding cascade
		self.menubar.add_cascade(label="Options", menu=self.options_menu)
        
		# label for displaying video frames
		self.video_label = Label(self.window)
		self.video_label.pack()

		# main camera initialization
		self.cap = cv2.VideoCapture(0)
		self.update_video()

		# starting mainloop
		self.window.mainloop()

	def update_video(self):
		# reading video capture frame by frame in BGR
		_, bgr_frame = self.cap.read()

		# converting BGR to RGB
		rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

		# detect body shape on current frame on BGR and RGB
		bgr_frame = body_detector.findPose(bgr_frame, draw=displaying_detection_skeleton)
		rgb_frame = body_detector.findPose(rgb_frame, draw=displaying_detection_skeleton)

		# function that returns arrays when body is detected and setting arguments for function on BGR and RGB
		frameList, bboxInfo = body_detector.findPosition(bgr_frame, bboxWithHands=displaying_rectangle, draw=displaying_rectangle)
		frameList, bboxInfo = body_detector.findPosition(rgb_frame, bboxWithHands=displaying_rectangle, draw=displaying_rectangle)

		# font instance
		font = cv2.FONT_HERSHEY_SIMPLEX

		# drawing date and time (imageVariable, "textString", (startingPointX, startingPointY), fontInstance, fontSize, (blueColor, greenColor, redColor), tickness, drawingMethod) on BGR and RGB
		drawing_date_and_time_on_frame_img_outline = cv2.putText(bgr_frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, BLACK, 4, cv2.LINE_AA)
		drawing_date_and_time_on_frame_img = cv2.putText(bgr_frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, WHITE, 1, cv2.LINE_AA)

		drawing_date_and_time_on_frame_img_outline = cv2.putText(rgb_frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, BLACK, 4, cv2.LINE_AA)
		drawing_date_and_time_on_frame_img = cv2.putText(rgb_frame, f"{strftime("%Y-%m-%d %H:%M:%S")}", (30, 20), font, 0.5, WHITE, 1, cv2.LINE_AA)

		global displaying_on_screen_data
		# if variable is true display on screen data (window info, app version)
		if displaying_on_screen_data:
			# drawing frame width and height (imageVariable, "textString", (startingPointX, startingPointY), fontInstance, fontSize, (blueColor, greenColor, redColor), tickness, drawingMethod) on BGR and RGB
			drawing_frame_width_and_height_on_frame_img_outline = cv2.putText(bgr_frame, f"w:{int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.4, BLACK, 4, cv2.LINE_AA)
			drawing_frame_width_and_height_on_frame_img = cv2.putText(bgr_frame, f"w:{int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.4, WHITE, 1, cv2.LINE_AA)

			drawing_frame_width_and_height_on_frame_img_outline = cv2.putText(rgb_frame, f"w:{int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.4, BLACK, 4, cv2.LINE_AA)
			drawing_frame_width_and_height_on_frame_img = cv2.putText(rgb_frame, f"w:{int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}, h:{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", (10, 40), font, 0.4, WHITE, 1, cv2.LINE_AA)

			# drawing app version (imageVariable, "textString", (startingPointX, startingPointY), fontInstance, fontSize, (blueColor, greenColor, redColor), tickness, drawingMethod) on BGR and RGB
			drawing_app_version_on_frame_img_outline = cv2.putText(bgr_frame, f"{__version__}", (2, int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 5)), font, 0.35, BLACK, 4, cv2.LINE_AA)
			drawing_app_version_on_frame_img = cv2.putText(bgr_frame, f"{__version__}", (2, int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 5)), font, 0.35, WHITE, 1, cv2.LINE_AA)

			drawing_app_version_on_frame_img_outline = cv2.putText(rgb_frame, f"{__version__}", (2, int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 5)), font, 0.35, BLACK, 4, cv2.LINE_AA)
			drawing_app_version_on_frame_img = cv2.putText(rgb_frame, f"{__version__}", (2, int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - 5)), font, 0.35, WHITE, 1, cv2.LINE_AA)

		# else or if variable is false do not display on screen data (window info, app version)
		else:
			pass

		# if there is a body detected condition
		if 	bboxInfo:
			global auto_save_frame_when_detected

			# draw green circle indicator if there is body detected and auto save frame is true
			if auto_save_frame_when_detected:
				detection_success_circle_outline = cv2.circle(bgr_frame, (15, 15), (8), BGR_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(bgr_frame, (15, 15), (6), BGR_GREEN, -1, cv2.LINE_AA)

				detection_success_circle_outline = cv2.circle(rgb_frame, (15, 15), (8), RGB_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(rgb_frame, (15, 15), (6), RGB_GREEN, -1, cv2.LINE_AA)

			# draw blue circle indicator if there is body detected and auto save frame is not true
			else:
				detection_success_circle_outline = cv2.circle(bgr_frame, (15, 15), (8), BGR_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(bgr_frame, (15, 15), (6), BGR_BLUE, -1, cv2.LINE_AA)

				detection_success_circle_outline = cv2.circle(rgb_frame, (15, 15), (8), RGB_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(rgb_frame, (15, 15), (6), RGB_BLUE, -1, cv2.LINE_AA)

			# if there is a body detected save frame as image
			if auto_save_frame_when_detected:
				body_detected = cv2.imwrite(f"{image_path}/body_detected_{strftime("%Y%m%d_%H%M%S")}.jpg", bgr_frame)

			# else do not save frame as image
			else:
				pass

		# if there is not body detected
		else:
			# draw red circle indicator if there is not body detected
			if auto_save_frame_when_detected == False:
				detection_success_circle_outline = cv2.circle(bgr_frame, (15, 15), (8), BGR_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(bgr_frame, (15, 15), (6), BGR_RED, -1, cv2.LINE_AA)

				detection_success_circle_outline = cv2.circle(rgb_frame, (15, 15), (8), RGB_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(rgb_frame, (15, 15), (6), RGB_RED, -1, cv2.LINE_AA)

			# draw green circle indicator if there is body detected
			else:
				detection_success_circle_outline = cv2.circle(bgr_frame, (15, 15), (8), BGR_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(bgr_frame, (15, 15), (6), BGR_GREEN, -1, cv2.LINE_AA)

				detection_success_circle_outline = cv2.circle(rgb_frame, (15, 15), (8), RGB_BACKGROUND_BLUE, -1, cv2.LINE_AA)
				detection_success_circle = cv2.circle(rgb_frame, (15, 15), (6), RGB_GREEN, -1, cv2.LINE_AA)

		# converting numpy to PIL (python image library) image frame
		img = Image.fromarray(rgb_frame)

		# converting PIL to photoimage
		imgtk = ImageTk.PhotoImage(image=img)

		# updating image label
		self.video_label.imgtk = imgtk
		self.video_label.config(image=imgtk)

		# update image frame after every N miliseconds
		self.window.after(10 , self.update_video)

	# liberate camera source after exiting app
	def __del__(self):
		self.cap.release()

# creating tkinter window
root = Tk()

# instantiating app with app title kwarg
app = BodyDetectionApp(root, window_title="Live Body Detection In Python3 With OpenCV2 And TKinter")