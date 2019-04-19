import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "D:\\Programming\\Anaconda\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "D:\\Programming\\Anaconda\\tcl\\tk8.6"

exec_list = [cx_Freeze.Executable("Maze Game.py", icon = "images\\icon.ico")]

package_list = ["numpy", "cv2", "arcade", "math", "random", "threading", "common",
"ImageProcessor","MathProcessor", "Maze", "Player", "Recognizer", "collections",
"pyglet"]

files_list = ["images", "levels", "tracks"]

cx_Freeze.setup(
	name = "Maze Game",
	options = {
		"build_exe": {"packages": package_list, "include_files": files_list}
	},
	description = "A Simple Maze Game using Hand Gesture Recognition",
	executables = exec_list,
	version = "5.1.1"
)