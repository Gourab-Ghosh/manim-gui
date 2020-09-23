import os, tkinter as tk
from copy import deepcopy
from tkinter import ttk, filedialog, colorchooser
from edit_default_frame import Frame
from functions_and_constants import get_manim_directory, DEFAULT_FONT

class ModifiedFrame(Frame):
	list_of_objects_to_be_disabled = []
	def add_by_default(self, *args, disable_when_required = False, **kwargs):
		obj = super().add_by_default(*args, **kwargs)
		if disable_when_required:
			self.list_of_objects_to_be_disabled.append(obj)

class MainFrame(ModifiedFrame):
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.MANIM_DIR_NOT_SET_MSG_LABEL = ttk.Label(self.frame, text = "", font = DEFAULT_FONT, foreground = "red")
		self.MANIM_DIR_NOT_SET_MSG_LABEL.grid(row = 0, columnspan = 3)
		self.NO_SCENE_FOUND_MESSAGE = "No Scene Found"
		self.FILE_NOT_FOUND_MESSAGE = "Invalid file"
		self.NO_SCENE_SELECTED_MESSAGE = "No Scene selected"
		self.initial_state_of_disabled_items_already_defined = False
		self.create_frame1(5, 5, frame_add_kwargs = dict(row = 1, rowspan = 3, column = 0, padx = 5, pady = 5, sticky = tk.N), button_kwargs = dict(fg = "blue", bg = "orange", width = 15, height = 2), spinbox_kwargs = dict(width = 46, foreground = "green", command = self.update_spin_boxes_range_of_selection))
		self.frame1.scenes_listbox.bind("<<ListboxSelect>>", self.update_selected_scenes_in_Listbox_label)
		self.create_frame2(5, 5, frame_add_kwargs = dict(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5, sticky = tk.N))
		self.add_by_default("status_label", "Label", obj_kwargs = dict(text = "Rendering Status :", font = DEFAULT_FONT, foreground = "#870C78"), add_kwargs = dict(row = 2, column = 1, padx = 5, pady = 5, sticky = tk.W))
		self.add_by_default("rendering_status_label", "Label", obj_kwargs = dict(text = "Not Rendering", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 2, column = 2, padx = 5, pady = 5, sticky = tk.W))
		self.add_by_default("time_taken_label", "Label", obj_kwargs = dict(text = "Time Taken :", font = DEFAULT_FONT, foreground = "#870C78"), add_kwargs = dict(row = 3, column = 1, padx = 5, pady = 5, sticky = tk.W))
		self.add_by_default("time_label", "Label", obj_kwargs = dict(text = "", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 3, column = 2, padx = 5, pady = 5, sticky = tk.W))
		self.add_by_default("render_video_button", "tk.Button", disable_when_required = True, obj_kwargs = dict(text = "Render Video", fg = "white", bg = "blue", width = 15, height = 2, command = self.render_video_function, state = "disabled"), add_kwargs = dict(row = 4, columnspan = 3, padx = 5, pady = 5))
		self.add_by_default("render_warning_label", "Label", obj_kwargs = dict(text = "", foreground = "blue"), add_kwargs = dict(row = 5, columnspan = 3, padx = 5, pady = 5))
		self.render_video_button.bind("<Button-1>", self.rendering_status_update)

	def create_frame1(self, padx, pady, frame_add_kwargs, button_kwargs, spinbox_kwargs):
		self.frame1 = ModifiedFrame(self.frame, text = "Select the file you want to render", add_method = "grid", add_kwargs = frame_add_kwargs)
		self.frame1.add_by_default("manim_dir_set_label", "Label", obj_kwargs = dict(text = "Enter the path of the file you want to render.", font = DEFAULT_FONT), add_kwargs = dict(row = 0, columnspan = 4, padx = padx, pady = pady))
		self.frame1.add_by_default("choose_file_label", "Label", obj_kwargs = dict(text = "Choose File :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 1, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("file_dir_entrybox", "Entry", disable_when_required = True, obj_kwargs = dict(foreground = "green", width = 100), add_kwargs = dict(row = 1, column = 1, columnspan = 2, padx = padx, pady = pady, sticky = tk.E))
		self.frame1.add_by_default("browse_button", "Button", disable_when_required = True, obj_kwargs = dict(text = "Browse File", command = self.browse_button_function), add_kwargs = dict(row = 1, column = 3, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("scenes_found_label", "Label", obj_kwargs = dict(text = "Scenes found :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 2, rowspan = 3, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("scenes_listbox", "Listbox", disable_when_required = True, obj_kwargs = dict(width = 97, height = 10, bg = "blue", fg = "white", selectmode = tk.MULTIPLE, activestyle = "none"), add_kwargs = dict(row = 2, rowspan = 3, column = 1, columnspan = 2, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("refresh_scenes_button", "tk.Button", disable_when_required = True, obj_kwargs = dict(text = "Refresh Scenes", **button_kwargs, command = self.refresh_scenes_function), add_kwargs = dict(row = 2, column = 3, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("select_all_scenes_button", "tk.Button", disable_when_required = True, obj_kwargs = dict(text = "Select All", **button_kwargs, command = self.select_all_scenes_button_function), add_kwargs = dict(row = 3, column = 3, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("clear_selected_scenes_button", "tk.Button", disable_when_required = True, obj_kwargs = dict(text = "Clear Selection", **button_kwargs, command = self.clear_selected_scenes_button_function), add_kwargs = dict(row = 4, column = 3, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("select_label", "Label", obj_kwargs = dict(text = "Selection range :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 5, rowspan = 2, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("starting_index_label", "Label", obj_kwargs = dict(text = "Starting index", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 5, column = 1, padx = padx, pady = pady))
		self.frame1.add_by_default("ending_index_label", "Label", obj_kwargs = dict(text = "Ending index", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 5, column = 2, padx = padx, pady = pady))
		self.frame1.add_by_default("start_number_spinbox", "Spinbox", disable_when_required = True, obj_kwargs = dict(from_ = 0, to = 0, state = "readonly", **spinbox_kwargs), add_kwargs = dict(row = 6, column = 1, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("end_number_spinbox", "Spinbox", disable_when_required = True, obj_kwargs = dict(from_ = 0, to = 0, state = "readonly", **spinbox_kwargs), add_kwargs = dict(row = 6, column = 2, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("select_scenes_button", "tk.Button", disable_when_required = True, obj_kwargs = dict(text = "Select Scenes", **button_kwargs, command = self.select_scenes_button_function, state = "disabled"), add_kwargs = dict(row = 5, rowspan = 2, column = 3, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("scene_name_label", "Label", obj_kwargs = dict(text = "Scene name :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 7, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("start_scenes_label", "Label", obj_kwargs = dict(text = "", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 7, column = 1, padx = padx, pady = pady))
		self.frame1.add_by_default("end_scenes_label", "Label", obj_kwargs = dict(text = "", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 7, column = 2, padx = padx, pady = pady))
		self.frame1.add_by_default("selected_scenes_label", "Label", obj_kwargs = dict(text = "Selected scenes :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 8, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame1.add_by_default("selected_scenes_in_Listbox_label", "Label", obj_kwargs = dict(text = self.NO_SCENE_SELECTED_MESSAGE, font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 8, column = 1, columnspan = 2, padx = padx, pady = pady))

	def create_frame2(self, padx, pady, frame_add_kwargs):
		self.frame2 = ModifiedFrame(self.frame, text = "Rendering options", add_method = "grid", add_kwargs = frame_add_kwargs)
		self.create_output_type_frame(padx, pady, frame_add_kwargs = dict(row = 0, column = 0, padx = padx, pady = pady, sticky = tk.N))
		self.create_output_quality_frame(padx, pady, frame_add_kwargs = dict(row = 0, column = 1, columnspan = 2, padx = padx, pady = pady, sticky = tk.N), entry_width = 15)
		self.frame2.add_by_default("play_video_checkbox", "Checkbutton", disable_when_required = True, obj_kwargs = dict(text = "Play Video"), add_kwargs = dict(row = 1, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("leave_progress_bars_checkbox", "Checkbutton", disable_when_required = True, obj_kwargs = dict(text = "Leave Progress Bars"), add_kwargs = dict(row = 1, column = 1, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("transparent_checkbox", "Checkbutton", disable_when_required = True, obj_kwargs = dict(text = "Transpatent", command = self.transpatent_function), add_kwargs = dict(row = 1, column = 2, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("background_label", "Label", obj_kwargs = dict(text = "Background :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 2, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("background_colour_entrybox", "Entry", disable_when_required = True, obj_kwargs = dict(foreground = "green", width = 40), add_kwargs = dict(row = 2, column = 1, columnspan = 2, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("background_colour_button", "Button", disable_when_required = True, obj_kwargs = dict(text = "Choose Colour", command = self.choose_colour_function), add_kwargs = dict(row = 3, column = 1, padx = padx, pady = pady))
		self.frame2.add_by_default("clear_background_colour_entrybox_button", "Button", disable_when_required = True, obj_kwargs = dict(text = "Clear Colour", command = lambda : self.frame2.background_colour_entrybox.delete(0, tk.END)), add_kwargs = dict(row = 3, column = 2, padx = padx, pady = pady))
		self.frame2.add_by_default("output_name_label", "Label", obj_kwargs = dict(text = "Output Name :", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 4, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.add_by_default("output_name_entrybox", "Entry", disable_when_required = True, obj_kwargs = dict(foreground = "green", width = 40), add_kwargs = dict(row = 4, column = 1, columnspan = 2, padx = padx, pady = pady, sticky = tk.W))
		self.checkbox_list = (self.frame2.play_video_checkbox, self.frame2.leave_progress_bars_checkbox, self.frame2.transparent_checkbox)
		self.command_list = (["!alternate", "selected"], ["!alternate", "selected"], ["!alternate"])
		for checkbox, command in zip(self.checkbox_list, self.command_list):
			checkbox.state(command)
		self.frame2.background_colour_entrybox.insert(0, "#000000")

	def create_output_type_frame(self, padx, pady, frame_add_kwargs):
		output_type_list = ["mp4", "gif", "Last Frame", "Save Frames"]
		self.frame2.output_type_frame = ModifiedFrame(self.frame2.frame, text = "Output type", add_method = "grid", add_kwargs = frame_add_kwargs)
		self.frame2.output_type_frame.radiobutton_variable = tk.StringVar()
		for i, quality in enumerate(output_type_list):
			self.frame2.output_type_frame.add_by_default(quality.replace(" ", "_").lower() + "_radiobutton", "Radiobutton", disable_when_required = True, obj_kwargs = dict(text = quality, variable = self.frame2.output_type_frame.radiobutton_variable, value = quality.lower().replace(" ", "_")), add_kwargs = dict(row = i, column = 0, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.output_type_frame.radiobutton_variable.set("mp4")

	def create_output_quality_frame(self, padx, pady, frame_add_kwargs, entry_width):
		output_quality_list = ["low quality", "medium quality", "high quality", "production quality", "default quality"]

		def edit_when_default_quality_in_video_quality():
			selected_button = self.frame2.output_quality_frame.radiobutton_variable.get()
			for item in (self.frame2.output_quality_frame.height_entrybox, self.frame2.output_quality_frame.width_entrybox):
				if selected_button == output_quality_list[-1]:
					item["state"] = "normal"
					item.insert(0, ["480" if item is self.frame2.output_quality_frame.height_entrybox else "854"][0])
				else:
					item.delete(0, tk.END)
					item["state"] = "disabled"

		def set_default_width_from_height(event):
			height = self.frame2.output_quality_frame.height_entrybox.get().strip()
			self.frame2.output_quality_frame.height_entrybox.delete(0, tk.END)
			if not all(i.isnumeric() for i in height):
				height = list(height)
				for string in deepcopy(height):
					if not string.isnumeric() and string != ".":
						height.pop(height.index(string))
				height = "".join(height)
			if height != "":
				height = int(round(float(height)))
				height += height % 2
				self.frame2.output_quality_frame.height_entrybox.insert(0, str(height))
				width = int(round(height * 16 / 9))
				width += width % 2
				self.frame2.output_quality_frame.width_entrybox.delete(0, tk.END)
				self.frame2.output_quality_frame.width_entrybox.insert(0, width)

		self.frame2.output_quality_frame = ModifiedFrame(self.frame2.frame, text = "Output quality", add_method = "grid", add_kwargs = frame_add_kwargs)
		self.frame2.output_quality_frame.radiobutton_variable = tk.StringVar()
		for i, quality in enumerate(output_quality_list):
			self.frame2.output_quality_frame.add_by_default(quality.replace(" ", "_") + "_radiobutton", "Radiobutton", disable_when_required = True, obj_kwargs = dict(text = quality.title(), variable = self.frame2.output_quality_frame.radiobutton_variable, value = quality.lower(), command = edit_when_default_quality_in_video_quality), add_kwargs = dict(row = i % 4, column = i // 4, padx = padx, pady = pady, sticky = tk.W))
		self.frame2.output_quality_frame.radiobutton_variable.set("medium quality")
		self.frame2.output_quality_frame.add_by_default("height_label", "Label", obj_kwargs = dict(text = "Height", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 1, column = 1, padx = padx, pady = pady))
		self.frame2.output_quality_frame.add_by_default("height_entrybox", "Entry", disable_when_required = True, obj_kwargs = dict(foreground = "green", width = entry_width, state = "disabled"), add_kwargs = dict(row = 2, column = 1, padx = padx, pady = pady))
		self.frame2.output_quality_frame.add_by_default("width_label", "Label", obj_kwargs = dict(text = "Width", font = DEFAULT_FONT, foreground = "green"), add_kwargs = dict(row = 3, column = 1, padx = padx, pady = pady))
		self.frame2.output_quality_frame.add_by_default("width_entrybox", "Entry", disable_when_required = True, obj_kwargs = dict(foreground = "green", width = entry_width, state = "disabled"), add_kwargs = dict(row = 4, column = 1, padx = padx, pady = pady))
		for event in ("<FocusOut>", "<Leave>"):
			self.frame2.output_quality_frame.height_entrybox.bind(event, set_default_width_from_height)
			self.frame2.output_quality_frame.width_entrybox.bind(event, self.update_width_and_height_entrybox)

	def disable_required_items(self):
		self.initial_state_of_disabled_items = []
		self.initial_state_of_disabled_items_already_defined = True
		for item in self.frame1.list_of_objects_to_be_disabled:
			self.initial_state_of_disabled_items.append(item["state"])
			item["state"] = "disabled"

	def enable_disabled_items(self):
		if self.initial_state_of_disabled_items_already_defined:
			for item_state, item in zip(self.initial_state_of_disabled_items, self.frame1.list_of_objects_to_be_disabled):
				item["state"] = item_state

	def do_after_manim_directory_is_set(self):
		self.import_req_functions()
		self.MANIM_DIR_NOT_SET_MSG_LABEL["text"] = ""
		self.enable_disabled_items()
		for checkbox, command in zip(self.checkbox_list, self.command_list):
			checkbox.state(command)

	def import_req_functions(self):
		global find_scenes
		global render_scenes
		try:
			find_scenes
			render_scenes
		except NameError:
			from manim_functions import find_scenes, render_scenes

	def browse_button_function(self):
		initialdir = None
		initialdir_preference = (self.LAST_RENDERED_FILE_DIR, self.MANIM_DIR, os.path.expanduser("~"))
		for path in initialdir_preference:
			if initialdir == None:
				initialdir = path
			else:
				break
		req_file = filedialog.askopenfilename(initialdir = initialdir, title = "Select the file you want to render.", filetypes = (("Python Files", ("*.py", "*.pyc")), ("All Files", "*.*")))
		if req_file != "":
			req_file = os.path.abspath(req_file)
		self.frame1.file_dir_entrybox.delete(0, "end")
		self.frame1.file_dir_entrybox.insert(0, req_file)
		self.current_file = req_file
		self.refresh_scenes_function()

	def refresh_scenes_function(self):
		self.frame1.scenes_listbox["state"] = "normal"
		self.frame1.scenes_listbox.delete(0, tk.END)
		file_path = self.frame1.file_dir_entrybox.get()
		if os.path.isfile(file_path) and file_path[-3:] == ".py":
			list_of_scenes = find_scenes(file_path)
			for scene in list_of_scenes:
				self.frame1.scenes_listbox.insert(tk.END, scene)
			if list_of_scenes == []:
				self.frame1.scenes_listbox.insert(tk.END, self.NO_SCENE_FOUND_MESSAGE)
				self.frame1.scenes_listbox["state"] = "disabled"
		else:
			self.frame1.scenes_listbox.insert(tk.END, self.FILE_NOT_FOUND_MESSAGE)
			self.frame1.scenes_listbox["state"] = "disabled"
		self.update_selected_scenes_in_Listbox_label()
		self.update_spinbox_after_refresh()

	def get_selected_item_in_listbox(self):
		return [self.frame1.scenes_listbox.get(i) for i in self.frame1.scenes_listbox.curselection()]

	def update_selected_scenes_in_Listbox_label(self, event = None):
		max_len_tolerance = 70
		if event == None:
			selected_scenes = self.get_selected_item_in_listbox()
		else:
			selected_scenes = [event.widget.get(i) for i in event.widget.curselection()]
		if len(selected_scenes) > 1:
			self.frame2.output_name_entrybox.delete(0, tk.END)
			self.frame2.output_name_entrybox["state"] = "disabled"
			self.frame2.play_video_checkbox.state(["!selected"])
		else:
			self.frame2.output_name_entrybox["state"] = "normal"
			self.frame2.play_video_checkbox.state(["selected"])
		if selected_scenes == []:
			self.frame1.selected_scenes_in_Listbox_label["text"] = self.NO_SCENE_SELECTED_MESSAGE
			self.render_video_button["state"] = "disabled"
		else:
			text = "Selected Scenes : " + ", ".join(selected_scenes)
			if len(text) <= max_len_tolerance:
				self.frame1.selected_scenes_in_Listbox_label["text"] = text
			else:
				self.frame1.selected_scenes_in_Listbox_label["text"] = text[: max_len_tolerance - 4] + " ..."
			self.render_video_button["state"] = "normal"
			self.render_warning_label["text"] = ""

	def update_spinbox_after_refresh(self):
		self.frame1.start_number_spinbox.set("")
		self.frame1.end_number_spinbox.set("")
		self.frame1.select_scenes_button["state"] = "disabled"
		if self.frame1.scenes_listbox["state"] == "disabled":
			number_of_items_in_list_boxes = 0
		else:
			number_of_items_in_list_boxes = self.frame1.scenes_listbox.size()
		self.frame1.start_number_spinbox['from_'] = min(1, number_of_items_in_list_boxes)
		self.frame1.start_number_spinbox["to"] = number_of_items_in_list_boxes
		self.frame1.end_number_spinbox['from_'] = min(1, number_of_items_in_list_boxes)
		self.frame1.end_number_spinbox["to"] = number_of_items_in_list_boxes
		self.update_spin_boxes_range_of_selection()

	def select_all_scenes_button_function(self):
		self.frame1.scenes_listbox.select_set(0, tk.END)
		self.update_selected_scenes_in_Listbox_label()

	def clear_selected_scenes_button_function(self):
		self.frame1.scenes_listbox.selection_clear(0, tk.END)
		self.update_selected_scenes_in_Listbox_label()

	def select_scenes_button_function(self):
		start = int(self.frame1.start_number_spinbox.get()) - 1
		end = int(self.frame1.end_number_spinbox.get()) - 1
		self.frame1.scenes_listbox.selection_clear(0, tk.END)
		self.frame1.scenes_listbox.select_set(start, end)
		self.update_selected_scenes_in_Listbox_label()

	def update_spin_boxes_range_of_selection(self):
		start = self.frame1.start_number_spinbox.get()
		end = self.frame1.end_number_spinbox.get()
		if start != "" and end == "":
			self.frame1.end_number_spinbox["from_"] = int(start)
		if start == "" and end != "":
			self.frame1.start_number_spinbox["to"] = int(end)
		if not (start == "" or end == ""):
			self.frame1.select_scenes_button["state"] = "normal"
			self.frame1.start_number_spinbox["to"] = int(end)
			self.frame1.end_number_spinbox["from_"] = int(start)
		self.edit_start_scene_and_end_scene_label()

	def edit_start_scene_and_end_scene_label(self):
		max_len_tolerance = 33
		start = self.frame1.start_number_spinbox.get()
		end = self.frame1.end_number_spinbox.get()
		def adjust_text(given_text):
			if len(given_text) <= max_len_tolerance:
				modidied_text = given_text
			else:
				modidied_text = given_text[: max_len_tolerance - 4] + " ..."
			return modidied_text
		if start == "":
			self.frame1.start_scenes_label["text"] = ""
		else:
			text = self.frame1.scenes_listbox.get(int(start) - 1)
			self.frame1.start_scenes_label["text"] = adjust_text(text)
		if end == "":
			self.frame1.end_scenes_label["text"] = ""
		else:
			text = self.frame1.scenes_listbox.get(int(end) - 1)
			self.frame1.end_scenes_label["text"] = adjust_text(text)

	def update_width_and_height_entrybox(self, event = None):
		for entrybox in (self.frame2.output_quality_frame.height_entrybox, self.frame2.output_quality_frame.width_entrybox):
			new_value = ""
			for char in deepcopy(entrybox.get()):
				if char.isnumeric():
					new_value += char
			entrybox.delete(0, tk.END)
			entrybox.insert(0, new_value)

	def transpatent_function(self):
		list_of_items = (self.frame2.background_colour_entrybox, self.frame2.background_colour_button, self.frame2.clear_background_colour_entrybox_button)
		if self.frame2.transparent_checkbox.instate(["selected"]):
			list_of_items[0].delete(0, tk.END)
			for item in list_of_items:
				item["state"] = "disabled"
		else:
			for item in list_of_items:
				item["state"] = "normal"
			list_of_items[0].insert(0, "#000000")

	def choose_colour_function(self):
		chosen_colour_hex = colorchooser.askcolor()[1]
		if chosen_colour_hex != None:
			chosen_colour_hex = chosen_colour_hex.upper()
			self.frame2.background_colour_entrybox.delete(0, tk.END)
			self.frame2.background_colour_entrybox.insert(0, chosen_colour_hex)

	def rendering_status_update(self, event = None):
		if self.render_video_button["state"] == "normal":
			self.rendering_status_label["foreground"] = "green"
			self.rendering_status_label["text"] = "Rendering"
			self.time_label["text"] = ""
		else:
			self.render_warning_label["text"] = "Select a scene to enable the Render Button."

	def render_video_function(self):
		self.update_width_and_height_entrybox()

		render_args = []
		render_kwargs = {}

		selected_scenes = self.get_selected_item_in_listbox()

		if self.frame2.play_video_checkbox.instate(["selected"]):
			render_args.append("play")
		if self.frame2.leave_progress_bars_checkbox.instate(["selected"]):
			render_args.append("progress_bars")
		if self.frame2.transparent_checkbox.instate(["selected"]):
			render_args.append("transparent")

		output_quality = self.frame2.output_quality_frame.radiobutton_variable.get()
		if output_quality == "default quality":
			output_quality = [["" if item.get() == "" and all(i.isnumeric() for i in item.get()) else int(round(float(item.get())))][0] for item in (self.frame2.output_quality_frame.height_entrybox, self.frame2.output_quality_frame.width_entrybox)]
			for item in deepcopy(output_quality):
				if item == "":
					output_quality.pop(item.index(item))

		render_kwargs.update(dict(
			output_type = self.frame2.output_type_frame.radiobutton_variable.get(),
			output_quality = output_quality,
			output_name = self.frame2.output_name_entrybox.get(),
			))
		if not self.frame2.transparent_checkbox.instate(["selected"]):
			render_kwargs.update(dict(bg_colour = self.frame2.background_colour_entrybox.get()))

		error, render_time = render_scenes(self.current_file, selected_scenes, *render_args, **render_kwargs)

		if error.returncode != 0:
			self.rendering_status_label["foreground"] = "red"
			self.rendering_status_label["text"] = "Incomplere Rendering"
		else:
			self.LAST_RENDERED_FILE = self.current_file
			self.rendering_status_label["foreground"] = "green"
			self.rendering_status_label["text"] = "Finished Rendering"
		self.time_label["text"] = render_time



# dir(locals()["__builtins__"]) -> Errors

# To edit -> colour handling, height width live update



# Jadavpur login id -> 25084001111162
# Jadavpur application no. mathematics -> JUBSC082503006752
# Jadavpur application no. physics -> JUBSC082501006774
# Vidyamandira application number -> 2020MTMA07804
# ["transparent + bg_colour"]
# ["file_name + browse", "scenes", "start_number + end_number", "output_type + transparent + bg_colour", "output_quality", "play + progress_bars", "output_name", "output_path"]