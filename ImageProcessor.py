from common import *

def acquire_image(cap) :
	_, frame = cap.read()
	cv.rectangle(frame, roi_1, roi_2, (0, 255, 0), 0)
	cropped = frame[roi_1[0]:roi_2[0], roi_1[1]:roi_2[1]]
	return frame, cropped


def pre_process_image(image) :
	denoised = cv.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 3)
	blurred = cv.GaussianBlur(denoised, (11, 11), 0)
	hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
	hsv = cv.GaussianBlur(hsv, (11, 11), 0)
	return hsv
	
def get_skin_mask(image) :
	kernel = np.ones((5, 5))
	skin_mask = cv.inRange(image, skin_l1, skin_u1)
	skin_mask = cv.dilate(skin_mask, kernel, iterations = 2)
	skin_mask = cv.erode(skin_mask, kernel, iterations = 2)
	skin_mask = cv.GaussianBlur(skin_mask, (11, 11), 0)
	return skin_mask

def extract_feature(mask) :
	global binary
	try :
		ret, binary = cv.threshold(mask, 127, 255, 0)
		contours, _ = cv.findContours(binary.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		contour = max(contours, key=lambda x: cv.contourArea(x))
		return contour
	except :
		return None
		
def execute(capture) :
	global frame
	frame, cropped = acquire_image(capture)
	pre_processed = pre_process_image(cropped)
	skin_mask = get_skin_mask(pre_processed)
	contour = extract_feature(skin_mask)
	return cropped, contour
	
def show(GESTURE) :
	global frame, binary
	cv.namedWindow('Frame', cv.WINDOW_NORMAL)
	cv.moveWindow('Frame', 900, 100)
	cv.resizeWindow('Frame', 600, 400)
	cv.namedWindow('Binary')
	cv.moveWindow('Binary', 900, 400)
	cv.imshow('Frame', frame)
	cv.imshow('Binary', binary)
	cv.putText(frame, GESTURE,(0,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)