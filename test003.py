#_-_coding:utf-8_-_
#   Author: Qing
# Function: about tlc file , tlc function as a node, call graph, graph nodes, others
import os
import sys
import shutil
from tlc_utility import *
import time
from graphviz import Digraph, Graph

# input : <prog> file1 file2 ...
# output : function call graph of these files


fileList = ['D:\\Program Files\\MATLAB\R2020a\\rtw\\c\\tlc\\mw\\rtmdldefs.tlc', 
            'D:\\Program Files\\MATLAB\R2020a\\rtw\\c\\tlc\\mw\\rtmdllib.tlc', 
            'D:\\Program Files\\MATLAB\R2020a\\rtw\\c\\tlc\\mw\\rtmdllib_obs.tlc', 
            'D:\\Program Files\\MATLAB\R2020a\\rtw\\c\\tlc\\mw\\rtmdlsuplib.tlc']

def main():
    fcnList = []
    localFcnList = []
    for filePath in fileList:
        filename = filePath.split('\\')[-1]
        tlcFileNode = tlc_file(filePath)
        for fnode in tlcFileNode.get_fcn_node_list():
            fcnList.append((fnode.get_name(), fnode.get_call_names(), filename))
            localFcnList.append(fnode.get_name())
    for rec in fcnList:
        print(rec)

    # print call_graph
    dot = Digraph('structs', engine='dot')
    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr['splines'] = 'ortho'
    dot.node_attr['shape'] = 'box'
    dot.graph_attr['epsilon'] = '0.01'
    dot.graph_attr['overlap'] = 'false'
    for rec in fcnList:
        fcnIn = rec[0]
        for fcnOut in rec[1]:
            if fcnOut in localFcnList:
                dot.edge(fcnIn, fcnOut)
                
    dot.attr(arrowhead='vee', arrowsize='4')
    dot.render('test-output/rtmdl_callGraph.gv', view=True)  
        
if __name__ == '__main__':
    main()
