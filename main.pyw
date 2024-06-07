from tkinter import *
import Levenshtein
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import sys
from PIL import Image
import os
from tkinter.ttk import Label, Style
import threading
from scipy.spatial import KDTree
from functools import lru_cache
import numpy as np
from PIL import Image
from PIL import ImageSequence


actual_world_name = ""
generalTheme = "light"
specificTheme = "basic_theme"
canConvert = False



def image_to_pixel_list(image):
    np_image = np.array(image)

    pixels = []

    height, width, _ = np_image.shape

    for y in range(height):
        for x in range(width):
            r, g, b = np_image[y, x]
            pixels.append([x, y, r, g, b])

    return pixels


def resize_image(input_path, max_size):
    image = Image.open(input_path)
    image.thumbnail((max_size, max_size))
    image = image.convert("RGB")
    return image

blocks = {
    'acacia_planks': (168, 90, 50),
    'andesite': (136, 136, 136),
    'bedrock': (85, 85, 85),
    'bee_nest': (196, 150, 77),
    'beehive': (157, 126, 75),
    'birch_log': (216, 215, 210),
    'birch_planks': (192, 175, 121),
    'black_concrete': (8, 10, 15),
    'black_glazed_terracotta': (67, 30, 32),
    'black_terracotta': (37, 23, 16),
    'black_wool': (21, 21, 26),
    'blue_concrete': (45, 47, 143),
    'blue_glazed_terracotta': (47, 64, 139),
    'blue_terracotta': (74, 60, 91),
    'blue_wool': (53, 57, 157),
    'bone_block': (229, 225, 207),
    'bookshelf': (117, 94, 59),
    'bricks': (150, 97, 83),
    'brown_concrete': (96, 60, 31),
    'brown_glazed_terracotta': (119, 106, 85),
    'brown_terracotta': (77, 51, 36),
    'brown_wool': (114, 71, 40),
    'carved_pumpkin': (150, 84, 17),
    'chiseled_quartz_block': (231, 226, 218),
    'chiseled_red_sandstone': (183, 96, 27),
    'chiseled_sandstone': (216, 202, 155),
    'chiseled_stone_bricks': (119, 118, 119),
    'clay': (160, 166, 179),
    'coal_block': (16, 15, 15),
    'coal_ore': (116, 116, 116),
    'coarse_dirt': (119, 85, 59),
    'cobblestone': (127, 127, 127),
    'composter': (112, 70, 31),
    'cracked_stone_bricks': (118, 117, 118),
    'crafting_table': (128, 102, 63),
    'cyan_concrete': (21, 119, 136),
    'cyan_glazed_terracotta': (52, 118, 125),
    'cyan_terracotta': (87, 91, 91),
    'cyan_wool': (21, 137, 145),
    'dark_oak_log': (60, 46, 26),
    'dark_oak_planks': (66, 43, 20),
    'dark_prismarine': (51, 91, 75),
    'dead_brain_coral_block': (124, 117, 114),
    'dead_bubble_coral_block': (131, 123, 119),
    'dead_fire_coral_block': (131, 123, 119),
    'dead_horn_coral_block': (133, 126, 122),
    'dead_tube_coral_block': (130, 123, 119),
    'diamond_block': (73, 242, 236),
    'diamond_ore': (125, 142, 141),
    'diorite': (188, 188, 188),
    'dirt': (134, 96, 67),
    'dried_kelp_block': (50, 58, 38),
    'emerald_block': (42, 203, 87),
    'emerald_ore': (117, 136, 124),
    'fletching_table': (197, 180, 133),
    'glowstone': (171, 131, 84),
    'gold_block': (246, 208, 61),
    'gold_ore': (143, 140, 125),
    'granite': (149, 103, 85),
    'gray_concrete': (55, 58, 62),
    'gray_glazed_terracotta': (83, 90, 93),
    'gray_terracotta': (58, 42, 36),
    'gray_wool': (62, 68, 71),
    'green_concrete': (73, 91, 36),
    'green_glazed_terracotta': (117, 142, 67),
    'green_terracotta': (76, 83, 42),
    'green_wool': (83, 109, 27),
    'hay_block': (166, 136, 38),
    'honeycomb_block': (229, 148, 29),
    'iron_block': (220, 220, 220),
    'iron_ore': (136, 130, 127),
    'jack_o_lantern': (214, 152, 52),
    'jukebox': (90, 52, 32),
    'jungle_log': (85, 67, 25),
    'jungle_planks': (160, 115, 80),
    'lapis_block': (30, 67, 140),
    'lapis_ore': (99, 110, 132),
    'light_blue_concrete': (36, 137, 199),
    'light_blue_glazed_terracotta': (94, 164, 208),
    'light_blue_terracotta': (113, 109, 138),
    'light_blue_wool': (58, 175, 217),
    'light_gray_concrete': (125, 125, 115),
    'light_gray_glazed_terracotta': (144, 166, 167),
    'light_gray_terracotta': (135, 107, 98),
    'light_gray_wool': (142, 142, 134),
    'lime_concrete': (94, 169, 24),
    'lime_glazed_terracotta': (162, 197, 55),
    'lime_terracotta': (103, 118, 53),
    'lime_wool': (112, 185, 26),
    'loom': (142, 119, 91),
    'magenta_concrete': (169, 48, 159),
    'magenta_glazed_terracotta': (208, 100, 191),
    'magenta_terracotta': (150, 88, 109),
    'magenta_wool': (189, 69, 180),
    'magma_block': (142, 63, 31),
    'melon': (114, 146, 30),
    'mossy_stone_bricks': (115, 121, 105),
    'nether_quartz_ore': (117, 65, 62),
    'nether_wart_block': (114, 2, 2),
    'netherrack': (97, 38, 38),
    'note_block': (88, 58, 40),
    'oak_log': (109, 85, 50),
    'oak_planks': (162, 130, 78),
    'observer': (70, 68, 68),
    'obsidian': (20, 18, 29),
    'orange_concrete': (224, 97, 1),
    'orange_glazed_terracotta': (154, 147, 91),
    'orange_terracotta': (162, 84, 38),
    'orange_wool': (241, 118, 20),
    'pink_concrete': (229, 153, 181),
    'pink_glazed_terracotta': (235, 154, 181),
    'pink_terracotta': (162, 78, 79),
    'pink_wool': (237, 141, 172),
    'polished_andesite': (132, 134, 133),
    'polished_diorite': (192, 193, 194),
    'polished_granite': (154, 106, 89),
    'prismarine': (99, 156, 151),
    'prismarine_bricks': (99, 171, 158),
    'pumpkin': (195, 114, 24),
    'purple_concrete': (100, 32, 156),
    'purple_glazed_terracotta': (109, 48, 152),
    'purple_terracotta': (118, 70, 86),
    'purple_wool': (121, 42, 172),
    'purpur_block': (169, 125, 169),
    'purpur_pillar': (171, 129, 171),
    'quartz_block': (235, 229, 222),
    'red_concrete': (142, 33, 33),
    'red_glazed_terracotta': (181, 59, 53),
    'red_nether_bricks': (69, 7, 9),
    'red_sandstone': (186, 99, 29),
    'red_terracotta': (143, 61, 47),
    'red_wool': (161, 39, 35),
    'redstone_block': (148, 20, 0),
    'redstone_lamp': (95, 54, 30),
    'redstone_ore': (133, 107, 107),
    'sandstone': (216, 203, 155),
    'sea_lantern': (172, 199, 190),
    'smithing_table': (57, 58, 70),
    'smoker': (102, 91, 75),
    'snow_block': (249, 254, 254),
    'soul_sand': (81, 62, 50),
    'sponge': (195, 192, 74),
    'spruce_log': (58, 37, 16),
    'spruce_planks': (114, 84, 48),
    'stone': (125, 125, 125),
    'stone_bricks': (122, 121, 122),
    'stripped_acacia_wood': (174, 92, 59),
    'stripped_birch_wood': (196, 176, 118),
    'stripped_dark_oak_wood': (96, 76, 49),
    'stripped_jungle_wood': (171, 132, 84),
    'stripped_oak_wood': (177, 144, 86),
    'stripped_spruce_wood': (115, 89, 52),
    'wet_sponge': (171, 181, 70),
    'white_concrete': (207, 213, 214),
    'white_glazed_terracotta': (188, 212, 202),
    'white_terracotta': (210, 178, 161),
    'white_wool': (233, 236, 236),
    'yellow_concrete': (241, 175, 21),
    'yellow_glazed_terracotta': (154, 147, 91),
    'yellow_terracotta': (186, 133, 35),
    'yellow_wool': (248, 198, 40)
}
block_colors = list(blocks.values())
block_names = list(blocks.keys())
block_tree = KDTree(block_colors)

