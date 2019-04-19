from common import *
import threading
import ImageProcessor
import MathProcessor
import time
capture = cv.VideoCapture(0)
if not capture.isOpened() :
	print("No Camera Detected.")
	input("Press any key to exit.")
	exit(1)

CAMERA_IS_ON = True
GESTURE = ""
SHOW_MENU = True
SHOW_GUIDE = False
SHOW_INST = False
#SLEEP = False
def move_gesture(count, angle, ratio, side, contour_area) :
	#print("move_gesture")
	if ratio > 50 and contour_area > 600 :
		if count == 1 :
			if 82 <= ratio <= 95 :
				if 53 <= angle <= 90 and side == "right" :
					return "Left"
				elif 0 <= angle <= 20 and side == "left" :
					return "Right"
			
			elif 20 <= angle <= 53 and 60 <= ratio <= 78 :
				return "Rock"				
			elif 0 <= angle <= 18 and 64 <= ratio <= 80:
				return "Down"
		elif count == 0 :
			if 6 <= angle <= 50 and 75 <= ratio <= 90 and side == "right" :
				return "Up"
			elif ratio > 90 and angle > 50 :
				return "Fist"
		elif count == 2 :
			if 0 <= angle <= 18 and 64 <= ratio <= 80:
				return "Down"
		elif count == 4 :
			return "Five"

	return "Invalid"

def menu_select_maze(count, ratio, contour_area, angle, side) :
	#print("SHOW_MENU_gesture")
	if ratio > 50 and contour_area > 600 :
		if count == 4 :
			return "Guide"
		elif count == 1 and 20 <= angle <= 53 and 60 <= ratio <= 78 :
			return "Rock"
		elif count == 0 and 6 <= angle <= 50 and 75 <= ratio <= 90 and side == "right" :
			return "Easy"
		elif count == 1 and 0 <= angle <= 18 and 64 <= ratio <= 80 :
			return "Medium"
		elif count == 2 and 16 <= angle <= 50 and 65 <= ratio <= 90 :
			return "Hard"

	return "Invalid"

def back_to_menu_gesture(count, ratio, contour_area) :
	#print("back t_gesture")
	if ratio > 80 and contour_area > 600 and  count == 0 :
		return "Fist"
	return "Invalid"
	
	
def get_input() :
	global CAMERA_IS_ON, GESTURE, capture, frame, SHOW_MENU, SHOW_GUIDE, SHOW_INST
	while CAMERA_IS_ON :
		try :

			roi_image, contour = ImageProcessor.execute(capture)
			if contour is None :
				GESTURE = "Put the Hand Inside the Box"
			ImageProcessor.show(GESTURE)
			ratio, angle, defects_count, side, hull, contour_area = MathProcessor.execute(roi_image, contour)
			MathProcessor.show(roi_image, contour, hull)

			if contour_area < 5000 :
				GESTURE = "Put the Hand Inside the Box"
			elif SHOW_MENU :
				GESTURE = menu_select_maze(defects_count, ratio, contour_area, angle ,side)
			elif SHOW_GUIDE or SHOW_INST :
				GESTURE = back_to_menu_gesture(defects_count, ratio, contour_area)
			else :	
				GESTURE = move_gesture(defects_count, angle, ratio, side, contour_area)
			ImageProcessor.show(GESTURE)
		except Exception as e:
			#print(e)
			ImageProcessor.show("Put the Hand Inside the Box")
			pass
		if ord('q') == cv.waitKey(2) :
			break
		#cv.waitKey(2)
	#end_while
	capture.release()
	cv.destroyAllWindows()		


class RecogThread(threading.Thread) :
	def run(self) :
		get_input()
		
	#def sleep(self, ts) :
	#	time.sleep(ts)

if __name__ == "__main__" :
	RecogThread().start()