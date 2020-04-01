# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 22:16:35 2020

@author: hill103
"""

"""
Windows下更改指定文件夹中（不包括子文件夹）所有文件的创建时间（Creation time）和修改时间（Modified time）为指定时间
文件的创建时间和修改时间会以1分钟为间隔递增
"""


import sys, os
from getopt import getopt
from time import time, mktime
import datetime
from natsort import natsorted
import pywintypes, win32file, win32con


def usage():
    '''对主函数进行简介
    '''
    print('''
python set_time.py [option][value]...
    -h or --help   "print this help infos"
    -i or --input  "folder for input，with absolute or relative path"
    -t or --time   "start time for the first file in the floder, with the format YYYY-MM-DD-HH-MM-SS"
''')


def changeFileCreationTime(fname, newtime):
    '''Windows下更改文件创建时间
    '''
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, None)

    winfile.close()
    

def changeTime(folder, start_time):
    '''更改文件夹中所有文件的创建时间和修改时间
    文件的创建时间和修改时间会以1分钟为间隔递增
    '''
    # 读入文件夹下所有文件，并naturally排序
    files = natsorted([os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

    # 更改每一个文件的时间
    for count, f in enumerate(files):
        this_time = start_time + datetime.timedelta(minutes=count)
        # 创建时间
        changeFileCreationTime(f, this_time)
        # 更改时间
        os.utime(f, (mktime(datetime.datetime.now().timetuple()), mktime(this_time.timetuple())))
    
    print('Time of total {:,} files are changed.'.format(len(files)))
    
    return True
   
    
#############主函数#####################################################################
# 如果没有任何参数，显示提示信息，并退出
if len(sys.argv) == 1:
    print('No options exist!')
    print('Use -h or --help for detailed help!')
    sys.exit(1)


# 定义命令行参数
# 短选项名后的冒号(:)表示该选项必须有附加的参数
# 长选项名后的等号(=)表示该选项必须有附加的参数
shortargs = 'hi:t:'
longargs = ['help', 'input=', 'time=']

# 解析命令行参数
# sys.argv[0]为python脚本名，后续全为参数
# opts为分析出的参数信息，args为不符合格式信息的剩余参数
opts, args = getopt(sys.argv[1:], shortargs, longargs)


# 如果存在不符合格式信息的剩余参数，显示提示信息，并退出
if args:
    print('Invalid options exist!')
    print('Use -h or --help for detailed help')
    sys.exit(1)

   
# 定义dict类型的参数集，使得算法更稳健
paramdict = {'input_folder':None, 'set_time':None}
 
for opt,val in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(1)
        
    if opt in ('-i', '--input'):
        if not os.path.isdir(val):
            # 输入不是一个确实存在的文件夹
            raise Exception('Invalid input folder!')
        # 采用realpath函数，获得真实绝对路径
        paramdict['input_folder'] = os.path.realpath(val)
        continue
    
    if opt in ('-t', '--time'):
        try:
            # 解析输入时间
            paramdict['set_time'] = datetime.datetime.strptime(val, '%Y-%m-%d-%H-%M-%S')
        except:
            raise Exception('Unsupported time format! You must use format YYYY-MM-DD-HH-MM-SS!')
        continue

# 检查参数是否齐全
for k,v in paramdict.items():
    if v is None:
        raise Exception('Option "{}" is missing!'.format(k))


# 调用分析函数
print('Input folder: "{}"'.format(paramdict['input_folder']))
print('Date time for first file: "{}"'.format(paramdict['set_time'].strftime('%Y-%m-%d %H:%M:%S')))

start_time = time()
changeTime(paramdict['input_folder'], paramdict['set_time'])
print('Elapsed time: {:.2f} seconds.'.format(time()-start_time))
