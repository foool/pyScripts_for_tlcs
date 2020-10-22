#_-_coding:utf-8_-_
#   Author: Qing
# Function: backup tlc files, add contents begore any functions in all tlc files

import os
import sys
import shutil
import re


def backup_all_tlc():
    rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c',\
    'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw']
        
    #   backup all *.tlc files to *.tlc.bklq files locally
    for rootdir in rootdir_list:
        for root, subFolders, files in os.walk(rootdir):
            for filename in files:
                dirname = root.split('\\')[-1]
                filename_new = filename+'.bklq'
                if filename.endswith('tlc'):
                    filepath = os.path.join(root, filename)
                    filepath_to = os.path.join(root, filename_new)
                    shutil.copyfile(filepath, filepath_to)
    
def restore_all_tlc():
    rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c',\
    'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw']
        
    #   restore all *.tlc.bklq files to *.tlc files locally
    for rootdir in rootdir_list:
        for root, subFolders, files in os.walk(rootdir):
            for filename in files:
                if filename.endswith('bklq'):
                    filepath = os.path.join(root, filename)
                    shutil.copyfile(filepath, filepath[:-5])

def insert_into_tlc():
    rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c',\
    'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw']
        
    content_ins_raw = '%selectfile STDOUT\n+++'
    
    #  for each *.tlc file, insert content_ins into each file
    for rootdir in rootdir_list:
        for root, subFolders, files in os.walk(rootdir):
            for filename in files:
                if filename.endswith('tlc'):
                    #insert contents to this file (filename)
                    filepath = os.path.join(root, filename)
                    contents = ''
                    with open(filepath, 'r') as fp:
                        contents = fp.readlines()
                    content_ins = content_ins_raw+filename+'\n%closefile STDOUT\n'
                    is_write = False
                    for ii in range(0, len(contents)):
                        if re.match(r'^[\* ]{0,100}\%\%', contents[ii]) != None:
                            continue
                        else:
                            contents.insert(ii, content_ins)
                            is_write = True
                            break
                    if is_write != True:
                        print("<><><>", filepath ,"is not written!\n")
                    contents = "".join(contents)
                    contents += '\n%selectfile STDOUT\n---'+filename+'\n%closefile STDOUT\n'
                    with open(filepath, 'w') as fp:
                        fp.write(contents)
                        

def main():
    if 1:
        #backup_all_tlc()
        restore_all_tlc()
        #insert_into_tlc()
    


if __name__ == '__main__':
    main()
