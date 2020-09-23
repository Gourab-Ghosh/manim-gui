import os, sys, subprocess, time
from functions_and_constants import *

MANIM_DIR = get_manim_directory()

sys.path.insert(1, MANIM_DIR)
get_module = import_module_from_path(os.path.join(MANIM_DIR, "manimlib", "config.py")).get_module
get_scene_classes = import_module_from_path(os.path.join(MANIM_DIR, "manimlib", "extract_scene.py")).get_scene_classes_from_module

def find_scenes(file_path):
	final_list_of_scenes = []
	list_of_scenes = [scene.__name__ for scene in get_scene_classes(get_module(file_path))]
	file = import_module_from_path(file_path)
	if hasattr(file, "SCENES_IN_ORDER"):
		arbitary_list = []
		SCENES_IN_ORDER = file.SCENES_IN_ORDER
		common_scenes = set(SCENES_IN_ORDER).intersection(set(list_of_scenes))
		for scene in list_of_scenes:
			if scene in common_scenes:
				final_list_of_scenes.append(scene)
			else:
				arbitary_list.append(scene)
		final_list_of_scenes += arbitary_list
	else:
		final_list_of_scenes = list_of_scenes
	return final_list_of_scenes

def handle_colour_code(colour):
	colour = colour.upper()
	constants = import_module_from_path(os.path.join(get_manim_directory(), "manimlib", "constants.py"))
	if colour == "":
		colour = "#000000"
	elif colour in constants.COLOR_MAP or colour + "_C" in constants.COLOR_MAP:
		try:
			colour = constants.COLOR_MAP[colour]
		except KeyError:
			colour = constants.COLOR_MAP[colour + "_C"]
	return colour

def render_scenes(file_name, scenes, *args, **kwargs):
	scenes_including_file_name = [handle_spaces(file_name)] + list(scenes)
	commands = ["python", "-m", "manim"] + scenes_including_file_name + ["-"]
##########################################################################################################################################
	# Play Video(play)
	if "play" in args:
		commands[-1] += "p"
##########################################################################################################################################
	# Output Type(output_type)
	file_type_list = ["mp4", "gif", "last_frame", "save_frames"]
	command_list = ["", "i", "s", "g"]
	for file_type , command in zip(file_type_list, command_list):
		if file_type == kwargs["output_type"]:
			commands[-1] += command
##########################################################################################################################################
	# Transparent Video(transparent)
	if "transparent" in args:
		commands[-1] += "t"
##########################################################################################################################################
	# Output Quality(output_quality)
	quality = kwargs["output_quality"]
	if type(quality) in (list, tuple):
		if len(quality) == 0:
			quality = "production quality"
	commands[-1] += [quality[0] if quality in ("low quality", "medium quality") else "r \"" + str(quality)[1 : -1] + "\"" if type(quality) in (list, tuple) else ""][0]
	if quality == "high quality":
		commands += ["--high_quality"]

	for i in range(2):
		if commands[-(i + 1)] == "-":
			commands.pop(-(i + 1))
##########################################################################################################################################
	# Background colour(bg_colour)
	if "bg_colour" in kwargs:
		commands += ["-c", handle_colour_code(kwargs["bg_colour"])]
##########################################################################################################################################
	# Output Name(output_name)
	if kwargs["output_name"] != "":
		commands += ["-o", str(kwargs["output_name"])]
##########################################################################################################################################
	# Output path(output_path)
	if get_video_directory() != None:
		if quality == "low quality":
			output_folder_name = "480p15"
		elif quality == "medium quality":
			output_folder_name = "720p30"
		elif quality == "high quality":
			output_folder_name = "1080p60"
		elif quality == "production quality":
			output_folder_name = "1440p60"
		else:
			output_folder_name = f"{quality[0]}p60"
		output_path = handle_spaces(os.path.join(get_video_directory(), os.path.splitext(os.path.split(file_name)[1])[0], output_folder_name))
		commands += ["--video_output_dir", output_path]
##########################################################################################################################################
	# Leave progress bars(progress_bars)
	if "progress_bars" in args:
		commands += ["--leave_progress_bars"]
##########################################################################################################################################
	final_command = " ".join(commands)

	print(f"command -> {final_command}\n")
	current_time = time.time()

	error = subprocess.run(final_command, shell = True)

	render_time = seconds_to_normal_time(time.time() - current_time)
	return error, render_time