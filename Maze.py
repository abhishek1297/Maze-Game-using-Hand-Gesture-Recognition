from common import *
from random import randint
class Maze :
	def __init__(self, mode, index):
		self.mode = mode
		self.sq_side = mode[1]
		self.width = mode[2]
		self.height = mode[3]
		self.WALL_SCALE = WALL_SCALE[index]
		self.maze = None
		self.start = None
		self.end = None
		self.st_xy, self.en_xy = [None] * 2
		self.wall_list = None
		self.shape_list = None
		
	def load_maze(self) :
		fp = None
		r = str(randint(1, 5))
		if self.mode[0] == "easy" :
			#self.sq_side, self.width, self.height = 40, 600, 600
			f = "levels\easy\easy" + r
			self.maze = np.loadtxt(f, dtype = np.uint)
			fp = open("levels\easy\start_end.txt", "r")
			index = int(f[-1]) - 1
			self.start, self.end = fp.readlines()[index].split("-")
			self.start = tuple(map(int, self.start.split(",")))
			self.end = tuple(map(int, self.end.split(",")))

		elif self.mode[0] == "medium" :
			#self.sq_side, self.width, self.height = 40, 640, 640
			f = "levels\medium\medium" + r
			self.maze = np.loadtxt(f, dtype = np.uint)
			fp = open("levels\medium\start_end.txt", "r")
			index = int(f[-1]) - 1
			self.start, self.end = fp.readlines()[index].split("-")
			self.start = tuple(map(int, self.start.split(",")))
			self.end = tuple(map(int, self.end.split(",")))

		elif self.mode[0] == "hard" :
			#self.sq_side, self.width, self.height = 30, 750, 750
			f = "levels\hard\hard" + r
			self.maze = np.loadtxt(f, dtype = np.uint)
			fp = open("levels\hard\start_end.txt", "r")
			index = int(f[-1]) - 1
			self.start, self.end = fp.readlines()[index].split("-")
			self.start = tuple(map(int, self.start.split(",")))
			self.end = tuple(map(int, self.end.split(",")))
		fp.close()
		
	def setup(self) :
	
		self.load_maze()
		self.wall_list = arc.SpriteList()
		self.shape_list = arc.ShapeElementList()
		rows, cols = self.maze.shape
		hf_sq_side = self.sq_side // 2
		x = 0
		y = hf_sq_side
		for i in range(rows) :
			x = hf_sq_side
			for j in range(cols) :
				if self.maze[i][j] == 1 :
					wall = arc.Sprite("images\wall_sprite.png", self.WALL_SCALE)
					wall.center_x = x
					wall.center_y = y
					self.wall_list.append(wall)
				#else :
				#	rect = arc.create_rectangle_outline(x, y, self.sq_side, self.sq_side, arc.color.WHITE)
				#	self.shape_list.append(rect)
				
				if self.start == (i, j) :
					self.st_xy = (x, y)
					shape = arc.create_ellipse_filled(x, y, hf_sq_side // 2, hf_sq_side // 2, arc.color.RED)
					self.shape_list.append(shape)
				elif self.end == (i, j) :
					self.en_xy = (x, y)
					shape = arc.create_ellipse_filled(x, y, hf_sq_side // 2, hf_sq_side // 2, arc.color.GREEN)
					self.shape_list.append(shape)
				
				x += self.sq_side
			y += self.sq_side

	def get_dimension(self) :
		return self.width, self.height
	
	def get_start_end(self) :
		return self.st_xy, self.en_xy
	
	def draw(self) :
		self.wall_list.draw()
		self.shape_list.draw()
		
#end_maze