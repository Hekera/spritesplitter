from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk

class Sprite():
	names = []
	exclude = False
	default = ""
	
	def __init__(self, image, default):
		self.image = image
		self.default = default

class SplitterUtil():
	
	def __init__(self):
		pass
	

class SplitterGUI():
	util = SplitterUtil()
	bg_colors = ("#202124", "#35363a", "#3c4043")
	fg_color = "white"
	sprite_width = 0;
	sprite_height = 0;

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
			self.image = Image.open(fd.askopenfilename(filetypes=[("Image File",'.png')]))
			file_name["text"] = self.image.filename[self.image.filename.rindex("/") + 1:]
			file_dim ["text"] = f"{self.image.width} x {self.image.height}"
		
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
		width_entry = Entry(dimension_input, width=5, bg=self.bg_colors[2])
		width_entry.pack(padx=5, pady=5)
		Label(dimension_label, text="Tile Height:", fg=self.fg_color, bg=self.bg_colors[0]).pack(pady=5)
		height_entry = Entry(dimension_input, width=5, bg=self.bg_colors[2])
		height_entry.pack(padx=5, pady=5)
		
		error = Label(submit, text="", fg=self.fg_color, bg=self.bg_colors[0])
		error.pack()
		Button(submit, text="Let's go!",command=verify, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		Button(submit, text="Skip",command=self.editor, fg=self.fg_color, bg=self.bg_colors[0]).pack()
		
		self.window.mainloop()


	def editor(self):
		names = []
		
		def add_name():
			names.append(name_input.get())
		
		def test():
			print("success!")
		
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
		wrapper_canvas.pack(side=LEFT, expand=True, fill=BOTH)
		wrapper_canvas.config(width=300,height=300, scrollregion=(0,0,1000,1000))
		
		workspace = Frame(self.window, padx=5, pady=10, bg=self.bg_colors[1])
		workspace.pack(side=LEFT)
		
		#panel stuff
		
		
		tiles = []
		file_labels = []
		for i in range(0, int(self.image.height/self.tile_height)+1):
			if i > 0:
				row = []
				label_row[]
				for j in range(0, int(self.image.width/self.tile_width)+1):
					frame = Frame(workspace, bg=self.bg_colors[0])
					frame.grid(row=i, column=j)
					if j > 0:
						coords = ((j-1)*self.tile_width, (i-1)*self.tile_height, j*self.tile_width, i*self.tile_height)
						row.append(Sprite(Image.crop(box=coords)))
						Button(workspace, image=tk_image, command=test, relief=FLAT).pack()
						file_label = Label(workspace, text=f"{j}-{i}.png", fg=self.fg_color, bg=self.bg_colors[0])
						file_label.pack()
						label_row.append(file_label)
				tiles.append(row)
				file_labels.append(label_row)
			
		
		
		
		print(self.image.filename)
		tk_image = ImageTk.PhotoImage(self.image)
		image = Button(self.window, image=tk_image, command=test, relief=FLAT)
		image.pack()
		
		self.window.mainloop()

gui = SplitterGUI()
