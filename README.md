# Image-to-Minecraft 🔥
A tool for converting images into an .mcfunction file to place blocks that recreate the image in Minecraft.

# Download Executable (no account required) ⬇️
[Dropbox Download](https://www.dropbox.com/scl/fi/hhzi6krv1obu86a060418/image_to_minecraft.exe?rlkey=f1g7sxc9vo3gy7b3a8c4yb4c7&st=prryoqua&dl=0)

# Special Thanks to Ydop_ for the 🎉 [Showcase Video](about:blank) 🎉

# Notes 📝
- Once a pixel color is translated to a Minecraft block once, the result is cached, and the program should translate the same color quicker later
- The max length for any dimension of the image is 256 blocks. The other dimension is scaled accordingly. For example, if an image is 500x1000, it will be 128x256 in Minecraft
- UI built with Tkinter, but I would use CustomTkinter if I had to remake this
- Does not convert .AVIF files, but it will convert a wide variety of image formats
- There are other themes referenced in the code, but are not implemented. The dark theme gets the job done, and it looks good, so it will be the only theme for the forseeable future
- All code is in main_with_ui.py
- 1.21+ is currently supported, if you wish to use an earlier version, change the folder name "function" to "functions" in your world's datapack after using the program like normal

