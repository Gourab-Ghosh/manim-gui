import os, tkinter as tk
from tkinter import ttk
from functions_and_constants import get_manim_directory, DEFAULT_FONT
from main_frame import MainFrame
from edit_default_frame import EditDefaultFrame

class Root(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("Manim GUI")
		self.state("zoomed")
		self.configure(background = "blue")
		# self.minsize(width = 1000, height = 1000)
		# self.maxsize(width = 1000, height = 1000)
		# self.iconbitmap()

		self.fullscreen_state = False
		self.bind("<F11>", self.toggle_fullscreen)
		self.bind("<Escape>", self.exit_fullscreen)

	def toggle_fullscreen(self, event = None):
		self.fullscreen_state = not self.fullscreen_state
		self.attributes("-fullscreen", self.fullscreen_state)

	def exit_fullscreen(self, event = None):
		self.fullscreen_state = False
		self.attributes("-fullscreen", self.fullscreen_state)

root = Root()

padx = pady = 10

MANIM_DIR = get_manim_directory()

main_frame = MainFrame(
	root,
	text = "Manim Rendering GUI",
	add_kwargs = dict(
		padx = padx,
		pady = pady,
		fill = tk.BOTH,
		expand = 1,
		),
	)
edit_default_frame = EditDefaultFrame(
	root,
	main_frame,
	text = "Manim GUI default configurations",
	add_kwargs = dict(
		padx = padx,
		pady = pady,
		fill = tk.BOTH,
		expand = 1,
		),
	)

if MANIM_DIR == None:
	main_frame.MANIM_DIR_NOT_SET_MSG_LABEL["text"] = "Default Manim directoty path is either not set or the path do not exists. Edit the path to enable rendering options."
	main_frame.disable_required_items()
else:
	os.chdir(MANIM_DIR)
	main_frame.import_req_functions()

root.mainloop()








































# render_scenes(os.path.join(get_manim_directory(), "example_scenes.py"), ["WriteStuff", "SquareToCircle"], output_type = "last_frame")
# print(find_scenes(os.path.join(MANIM_DIR, "example_scenes.py")))