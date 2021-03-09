from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from PIL.Image import NEAREST as NEAREST
from os import path

class Sprite():
	
	def __init__(self, image, default, file_label, tk_image):
		self.names = []
		self.exclude = False
		self.image = image
		self.default = default
		self.label = file_label
		self.tk_image = tk_image

class SplitterUtil():
	
	def __init__(self):
		pass
	

class SplitterGUI():
	util = SplitterUtil()
	bg_colors = ("#202124", "#35363a", "#3c4043")
	fg_color = "white"
	sprite_width = 0
	sprite_height = 0
	selected_name_index = -1

	def __init__(self):
		self.landing()

	def landing(self):
		def error(message):
			Label(text=message).pack()
		
		def verify():
			if hasattr(self, "image"):
				try:
					input_width = int(width_entry.get())
					input_height = int(height_entry.get())
					if self.image.width % input_width == 0 and self.image.height % input_height == 0:
						self.tile_width = input_width
						self.tile_height = input_height
						self.editor()
					else:
						error["text"] = "Image size must be divisible by tile size!"
				except ValueError:
					error["text"] = "You must input integral values!"
			else:
				error["text"] = "You must choose an image file!"
		
		def open_file():
			try:
				self.image = Image.open(fd.askopenfilename(filetypes=[("Image File",'.png')]))
				file_name["text"] = self.image.filename[self.image.filename.rindex("/") + 1:]
				file_dim ["text"] = f"{self.image.width} x {self.image.height}"
			except AttributeError:
				pass
		
		self.window = Tk()
		self.window.title("Ez Pz Sprite Splitter")
		self.window["bg"] = self.bg_colors[0]
		
		Label(self.window, text="Welcome to the Ez Pz Sprite Splitter!", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		Label(self.window, text="Choose an image and input the dimensions of your tiles.", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		inputs = Frame(self.window, bg=self.bg_colors[0])
		inputs.pack()
		submit = Frame(self.window, padx=5, pady=10, bg=self.bg_colors[0])
		submit.pack()
		
		file_input = Frame(inputs, bg=self.bg_colors[0])
		file_input.grid(row=1, column=0, padx=25, pady=5)
		dimension_label = Frame(inputs, bg=self.bg_colors[0])
		dimension_label.grid(row=1, column=1, pady=5)
		dimension_input = Frame(inputs, bg=self.bg_colors[0])
		dimension_input.grid(row=1, column=2, pady=5)
		
		file_name = Label(file_input, text="No file selected.", fg=self.fg_color, bg=self.bg_colors[0])
		file_name.pack()
		file_dim = Label(file_input, text="", fg=self.fg_color, bg=self.bg_colors[0])
		file_dim.pack()
		Button(file_input, text="Browse...",command=open_file, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		
		Label(dimension_label, text="Tile Width:", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		width_entry = Entry(dimension_input, width=5, fg=self.fg_color, bg=self.bg_colors[2])
		width_entry.pack(padx=5, pady=5)
		Label(dimension_label, text="Tile Height:", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		height_entry = Entry(dimension_input, width=5, fg=self.fg_color, bg=self.bg_colors[2])
		height_entry.pack(padx=5, pady=5)
		
		error = Label(submit, text="", fg=self.fg_color, bg=self.bg_colors[0])
		error.pack()
		Button(submit, text="Let's go!",command=verify, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		
		self.window.mainloop()


	def editor(self):
		name_list = []
		name_buttons = []
		
		def on_mousewheel(event):
			wrapper_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
		
		def toggle_exclude_mode():
			exclude_mode[0] = True
			exclude_mode[1]["bg"] = "red"
			delete_mode[0] = False
			delete_mode[1]["bg"] = self.bg_colors[0]
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
		
		def toggle_delete_mode():
			exclude_mode[0] = False
			exclude_mode[1]["bg"] = self.bg_colors[0]
			delete_mode[0] = True
			delete_mode[1]["bg"] = "red"
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
		
		def add_name():
			new_name = name_entry.get()
			if not name_list.count(new_name):
				button = Button(panel, text=new_name, command=lambda x=new_name: change_selected_name(x), fg=self.fg_color, bg=self.bg_colors[0])
				name_buttons.append(button)
				button.pack(padx=5, pady=3)
				name_list.append(new_name)
		
		def change_selected_name(name):
			exclude_mode[0] = False
			exclude_mode[1]["bg"] = self.bg_colors[0]
			delete_mode[0] = False
			delete_mode[1]["bg"] = self.bg_colors[0]
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
			self.selected_name_index = name_list.index(name)
			name_buttons[self.selected_name_index]["bg"] = "red"
	
		def append_name(row_index, col_index):
			sprite = self.sprites[row_index][col_index]
			if exclude_mode[0]:
				sprite.exclude = not sprite.exclude
				update_file_label(sprite)
			elif delete_mode[0]:
				sprite.names = []
				update_file_label(sprite)
			elif self.selected_name_index > -1:
				sprite.names.append(name_list[self.selected_name_index])
				update_file_label(sprite)
		
		def append_name_col(index):
			for i in range(len(self.sprites)):
				append_name(i, index)
	
		def append_name_row(index):
			for i in range(len(self.sprites[0])):
				append_name(index, i)
		
		def get_file_label(sprite):
			if len(sprite.names) == 0:
				return sprite.default
			else: 
				new_label = ""
				for name in sprite.names:
					new_label += name + delimiter_entry.get()
				return new_label[:new_label.rindex(delimiter.get())]
		
		def update_file_label(sprite):
			if sprite.exclude:
				sprite.label["text"] = ""
			else:
				sprite.label["text"] = get_file_label(sprite)
		
		def update_file_labels():
			for row in self.sprites:
				for sprite in row:
					update_file_label(sprite)
		
		def open_folder():
			folder = fd.askdirectory(mustexist=True)
			if len(folder) > 0:
				self.folder = folder
				folder_name["text"] = folder
	
		def submit():
			print("submitting...")
			if hasattr(self, "folder"):
				print("has folder!")
				for row in self.sprites:
					for sprite in row:
						if not sprite.exclude:
							sprite.image.save(path.join(self.folder,get_file_label(sprite) + ".png"))
							error["text"] = "Sprites successfully saved!"
			else:
				error["text"] = "No directory selected!"
		
		self.window.destroy()
		self.window = Tk()
		self.window.title("Editor")
		self.window["bg"] = self.bg_colors[0]
		
		panel = Frame(self.window, bg=self.bg_colors[0], width=300)
		panel.pack(side=LEFT, fill=Y)
		wrapper_frame = Frame(self.window, bg=self.bg_colors[0])
		wrapper_frame.pack(side=LEFT, expand=True, fill=BOTH)
		wrapper_canvas = Canvas(wrapper_frame, borderwidth=0, bg=self.bg_colors[1], scrollregion=(0,0,500,500))
		hbar = Scrollbar(wrapper_frame, orient=HORIZONTAL)
		hbar.pack(side=BOTTOM, fill=X)
		hbar.config(command=wrapper_canvas.xview)
		vbar = Scrollbar(wrapper_frame, orient=VERTICAL)
		vbar.pack(side=RIGHT, fill=Y)
		vbar.config(command=wrapper_canvas.yview)
		wrapper_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		wrapper_canvas.bind_all("<MouseWheel>", on_mousewheel)
		wrapper_canvas.pack(side=LEFT, expand=True, fill=BOTH)
		workspace = Frame(wrapper_canvas, bg=self.bg_colors[1])
		workspace.pack(side=LEFT, padx=5, pady=10)
		wrapper_canvas.create_window((0,0), window=workspace, anchor="nw",tags="workspace")
		
		#Label(panel, text="Options", fg=self.fg_color, bg=self.bg_colors[0], font=("TkDefaultFont", 20) ).pack()
		delimiter_input = Frame(panel, bg=self.bg_colors[0])
		delimiter_input.pack(padx=5, pady=10)
		mode_input = Frame(panel, bg=self.bg_colors[0])
		mode_input.pack(padx=5, pady=5)
		Label(panel, text="Names", fg=self.fg_color, bg=self.bg_colors[0], font=("TkDefaultFont", 14)).pack(padx=5, pady=5)
		name_input = Frame(panel, bg=self.bg_colors[0])
		name_input.pack(padx=5)
		submit_input = Frame(panel, bg=self.bg_colors[0])
		submit_input.pack(side=BOTTOM, padx=5, pady=10)
		folder_input = Frame(panel, bg=self.bg_colors[0])
		folder_input.pack(side=BOTTOM, padx=5)
		
		Label(delimiter_input, text="Delimiter:", fg=self.fg_color, bg=self.bg_colors[0]).pack(side=LEFT)
		delimiter = StringVar(value="_")
		delimiter.trace_add("write", lambda name, index, mode: update_file_labels())
		delimiter_entry = Entry(delimiter_input, textvariable=delimiter, fg=self.fg_color, bg=self.bg_colors[2], width=4)
		delimiter_entry.pack(side=LEFT)
		
		exclude_toggle = Button(mode_input, text="Exclude Mode", command=toggle_exclude_mode, fg=self.fg_color, bg=self.bg_colors[0])
		exclude_toggle.pack(side=LEFT, padx=5)
		delete_toggle = Button(mode_input, text="Clear Mode", command=toggle_delete_mode, fg=self.fg_color, bg=self.bg_colors[0])
		delete_toggle.pack(side=LEFT, padx=5)
		exclude_mode = [False, exclude_toggle]
		delete_mode = [False, delete_toggle]
		
		name_entry = Entry(name_input, fg=self.fg_color, bg=self.bg_colors[2])
		name_entry.pack(side=LEFT)
		Button(name_input, text="Add Name",command=add_name, fg=self.fg_color, bg=self.bg_colors[0]).pack(side=LEFT, padx=5)
		
		folder_name = Label(folder_input, text="No directory selected.", fg=self.fg_color, bg=self.bg_colors[0], wraplength=180)
		folder_name.pack()
		Button(folder_input, text="Browse...",command=open_folder, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		
		error = Label(submit_input, text="", fg=self.fg_color, bg=self.bg_colors[0])
		error.pack()
		Button(submit_input, text="Save Sprites!",command=submit, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		
		tiles = []
		for i in range(0, int(self.image.height/self.tile_height)+1):
			if i > 0:
				row = []
			for j in range(0, int(self.image.width/self.tile_width)+1):
				frame = Frame(workspace, bg=self.bg_colors[1], borderwidth=1, relief="solid")
				frame.grid(row=i, column=j, sticky="n")
				if j > 0 and i > 0:
					coords = ((j-1)*self.tile_width, (i-1)*self.tile_height, j*self.tile_width, i*self.tile_height)
					image = self.image.crop(box=coords)
					file_label = Label(frame, text=f"{i}-{j}", fg=self.fg_color, bg=self.bg_colors[1], wraplength=80)
					new_sprite = Sprite(image, f"{i}-{j}", file_label, ImageTk.PhotoImage(image.resize((80, 80), NEAREST)))
					row.append(new_sprite)
					Button(frame, image=new_sprite.tk_image, command=lambda x=i-1,y=j-1: append_name(x,y), relief=FLAT,bg=self.bg_colors[1]).pack()
					file_label.pack()
				elif j == 0 and i > 0:
					Button(frame, text="",command=lambda x=i-1: append_name_row(x), fg=self.fg_color, bg=self.bg_colors[0],width=2,height=6).pack()
				elif i == 0 and j > 0:
					Button(frame, text="",command=lambda x=j-1: append_name_col(x), fg=self.fg_color, bg=self.bg_colors[0],width=10,height=1).pack()
			if i > 0:
				tiles.append(tuple(row))
			
		self.sprites = tuple(tiles)
		
		workspace.update()
		wrapper_canvas.config(width=300,height=300, scrollregion=(0,0,workspace.winfo_width(),workspace.winfo_height()))
		
		
		self.window.mainloop()

gui = SplitterGUI()
