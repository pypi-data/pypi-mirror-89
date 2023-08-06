# Backup folder to zip
Copies an entire folder and its contains into a zip file whose filename increments. 

## Install

``` bash
$ pip install backup-folder-to-zip
```

## How to use

``` python
# Import pakage
from backup_folder_to_zip import backup

#  Save local folders
from_folder = "c:\\user\\my_files"
to_folder = "c:\\user\\backup_of_my_files"

# backup folder 
mybackup = extractor.Extractor(from_folder, to_folder)
```
