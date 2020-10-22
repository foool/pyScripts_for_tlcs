#_-_coding:utf-8_-_
#   Author: Qing
# Function: about tlc file , tlc function as a node, call graph, graph nodes, others
import os
import sys
import shutil
from tlc_utility import *
import time
from graphviz import Digraph, Graph

def print_the_whole_tree():
    pass



def print_tlc_functions(tlc_filename):
    ''' Print all tlc functions in this tlc file '''
    tlc_node = tlc_file(tlc_filename)
    print("  name:", tlc_node.get_name())
    print("----- functions -----")
    for fnode in tlc_node.get_fcn_node_list():
        count = 0
        print("T", fnode.get_name())
        for called_func_in_fnode in fnode.call_name_list:
            count = count+1
            print("L", count, " ", called_func_in_fnode)


def get_all_functions_and_locations():
    ''' Print all tlc functions and locations in MATLAB/Simulink '''
    rootdir_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c',\
    'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw']
    
    exclude_list = [] 
    '''['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\blocks', \
    'D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tornado']'''

    file_list = []
    function_list = []
    
    # get file list
    for rootdir in rootdir_list:
        for root, subFolders, files in os.walk(rootdir):
            #print(root)
            #print(subFolders)
            #print(files)
            if root in exclude_list:
                continue
            for filename in files:
                dirname = root.split('\\')[-1]
                if filename.endswith('tlc'):
                    filepath = os.path.join(root, filename)
                    dirandfile = dirname+'\n'+filename
                    file_list.append([filename, filepath, dirandfile])
    count = 1
    for each in file_list:
        #print(count, each)
        count += 1;
        #time.sleep(0.1)
    # get tlc files and tlc functions' lists
    for efile in file_list:
        tlc_node = tlc_file(efile[1])       # filepath
        for fnode in tlc_node.get_fcn_node_list():
            fnode_name = fnode.get_name()
            tlc_name = tlc_node.get_name()
            tlc_path = tlc_node.get_path()
            bfound = False
            for ii in range(0, len(function_list)):
                if fnode_name == function_list[ii]['func']:
                    function_list[ii]['tlc'].append((tlc_name, tlc_path))
                    True
                    break
            if bfound == False:         # not in the function list, append it
                dd = {'func': fnode_name, 'tlc': [(tlc_name, tlc_path)]}
                function_list.append(dd)

    
    # print the result
    with open("functions_and_locations.txt", 'w') as fp:
        for each in function_list:
            fp.write("--"+each['func']+'\n')
            if len(each['tlc']) > 1:
                for tt in each['tlc']:
                    fp.write("  ||=="+str(tt)+'\n')
            else:       #only one
                fp.write("   |--"+str(each['tlc'][0])+'\n')
            
            
    return (file_list, function_list)   



def print_file_called_tlc_functions(this_file_path, function_list):
    related_tlc_list = []
    if os.path.isfile(this_file_path) and os.access(this_file_path, os.R_OK):
        pass # the file exists and readable
    else:
        print("ERROR: Either the file is missing or not readable")
        return 
    tlc_node = tlc_file(this_file_path)
    print(tlc_node.get_name())
    fcn_nodes = tlc_node.get_fcn_node_list()
    for fnode in fcn_nodes:                     # each function in tlc file
        print("- - ", fnode.get_name())
        funcs_called = fnode.get_call_names()   # called functions by this func
        for called in funcs_called:
            print("    = = ",called)
            bfound = False
            for ii in range(len(function_list)):    # find in function_list
                if called.strip() in function_list[ii]['func']:
                    bfound = True
                    tlc_list = [tlc[1] for tlc in function_list[ii]['tlc']]
                    closest_idx = tlc_node.choose_cloest_tlc(tlc_list)
                    related_tlc_list.append(function_list[ii]['tlc'][closest_idx][0])
                    print("        ==>", tlc_list[closest_idx])
                    break
            if(bfound == False):
                print("function is >",called,"< cannnot find its location")
    related_tlc_list = list(set(related_tlc_list))
    print(">>>", related_tlc_list)
    
    
