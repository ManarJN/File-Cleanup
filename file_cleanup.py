#! python3

# Manar Naboulsi - 04 March, 2018
#
# File Cleanup - Cleans up a specified folder of YYYYMMDD_HH:MM timestamped files by deleting
#                documents older than a specified number of days and adding leading zero to
#                file names with _H:MM formatted times.

# Arguments:
#   - location = location of backup files
#   - remove = number of days before deleting a file 


import os, re, datetime, shutil, stat

# removes read only attribute of files so folders can be deleted
def onerror_handler(func, path):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

regex = re.compile(r'^(\d{8})_([0-9 ]{6})$')  # pattern to read file names

# renames files with 4-digit times to include a leading 0
def backup_rename(location):
    for file in os.listdir(location):    
        # skips items that aren't folders with datetimes as their names
        if re.match(regex, file) is None:
            continue
        
        # extracts date and time from file name
        dtstamp = regex.search(file)        
        dt_str = dtstamp.group(1)  # date
        tm_str = dtstamp.group(2)  # time
              
        # adds leading zero to remaining file names with 4-digit time     
        if tm_str.startswith(' ') is True:
            os.rename(os.path.join(location, file), os.path.join(location, dt_str + '_0' + tm_str[1:]))
# end of backup_rename
        
        
# deletes backups older than 4 days        
def backup_cleanup(location, remove):
    startdt = datetime.datetime.now()  # obtains current datetime

    for file in os.listdir(location):    
        # skips items that aren't folders with datetimes as their names
        if re.match(regex, file) is None:
            continue
        
        # extracts date and time from file name
        dtstamp = regex.search(file)   
        dt = datetime.datetime.strptime(dtstamp.group(1), "%Y%m%d")
                
        # deletes backups older than 4 days
        if (startdt - dt).days > remove:
            shutil.rmtree(os.path.join(location, file), ignore_errors=False, onerror=onerror_handler)
# end of backup_cleanup
	
	
# run program 
#backup_rename('')
#backup_cleanup('', )
