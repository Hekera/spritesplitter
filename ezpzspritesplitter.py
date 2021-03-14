from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from PIL.Image import NEAREST as NEAREST
from os import path
import json

bg_colors = ("#202124", "#35363a", "#4f5459")
fg_color = "white"
select_color = "red"
tile_display_size = 80

def get_resize(width, height):
	multiplier = max(tile_display_size//width, tile_display_size//height)
	return (multiplier*width, multiplier*height)
	
class Confirm():
	def __init__(self, message, function):
		self.window = Tk()
		self.window.title("Warning")
		self.window["bg"] = bg_colors[0]
		self.function=function
		
		Label(self.window, text=message, wraplength=300, fg=fg_color, bg=bg_colors[0]).pack(pady=5)
		frm_buttons = Frame(self.window, bg=bg_colors[0])
		frm_buttons.pack(padx=5)
		Button(frm_buttons, text="Yes",command=lambda x=True: self.answer(x), fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(side=LEFT, padx=5, pady=5)
		Button(frm_buttons, text="No",command=lambda x=False: self.answer(x), fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(side=LEFT, padx=5, pady=5)
		
		self.window.mainloop()
	
	def answer(self, response):
		self.window.destroy()
		self.function(response)

class FileRequester(Frame):
	def __init__(self, parent, file_type, function=None):
		Frame.__init__(self, parent, bg=bg_colors[0])
		self.lbl_file = Label(self, text="No file selected.", fg=fg_color, bg=bg_colors[0])
		self.lbl_file.pack()
		self.lbl_size = Label(self, text="", fg=fg_color, bg=bg_colors[0])
		self.lbl_size.pack()
		self.file_type = file_type
		self.function = function
		Button(self, text="Browse...",command=self.open_file, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack()
	
	def open_file(self):
		try:
			self.file = fd.askopenfilename(filetypes=[self.file_type])
			self.lbl_file["text"] = self.file[self.file.rindex("/") + 1:]
			if self.function is not None:
				self.function()
		except AttributeError:
			pass
		except ValueError:
			pass

class ImageRequester(FileRequester):
	def __init__(self, parent):
		FileRequester.__init__(self, parent, ("PNG File",'.png'))
	
	def open_file(self):
		FileRequester.open_file(self)
		self.file = Image.open(self.file)
		self.lbl_size["text"] = f"{self.file.width} x {self.file.height}"

class SizeInput(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, bg=bg_colors[0])
		
		vcmd = (self.register(self.on_validate), '%P')
		Label(self, text="Tile Width:", fg=fg_color, bg=bg_colors[0]).grid(row=0, column=0, pady=5)
		Label(self, text="Tile Height:", fg=fg_color, bg=bg_colors[0]).grid(row=1, column=0, pady=5)
		self.ent_width = Entry(self, width=5, fg=fg_color, bg=bg_colors[2], relief=FLAT, validate="key", validatecommand=vcmd)
		self.ent_width.grid(row=0, column=1, padx=5, pady=5)
		self.ent_height = Entry(self, width=5, fg=fg_color, bg=bg_colors[2], relief=FLAT, validate="key", validatecommand=vcmd)
		self.ent_height.grid(row=1, column=1, padx=5, pady=5)
	
	def on_validate(self, P):
		return P == "" or P.isnumeric()

class VScrollable(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.canvas = Canvas(self, highlightthickness=0, bg=bg_colors[1], width=200, height=40, scrollregion=(0,0,500,500))
		self.frame = Frame(self.canvas, bg=bg_colors[1])
		self.frame.top = self
		self.vbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
		self.canvas.config(yscrollcommand=self.vbar.set)
		
		self.vbar.pack(side=RIGHT, fill=Y)
		self.canvas.pack(fill=Y, expand=True)
		self.window = self.canvas.create_window((100,10), window=self.frame, anchor="n", tags="self.frame")
		self.frame.bind("<Configure>", self.on_frame_configure)
		
		self.canvas.bind("<MouseWheel>", self.on_mousewheel)
		self.frame.bind("<MouseWheel>", self.on_mousewheel)
	
	def on_frame_configure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
	def on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
	
class BothScrollable(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.canvas = Canvas(self, highlightthickness=0, bg=bg_colors[1], width=200, height=40, scrollregion=(0,0,500,500))
		
		self.frame = Frame(self.canvas, bg=bg_colors[1])
		self.frame.top = self
		self.vbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
		self.hbar = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
		self.canvas.config(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set, height=500, width=500)
		
		self.vbar.pack(side=RIGHT, fill=Y)
		self.hbar.pack(side=BOTTOM, fill=X)
		self.canvas.pack(fill=BOTH, expand=True)
		self.window = self.canvas.create_window((10,10), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", self.on_frame_configure)
		
		self.canvas.bind("<MouseWheel>", self.on_mousewheel)
		self.frame.bind("<MouseWheel>", self.on_mousewheel)
	
	def on_frame_configure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
	def on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
	
class SpriteElement(Frame):
	def __init__(self, parent, image, index, name_list=None, exclude=False):
		Frame.__init__(self, parent, bg=bg_colors[1], borderwidth=1, relief="solid")
		self.sprite = image
		self.thumbnail = ImageTk.PhotoImage(self.sprite.resize(get_resize(image.width, image.height), NEAREST))
		if name_list is None:
			self.names = []
		else:
			self.names = name_list
		self.index = index
		self.exclude = exclude
		self.workspace = parent.top
		self.button = Button(self, image=self.thumbnail, command=lambda x=index[0],y=index[1]: self.workspace.on_sprite_click(x,y), relief=FLAT, bg=bg_colors[1], borderwidth=0)
		self.label = Label(self, text=self.get_default(), fg=fg_color, bg=bg_colors[1], wraplength=tile_display_size)
		
		self.button.pack()
		self.label.pack()
		
		self.bind("<MouseWheel>", self.workspace.on_mousewheel)
		self.label.bind("<MouseWheel>", self.workspace.on_mousewheel)
		self.button.bind("<MouseWheel>", self.workspace.on_mousewheel)
	
	def get_default(self):
		return f"{self.index[0]}-{self.index[1]}"
	
	def __dict__(self):
		return {"index": self.index, "exclude": self.exclude, "names": self.names}
	
	def update_label(self, event=None):
		if self.exclude:
			self.label["text"] = ""
		else:
			self.label["text"] = self.get_label()
	
	def get_label(self):
		if len(self.names) == 0:
			return self.get_default()
		else: 
			new_label = ""
			for name in self.names:
				new_label += name + self.workspace.delimiter.get()
			return new_label[:new_label.rindex(self.workspace.delimiter.get())]
	
class Workspace(BothScrollable):
	def __init__(self, parent, image, tile_size):
		BothScrollable.__init__(self, parent)
		
		self.image = image
		self.tile_width = tile_size[0]
		self.tile_height = tile_size[1]
		self.exclude_mode = False
		self.delete_mode = False
		self.parent = parent
		self.name_list = []
		self.selected_name_index = -1
		self.delimiter = StringVar(value="_")
		self.delimiter.trace_add("write", lambda name, index, mode: self.update_file_labels())
		
		self.populate()
	
	def populate(self):
	
		def get_coords(x_index, y_index):
			return ((x_index-1)*self.tile_width, (y_index-1)*self.tile_height, x_index*self.tile_width, y_index*self.tile_height)
		
		for i in range(0, int(self.image.height/self.tile_height)+1):
			for j in range(0, int(self.image.width/self.tile_width)+1):
				if j > 0 and i > 0:
					SpriteElement(self.frame, self.image.crop(box=get_coords(j, i)), (i,j)).grid(row=i, column=j, sticky="n")
				elif j == 0 and i > 0:
					button = Button(self.frame, text="",command=lambda x=i: self.on_click_row(x), fg=fg_color, bg=bg_colors[0],width=2,height=(6*get_resize(self.tile_width, self.tile_height)[1])//tile_display_size)
					button.bind("<MouseWheel>", self.on_mousewheel)
					button.grid(row=i, column=j, sticky="w")
				elif i == 0 and j > 0:
					button = Button(self.frame, text="",command=lambda x=j: self.on_click_col(x), fg=fg_color, bg=bg_colors[0],width=(10*get_resize(self.tile_width, self.tile_height)[0])//tile_display_size,height=1)
					button.bind("<MouseWheel>", self.on_mousewheel)
					button.grid(row=i, column=j, sticky="n")
		
	def get_sprite_elements(self, row=None, col=None):
		if col is None and row is None:
			return [x for x in self.frame.grid_slaves() if type(x) == SpriteElement]
		if col is not None and row is not None:
			return self.frame.grid_slaves(row=row, column=col)[0]
		if row is not None:
			return [x for x in self.frame.grid_slaves(row=row) if type(x) == SpriteElement]
		if col is not None:
			return [x for x in self.frame.grid_slaves(column=col) if type(x) == SpriteElement]
	
	def on_sprite_click(self, row_index, col_index):
		sprite = self.get_sprite_elements(row=row_index, col=col_index)
		if self.exclude_mode:
			sprite.exclude = not sprite.exclude
			sprite.update_label()
		elif self.delete_mode:
			sprite.names = []
			sprite.update_label()
		elif self.selected_name_index > -1:
			sprite.names.append(self.name_list[self.selected_name_index])
			sprite.update_label()
	
	def on_click_col(self, index):
		sprites = self.get_sprite_elements(col=index)
		if self.exclude_mode:
			exclude_all = True
			for sprite in sprites:
				exclude_all = exclude_all and sprite.exclude
			for sprite in sprites:
				sprite.exclude = not exclude_all
				sprite.update_label()
		else:
			for i in range(0, len(sprites)):
				self.on_sprite_click(i+1, index)

	def on_click_row(self, index):
		sprites = self.get_sprite_elements(row=index)
		if self.exclude_mode:
			exclude_all = True
			for sprite in sprites:
				exclude_all = exclude_all and sprite.exclude
			for sprite in sprites:
				sprite.exclude = not exclude_all
				sprite.update_label()
		else:
			for i in range(0, len(sprites)):
				self.on_sprite_click(index, i+1)
	
	def update_file_labels(self):
		sprites = self.get_sprite_elements()
		for sprite in sprites:
			sprite.update_label(self.delimiter.get())

class Panel(Frame):
	def __init__(self, parent, delimiter_string):
		Frame.__init__(self, parent, bg=bg_colors[0], width=300)
		self.editor = parent
		
		self.frm_delimiter = Frame(self, bg=bg_colors[0])
		self.frm_delimiter.pack(padx=5, pady=10)
		self.frm_mode = Frame(self, bg=bg_colors[0])
		self.frm_mode.pack(padx=5, pady=5)
		Label(self, text="Names", fg=fg_color, bg=bg_colors[0], font=("TkDefaultFont", 14)).pack(padx=5, pady=5)
		self.frm_name = Frame(self, bg=bg_colors[0])
		self.frm_name.pack(padx=5)
		self.name_list = VScrollable(self)
		self.name_list.pack(padx=10, pady=10, expand=True, fill=Y)
		self.frm_submit = Frame(self, bg=bg_colors[0])
		self.frm_submit.pack(side=BOTTOM, padx=5, pady=10)
		self.frm_folder = Frame(self, bg=bg_colors[0])
		self.frm_folder.pack(side=BOTTOM, padx=5)
		
		Label(self.frm_delimiter, text="Delimiter:", fg=fg_color, bg=bg_colors[0]).pack(side=LEFT)
		self.ent_delimiter = Entry(self.frm_delimiter, textvariable=delimiter_string, fg=fg_color, bg=bg_colors[2], width=4, relief=FLAT)
		self.ent_delimiter.pack(side=LEFT)
		
		self.btn_exclude_mode = Button(self.frm_mode, text="Exclude Mode", command=parent.set_exclude_mode, fg=fg_color, bg=bg_colors[1], relief=FLAT)
		self.btn_exclude_mode.pack(side=LEFT, padx=5)
		self.btn_delete_mode = Button(self.frm_mode, text="Clear Mode", command=parent.set_delete_mode, fg=fg_color, bg=bg_colors[1], relief=FLAT)
		self.btn_delete_mode.pack(side=LEFT, padx=5)
		
		self.ent_name = Entry(self.frm_name, fg=fg_color, bg=bg_colors[2], relief=FLAT)
		self.ent_name.bind('<Return>', parent.add_name)
		self.ent_name.pack(side=LEFT)
		Button(self.frm_name, text="Add Name",command=parent.add_name, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(side=LEFT, padx=5)
		
		self.lbl_folder = Label(self.frm_folder, text="No directory selected.", fg=fg_color, bg=bg_colors[0], wraplength=200)
		self.lbl_folder.pack()
		Button(self.frm_folder, text="Browse...",command=parent.open_folder, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack()
		
		self.lbl_submit = Label(self.frm_submit, text="", fg=fg_color, bg=bg_colors[0], wraplength=200)
		self.lbl_submit.pack()
		Button(self.frm_submit, text="Save Configuration",command=parent.save_config, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(pady=5)
		Button(self.frm_submit, text="Export Sprites",command=parent.export, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(pady=5)

class Editor(Frame):
	def __init__(self, parent, file, tile_size, data=None):
		Frame.__init__(self, parent)
		self.workspace = Workspace(self, file, tile_size)
		self.panel = Panel(self, self.workspace.delimiter)
		self.panel.pack(side=LEFT, fill=Y)
		self.workspace.pack(side=LEFT, fill=BOTH, expand=True)
		if data is not None:
			self.load_config(data)
	
	def set_delete_mode(self):
		self.reset_selection()
		self.workspace.delete_mode = True
		self.panel.btn_delete_mode["bg"] = select_color
	
	def set_exclude_mode(self):
		self.reset_selection()
		self.workspace.exclude_mode = True
		self.panel.btn_exclude_mode["bg"] = select_color
	
	def select_name(self, name):
		self.reset_selection()
		self.workspace.selected_name_index = self.workspace.name_list.index(name)
		self.panel.name_list.frame.pack_slaves()[self.workspace.selected_name_index]["bg"] = select_color
	
	def reset_selection(self):
		self.workspace.exclude_mode = False
		self.workspace.delete_mode = False
		for button in self.panel.name_list.frame.pack_slaves():
			button["bg"] = bg_colors[0]
		self.panel.btn_delete_mode["bg"] = bg_colors[1]
		self.panel.btn_exclude_mode["bg"] = bg_colors[1]
	
	def add_name(self, event=None):
		new_name = self.panel.ent_name.get()
		if new_name != "" and not self.workspace.name_list.count(new_name):
			self.panel.ent_name.delete(0, len(new_name))
			button = Button(self.panel.name_list.frame, text=new_name, command=lambda x=new_name: self.select_name(x), fg=fg_color, bg=bg_colors[0], width=25, wraplength=175, relief=FLAT)
			button
			button.bind("<MouseWheel>", self.panel.name_list.on_mousewheel)
			button.pack(padx=5, pady=3)
			self.workspace.name_list.append(new_name)
	
	def open_folder(self):
		folder = fd.askdirectory(mustexist=True)
		if len(folder) > 0:
			self.folder = folder
			self.panel.lbl_folder["text"] = folder
	
	def export(self):
		if hasattr(self, "folder"):
			for sprite_element in self.workspace.get_sprite_elements():
				if not sprite_element.exclude:
					sprite_element.sprite.save(path.join(self.folder, sprite_element.get_label() + ".png"))
					self.panel.lbl_submit["text"] = "Sprites successfully saved!"
		else:
			self.panel.lbl_submit["text"] = "No directory selected!"
	
	def save_config(self):
		if hasattr(self, "folder"):
			sprite_info = []
			for sprite_element in self.workspace.get_sprite_elements():
				sprite_info.append(sprite_element.__dict__())
			with open(path.join(self.folder,"config.json"), "w") as json_file:
				json.dump({"tile_size": (self.workspace.tile_width, self.workspace.tile_height), "image_size": (self.workspace.image.width, self.workspace.image.height), "available_names": self.workspace.name_list, "sprite_info": sprite_info}, json_file, indent=4)
			self.panel.lbl_submit["text"] = "Config successfully saved as config.json!"
		else:
			self.panel.lbl_submit["text"] = "No directory selected!"
	
	def load_config(self, data):
		for name in data["available_names"]:
			self.panel.ent_name.insert(0, name)
			self.add_name()
		list = self.workspace.get_sprite_elements()
		for info in data["sprite_info"]:
			for sprite_element in list:
				if sprite_element.index == tuple(info["index"]):
					sprite_element.names = info["names"]
					sprite_element.exclude = info["exclude"]
					list.remove(sprite_element)
					break
		self.workspace.update_file_labels()

class Splitter():

	def __init__(self):
		self.landing()
	
	def landing(self):
		self.window = Tk()
		self.window.title("Ez Pz Sprite Splitter")
		self.window["bg"] = bg_colors[0]
		
		Label(self.window, text="Welcome to the Ez Pz Sprite Splitter!", fg=fg_color, bg=bg_colors[0]).pack(pady=5)
		Label(self.window, text="Would you like to load a previous configuration or start from scratch?", fg=fg_color, bg=bg_colors[0]).pack(pady=5)
		Button(self.window, text="Start New",command=self.new, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(pady=5)
		Button(self.window, text="Load from File",command=self.load, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack(pady=5)
		
		self.window.mainloop()

	def new(self):		
		def verify():
			if not hasattr(image_input, "file"):
				error["text"] = "You must choose an image file!"
				return
			if size_input.ent_width.get() == "" or size_input.ent_height.get() == "":
				error["text"] = "You must input tile width and height values!"
				return
			self.image = image_input.file
			input_width = int(size_input.ent_width.get())
			input_height = int(size_input.ent_height.get())
			if self.image.width % input_width != 0 or self.image.height % input_height != 0:
				error["text"] = "Image size must be divisible by tile size!"
				return
			self.tile_size = (input_width, input_height)
			self.edit()
		
		self.window.destroy()
		self.window = Tk()
		self.window.title("Start New")
		self.window["bg"] = bg_colors[0]
		
		Label(self.window, text="Choose a png image and input the dimensions of your tiles.", fg=fg_color, bg=bg_colors[0]).pack(pady=5)
		inputs = Frame(self.window, bg=bg_colors[0])
		inputs.pack()
		submit = Frame(self.window, padx=5, pady=10, bg=bg_colors[0])
		submit.pack()
		
		image_input = ImageRequester(inputs)
		image_input.grid(row=0, column=0, padx=25, pady=5)
		size_input = SizeInput(inputs)
		size_input.grid(row=0, column=1, padx=25, pady=5)
		
		error = Label(submit, text="", fg=fg_color, bg=bg_colors[0])
		error.pack()
		Button(submit, text="Let's go!",command=verify, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack()
		
		self.window.mainloop()
	
	def load(self):
		def verify():
			if not hasattr(image_input, "file"):
				error["text"] = "You must choose an image file!"
				return
			if not hasattr(config_input, "file"):
				error["text"] = "You must choose a config file!"
				return
			if size_input.ent_width.get() == "" or size_input.ent_height.get() == "":
				error["text"] = "You must input tile width and height values!"
				return
			self.image = image_input.file
			input_width = int(size_input.ent_width.get())
			input_height = int(size_input.ent_height.get())
			with open(config_input.file) as json_file:
				self.data = json.load(json_file)
				if self.image.width % input_width != 0 and self.image.height % input_height != 0:
					error["text"] = "Image size must be divisible by tile size!"
					return
				message = ""
				if (self.data["image_size"][0] != self.image.width or self.data["image_size"][1] != self.image.height):
					message += "The size of the selected image and the size of the original image the config was saved from do not match. "
				if input_width != self.data["tile_size"][0] or input_height != self.data["tile_size"][1]:
					message += "The input tile size and the tile size of the original image the config was saved from do not match. "
				self.tile_size = (input_width, input_height)
				if message == "":
					answer(True)
				else:
					self.confirm = Confirm(message + "Proceed anyway?", answer)
		
		def answer(response):
			if response:
				self.edit()
		
		def on_file_load():
			if size_input.ent_width.get() != "" and size_input.ent_height.get() != "":
				return
			with open(config_input.file) as json_file:
				tile_size = tuple(json.load(json_file)["tile_size"])
				if size_input.ent_width.get() == "":
					size_input.ent_width.insert(0, tile_size[0])
				if size_input.ent_height.get() == "":
					size_input.ent_height.insert(0, tile_size[1])
		
		self.window.destroy()
		self.window = Tk()
		self.window.title("Load from Config")
		self.window["bg"] = bg_colors[0]
		
		Label(self.window, text="Choose a png image and a json configuration file.", fg=fg_color, bg=bg_colors[0]).pack(pady=5)
		inputs = Frame(self.window, bg=bg_colors[0])
		inputs.pack()
		submit = Frame(self.window, padx=5, pady=10, bg=bg_colors[0])
		submit.pack()
		
		Label(inputs, text="Image", fg=fg_color, bg=bg_colors[0]).grid(row=0, column=0, padx=10, pady=5)
		image_input = ImageRequester(inputs)
		image_input.grid(row=1, column=0, padx=25, pady=5)
		Label(inputs, text="Config", fg=fg_color, bg=bg_colors[0]).grid(row=0, column=1, padx=25, pady=5)
		config_input = FileRequester(inputs, ("JSON File",'.json'), function=on_file_load)
		config_input.grid(row=1, column=1, padx=25, pady=5)
		size_input = SizeInput(inputs)
		size_input.grid(row=1, column=2, padx=10, pady=5)
		
		error = Label(submit, text="", fg=fg_color, bg=bg_colors[0])
		error.pack()
		Button(submit, text="Let's go!",command=verify, fg=fg_color, bg=bg_colors[1], relief=FLAT).pack()
		
		self.window.mainloop()

	def edit(self):
		self.window.destroy()
		self.window = Tk()
		self.window.title("Editor")
		self.window.config(bg=bg_colors[0])
		
		if hasattr(self, "data"):
			self.editor = Editor(self.window, self.image, self.tile_size, self.data)
		else:
			self.editor = Editor(self.window, self.image, self.tile_size)
		self.editor.pack(side=LEFT, fill=BOTH, expand=True)
		
		self.window.mainloop()

splitter = Splitter()