def ss_node(path):
    ss_path = path.replace(' ', '_').replace('\\', '_').replace(':', '_')
    return ss_path

def path_in_pathlist(path, path_list):
    for each in path_list:
        if os.path.samefile(path, each):
            return True
    return False

def main():
    if 0:
        path1 = 'D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\mw\\ertmainlib.tlc'
        #path1 = 'D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\mw\\codetemplatelib.tlc'
        print_tlc_functions(path1)
    if 0:
        (file_list, function_list) = get_all_functions_and_locations()
        print(" Files: ", len(file_list))
        print(" Funcs: ", len(function_list))
    if 0:
        (file_list, function_list) = get_all_functions_and_locations()
        path_test_list = [\
        'D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\public_api\\codegenentry.tlc', \
        ]
        for path in path_test_list:
            print_file_called_tlc_functions(path, function_list)
            print("------------------------------------------")
            time.sleep(3)
    if 0:
        ''' find test_file's subordinate tlc files '''
        path_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\', \
        'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\']
        sl = sltlc(path_list)
        count = 0
        '''
        for file in sl.get_file_list():
            print(count, file)
            count += 1
        print("total", count, "files")
        '''
        print("total",len(sl.get_function_list()),"functions")
        test_file = 'D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\mw\\bareboard_mrmain.tlc'
        called_files = sl.get_files_by_called_functions(test_file)
        for file in called_files:
            print(file)
        print("All", len(called_files), "subordinate files")
    if 0:
        ''' paint call graph by files can files related by call functions '''
        path_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\', \
        'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\']
        sl = sltlc(path_list)


        dot = Digraph(comment='The Round Table')        
        call_depth = 1
        my_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\mw\\commonthreadlib.tlc']
        my_file_list = []
        for ii in range(call_depth-1):
            for each in my_list:
                if os.path.isfile(each):
                    for sub_file in sl.get_files_by_called_functions(each):
                        my_list.append(os.path.realpath(sub_file[1]))   
                my_list = list(set(my_list))
        print(my_list)
        for each in my_list:
            if os.path.isdir(each):
                for root, subfolders, files in os.walk(each):
                    for filename in files:
                        if filename.endswith('tlc'):
                            filepath = os.path.join(root, filename)
                            my_file_list.append(filepath)
            if os.path.isfile(each):
                my_file_list.append(os.path.realpath(each))        
            
        
        # plot each tlc file as a node
        for file in my_file_list:
            # dot.node(node_id, node_name)
            dot.node(ss_node(file), os.path.basename(file))
          
        for filename in my_file_list:
            for sub_file in sl.get_files_by_called_functions(filename):
                if os.path.samefile(sub_file[1], filename):
                    continue    # edge to node-self
                #if path_in_pathlist(sub_file[1], my_file_list):
                #    dot.edge(ss_node(filename), ss_node(sub_file[1]))
                dot.edge(ss_node(filename), ss_node(sub_file[1]))


        dot.render('test-output/call_graph_byfuncs.gv', view=True)  
    if 0:
        path_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\', \
        'D:\\Program Files\\MATLAB\\R2020a\\toolbox\\rtw\\']

        for each in path_list:
            for root, subfolders, files in os.walk(each):
                print("--", root)
                for filename in files:
                    if filename.endswith('tlc'):
                        filepath = os.path.join(root, filename)
                        tlc_node = tlc_file(filepath)
                        print("= = = = ", tlc_node.get_name(), " = = = =")
                        print(tlc_node.get_file_description())
                        input()
    if 1:       
        path_list = ['D:\\Program Files\\MATLAB\\R2020a\\rtw\\c\\tlc\\mw']
        (file_list, function_list) = get_all_functions_and_locations()
        function_list = list(set([uu['func'] for uu in function_list]))
        with open('function_list.txt', 'w') as fp:
            for ff in function_list:
                if ff[:3] not in ['SLi', 'Lib', 'Fcn', 'RTM']:
                    continue
                fp.write(ff+'\n')

        
        
if __name__ == '__main__':
    main()