@lru_cache(maxsize=200000)
def rgb_to_minecraft_block(r, g, b):
    # closest
    index = block_tree.query([r, g, b])[1]

    return block_names[index]


def init(image_path, mcfunction_path, max_dimension=256):
    max_dimension, image_path = max_dimension, image_path 

    resized_image = resize_image(image_path, max_dimension)
    pixels = image_to_pixel_list(resized_image)

    result_list = []
    last_block = None
    start_coord = None
    end_coord = None
    height = resized_image.size[1]
    
    # player loc
    x_offset = -(resized_image.size[0] // 2)

    for pixel in pixels:
        x, y, r, g, b = pixel
        current_block = rgb_to_minecraft_block(r, g, b)
        
        if not last_block:
            start_coord = (x + x_offset, y)
            end_coord = (x + x_offset, y)
            last_block = current_block
        else:
            if current_block == last_block and x == (end_coord[0] - x_offset) + 1:
                end_coord = (x + x_offset, y)
            else:
                if start_coord == end_coord:
                    result_list.append(f"setblock ~{start_coord[0]} ~{height - start_coord[1]} ~ {last_block}\n")
                else:
                    result_list.append(f"fill ~{start_coord[0]} ~{height - start_coord[1]} ~ ~{end_coord[0]} ~{height - end_coord[1]} ~ {last_block}\n")
                start_coord = (x + x_offset, y)
                end_coord = (x + x_offset, y)
                last_block = current_block

    if start_coord == end_coord:
        result_list.append(f"setblock ~{start_coord[0]} ~{height - start_coord[1]} ~ {last_block}\n")
    else:
        result_list.append(f"fill ~{start_coord[0]} ~{height - start_coord[1]} ~ ~{end_coord[0]} ~{height - end_coord[1]} ~ {last_block}\n")

    output_path = mcfunction_path

  
    output_string = ''.join(result_list)

    with open(output_path, "w") as f:
        f.write(output_string)

# home dir
home = os.path.expanduser("~")

saves_path = os.path.join(home, "AppData", "Roaming", ".minecraft", "saves")

if os.path.exists(saves_path):
    files = set(os.listdir(saves_path))
else:
    print(f"The path {saves_path} does not exist.")

root = Tk()
root.geometry("900x600")
root.title("Image to Minecraft | By breakdown55")
root.resizable(False, False)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
root.iconbitmap(resource_path("assets/thumb.ico"))







def use_suggestion():
    global actual_world_name, expected
    try:
        world_name_input.delete(0, END)
        world_name_input.insert(0, expected)
        actual_world_name = expected
    except:
        pass

    
def on_entry_change(*args):
    global actual_world_name, expected
    input = world_name_input_var.get()
    if len(input) > 0:
        #lev dist if required
        if input in files:
            actual_world_name = input
            world_name_help.config(text="World name set to: " + input)
            return  

        
        currentLowest = float('inf')
        for item in files:
            distance = Levenshtein.distance(input, item)
            if distance < currentLowest:
                currentLowest = distance
                expected = item

        world_name_help.config(text="Did you mean: " + expected)
    else:
        world_name_help.config(text="Start typing to see suggestions...")



world_name_input_var = StringVar()
world_name_input_var.trace_add("write", on_entry_change)








def open_image():
    global canConvert
    file_path = filedialog.askopenfilename()

    if not file_path:
        return
    try:
        image = Image.open(file_path)
    except:
        output.config(text="Image unprovided or invalid", foreground="red")

    # 1st frame of gif
    if file_path.endswith(".gif"):
        image = image.convert("RGBA")
        frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
        image = frames[0]

    if image.mode != 'RGB':
        image = image.convert('RGB')

    try:
        image.save(extend_path("test.jpg"))
        canConvert = True
        output.config(text="Click 'Apply Image'", foreground="black")
    except Exception as e:
        output.config(text=f"Error saving image: {e}", foreground="red")

    else:
        image = Image.open(file_path)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        try:
            image.save(extend_path("test.jpg"))
            canConvert = True
            output.config(text="Click 'Apply Image'", foreground="black")


        except Exception as e:
            output.config(text=f"Error saving image: {e}", foreground="red")


        aspect_ratio = image.width / image.height
        
        new_width = canvas.winfo_width()
        new_height = int(new_width / aspect_ratio)

        # height > canvas?
        if new_height > canvas.winfo_height():
            new_height = canvas.winfo_height()
            new_width = int(new_height * aspect_ratio)


        image = image.resize((new_width, new_height))
        
        photo = ImageTk.PhotoImage(image)
        
        # display in canvas
        canvas.create_image((canvas.winfo_width() - new_width) // 2, (canvas.winfo_height() - new_height) // 2, anchor=NW, image=photo)
        canvas.image = photo



def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder created at: {path}")
    else:
        print(f"Folder already exists at: {path}")

def write_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)
        print(f"File {os.path.basename(path)} created in {os.path.dirname(path)}")

def write_json_to_file(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"File {os.path.basename(path)} created in {os.path.dirname(path)}")

def extend_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    


    # check if bundled exe
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(application_path, 'assets', 'test.jpg')

    return image_path


def convert():
    global actual_world_name

    try:
        # Verify actual_world_name
        if actual_world_name not in files:
            output.config(text="Invalid World Name", foreground="red")
            return

        if canConvert == True:
            functions_path = os.path.join(saves_path, actual_world_name, "datapacks", "image_to_mc", "data", "to_minecraft", "functions")
            datapack_path = os.path.join(saves_path, actual_world_name, "datapacks", "image_to_mc")
            
            ensure_directory_exists(functions_path)
            
            mcfunction_path = os.path.join(functions_path, "convert.mcfunction")
            write_to_file(mcfunction_path, "# If you're seeing this, an error occured while constructing the datapack files.")
            
            # Create pack.mcmeta
            pack_data = {
                "pack": {
                    "pack_format": 15,
                    "description": "Datapack used to write image data with Image --> Minecraft"
                }
            }
            mcmeta_path = os.path.join(datapack_path, "pack.mcmeta")
            write_json_to_file(mcmeta_path, pack_data)

            init(extend_path("test.jpg"), mcfunction_path=mcfunction_path)
            output.config(text="Conversion Successful!", foreground="green")
        else:
            output.config(text="Image unprovided or invalid", foreground="red")


    except NameError:
        print("invalid world name")
        output.config(text="Invalid World Name", foreground="red")



global converter_tab_button
def converter():
    for item in [pristine_theme_button, dark_theme_button, light_theme_button, crystal_theme_button, sunset_theme_button]:
        item.place_forget()

    selected_instructions_tab_button.place_forget()
    instructions_tab_button.place_forget()
        
    converter_tab_button.place_forget()
    deselected_converter_tab_button.place_forget()


    # set bg
    if specificTheme == "basic_theme":
        bg_image_path = resource_path("assets/basic_theme_bg.png")

        bg_image = Image.open(bg_image_path)
        bg_photo = ImageTk.PhotoImage(bg_image)
        desired_size = (900, 600)
        bg_image = bg_image.resize(desired_size)
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)




        converter_tab_button.place(relx=0.3, rely=0.031, anchor=CENTER)
        instructions_tab_button.place(relx=0.7, rely=0.031, anchor=CENTER)


        #misc elements
        canvas.place(anchor=CENTER, relx=0.795, rely=0.7125)
        world_name_help_button3.place(relx=0.45, rely=0.8, anchor=CENTER)
        world_name_help_button2.place(relx=0.185, rely=0.8, anchor=CENTER)
        output.place(anchor=CENTER, relx=0.8, rely=.955)
        world_name_input.place(anchor=CENTER, relx=0.65, rely=0.337)
        world_name_help_button.place(relx=0.185, rely=0.51, anchor=CENTER)

        world_name_help.place(relx=0.27, rely=0.41, anchor=CENTER)








