import os, tkinter as tk
from tkinter import ttk, TclError, filedialog
from functions_and_constants import *

class Listbox(tk.Listbox):
	def __init__(self, root, *args, **kwargs):
		self.root = root
		self.frame = ttk.Frame(self.root)

		self.scrollbar = ttk.Scrollbar(
			self.frame,
			orient = tk.VERTICAL,
			takefocus = 0,
			)

		super().__init__(self.frame, *args, **kwargs, yscrollcommand = self.scrollbar.set)

		self.scrollbar.config(command = self.yview)
		self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

		super().pack(fill = tk.BOTH)

	def grid(self, *args, **kwargs):
		self.frame.grid(*args, **kwargs)

	def pack(self, *args, **kwargs):
		self.frame.pack(*args, **kwargs)

ttk.Listbox = Listbox

class Frame:
	def __init__(
		self,
		root,
		add_method = "pack",
		*args,
		frame_type = ttk,
		add_kwargs = {},
		**kwargs,
		):

		self.root = root
		self.frame = frame_type.LabelFrame(self.root, *args, **kwargs)
		if add_method == "pack":
			self.frame.pack(**add_kwargs)
		if add_method == "grid":
			self.frame.grid(**add_kwargs)

	def add(
		self,
		obj_name,
		obj_type,
		add_method,
		create_new_object = True,
		obj_args = [],
		obj_kwargs = {},
		add_args = [],
		add_kwargs = {},
		):

		if create_new_object:
			obj = obj_type(self.frame, *obj_args, **obj_kwargs)
			exec(f"self.{obj_name} = obj")
		exec(f"self.{obj_name}.{add_method}(*add_args, **add_kwargs)")
		return obj

	def add_by_default(
		self,
		obj_name,
		object_type,
		add_method = "grid",
		create_new_object = True,
		obj_args = [],
		obj_kwargs = {},
		add_args = [],
		add_kwargs = {},
		):

		if object_type.startswith("tk.") or object_type.startswith("ttk."):
			exec(
				f"obj_type = {object_type}",
				globals(),
				)
		else:
			try:
				exec(
					f"obj_type = ttk.{object_type}",
					globals(),
					)
			except AttributeError:
				exec(
					f"obj_type = tk.{object_type}",
					globals(),
					)
		try:
			obj = self.add(
				obj_name,
				obj_type,
				add_method,
				create_new_object,
				obj_args,
				obj_kwargs,
				add_args,
				add_kwargs,
				)
		except TclError:
			add_method = ["grid" if add_method == "pack" else "pack"][0]
			obj = self.add(
				obj_name,
				obj_type,
				add_method,
				create_new_object,
				obj_args,
				obj_kwargs,
				add_args,
				add_kwargs,
				)
		return obj

	def remove(self, obj_name, parmanently_delete = False):
		exec(f"self.{obj_name}.grid_forget()")
		if parmanently_delete:
			exec(f"del self.{obj_name}")

	@property
	def MANIM_DIR(self):
		return get_manim_directory()

	@MANIM_DIR.setter
	def MANIM_DIR(self, path):
		reset_manim_directory(path)

	@property
	def VIDEO_DIR(self):
		return get_video_directory()

	@VIDEO_DIR.setter
	def VIDEO_DIR(self, path):
		reset_video_directory(path)

	@property
	def LAST_RENDERED_FILE(self):
		return get_last_rendered_file()

	@LAST_RENDERED_FILE.setter
	def LAST_RENDERED_FILE(self, file):
		reset_last_rendered_file(file)

	@property
	def LAST_RENDERED_FILE_DIR(self):
		return get_last_rendered_file_dir()

