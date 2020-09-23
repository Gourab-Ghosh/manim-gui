import os, importlib

MANIM_GUI_CONFIG_DIR = os.path.expanduser("~") + os.sep + ".MANIM_GUI_CONFIG"
if not os.path.exists(MANIM_GUI_CONFIG_DIR):
	os.makedirs(MANIM_GUI_CONFIG_DIR)

DEFAULT_FONT = ("algerian", 11)

def import_module_from_path(module_full_path):
	return importlib.util.spec_from_file_location(
		os.path.splitext(
			os.path.split(
				module_full_path
				)[1]
			)[0],
		module_full_path,
		).loader.load_module()

def get_file_dir(file_path):
	file_dir, file_name = os.path.split(file_path)
	return file_dir

def access_manim_gui_directory_files(file_name , operation, text = "", makedirs = True):
	global MANIM_GUI_CONFIG_DIR
	operation = operation.lower().strip()
	text_file = os.path.join(MANIM_GUI_CONFIG_DIR, file_name + ".txt")
	if operation == "read":
		if os.path.isfile(text_file):
			with open(text_file, "r") as file:
				path = file.read()
			if os.path.exists(path):
				return path
			else:
				if makedirs:
					os.makedirs(path)
					return path
	if operation in ("write", "append"):
		with open(text_file, operation[0]) as file:
			file.write(text)

def verify_manim_directory(manim_path):
	return all(
		[
			os.path.isfile(
				os.path.abspath(
					os.path.join(
						manim_path,
						"manimlib",
						file,
						)
					)
				)
			for file in (
				"constants.py",
				"extract_scene.py",
				"config.py",
				)
			]
		) and os.path.isfile(
			os.path.abspath(
				os.path.join(
					manim_path,
					"manim.py",
					)
				)
			)

def get_manim_directory():
	manim_path = access_manim_gui_directory_files("manim_location", "read", makedirs = False)
	if manim_path == None:
		return
	if verify_manim_directory(manim_path):
		return manim_path

def reset_manim_directory(path):
	access_manim_gui_directory_files("manim_location", "write", path)

def get_video_directory():
	return access_manim_gui_directory_files("video_saving_directory", "read")

def reset_video_directory(path):
	access_manim_gui_directory_files("video_saving_directory", "write", path)

def get_last_rendered_file():
	file = access_manim_gui_directory_files("last_rendered_file", "read", makedirs = False)
	if file != None:
		if os.path.isfile(file) and file[-3:] == ".py":
			return file

def reset_last_rendered_file(file):
	access_manim_gui_directory_files("last_rendered_file", "write", file)

def get_last_rendered_file_dir():
	if get_last_rendered_file() != None:
		return get_file_dir(get_last_rendered_file())

def handle_spaces(path):
	return ["\"" + path + "\"" if " " in path else path][0]

def seconds_to_normal_time(seconds = None):
	if seconds != None:
		seconds = int(round(float(seconds)))
		Time = []
		Time.append(seconds % 60)
		minute = seconds // 60
		Time.append(minute % 60)
		hour = minute // 60
		Time.append(hour)
		while Time[-1] == 0:
			Time.pop(-1)
		Time = [str(item) for item in Time[::-1]]
		Time = ":".join([item if len(item) == 2 else "0" + item for item in Time])
		if ":" not in Time:
			Time = "00:" + Time
		return Time