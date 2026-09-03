# IMPORT

import tkinter as tk
from tkinter import messagebox
import os
import json

# Load Config
with open("config.json", "r", encoding="utf-8") as file:
    CONFIG = json.load(file)

WINDOWS_USER_NAME = CONFIG["WINDOWS_USER_NAME"]
AUTHOR = CONFIG["AUTHOR"]
DEFAULT_MC_VERSION = CONFIG["DEFAULT_MC_VERSION"]
DEFAULT_WORLD_NAME = CONFIG["DEFAULT_WORLD_NAME"]
DEFAULT_PACK_FORMAT = CONFIG["DEFAULT_PACK_FORMAT"]
DEFAULT_PACK_ICON_PATH = CONFIG["DEFAULT_PACK_ICON_PATH"]
OPEN_DATAPACK_IN_EXPLORER = CONFIG["OPEN_DATAPACK_IN_EXPLORER"]
VERSION = "v1.0"

# FUNCTIONS

def create():
    name = name_entry.get()
    namespace = namespace_entry.get().strip()
    world_name = world_name_entry.get().strip()
    pack_format = pack_format_entry.get().strip()
    description = description_entry.get("1.0", tk.END).strip()
    default_functions = default_functions_var.get()
    pack_icon = pack_icon_var.get()
    pack_icon_path = pack_icon_path_entry.get().strip()
    credits = credits_var.get()

    pack_name = name + " " + VERSION
    world_path = f"C:\\Users\\{WINDOWS_USER_NAME}\\AppData\\Roaming\\.minecraft\\saves\\{world_name}"

    # Checks
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return

    if not namespace:
        namespace = name.lower().replace(" ", "_")
        namespace_entry.insert(0, namespace)

    if not os.path.isdir(world_path):
        messagebox.showerror("Error", "Invalid world name or path.")
        return

    # Create Datapack Structure
    os.makedirs(os.path.join(world_path, "datapacks", pack_name, "data", namespace), exist_ok=True)

    # pack.mcmeta
    with open("resources/datapack/pack.mcmeta.json", "r", encoding="utf-8") as file:
        pack_mcmeta = json.load(file)
    print("description=", description)
    pack_mcmeta["pack"]["description"] = description
    pack_mcmeta["pack"]["pack_format"] = int(pack_format)
    pack_mcmeta["pack"]["max_format"] = int(pack_format)

    with open(os.path.join(world_path, "datapacks", pack_name, "pack.mcmeta"), "w", encoding="utf-8") as file:
        json.dump(pack_mcmeta, file, indent=4)

    # Default Functions (minecraft/tags/function/)
    if default_functions:
        # namespace/function
        functions_path = os.path.join(world_path, "datapacks", pack_name, "data", namespace, "function")
        os.makedirs(functions_path, exist_ok=True)

        # minecraft/tags/function
        minecraft_functions_path = os.path.join(world_path, "datapacks", pack_name, "data", "minecraft", "tags", "function")
        os.makedirs(minecraft_functions_path, exist_ok=True)

        # Create empty load.mcfunction and tick.mcfunction files
        open(os.path.join(functions_path, "load.mcfunction"), "w").close()
        open(os.path.join(functions_path, "tick.mcfunction"), "w").close()

        # Create load.json and tick.json files
        with open(os.path.join(minecraft_functions_path, "load.json"), "w", encoding="utf-8") as file:
            json.dump({"values": [f"{namespace}:load"]}, file, indent=4)
        with open(os.path.join(minecraft_functions_path, "tick.json"), "w", encoding="utf-8") as file:
            json.dump({"values": [f"{namespace}:tick"]}, file, indent=4)

    # Copy pack.png
    if pack_icon and os.path.isfile(pack_icon_path) and pack_icon_path.lower().endswith(".png"):
        os.makedirs(os.path.join(world_path, "datapacks", pack_name), exist_ok=True)
        with open(pack_icon_path, "rb") as src_file:
            with open(os.path.join(world_path, "datapacks", pack_name, "pack.png"), "wb") as file:
                file.write(src_file.read())

    # Copy CREDITS.txt and replace placeholders
    if credits:
        with open("resources/datapack/CREDITS.txt", "r", encoding="utf-8") as src_file:
            # placeholders: $AUTHOR, $VERSION, $MC_VERSION
            src_file_content = src_file.read()
            src_file_content = src_file_content.replace("$AUTHOR", AUTHOR)
            src_file_content = src_file_content.replace("$VERSION", VERSION)
            src_file_content = src_file_content.replace("$MC_VERSION", DEFAULT_MC_VERSION)

            with open(os.path.join(world_path, "datapacks", pack_name, "CREDITS.txt"), "w", encoding="utf-8") as file:
                file.write(src_file_content)

    if OPEN_DATAPACK_IN_EXPLORER:
        os.startfile(os.path.join(world_path, "datapacks", pack_name))