class EditDefaultFrame(Frame):
	def __init__(self, root, main_frame, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.main_frame = main_frame

		padx = 25; pady = 5

		self.add_by_default(
			"manim_dir_set_label",
			"Label",
			obj_kwargs = dict(
				text = "Enter the Default Manim directory path or Video directory path and click the corresponding button below to set or reset the directory path.",
				font = DEFAULT_FONT,
				),
			add_kwargs = dict(
				row = 0,
				columnspan = 4,
				padx = padx,
				pady = pady,
				),
			)
		self.add_by_default(
			"choose_file_label",
			"Label",
			obj_kwargs = dict(
				text = "Choose File :",
				font = DEFAULT_FONT,
				foreground = "green",
				),
			add_kwargs = dict(
				row = 1,
				column = 0,
				padx = padx,
				pady = pady,
				sticky = tk.E,
				),
			)
		self.add_by_default(
			"dir_entrybox",
			"Entry",
			obj_kwargs = dict(
				foreground = "green",
				width = 100,
				),
			add_kwargs = dict(
				row = 1,
				column = 1,
				columnspan = 2,
				padx = padx,
				pady = pady,
				),
			)
		self.add_by_default(
			"browse_button",
			"Button",
			obj_kwargs = dict(
				text = "Browse Path",
				command = self.browse_button_function,
				),
			add_kwargs = dict(
				row = 1,
				column = 3,
				padx = padx,
				pady = pady,
				sticky = tk.W,
				),
			)
		self.add_by_default(
			"manim_set_directory_button",
			"Button",
			obj_kwargs = dict(
				text = "",
				command = self.set_manim_directory_button_function,
				),
			add_kwargs = dict(
				row = 2,
				column = 1,
				padx = padx,
				pady = pady,
				),
			)
		self.add_by_default(
			"video_set_directory_button",
			"Button",
			obj_kwargs = dict(
				text = "",
				command = self.set_video_directory_button_function,
				),
			add_kwargs = dict(
				row = 2,
				column = 2,
				padx = padx,
				pady = pady,
				),
			)
		self.add_by_default(
			"dir_set_confirmation_label",
			"Label",
			obj_kwargs = dict(
				text = "",
				font = ("halvetica", 11),
				),
			add_kwargs = dict(
				row = 3,
				columnspan = 4,
				padx = padx,
				pady = pady,
				),
			)

		self.check_set_directory_button_text()

	def browse_button_function(self):
		initialdir = None

		for path in (
			self.VIDEO_DIR,
			self.MANIM_DIR,
			os.path.expanduser("~"),
			):

			if initialdir == None:
				initialdir = path
			else:
				break

		req_dir = filedialog.askdirectory(
			initialdir = initialdir,
			title = f"Choose the directory to reset defaults."
			)

		if req_dir != "":
			req_dir = os.path.abspath(req_dir)

		self.dir_entrybox.delete(0, "end")
		self.dir_entrybox.insert(0, req_dir)

	def set_manim_directory_button_function(self):
		manim_dir = self.dir_entrybox.get()

		if verify_manim_directory(manim_dir):
			self.MANIM_DIR = os.path.abspath(manim_dir)
			self.do_after_setting_manim_dir()
			self.dir_set_confirmation_label["foreground"] = "green"

			if os.path.abspath(manim_dir) == manim_dir:
				self.dir_set_confirmation_label["text"] = "Default Manim directory successfully saved."
			else:
				self.dir_set_confirmation_label["text"] = f"Default Manim directory set as {os.path.abspath(manim_dir)}."

		else:
			self.dir_set_confirmation_label["foreground"] = "red"
			self.dir_set_confirmation_label["text"] = "The path you provided is either invalid or it is not the correct path to the Manim directory. Please try again."

		self.check_set_directory_button_text()
		self.dir_entrybox.delete(0, "end")

	def set_video_directory_button_function(self):

		video_dir = self.dir_entrybox.get()
		self.VIDEO_DIR = os.path.abspath(video_dir)
		self.dir_set_confirmation_label["foreground"] = "green"

		if os.path.abspath(video_dir) == video_dir:
			self.dir_set_confirmation_label["text"] = "Default Video directory successfully saved."

		else:
			self.dir_set_confirmation_label["text"] = f"Default Video directory set as {os.path.abspath(video_dir)}."

		self.check_set_directory_button_text()
		self.dir_entrybox.delete(0, "end")

	def check_set_directory_button_text(self):

		if self.MANIM_DIR == None:
			self.manim_set_directory_button["text"] = "Set Default Manim directory"

		else:
			self.manim_set_directory_button["text"] = "Reset Default Manim directory"

		if self.VIDEO_DIR == None:
			self.video_set_directory_button["text"] = "Set Default Video directory"

		else:
			self.video_set_directory_button["text"] = "Reset Default Video directory"

	def do_after_setting_manim_dir(self):
		os.chdir(self.MANIM_DIR)
		self.main_frame.do_after_manim_directory_is_set()