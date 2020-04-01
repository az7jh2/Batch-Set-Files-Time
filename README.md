# Batch-Set-Files-Time
Windows下批量更改指定文件夹中（不包括子文件夹）所有文件的创建时间（Creation time）和修改时间（Modified time）为指定时间，并且文件的创建时间和修改时间会以1分钟为间隔递增

## Feature
1. 用于Windows
2. 文件夹**不**包括子文件夹
3. 修改**创建时间**（**Creation time**）和**修改时间**（**Modified time**）
4. 时间会以**1分钟**为间隔递增

## Needed Packages
* 使用[natsort](https://github.com/SethMMorton/natsort)来对所有文件名自然排序
* 使用[pywintypes](https://github.com/mhammond/pywin32)来修改windows文件的创建时间
* 使用[os.utime](https://docs.python.org/3/library/os.html)来修改windows文件的修改时间

## Usage
```bash
python set_time.py [option][value]...
    -h or --help
    -i or --input  "folder for input，with absolute or relative path"
    -t or --time   "start time for the first file in the floder, with the format YYYY-MM-DD-HH-MM-SS"
```