def generate_description():
    name = name_entry.get().strip()
    description_entry.insert(0.0, f"{name} {VERSION} - {DEFAULT_MC_VERSION} - by §6§n{AUTHOR}")

def update_pack_icon_state():
    if pack_icon_var.get():
        pack_icon_path_entry.configure(state="normal")
    else:
        pack_icon_path_entry.configure(state="disabled")

# CREATE GUI

# Window
root = tk.Tk()
root.title("Datapack Generator - v1.0.0")
root.geometry("500x800")
root.resizable(False, False)
root.iconbitmap("resources/app/icon.ico")

# Name
tk.Label(root, text="Datapack Name").pack(anchor="w", padx=10, pady=(10, 0))
name_entry = tk.Entry(root, width=80)
name_entry.pack(anchor="w", padx=10)

# Namespace
tk.Label(root, text="Namespace").pack(anchor="w", padx=10, pady=(10, 0))
namespace_entry = tk.Entry(root, width=80)
namespace_entry.pack(anchor="w", padx=10)

# World Name
tk.Label(root, text="World Name").pack(anchor="w", padx=10, pady=(10, 0))
tk.Label(root, text=f"C:\\Users\\{WINDOWS_USER_NAME}\\AppData\\Roaming\\.minecraft\\saves\\WORLD_NAME", fg="gray").pack(anchor="w", padx=10, pady=(0, 0))
world_name_entry = tk.Entry(root, width=80)
world_name_entry.pack(anchor="w", padx=10)
world_name_entry.insert(0, DEFAULT_WORLD_NAME)

# Description
description_frame = tk.Frame(root)
description_frame.pack(anchor="w", padx=10, pady=(10, 5))

tk.Label(
    description_frame,
    text="Datapack Description"
).pack(side="left")

tk.Button(
    description_frame,
    text="Generate",
    width=9,
    command=generate_description
).pack(side="left", padx=5)

description_entry = tk.Text(root, width=50, height=7)
description_entry.pack(anchor="w", padx=10)

# Pack Format
tk.Label(root, text="Pack Format").pack(anchor="w", padx=10, pady=(10, 0))
pack_format_entry = tk.Entry(root, width=10)
pack_format_entry.pack(anchor="w", padx=10)
pack_format_entry.insert(0, DEFAULT_PACK_FORMAT)

# Default Functions Checkbox
default_functions_var = tk.BooleanVar(value=False)
default_functions_check = tk.Checkbutton(
    root,
    text="Create 'load' and 'tick' functions",
    variable=default_functions_var
)
default_functions_check.pack(anchor="w", padx=10, pady=(10, 0))

# Pack Icon
pack_icon_var = tk.BooleanVar(value=False)
pack_icon_check = tk.Checkbutton(
    root,
    text="Create pack.png",
    variable=pack_icon_var,
    command=update_pack_icon_state
)
pack_icon_check.pack(anchor="w", padx=10, pady=(10, 0))

# Pack Icon Path
pack_icon_path_entry = tk.Entry(root, width=80)
pack_icon_path_entry.pack(anchor="w", padx=(25, 10))
pack_icon_path_entry.insert(0, DEFAULT_PACK_ICON_PATH)
pack_icon_path_entry.configure(state="disabled")

# Credits Checkbox
credits_var = tk.BooleanVar(value=True)
credits_check = tk.Checkbutton(
    root,
    text="Create CREDITS.txt",
    variable=credits_var
)
credits_check.pack(anchor="w", padx=10, pady=(10, 0))

# Create Button
create_button = tk.Button(
    root,
    text="Create Datapack",
    width=25,
    command=create
)
create_button.pack(anchor="w", padx=10, pady=(10, 0))

# Mainloop
root.mainloop()