#!/usr/bin/python
import gspread
import re, os, sys, functools

# ASCII art:
#
# 
ascii_art = """
                ===========================================
                            SHEET TO STRUCTURE
                ===========================================
                
                     +++        `  ___  '        \|/      
                    (o o)      -  (O o)  -      (o o)     
                ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-
                ===========================================
                                  
"""

# Functions:
#
def win_getpass(prompt='Password: ', stream=None):
    """Prompt for password with echo off, using Windows getch()."""
    import msvcrt
    for c in prompt:
        msvcrt.putch(c)
    pw = ""
    while 1:
        c = msvcrt.getch()
        if c == '\r' or c == '\n':
            break
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b':
            pw = pw[:-1]
            msvcrt.putch('\b')
        else:
            pw = pw + c
            msvcrt.putch("*")
    msvcrt.putch('\r')
    msvcrt.putch('\n')
    return pw

def get_working_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def make_folders(root_dir, subfolders):
    concat_path = functools.partial(os.path.join, root_dir)
    map(os.makedirs, map(concat_path, subfolders))

# Code:
#
# Get user and pass data
print ascii_art
username = raw_input('Username: ')
password = win_getpass()
sheeturl = raw_input('     URL: ')
print 'Logging in...'
try:
    gc = gspread.login(username,password)
except:
    print ''
    print 'Failed to login!'
    print ''
    print 'Press any key to continue...'
    raw_input()
    sys.exit(1)

# Define worksheet
worksheet = gc.open_by_url(sheeturl).sheet1
values_list_dirty = worksheet.col_values(3)
values_list = [x for x in values_list_dirty if x is not None]

# Define variables
items = []
listed_values = []
lists = {}
folders = []
failed_folders = []

# Create list of folders from column
for x in values_list:
    if x.isupper():
        items.append(x)

for index, i in enumerate(items):
    iStart = values_list.index(i)
    try:
        iEnd = values_list.index(items[index + 1])
    except IndexError:
        iEnd = len(values_list)
    listed_values.append([i, iStart, iEnd])

for index, j in enumerate(listed_values):
    lists[j[0]] = values_list[j[1]+1:j[2]]

for key, value in lists.iteritems():
    for v in value:
        folders.append(key + "_" + v)

# User info
print ''
print 'Creating following folders:'
print folders
print ''

# Necesery variables
game_name = raw_input('Game Name: ')
game_dir = get_working_dir() + '\\' + game_name
dir_array = ['after', 'info/mat', 'paint/mat', 'paint/wip', 'lipsync', 'render', 'scene']

# Main:
#
# Create folders
if __name__=='__main__':
    subfolders = (dir_array)
    if not os.path.exists(game_dir):
        os.makedirs(game_dir)
    for i in folders:
        main_dir = game_dir + '\\' + i
        if not os.path.exists(main_dir):
            make_folders(main_dir, subfolders)
        else:
            failed_folders.append(main_dir.replace(game_dir + '\\', ''))

# User info
print ''
print 'Failed to create:'

if failed_folders:
    print failed_folders
    
if not failed_folders:
    print 'none'

print ''
print 'Press any key to continue...'
raw_input()