def instructions():

    # Hide all items
    for item in [pristine_theme_button, dark_theme_button, light_theme_button, crystal_theme_button, sunset_theme_button, bg_label, world_name_help_button2, canvas, world_name_help_button3, output, world_name_input, world_name_help, world_name_help_button, instructions_tab_button, converter_tab_button]:
        item.place_forget()

    if generalTheme == 'light':
        bg_image_path = resource_path("assets/light_theme_instructions_bg.png")
    elif generalTheme == 'dark':
        bg_image_path = resource_path("assets/dark_theme_instructions_bg.png")
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    desired_size = (900, 600)
    bg_image = bg_image.resize(desired_size)
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(relwidth=1, relheight=1)

    selected_instructions_tab_button.place(relx=0.7, rely=0.031, anchor=CENTER)

    deselected_converter_tab_button.place(relx=0.3, rely=0.031, anchor=CENTER)
    



def themes():
    global converter_tab_button, deselected_converter_tab_button
    for item in [bg_label, world_name_help_button2, canvas, world_name_help_button3, output, world_name_input, world_name_help, world_name_help_button, instructions_tab_button, converter_tab_button]:
        item.place_forget()


    selected_instructions_tab_button.place_forget()
    instructions_tab_button.place_forget()
        
    converter_tab_button.place_forget()
    deselected_converter_tab_button.place_forget()


    if generalTheme == "light":
        bg_image_path = resource_path("assets/light_theme_theme_bg.png")


    elif generalTheme == "dark":
        bg_image_path = resource_path("assets/dark_theme_theme_bg.png")

    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    desired_size = (900, 600)
    bg_image = bg_image.resize(desired_size)
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(relwidth=1, relheight=1)
    bg_label.lower()


    

    instructions_tab_button.place(relx=0.7, rely=0.031, anchor=CENTER)
    deselected_converter_tab_button.place(relx=0.3, rely=0.031, anchor=CENTER)



    light_theme_button.place(relx=0.181, rely=0.25, anchor=CENTER)
    dark_theme_button.place(relx=0.5, rely=0.25, anchor=CENTER)
    sunset_theme_button.place(relx=0.819, rely=0.25, anchor=CENTER)
    
    crystal_theme_button.place(relx=0.181, rely=0.55, anchor=CENTER)
    pristine_theme_button.place(relx=0.5, rely=0.55, anchor=CENTER)



