#!/usr/bin/env python3

# Changelog and build json creator for github update service

import sys
import os
import json
from datetime import datetime

# Process file and create json output
def process_file(filename,device,output_folder,sf_repo,sf_uname):
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
    data['url'] = sf_repo + os.path.join(str(device),str(date),rom_filename)+"/download"

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

  open(os.path.join(change_folder,rom_filename).replace(".zip",".zip.txt"),'a').close()
  
  # Copy file to source forge by ssh connection using public/private key and username
  
  # Create folder structure for device
  project = os.path.basename(os.path.normpath(sf_repo))
  
  device_folder = os.path.join("/home/frs/project/",str(project),"files","devices",str(device),str(date))
    
  print(device_folder)
  os.system("sftp -o \"StrictHostKeyChecking no\" " + sf_uname + "@frs.sourceforge.net << EOF \ mkdir " + device_folder + "\ EOF")
  
  # Copy file to created directory
  #print("Uploading " + filename.replace(".zip.json",".zip") + " to " + device_folder)
  #os.system("scp -o \"StrictHostKeyChecking no\" " + filename.replace(".zip.json",".zip") + " " + sf_uname + "@frs.sourceforge.net:" + device_folder)

# Checks
if len(sys.argv) < 5:
  print("USAGE: " + sys.argv[0] + " [FOLDER IN] [FOLDER_OUT] [SOURCEFORGE PROJECT] [SOURCEFORGE SSH USERNAME]");
  sys.exit(1);

folder_in=sys.argv[1];
folder_out=sys.argv[2];
sf_repo=sys.argv[3];
sf_uname=sys.argv[4]

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
  
if not "https://sourceforge.net/projects/" in sf_repo:
  print("Error - " + sf_repo + " isn't valid\n e.g: https://sourceforge.net/projects/evo9810ota/files/devices/");
  sys.exit(5)  

if not os.path.exists(os.path.expanduser("~/.ssh/")):
  print("Error - ssh keys doesn't exist");
  sys.exit(6)                             
                             
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
      process_file(os.path.join(folder1_path,filename),folder1,folder_out,sf_repo,sf_uname);
      count=count+1

# Error check
if count == 0:
  print(sys.argv[0] + " - Failed to process any files.");
else:
  # Auto push to github if repo has been initialized within output directory
  if os.path.exists(os.path.join(folder_out,".git")):
    os.system("cd \"" + folder_out + "\"; git commit -am \"auto push\"; git push -f origin master")
