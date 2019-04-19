from common import *

class Player(arc.Sprite) :

	def __init__(self, filename, scale, w, h, start, wall_list, dist) :
		super().__init__(filename, scale)
		self.screen_width = w
		self.screen_height = h
		self.center_x, self.center_y = self.start = start
		self.wall_list = wall_list
		self.num = 0
		self.dist = dist
		self.hit_sound = arc.load_sound("tracks/collide.mp3")
		
	def reset(self) :
		self.center_x, self.center_y = self.start
	
	def check_for_collision(self) :
		return len(arc.check_for_collision_with_list(self, self.wall_list)) > 0
				
	def update(self) :
		prev_x = self.center_x
		prev_y = self.center_y
		self.center_x += self.change_x
		self.center_y += self.change_y
		if self.check_for_collision() :
			self.num += 1
		if self.num > 30 :
			self.num = 0
			arc.play_sound(self.hit_sound)
		if self.left < 0 :
			self.left = 0
		elif self.right > self.screen_width - 1 :
			self.right = self.screen_width - 1
		if self.bottom < 0 :
			self.bottom = 0
		elif self.top > self.screen_height - 1 :
			self.top = self.screen_height - 1