##########################     THEME BUTTONS

def enable_basic_theme():
    global generalTheme, specificTheme
    generalTheme = "light"
    specificTheme = "basic_theme"

 
light_theme_button_image_path = resource_path("assets/basic_theme_button.png")
light_theme_image = Image.open(light_theme_button_image_path)
light_theme_photo = ImageTk.PhotoImage(light_theme_image)

light_theme_button = Button(root, width=255, height=166, command=enable_basic_theme, image=light_theme_photo, compound="center", border=0)




def enable_dark_theme():
    global generalTheme, specificTheme
    generalTheme = "dark"
    specificTheme = "dark"

 
dark_theme_button_image_path = resource_path("assets/dark_theme_button.png")
dark_theme_image = Image.open(dark_theme_button_image_path)
dark_theme_photo = ImageTk.PhotoImage(dark_theme_image)

dark_theme_button = Button(root, width=255, height=166, command=enable_dark_theme, image=dark_theme_photo, compound="center", border=0)


def enable_sunset_theme():
    global generalTheme, specificTheme
    generalTheme = "light"
    specificTheme = "sunset"

 
sunset_theme_button_image_path = resource_path("assets/sunset_theme_button.png")
sunset_theme_image = Image.open(sunset_theme_button_image_path)
sunset_theme_photo = ImageTk.PhotoImage(sunset_theme_image)

