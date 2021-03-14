# Spritesplitter

This python script is designed to be an easy-to-use, GUI-based method of taking a large spritesheet and splitting it into many sprites of the same size. 
It also allows for efficient naming of sprites, especially if they are grouped in rows/columns of similarly-named sprites. Requires the [Pillow library](https://pillow.readthedocs.io/).

# Instructions
### Start New
To start, simply press "Start New", load your spritesheet up, enter the height and width of each tile, and press the button to get started.
This will take you to the editor window, where you can assign names to certain sprites or use exclude mode to prevent them from being exported.
You may then choose to export your sprites directly with the assigned defaults (and rename them outside the program), or assign names within the program.
To assign names to sprites, you will have to first add your names in the panel on the left.
Then, click on individual sprites to add that name to them, or on the buttons above columns/to the left of rows to assign a name to all sprites in that row/column.
Each sprite can have as many names as you like, delimited by the character in the delimiter field at the top of the panel.
For example, naming a sprite "person" then "running" with the default delimiter (underscore) will result in a file called "person_running.png".
Clear mode can be used to clear all names from a given sprite.
Once you are done, select a directory to export your sprites into, and press the export button.
You may also wish to save the configuration so you can use it in the future, either for a different spritesheet or for the same spritesheet after it has been edited. 
In this case, you may also press the "Save Configuration" button, which will save the config as "config.json" in the selected directory.

### Load Configuration
To load a config, press the "Load from File" option upon startup instead.
When you select a config file, the fields for tile width and height will automatically populate with values from the original file; however, you are not obligated to use these values.
A warning will pop up if the image or tile size differs from the original file.
If you choose to continute, the editor will open up, populated with the saved names and exclusions.
