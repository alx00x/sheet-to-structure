#!/usr/bin/python
import gspread
import re, os, sys

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

# Get user and pass data
username = raw_input('Username: ')
password = win_getpass()
sheeturl = raw_input('     URL: ')
print "Logging in..."
gc = gspread.login(username,password)

worksheet = gc.open_by_url(sheeturl).sheet1
values_list_dirty = worksheet.col_values(3)
values_list = [x for x in values_list_dirty if x is not None]

items = []
listedValues = []
lists = {}
folders = []

for x in values_list:
    if x.isupper():
        items.append(x)

for index, i in enumerate(items):
    iStart = values_list.index(i)
    try:
        iEnd = values_list.index(items[index + 1])
    except IndexError:
        iEnd = len(values_list)
    listedValues.append([i, iStart, iEnd])

for index, j in enumerate(listedValues):
    lists[j[0]] = values_list[j[1]+1:j[2]]

for key, value in lists.iteritems():
    for v in value:
        folders.append(key + "_" + v)

print folders

# print "Creating following folders:"
# print folders

# print "Failed to create:"
# print failedFolders