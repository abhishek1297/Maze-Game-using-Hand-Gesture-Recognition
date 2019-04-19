from common import *
from Maze import Maze, randint
from Player import Player
import Recognizer
from collections import Counter
#import inspect
#import pdb
import pyglet
pyglet.options['debug_gl'] = False
CAMERA = Recognizer.RecogThread()
Recognizer.SHOW_MENU = True

class MazeGame(arc.Window) :
	
	def __init__(self, width, height, title) :
		super().__init__(width, height, title, resizable = True)
		self.w = width
		self.h = height
		arc.set_background_color((33, 0, 0))
		self.reached_end_flag = False
		self.player = None
		self.physics = None
		self.level = -1
		self.maze = None
		self.start, self.end = 0, 0
		self.num1 = 0
		self.num2 = 0
		self.num3 = 0
		self.iters = 30
		self.level_list = [-1] * self.iters # list of selected level in menu mode
		self.guide_list = [-1] * self.iters# list for selected gesture in guide mode
		self.gestures_list = [""] * self.iters# performed moves on player
		self.CAN_PLAY = False
		Recognizer.SHOW_GUIDE = False
		self.level_sprites = None
		self.guide_sprites = None
		self.rand_xy_list = [(randint(30, 470), randint(30, 470)) for _ in range(100)]
		self.wall_texture = arc.load_texture("images/wall_sprite.png")
		self.select_sound = arc.load_sound("tracks/select.mp3")
		self.win_sound = arc.load_sound("tracks/win.mp3")
		#pdb.set_trace()
	#end_init
	
	def reinit(self) :
		arc.set_background_color((33, 0, 0))
		self.CAN_PLAY = False
		self.num1 = 0
		self.num2 = 0
		self.num3 = 0
		self.level_list = [-1] * self.iters
		self.gestures_list = [""] * self.iters
		self.guide_list = [-1] * self.iters

	def on_resize(self, width, height) :
		super().on_resize(self.w, self.h)

	def get_maze_level(self) :
		
		if Recognizer.GESTURE == "Easy" : return 0
		elif Recognizer.GESTURE == "Medium" : return 1
		elif Recognizer.GESTURE == "Hard" : return 2
		elif Recognizer.GESTURE == "Guide" : return 3
		elif Recognizer.GESTURE == "Rock" : return 5
		return -1

	def get_guide_exit_num(self) :
		if Recognizer.GESTURE == "Fist" : return 4
		return -1
	def get_player_sprite(self) :
		
		self.start, self.end = self.maze.get_start_end()
		pl = Player("images\player_sprite.png", PLAYER_SCALE[self.level], self.w, self.h,
		self.start, self.maze.wall_list, self.maze.sq_side)
		return pl

	def move_player(self) :
		
		counter = Counter(self.gestures_list)
		gest = list(counter.keys())[0]
		if gest == "Fist" :
			arc.pause(1)
			Recognizer.SHOW_MENU = True
			arc.play_sound(self.select_sound)
			self.reinit()
			self.level = -1
		elif gest == "Left" :
			self.player.change_x = -STEP[self.level]
		elif  gest == "Right" :
			self.player.change_x = STEP[self.level]
		elif gest == "Up" :
			self.player.change_y = STEP[self.level]
		elif gest == "Down" :
			self.player.change_y = -STEP[self.level]
		elif gest == "Five" :
			arc.pause(0.5)
			self.player.reset()
			self.CAN_PLAY = False

	def create_level(self) :
		
		levels = [["easy", 62.5, 500, 500],
		["medium", 35.714, 500, 500],
		["hard", 21.739, 500, 500]]
		self.maze = Maze(levels[self.level], self.level)
		self.w, self.h = self.maze.get_dimension()
		self.maze.setup()
			
	def setup(self) :
		
		if 0 <= self.level <= 2 :
			arc.set_background_color((33, 0, 0))
			self.create_level()
			self.player = self.get_player_sprite()
			self.physics = arc.PhysicsEngineSimple(self.player, self.maze.wall_list)

