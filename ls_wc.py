import argparse
import datetime
from grp import getgrgid
import os
from pwd import getpwuid
from stat import ST_MTIME, ST_NLINK, ST_SIZE, ST_UID, filemode
global flag_l 
global flag_i 
def wc(filenames):
    results = []

    for filename in filenames:
        chars = 0
        words = 0
        lines = 0
        try:
            with open(os.path.join(os.getcwd(),filename)) as fh:
                for line in fh:
                    lines += 1
                    words += len(line.split())
                    chars += len(line)
            results.append([
                str(lines),
                str(words),
                str(chars),
                str(filename)
            ]
            )
        except Exception as err:
            print(err)
    printFormatted(results)
 
def ls(args):
    dir_list = os.listdir(args.path)
    print(dir_list)

def get_input():
    command = input(os.getcwd()+" ")
    command_list = command.split(" ")
    if(len(command_list)==0):
         return [""]
    else:
        return command_list
def setFlag(command):
    for i in command:
        if i == '-i':
            global flag_i 
            flag_i = True
        if i == '-l':
            global flag_l
            flag_l = True

def handle_ls(path,command):

    notOriginList = True
    for i in command:
        if(len(command)==1):
            break
        if i == '-a':
            list = ['.','..'] + os.listdir(path)
            notOriginList = False
            break
        elif i == '-R':
            command.remove('-R')
            list = []
            getAllFilesRecursive(path,list,command)
            notOriginList = False
            break
        elif i == '-d':
            list = ['.']
            notOriginList = False
            break
    if notOriginList == True:
        list = os.listdir(path)
    ans = []
    for i in list:
        ans.append( each_ls(path,i))
    printFormatted(ans)
def getAllFilesRecursive(path,list,command):
    print(path + " : ")
    files = os.listdir(path)
    handle_ls(path,command)
    for f in files :
        fi_d = os.path.join(path,f)
        if os.path.isdir(fi_d):

            getAllFilesRecursive(fi_d,list,command)

def printFormatted(ans):    
    for a in ans:
        for i in a:
            print(i+'\t',end=' ')
        print('')

def just_ls():
    list = os.listdir()
    for i in list:
        print(i)

def each_ls(path,i):
    path = os.path.join(path,i)
    fileStats = os.lstat(path)
    ret =[]
    global flag_i
    global flag_l
    if flag_i == True:
        ret = ret + [str(fileStats.st_ino)]
    if flag_l == True:
        ret = ret + [
            filemode(fileStats.st_mode),
            str(fileStats.st_nlink),
            getpwuid(fileStats.st_uid).pw_name,
            getgrgid(fileStats.st_gid).gr_name,
            str(fileStats.st_size),
            formatted_time(fileStats.st_mtime),
        ]
    ret = ret + [i]
    return ret

def formatted_time(st_mtime):
    dt = datetime.datetime.fromtimestamp(st_mtime)
    return dt.strftime('%b %d %H:%M')
        
if __name__ == "__main__":
    command = [""]
    
    while 1:
        flag_i = False
        flag_l = False
        command = get_input()

        if(command[0]==""):
            continue
        if(command[0]=="ls"):
            setFlag(command)
            handle_ls(os.getcwd(),command)
        elif (command[0]=="wc"):
            wc(command[1:])
            pass
        elif( command[0]=='exit'):
            break
        else:
            print(command[0]+": command not found")