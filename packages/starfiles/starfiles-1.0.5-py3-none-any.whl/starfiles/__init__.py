"""
Starfiles

Simplify starfiles, if it wasn't simple enough already
"""

__version__ = "1.0.1"
__author__ = 'DwifteJB'
__credits__ = 'Quixthe2nd'

import json
import requests
import re
import os
import time
import sys
  

def upload(filename):
  try:
    files = {
      'upload': (f'{filename}', open(f'{filename}', 'rb')),
    }
  except FileNotFoundError as e:
    print(f"[ ERROR ] : {e}")
    return f"[ ERROR ] : {e}"
  response = requests.post('https://api.starfiles.co/upload/upload_file?profile={profile}', files=files)
  api = json.loads(response.text)
  file = api['file']
  link = f"https://api.starfiles.co/direct/{file}"
  size = round(int(os.path.getsize(filename)) / 1000000, 2)
  name = re.sub(r'^.*?/', '', filename)
  print("\n")
  print(f"------------ Uploaded {name} ------------")
  print(f"Name: {name}")
  print(f"Size: {size}mb")
  print(f"Download Link:\nRegular: https://starfiles.co/file/{file}\nDirect: {link}")
  if re.search("ipa$", filename):
    print(f"Plist: https://api.starfiles.co/installipa/{file}\nInstall URL: itms-services://?action=download-manifest&url=https://api.starfiles.co/installipa/{file}")
  return link