#----------------DRAWING-------------------
	def draw_gesture_images(self) :
		
		try :
			self.level_sprites = arc.SpriteList()
			gest = arc.Sprite("images/my/one.png", 0.18)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 250
			self.level_sprites.append(gest)

			gest = arc.Sprite("images/my/two.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 310
			self.level_sprites.append(gest)
			
			gest = arc.Sprite("images/my/three.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 372
			self.level_sprites.append(gest)

			gest = arc.Sprite("images/my/five.png", 0.14)
			gest.center_x = 25
			gest.center_y = 30
			self.level_sprites.append(gest)

			gest = arc.Sprite("images/my/rock.png", 0.17)
			gest.center_x = 475
			gest.center_y = 30
			self.level_sprites.append(gest)
			
			self.level_sprites.draw()
		except :
			pass
	
	def draw_guide_sprites(self) :
		
		try :
			self.guide_sprites = arc.SpriteList()
			gest = arc.Sprite("images/my/rock.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 120
			self.guide_sprites.append(gest)

			gest = arc.Sprite("images/my/five.png", 0.13)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 180
			self.guide_sprites.append(gest)
			
			gest = arc.Sprite("images/my/left.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 240
			self.guide_sprites.append(gest)
			
			gest = arc.Sprite("images/my/right.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 300
			self.guide_sprites.append(gest)

			gest = arc.Sprite("images/my/one.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 360
			self.guide_sprites.append(gest)
			
			gest = arc.Sprite("images/my/two.png", 0.15)
			gest.center_x = WIDTH // 2 - 60
			gest.center_y = HEIGHT - 420
			self.guide_sprites.append(gest)
			
			gest = arc.Sprite("images/my/fist.png", 0.2)
			gest.center_x = 30
			gest.center_y = 30
			self.guide_sprites.append(gest)
			
			self.guide_sprites.draw()
		except Exception as e:
			print(e)

	def draw_show_guide(self) :
		
		self.draw_background()
		arc.draw_text("Player Controls", WIDTH // 2, HEIGHT - 20,
		arc.color.WHITE, 20, width = 200, align = "center",
		anchor_x="center", anchor_y="center")
		
		arc.draw_text("A Simple Maze Game having three Difficulties.\nPlayer can use following gestures.",
		WIDTH // 2, HEIGHT - 70,
		arc.color.WHITE, 15, width = 350, align = "center",
		anchor_x="center", anchor_y="center")
		
		arc.draw_text("Start the Game", WIDTH // 2 + 30, HEIGHT - 120,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")
			
		arc.draw_text("Reset", WIDTH // 2, HEIGHT - 180,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")

		arc.draw_text("Left", WIDTH // 2 - 5, HEIGHT - 240,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")
		
		arc.draw_text("Right", WIDTH // 2, HEIGHT - 300,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")
		
		arc.draw_text("Up", WIDTH // 2 - 5, HEIGHT - 360,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")
		
		arc.draw_text("Down", WIDTH // 2, HEIGHT - 420,
			arc.color.WHITE, 14, width = 150, align = "center",
			anchor_x="center", anchor_y="center")

		arc.draw_text("Back to Menu (From Game also)", 30, 30,
			arc.color.WHITE, 10, width = 200, align = "center",
			anchor_x="left", anchor_y="center")
		
		self.draw_guide_sprites()

	
	def draw_instructions(self) :

		self.draw_background()
		
		arc.draw_text("Instructions", WIDTH // 2, HEIGHT - 20,
		arc.color.WHITE, 20, width = 200, align = "center",
		anchor_x="center", anchor_y="center", bold = True)
		
		arc.draw_text("1) Rest your elbow on something so that your hand won't tire.",
		WIDTH // 2, HEIGHT - 70,
		arc.color.WHITE, 14, width = 450, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		arc.draw_text("2) The Game does not work in\ndark lighting conditions.",
		WIDTH // 2, HEIGHT - 110,
		arc.color.WHITE, 14, width = 350, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		arc.draw_text("3) For Better Accuracy, make sure that the\nRectangle in which you put your hand in, has a plain\nbackground remotely resembling the skin color.",
		WIDTH // 2, HEIGHT - 160,
		arc.color.WHITE, 14, width = 500, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		arc.draw_text("4) Illumination has a great impact on the Game, Check the Binary\n(Black and White) Image which is in the small window. The result\nwill be more accurate if the performed gesture is filled with White\ncolor and the background is Black. Make sure to sit accordingly.",
		WIDTH // 2, HEIGHT - 230,
		arc.color.WHITE, 14, width = 500, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		arc.draw_text("5) It is possible that some gestures may give\nwrong outcome because of some similarities.",
		WIDTH // 2, HEIGHT - 300,
		arc.color.WHITE, 14, width = 400, align = "center",
		anchor_x="center", anchor_y="center", bold = True)
		
		arc.draw_text("6) Only put your hand inside the Box and Not the part which\nis below the Wrist. Try keeping all the fingers and palm inside\nthe Box. Do not put your hand too far or near from the Camera.",
		WIDTH // 2, HEIGHT - 360,
		arc.color.WHITE, 14, width = 500, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		arc.draw_text("7) For Seamless movements, Perform\nGestures prior making a move.",
		WIDTH // 2, HEIGHT - 410,
		arc.color.WHITE, 14, width = 400, align = "center",
		anchor_x="center", anchor_y="center", bold = True)

		gest = arc.Sprite("images/my/fist.png", 0.2)
		gest.center_x = 30
		gest.center_y = 30
		gest.draw()
		
		arc.draw_text("Back to Menu", 30, 30,
			arc.color.WHITE, 10, width = 150, align = "center",
			anchor_x="left", anchor_y="center")
		
		
	def draw_background(self) :
		for tup in self.rand_xy_list :
			arc.draw_texture_rectangle(tup[0], tup[1], 30, 30, self.wall_texture)

	def draw_menu(self) :
		self.draw_background()
		arc.draw_text("MAZE GAME", WIDTH // 2, HEIGHT - 100,
			arc.color.WHITE, 50, width = 360, align = "center",
			anchor_x="center", anchor_y="center", bold = True)
		arc.draw_text("Select Difficulty", WIDTH // 2, HEIGHT - 200,
			arc.color.WHITE, 20, width = 180, align = "center",
			anchor_x="center", anchor_y="center", bold = True)
		arc.draw_text("Easy", WIDTH // 2, HEIGHT - 250,
			arc.color.WHITE, 16, width = 150, align = "center",
			anchor_x="center", anchor_y="center", bold = True)
		arc.draw_text("Medium", WIDTH // 2, HEIGHT - 310,
			arc.color.WHITE, 16, width = 150, align = "center",
			anchor_x="center", anchor_y="center", bold = True)
		arc.draw_text("Hard", WIDTH // 2, HEIGHT - 372,
			arc.color.WHITE, 16, width = 150, align = "center",
			anchor_x="center", anchor_y="center", bold = True)
		arc.draw_text("Player Guide", 50, 25,
			arc.color.WHITE, 12, width = 100, align = "center",
			anchor_x="left", anchor_y="center", bold = True)
		arc.draw_text("Read Instructions", 330, 25,
			arc.color.WHITE, 12, width = 120, align = "center",
			anchor_x="left", anchor_y="center", bold = True)
		
		self.draw_gesture_images()
	
	def draw_text_level(self) :
		txt = ""
		if Recognizer.GESTURE != "Put the Hand Inside the Box" :
			txt = Recognizer.GESTURE
		
		arc.draw_text(txt, 70, 470,
			arc.color.WHITE, 30, width = 120, align = "center",
			anchor_x="center", anchor_y="center")
	
	def draw_game(self) :
		
		self.maze.draw()
		self.player.draw()
	
	def draw(self) :
		if Recognizer.SHOW_GUIDE :
			self.draw_show_guide()
		elif Recognizer.SHOW_INST :
			self.draw_instructions()
		elif Recognizer.SHOW_MENU :
			self.draw_menu()
		elif 0 <= self.level <= 2:
			self.draw_game()

		self.draw_text_level()
	
	def on_draw(self) :
		
		arc.start_render()
		self.draw()

#-----------------UPDATE--------------------
	def set_reached_end(self) :
		
		if 0 <= self.level <= 2 :
			diff1 = abs(self.end[0] - self.player.center_x)
			diff2 = abs(self.end[1] - self.player.center_y)
			self.reached_end_flag =  diff1 <= BOUND[self.level] and diff2 <= BOUND[self.level]	
			
	def update_guide_instruction(self) :
		
		#print("num3 = ", self.num3)
		self.guide_list[self.num3] = self.get_guide_exit_num()
		self.num3 += 1
		if self.num3 == self.iters :
			self.num3 = 0
			self.level = list(Counter(self.guide_list).keys())[0]
		if self.level == 4 :
			Recognizer.SHOW_INST = False
			Recognizer.SHOW_GUIDE = False
			Recognizer.SHOW_MENU = True
			self.reinit()
			self.level = -1
			arc.pause(0.7)
			arc.play_sound(self.select_sound)
			
	
	def update_game(self) :
		
		if not self.CAN_PLAY and Recognizer.GESTURE == "Rock" :
			self.CAN_PLAY = True
		if self.CAN_PLAY :
			#print("num1 = ", self.num1)
			self.gestures_list[self.num1] = Recognizer.GESTURE
			self.num1 += 1	
			if self.num1 == self.iters :
				self.player.change_x = 0
				self.player.change_y = 0
				if 0 <= self.level <= 2 :
					self.move_player()
				self.num1 = 0
				self.set_reached_end()
				if self.reached_end_flag :
					Recognizer.SHOW_MENU = True
					arc.pause(1)
					arc.play_sound(self.win_sound)
					self.level = -1
					#arc.play_sound(self.select_sound)
					self.reinit()
					
					return
			self.player.update()
			self.physics.update()

	def update_menu(self) :
		
		#print("num2 = ", self.num2)
		self.level_list[self.num2] = self.get_maze_level()
		self.num2 += 1
		if self.num2 == self.iters :
			self.num2 = 0
			self.level = list(Counter(self.level_list).keys())[0]
			if self.level == 3 :
				Recognizer.SHOW_GUIDE = True
				Recognizer.SHOW_MENU = False
				arc.play_sound(self.select_sound)
			elif self.level == 5 :
				Recognizer.SHOW_INST = True
				Recognizer.SHOW_MENU = False
				arc.play_sound(self.select_sound)
			elif self.level != -1 :
				arc.pause(1)
				Recognizer.SHOW_MENU = False
				arc.play_sound(self.select_sound)
				self.reinit()
				self.setup()
				
	def update(self, delta) :
		
		if Recognizer.SHOW_GUIDE or Recognizer.SHOW_INST : self.update_guide_instruction()
		elif Recognizer.SHOW_MENU : self.update_menu()
		else : self.update_game()
		
	def start_cam(self) :
		CAMERA.start()

	def __del__(self) :
		Recognizer.capture.release()
		Recognizer.cv.destroyAllWindows()		
		
		
def main() :
	try :
		window = MazeGame(500, 500, "Maze Game")
		window.start_cam()
		arc.run()
		Recognizer.CAMERA_IS_ON = False
	except Exception as e :
		print(e)

if __name__ == "__main__" :
	main()
	