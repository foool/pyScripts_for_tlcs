#_*_encoding:utf-8_*_
import os
import sys
import shutil
from graphviz import Digraph, Graph
import time
import re

 
#rootdir_list = ['C:\\Program Files\\MATLAB\\R2019a\\toolbox',
#'C:\\Program Files\\MATLAB\\R2019a\\rtw']

'''
rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\', \
'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw\\targets\\common\\', \
'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw\\targets\\ecoder\\', \
'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw\\rtw']
'''
rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\', \
'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\']


filename_list = []

for rootdir in rootdir_list:
    for root, subFolders, files in os.walk(rootdir):
        #print(root)
        #print(subFolders)
        #print(files)
        for filename in files:
            dirname = root.split('\\')[-1]
            if filename.endswith('tlc'):
                filepath = os.path.join(root, filename)
                dirandfile = dirname+'\n'+filename
                filename_list.append([filename, filepath, dirandfile])

'''
for each in filename_list:
    for other in filename_list:
        if each == other:
            continue
        else:
            if each[0] == other[0]:
                print(each);
                print(other)
'''
#for each in filename_list:
#    print(each)

dot = Digraph('structs', engine='dot')
dot.graph_attr['rankdir'] = 'LR'
dot.graph_attr['splines'] = 'ortho'
dot.node_attr['shape'] = 'box'
dot.graph_attr['epsilon'] = '0.01'
dot.graph_attr['overlap'] = 'false'
call_dic = {}
for each in filename_list:
    filename_without_postfix = each[0][:-4]
    
    filepath = each[1]
    print(filepath)
    
    # find all tlc files included in filepath
    with open(filepath, 'r', encoding="utf-8") as fp:
        try:
            all_include_tlcs = re.findall('\%include\ +\S+\.tlc', fp.read())
        except UnicodeDecodeError:
            continue
    if len(all_include_tlcs) > 0:
        call_dic[filename_without_postfix] =  []
    for tlc_raw in all_include_tlcs:
        tlc_ = re.findall('([a-zA-Z0-9_-]+)\.tlc', tlc_raw)
        if tlc_:
            call_dic[filename_without_postfix].append(tlc_[0])

# all included tlc files in the becalled_list
becalled_list = []
for kk in call_dic:
    becalled_list += call_dic[kk]


print("---------------------------")
print(call_dic)

            
for tlc_file in call_dic:
    inc_list = call_dic[tlc_file]
    combined_node = ''
    for inc_file in inc_list:
        if inc_file in call_dic:
            dot.edge(tlc_file, inc_file)
        else:   # inc_file not calling others
            if becalled_list.count(inc_file) > 1:
                dot.edge(tlc_file, inc_file)    # inc_file is called by other tlc_file
            else:
                combined_node += inc_file+'\n'
    if combined_node != '':
        combined_node = combined_node[:-1]
        dot.edge(tlc_file, combined_node)
 
''' 
for each in filename_list:
    filename_without_postfix = each[0][:-4]
    if filename_without_postfix in becalled_list:
        continue
    else:
        dot.node(filename_without_postfix, filename_without_postfix)
'''
         
dot.attr(arrowhead='vee', arrowsize='4')
dot.render('test-output/round-table3.gv', view=True)  
#use gvedit to generate png file







