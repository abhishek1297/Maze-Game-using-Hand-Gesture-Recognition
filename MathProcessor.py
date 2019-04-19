from common import *

def get_area_ratio(contour, hull) :
	try :
		contour_area = cv.contourArea(contour)
		hull_area = cv.contourArea(hull)
		return ((contour_area / hull_area) * 100)
	except ZeroDivisionError :
		return 0

def get_centroid(contour) :
	moment = cv.moments(contour)
	cx, cy = 0, 0
	if moment['m00'] != 0 :
		cx = int(moment['m10'] / moment['m00'])
		cy = int(moment['m01'] / moment['m00'])
	return tuple(map(int, (cx, cy)))


def get_farthest_point(defects, contour, centroid):
	#P(x1, y1) Q(x2, y2), d(P,Q) = sqrt(square(x2 - x1) + square(y2 - y1))
	if defects is None or centroid is None :
		return None
	s = defects[:, 0][:, 0] #array of staring points of all defects in an image
	cx, cy = centroid
	x = np.array(contour[s][:, 0][:, 0], dtype=np.float) # array of x values of all starting points
	y = np.array(contour[s][:, 0][:, 1], dtype=np.float) # array of y values of all starting points
	xp = cv.pow(cv.subtract(x, cx), 2) #subtract cx from every x and apply square
	yp = cv.pow(cv.subtract(y, cy), 2) #subtract cx from every x and apply square
	# dist is an array of all distances from starting points to centroid 
	dist = cv.sqrt(cv.add(xp, yp))
	#return the index of max value
	max_index = np.argmax(dist)

	if max_index < len(s) :
		farthest_defect = s[max_index]
		farthest_point = tuple(contour[farthest_defect][0])
		
		side = "left" if centroid[0] > farthest_point[0] else "right"
		return farthest_point, side

def get_centroid_angle(farthest, norm, centroid) :
	if farthest is None :
		return -1
	#finding distances
	a = math.sqrt((farthest[0] - norm[0]) ** 2 + (farthest[1] - norm[1]) ** 2)
	b = math.sqrt((centroid[0] - norm[0]) ** 2 + (centroid[1] - norm[1]) ** 2)
	c = math.sqrt((farthest[0] - centroid[0]) ** 2 + (farthest[1] - centroid[1]) ** 2)
	#applying cosine rule to find the angle
	angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14		
	return round(angle, 2)

def get_defects_count(contour, defects, image, area) :
	
	if defects is None :
		return None
	count = 0
	for i in range(defects.shape[0]):
		s, e, f, d = defects[i, 0]
		start = tuple(contour[s][0])
		end = tuple(contour[e][0])
		far = tuple(contour[f][0])
		
		a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
		b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
		c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
		angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

		# if angle <= 110 draw a circle at the far point i.e convexity defect
		if angle <= 110 and area < 20000 :
				count += 1
				cv.circle(image, far, 3, [0, 0, 255], -1)
	return count
	

def execute(roi_image, contour) :
	
	global x, y, w, h, centroid, normal, farthest
	hull1 = cv.convexHull(contour)
	ratio = get_area_ratio(contour, hull1)
	x, y, w, h = cv.boundingRect(contour)
	normal = (int((x + w)/2), y)
	centroid = get_centroid(contour)
	
	hull = cv.convexHull(contour, returnPoints = False)
	defects = cv.convexityDefects(contour, hull)
	contour_area = cv.contourArea(contour)
	count_defects = get_defects_count(contour, defects, roi_image, contour_area)
	farthest, side = get_farthest_point(defects, contour, centroid)
	angle = get_centroid_angle(farthest, normal, centroid)
	return ratio, angle, count_defects, side, hull1, contour_area

def show(roi_image, contour, hull) :
	global x, y ,w, h, centroid, normal, farthest
	drawing = np.zeros(roi_image.shape, dtype = np.uint8)
	cv.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
	cv.drawContours(drawing, [hull], -1, (0, 0, 255), 0)
	cv.line(roi_image, centroid, farthest, [0, 255, 0], 2)
	cv.line(roi_image, centroid, normal, [255, 0, 0], 2)
	cv.rectangle(roi_image, (x, y), (x + w, y + h), (0, 59, 119), 0)
	cv.namedWindow('Contour')
	cv.moveWindow('Contour', 1200, 400)
	cv.imshow('Contour', drawing)