sunset_theme_button = Button(root, width=255, height=166, command=enable_sunset_theme, image=sunset_theme_photo, compound="center", border=0)



def enable_crystal_theme():
    global generalTheme, specificTheme
    generalTheme = "dark"
    specificTheme = "crystal"

 
crystal_theme_button_image_path = resource_path("assets/crystal_theme_button.png")
crystal_theme_image = Image.open(crystal_theme_button_image_path)
crystal_theme_photo = ImageTk.PhotoImage(crystal_theme_image)

crystal_theme_button = Button(root, width=255, height=166, command=enable_crystal_theme, image=crystal_theme_photo, compound="center", border=0)



def enable_pristine_theme():
    global generalTheme, specificTheme
    generalTheme = "dark"
    specificTheme = "pristine"

 
pristine_theme_button_image_path = resource_path("assets/pristine_beauty_theme_button.png")
pristine_theme_image = Image.open(pristine_theme_button_image_path)
pristine_theme_photo = ImageTk.PhotoImage(pristine_theme_image)

pristine_theme_button = Button(root, width=255, height=166, command=enable_pristine_theme, image=pristine_theme_photo, compound="center", border=0)




##########################






















bg_image_path = resource_path("assets/basic_theme_bg.png")
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)
desired_size = (700, 500)
bg_image = bg_image.resize(desired_size)
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)





