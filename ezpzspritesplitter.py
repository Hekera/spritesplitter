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

#class SplitterUtil():
#	
#	def __init__(self, image, tile_size, names_list=[]):
#		self.image = image
#		self.tile_width = tile_size[0]
#		self.tile_height = tile_size[1]
#		self.names_list = names_list

class VScrollable(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.canvas = Canvas(self, borderwidth=0, bg=self.bg_colors[1], scrollregion=(0,0,500,500))
		self.frame = Frame(self.canvas, bg=self.bg_colors[1])
		self.vbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
		self.canvas.config(yscrollcommand=vbar.set)
		
		self.vbar.pack(side=RIGHT, fill=Y)
		self.canvas.pack(fill=Y, expand=True)
		self.window = self.canvas.create_window((10,10), window=self.frame, anchor="nw", tags="self.frame")
		
		self.frame.bind("<Configure>", self.onFrameConfigure)
		
		#self.canvas.bind("<MouseWheel>", on_workspace_mousewheel)
		#self.pack(side=LEFT, expand=True, fill=BOTH)
		#self.frame.pack(side=LEFT, padx=5, pady=10)
		#self.frame.bind("<MouseWheel>", on_workspace_mousewheel)
	
	def onFrameConfigure(self, event):
			self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
	
class SpriteGUI(Frame):
	def __init__(self, parent, image, index, name_list=[], exclude=False):
		Frame.__init__(self, parent)
		
		self.image = image
		self.thumbnail = ImageTk.PhotoImage(self.image.resize(get_resize(), NEAREST))
		self.names = name_list
		self.default = f"{index[0]}-{index[1]}"
		self.exclude = exclude
		
		self.button = Button(self, image=self.thumbnail, command=lambda x=i-1,y=j-1: on_sprite_click(x,y), relief=FLAT, bg=self.bg_colors[1])
		self.label = Label(self, text=self.default, fg=self.fg_color, bg=self.bg_colors[1], wraplength=tile_display_size)
		
		button.pack()
		label.pack()
		
		#file_label.bind("<MouseWheel>", on_workspace_mousewheel)
		#button.bind("<MouseWheel>", on_workspace_mousewheel)
	
	def __dict__(self):
		return {"id": self.default, "names": self.names, "exclude": self.exclude}
	
class Workspace(VScrollable):
	def __init__(self, parent, image):
		VScrollable.__init__(self, parent, tile_size, names_list=[])
		
		self.image = image
		self.tile_width = tile_size[0]
		self.tile_height = tile_size[1]
		self.names_list = names_list
		
		self.hbar = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
		self.canvas.config(xscrollcommand=hbar.set)
		self.hbar.pack(side=BOTTOM, fill=X)
		
		self.canvas.itemconfigure(self.window, (100,10), anchor="n")
	
	def populate(self):
	
		def get_coords(x_index, y_index):
			return ((x_index-1)*self.tile_width, (y_index-1)*self.tile_height, x_index*self.tile_width, y_index*self.tile_height)
		
		grid = []
		for i in range(0, int(self.image.height/self.tile_height)+1):
			if i > 0:
				row = []
			for j in range(0, int(self.image.width/self.tile_width)+1):
				frame = Frame(workspace, bg=self.bg_colors[1], borderwidth=1, relief="solid")
				frame.grid(row=i, column=j, sticky="n")
				frame.bind("<MouseWheel>", on_workspace_mousewheel)
				if j > 0 and i > 0:
					sprite_gui = SpriteGUI(self, self.image.crop(box=get_coords(j, i)), (i,j))
					row.append(sprite_gui)
					
				elif j == 0 and i > 0:
					button = Button(frame, text="",command=lambda x=i-1: on_sprite_click_row(x), fg=self.fg_color, bg=self.bg_colors[0],width=2,height=(6*get_resize()[1])//self.tile_display_size)
					button.bind("<MouseWheel>", on_workspace_mousewheel)
					button.pack()
				elif i == 0 and j > 0:
					button = Button(frame, text="",command=lambda x=j-1: on_sprite_click_col(x), fg=self.fg_color, bg=self.bg_colors[0],width=(10*get_resize()[0])//self.tile_display_size,height=1)
					button.bind("<MouseWheel>", on_workspace_mousewheel)
					button.pack()
			if i > 0:
				tiles.append(tuple(row))
			
		self.sprites = tuple(tiles)

class SplitterGUI():
	
	selected_name_index = -1

	def __init__(self):
		self.landing()

	def landing(self):
		def error(message):
			Label(text=message).pack()
		
		#def load():
		#	with open("config.json") as json_file:
		#		data = json.load(json_file)
		#		
		
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
		Button(file_input, text="Browse...",command=open_file, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack()
		
		Label(dimension_label, text="Tile Width:", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		width_entry = Entry(dimension_input, width=5, fg=self.fg_color, bg=self.bg_colors[2], relief=FLAT)
		width_entry.pack(padx=5, pady=5)
		Label(dimension_label, text="Tile Height:", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		height_entry = Entry(dimension_input, width=5, fg=self.fg_color, bg=self.bg_colors[2], relief=FLAT)
		height_entry.pack(padx=5, pady=5)
		
		error = Label(submit, text="", fg=self.fg_color, bg=self.bg_colors[0])
		error.pack()
		Button(submit, text="Let's go!",command=verify, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack()
		
		self.window.mainloop()
	
	
	

	def editor(self):
		name_list = []
		name_buttons = []
		
		def on_workspace_mousewheel(event):
			wrapper_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
		
		def on_names_mousewheel(event):
			names_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
		
		def get_resize():
			multiplier = max(self.tile_display_size//self.tile_width, self.tile_display_size//self.tile_height)
			return (multiplier*self.tile_width, multiplier*self.tile_height)
		
		def toggle_exclude_mode():
			exclude_mode[0] = True
			exclude_mode[1]["bg"] = select_color
			delete_mode[0] = False
			delete_mode[1]["bg"] = self.bg_colors[1]
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
		
		def toggle_delete_mode():
			exclude_mode[0] = False
			exclude_mode[1]["bg"] = self.bg_colors[1]
			delete_mode[0] = True
			delete_mode[1]["bg"] = select_color
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
		
		def add_name(event=None):
			new_name = name_entry.get()
			if new_name != "" and not name_list.count(new_name):
				name_entry.delete(0, len(new_name))
				button = Button(names_panel, text=new_name, command=lambda x=new_name: change_selected_name(x), fg=self.fg_color, bg=self.bg_colors[0], width=25, wraplength=175, relief=FLAT)
				name_buttons.append(button)
				button.pack(padx=5, pady=3)
				name_list.append(new_name)
				names_panel.update()
				names_canvas.config(width=200, scrollregion=(0,0,names_panel.winfo_width() + 10,names_panel.winfo_height() + 10))
		
		def change_selected_name(name):
			exclude_mode[0] = False
			exclude_mode[1]["bg"] = self.bg_colors[1]
			delete_mode[0] = False
			delete_mode[1]["bg"] = self.bg_colors[1]
			if self.selected_name_index > -1:
				name_buttons[self.selected_name_index]["bg"] = self.bg_colors[0]
			self.selected_name_index = name_list.index(name)
			name_buttons[self.selected_name_index]["bg"] = select_color
	
		def on_sprite_click(row_index, col_index):
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
		
		def on_sprite_click_col(index):
			if exclude_mode[0]:
				exclude_all = True
				for i in range(len(self.sprites)):
					exclude_all = exclude_all and self.sprites[i][index].exclude
				for i in range(len(self.sprites)):
					self.sprites[i][index].exclude = not exclude_all
					update_file_label(self.sprites[i][index])
			else:
				for i in range(len(self.sprites)):
					on_sprite_click(i, index)
	
		def on_sprite_click_row(index):
			if exclude_mode[0]:
				exclude_all = True
				for sprite in self.sprites[index]:
					exclude_all = exclude_all and sprite.exclude
				for sprite in self.sprites[index]:
					sprite.exclude = not exclude_all
					update_file_label(sprite)
			else:
				for i in range(len(self.sprites[0])):
					on_sprite_click(index, i)
		
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
	
		def export():
			if hasattr(self, "folder"):
				for row in self.sprites:
					for sprite in row:
						if not sprite.exclude:
							sprite.image.save(path.join(self.folder,get_file_label(sprite) + ".png"))
							error["text"] = "Sprites successfully saved!"
			else:
				error["text"] = "No directory selected!"
		
		def save():
			if hasattr(self, "folder"):
				sprite_info = []
				for row in self.sprites:
					info_row = []
					for sprite in row:
						info_row.append(sprite.__dict__())
					sprite_info.append(info_row)
				with open(path.join(self.folder,get_file_label(sprite) + ".json"), "w") as json_file:
					json.dump({"tile_width": self.tile_width, "tile_height": self.tile_height, "image_width": self.image.width, "image_height": self.image.height, "available_names": name_list, "sprite_info": sprite_info}, json_file, indent=4)
				error["text"] = "Config successfully saved!"
			else:
				error["text"] = "No directory selected!"
		
		self.window.destroy()
		self.window = Tk()
		self.window.title("Editor")
		self.window["bg"] = self.bg_colors[0]
		
		panel = Frame(self.window, bg=self.bg_colors[0], width=300)
		panel.pack(side=LEFT, fill=Y)
		
		
		#Label(panel, text="Options", fg=self.fg_color, bg=self.bg_colors[0], font=("TkDefaultFont", 20) ).pack()
		delimiter_input = Frame(panel, bg=self.bg_colors[0])
		delimiter_input.pack(padx=5, pady=10)
		mode_input = Frame(panel, bg=self.bg_colors[0])
		mode_input.pack(padx=5, pady=5)
		Label(panel, text="Names", fg=self.fg_color, bg=self.bg_colors[0], font=("TkDefaultFont", 14)).pack(padx=5, pady=5)
		name_input = Frame(panel, bg=self.bg_colors[0])
		name_input.pack(padx=5)
		names_frame = Frame(panel, bg=self.bg_colors[0])
		names_frame.pack(expand=True, fill=Y, padx=10, pady=5)
		names_canvas = Canvas(names_frame, width=200, borderwidth=0, bg=self.bg_colors[1], scrollregion=(0,0,0,0))
		names_vbar = Scrollbar(names_frame, orient=VERTICAL)
		names_vbar.pack(side=RIGHT, fill=Y)
		names_vbar.config(command=names_canvas.yview)
		names_canvas.config(yscrollcommand=names_vbar.set)
		names_canvas.bind("<MouseWheel>", on_names_mousewheel)
		names_canvas.pack(expand=True, fill=Y)
		names_panel = Frame(names_canvas, bg=self.bg_colors[1])
		names_panel.pack(side=LEFT, padx=5, pady=10)
		names_canvas.create_window((100,5), window=names_panel, anchor="n",tags="names_panel")
		submit_input = Frame(panel, bg=self.bg_colors[0])
		submit_input.pack(side=BOTTOM, padx=5, pady=10)
		folder_input = Frame(panel, bg=self.bg_colors[0])
		folder_input.pack(side=BOTTOM, padx=5)
		
		Label(delimiter_input, text="Delimiter:", fg=self.fg_color, bg=self.bg_colors[0]).pack(side=LEFT)
		delimiter = StringVar(value="_")
		delimiter.trace_add("write", lambda name, index, mode: update_file_labels())
		delimiter_entry = Entry(delimiter_input, textvariable=delimiter, fg=self.fg_color, bg=self.bg_colors[2], width=4, relief=FLAT)
		delimiter_entry.pack(side=LEFT)
		
		exclude_toggle = Button(mode_input, text="Exclude Mode", command=toggle_exclude_mode, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT)
		exclude_toggle.pack(side=LEFT, padx=5)
		delete_toggle = Button(mode_input, text="Clear Mode", command=toggle_delete_mode, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT)
		delete_toggle.pack(side=LEFT, padx=5)
		exclude_mode = [False, exclude_toggle]
		delete_mode = [False, delete_toggle]
		
		name_entry = Entry(name_input, fg=self.fg_color, bg=self.bg_colors[2], relief=FLAT)
		name_entry.bind('<Return>', add_name)
		name_entry.pack(side=LEFT)
		Button(name_input, text="Add Name",command=add_name, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack(side=LEFT, padx=5)
		
		folder_name = Label(folder_input, text="No directory selected.", fg=self.fg_color, bg=self.bg_colors[0], wraplength=180)
		folder_name.pack()
		Button(folder_input, text="Browse...",command=open_folder, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack()
		
		error = Label(submit_input, text="", fg=self.fg_color, bg=self.bg_colors[0])
		error.pack()
		#Button(submit_input, text="Save Configuration",command=save, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack(pady=5)
		Button(submit_input, text="Export Sprites!",command=export, fg=self.fg_color, bg=self.bg_colors[1], relief=FLAT).pack(pady=5)
		
		
		
		workspace.update()
		wrapper_canvas.config(width=500,height=500, scrollregion=(0,0,workspace.winfo_width() + 10,workspace.winfo_height() + 10))
		
		self.window.mainloop()

gui = SplitterGUI()
