#!/usr/bin/env python3

# Changelog and build json creator for github update service

import sys
import os
import json
from datetime import datetime

# Process file and create json output
def process_file(filename,device,output_folder):
  with open(filename, 'r+') as f:

    data = json.load(f)
    now = datetime.now()
    date = now.strftime("%d-%m-%y")
    rom_filename = os.path.basename(filename.replace(".zip.json",".zip"))

    # Add metadata to json output
    data['website_url'] = "https://evolution-x.org"
    data['version'] = "Ten"
    data['news_url'] = "https://t.me/EvolutionXOfficial"
    data['forum_url'] = ""
    data['donate_url'] = ""
    data['error'] = False
    data['maintainer'] = "Robert Balmbra"
    data['maintainer_url'] = "https://forum.xda-developers.com/member.php?u=4834466"
    data['telegram_username'] = "robbalmbra"
    data['url'] = "https://resources.rob-balmbra.co.uk/ROM/" + str(date) + "/" + rom_filename

  build_folder = os.path.join(output_folder,"builds")
  if not os.path.exists(build_folder):
    try:
      os.makedirs(build_folder)
    except:
      pass

  change_folder = os.path.join(output_folder,"changelogs",device)
  if not os.path.exists(change_folder):
    try:
      os.makedirs(change_folder)
    except:
      pass

  # Dump data
  file_out = os.path.join(build_folder,device + ".json")
  with open(file_out,'w') as f:
    json.dump(data, f, indent=2, sort_keys=True)

  open(os.path.join(change_folder,rom_filename).replace(".zip",".txt"),'a').close()

# Checks
if len(sys.argv) < 4:
  print("USAGE: " + sys.argv[0] + " [FOLDER IN] [FOLDER_OUT] [GIT REPO]");
  sys.exit(1);

folder_in=sys.argv[1];
folder_out=sys.argv[2];
git_repo=sys.argv[3];

# Check if in folder exists
if not os.path.isdir(folder_in):
  print("Error - " + folder_in + " isn't a valid input directory.")
  sys.exit(1);

# Check if out folder exists
if not os.path.isdir(folder_out):
  print("Error - " + folder_out + " isn't a valid output directory.")
  sys.exit(2);

# Check if user has access to output and input directory
if not os.access(folder_out, os.W_OK):
  print("Error - " + folder_out + "isn't writeable")
  sys.exit(3)

if not os.access(folder_out, os.R_OK):
  print("Error - " + folder_in + "isn't readable")
  sys.exit(4)

# Create rom directory for zips to be uploaded to
rom_directory = os.path.join(folder_in,"ROMS") 
if not os.path.exists(rom_directory):
  os.makedirs(rom_directory)

# Iterate over files within folder_in
print(sys.argv[0] + " - Processing files ...");
count=0
for folder1 in os.listdir(folder_in):
  folder1_path = os.path.join(folder_in,folder1)
  for filename in os.listdir(folder1_path):
    if filename.endswith('.zip.json'):
      process_file(os.path.join(folder1_path,filename),folder1,folder_out);
      count=count+1

# Error check
if count == 0:
  print(sys.argv[0] + " - Failed to process any files.");
