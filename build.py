# Importing required libraries for file and directory operations and command line argument parsing.
import os
import shutil
import argparse
from sys import platform

# Define the name of the Pakset and Makeobj settings.
PAKSET = "Pak128.Nordic"
MAKEOBJ_OPTIONS = "PAK128"

# List of directories containing files to be packed into the Pakset.
DIRECTORIES = [
    "Base/Big Logo",
    "Base/Misc_GUI_64",
    "Base/Misc_GUI",
    "Base/Smokes",
    "Base/Good",
    "Base/Landscape/Grounds",
    "Base/Landscape/Outside",
    "Base/Landscape/Rivers", "base/Landscape/Trees",
    "Base/Way/Air",
    "Base/Way/Bridges",
    "Base/Way/Crossings",
    "Base/Way/Maglev",
    "Base/Way/Monorail",
    "Base/Way/Narrowgauge",
    "Base/Way/Powelines",
    "Base/Way/Rail",
    "Base/Way/Road",
    "Base/Way/Sea",
    "Base/Way/Tramway",
    "Base/Wayobjects/Catenarys",
    "Base/Wayobjects/Rail Signals",
    "Base/Wayobjects/Street Signs",
    "Base/Buildings/City Buildings",
    "Base/Buildings/Factories",
    "Base/Buildings/Player buildings",
    "Base/Vehicles/Rail Vehicles/Goods Wagons",
    "Base/Vehicles/Rail Vehicles/Locomotives",
    "Base/Vehicles/Rail Vehicles/Multiple Unit-Railcars",
    "Base/Vehicles/Rail Vehicles/Passenger Carriages"
]

# Parse command line arguments using argparse.
parser = argparse.ArgumentParser(
    description=f"Simutrans {PAKSET} build script.")
parser.add_argument(
    '-s', help="Compile for Simutrans Standard", action='store_false')
parser.add_argument(
    '-e', help="Compile for Simutrans Extended (only available on Windows)", action='store_false')

args = parser.parse_args()

# Check the specified Simutrans version and the operating system platform to determine the appropriate makeobj executable.
if args.s and args.e is None:
    print("ERROR: You must specify a Simutrans version to compile for.")
    parser.print_help()
    exit(1)

if platform == "win32":
    if args.s:
        makeobj = "Makeobj.exe"
    elif args.e:
        makeobj = "Makeobj-Extended.exe"
else:
    if args.s:
        makeobj = "./makeobj"
    elif args.e:
        print("ERROR: Makeobj-Extended is only available on Windows.")
        exit(1)

# Check if the makeobj executable exists in the current working directory.
if not os.path.exists(makeobj):
    print(f"ERROR: {makeobj} was not found in {os.getcwd()}.")
    exit(1)

# Create the Pakset directory and necessary subdirectories for text files.
os.makedirs(PAKSET, exist_ok=True)
shutil.rmtree(PAKSET)
os.makedirs(os.path.join(PAKSET, "Text", "doc"), exist_ok=True)

# Copy text files and credits to the Pakset directory.
text_files = os.listdir("Text")
for file in text_files:
    shutil.copytree("Text", f"{PAKSET}{os.sep}", dirs_exist_ok=True)
shutil.copy("Credits.txt", os.path.join(
    PAKSET, "Text", "doc{os.sep}"))

# Function to pack files from source directory to destination directory using makeobj.


def pack_files(source_dir, destination_dir):
    print(f"Packing {source_dir}")
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if os.path.isdir(os.path.join(dirpath, filename)):
                continue
            os.system(
                f"{makeobj} {MAKEOBJ_OPTIONS} {os.path.join(dirpath, filename)} {destination_dir} >> {os.path.join(PAKSET, 'error.txt')}")


# Pack files from specified directories into the Pakset directory.
for directory in DIRECTORIES:
    pack_files(directory, PAKSET)

# Print a message indicating the successful completion of the script.
print(f"======\nDONE!\n======")