button_image_path2 = resource_path("assets/open_image_light.png")
button_image2 = Image.open(button_image_path2)
button_photo2 = ImageTk.PhotoImage(button_image2)
world_name_help_button2 = Button(root, width=217, height=105, command=open_image, image=button_photo2, compound="center", border=0)
world_name_help_button2.place(relx=0.185, rely=0.8, anchor=CENTER)




# Canvas to display the image
canvas = Canvas(root, bg="white", width=253, height=253, border=3, highlightbackground="#004aad")
canvas.place(anchor=CENTER, relx=0.795, rely=0.7125)



button_image_path3 = resource_path("assets/apply_image_light.png")
button_image3 = Image.open(button_image_path3)
button_photo3 = ImageTk.PhotoImage(button_image3)
world_name_help_button3 = Button(root, width=217, height=105, command=convert, image=button_photo3, compound="center", border=0)
world_name_help_button3.place(relx=0.45, rely=0.8, anchor=CENTER)




output = Label(root, text="", font= ("Arial", 15), background="#fff5ed")
output.place(anchor=CENTER, relx=0.8, rely=.955)



world_name_input = Entry(root, textvariable=world_name_input_var, font=("Ariel", 25), background="#004aad", fg="white")
world_name_input.place(anchor=CENTER, relx=0.65, rely=0.337)




world_name_help = Label(root, text="Your Text Here", font=("Arial", 20), style="TLabel", background="#fff5ed")
world_name_help.place(relx=0.27, rely=0.41, anchor=CENTER)
world_name_help.config(text = "(Start typing to see suggestions...)", font=("Arial", 15))





button_image_path = resource_path("assets/use_suggestion_light.png")
button_image = Image.open(button_image_path)
button_photo = ImageTk.PhotoImage(button_image)
world_name_help_button = Button(root, width=155, height=75, command=use_suggestion, image=button_photo, compound="center", border=0)
world_name_help_button.place(relx=0.185, rely=0.51, anchor=CENTER)







converter_tab_path = resource_path("assets/converter_selected.png")
converter_tab_image = Image.open(converter_tab_path)
converter_tab_photo = ImageTk.PhotoImage(converter_tab_image)
converter_tab_button = Button(root, width=276, height=23, command=converter, image=converter_tab_photo, compound="center", border=0)
converter_tab_button.place(relx=0.3, rely=0.031, anchor=CENTER)

instructions_tab_path = resource_path("assets/instructions_deselected.png")
instructions_tab_image = Image.open(instructions_tab_path)
instructions_tab_photo = ImageTk.PhotoImage(instructions_tab_image)
instructions_tab_button = Button(root, width=276, height=23, command=instructions, image=instructions_tab_photo, compound="center", border=0)
instructions_tab_button.place(relx=0.7, rely=0.031, anchor=CENTER)

themes_tab_path = resource_path("assets/themes_deselected.png")
themes_tab_image = Image.open(themes_tab_path)
themes_tab_photo = ImageTk.PhotoImage(themes_tab_image)
#themes_tab_button = Button(root, width=276, height=23, command=themes, image=themes_tab_photo, compound="center", border=0)
#themes_tab_button.place(relx=0.819, rely=0.031, anchor=CENTER)






selected_instructions_tab_path = resource_path("assets/instructions_selected.png")
selected_instructions_tab_image = Image.open(selected_instructions_tab_path)
selected_instructions_tab_photo = ImageTk.PhotoImage(selected_instructions_tab_image)
selected_instructions_tab_button = Button(root, width=276, height=23, command=instructions, image=selected_instructions_tab_photo, compound="center", border=0)

deselected_converter_tab_path = resource_path("assets/converter_deselected.png")
deselected_converter_tab_image = Image.open(deselected_converter_tab_path)
deselected_converter_tab_photo = ImageTk.PhotoImage(deselected_converter_tab_image)
deselected_converter_tab_button = Button(root, width=276, height=23, command=converter, image=deselected_converter_tab_photo, compound="center", border=0)

















root.mainloop()







