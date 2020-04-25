# EvoXOTA

## Description

Create structure and json files for unofficial builds of evox. Auto pushes to git repo if git has been initialized within the output directory.

## Usage

    python3 process.py [FOLDER IN] [FOLDER_OUT] [SOURCEFORGE PROJECT] [SOURCEFORGE SSH USERNAME]
    python3 process.py rom/out/target/product/ ota/ https://sourceforge.net/projects/evo9810ota/files/devices/ test123

# Notes

Uses public/private key to authenticiate the specified user to sourceforge, create and upload to sourceforge a public key to allow script to function correctly.
