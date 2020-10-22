#_-_coding:utf-8_-_
#   Author: Qing
# Function: about tlc file , tlc function as a node, call graph, graph nodes, others
import os
import re
import traceback
import shutil

BI_functions = ["ADD_CUSTOM_SECTION", "ADD_CUSTOM_SECTION_CONTENT", \
"APPEND_MISSING_TOKENS", "CAST", "CGMODEL_ACCESS", "CLEAR_FILE_BUFFERS", \
"CLEAR_FILE_SECTION", "CLEAR_TYPE_LIMIT_ID_REPLACEMENT_MAP", \
"CREATE_SOURCE_FILE", "EXISTS", "FEATURE", "FEVAL", "FIELDNAMES", \
"FILE_EXISTS", "GENERATE", "GENERATE_FORMATTED_VALUE", \
"GENERATE_FUNCTION_EXISTS", "GENERATE_TYPE", \
"GENERATE_TYPE_FUNCTION_EXISTS", "GET_CUSTOM_SECTION_CONTENT", \
"GET_FILE_ATTRIBUTE", "GET_FILE_REP_SCRATCH_BUFFER_CONTENTS", \
"GET_TYPE_ID_REPLACEMENT", "GETFIELD", "IDNUM", "IMAG", "IS_CUSTOM_SECTION", \
"ISEMPTY", "ISEQUAL", "ISFIELD", "ISFINITE", "ISINF", "ISNAN", "ISSLDATAREF", \
"NEEDS_COMMENT", "NEEDS_PAREN", "NUM_SOURCE_FILES", "REAL", "REMOVEFIELD", \
"ROLL_ITERATIONS", "SET_CUSTOM_SECTION_TOKEN_IN_USE", "SET_FILE_ATTRIBUTE", \
"SET_TYPE_LIMIT_ID_REPLACEMENT_MAP", "SETFIELD", "SIZE", "SOURCE_FILE_EXISTS", \
"SPRINTF", "STRING", "STRINGOF", "SYSNAME", "TYPE", "UNLOAD_GENERATE_TYPE", \
"WHITE_SPACE", "WILL_ROLL", "WRITE_FILE_SECTION"]

BI_functions = BI_functions + ["if", "else", 'case', 'switch', 'with', 'for',\
'while', 'assert', 'which', 'error', 'elseif', 'gainScalar', 'sizeof', 'return', \
'void', 'char', ]
#which is not defined

### Class gnode
class gnode(object):
    def __init__(self, param):
        self._tlc_file_ = ''
        self._fcn_node_ = ''
        self._uname_ = ''
        self.to_nodes = []
        self.from_nodes = []
        if 'tlc_file' in param:
            self._tlc_file_ = param['tlc_file']
        if 'fcn_node' in param:
            self._fcn_node_ = param['fcn_node']
            self._uname_ = param['fcn_node'].get_name()
        if 'uname' in param:
            self._uname_ = param['uname']
        if self._uname_ == '':
            print("Error: fail to init a gnode, init parameter:")
            if 'tlc_file' in param:
                print("tlc_file:", param['tlc_file'].get_path())
            if 'fcn_node' in param:
                print("fcn_node:", param['fcn_node'].get_name())
                print(self._uname_)
            print(param)
            return None
    
    def get_tlcfile(self):
        if self.isnull(self._tlc_file_):
            return False
        return self._tlc_file_
        
    def get_fcnnode(self):
        if self.isnull(self._fcn_node_):
            return False
        return self._fcn_node_
        
    def get_uname(self):
        if self.isnull(self._uname_):
            return False
        return self._uname_
    
    def set_tlcfile(self, tlc_file):
        self.update_tlcfile(tlc_file)
        
    def set_fcnnode(self, fcn_node):
        set.update_fcnnode(fcn_node)
    
    def isnull(self, arg):
        if arg == False:
            return True
        if isinstance(arg, str):
            if arg == '':
                return True
            else:
                return False
        if arg.__class__.__name__ not in self.__dict__:    # if arg is not an attribute
            return False
            print("Warning: %s has no value %s"%(type(self), type(arg)))
        return False
        
    def update_tlcfile(self, tlc_file):
        if self.isnull(self._tlc_file_):
            self._tlc_file_ = tlc_file
        else:
            print("Warning: fail to update the non-null tlc_file of a gnode!")
            return False
    
    def update_fcnnode(self, fcn_node):
        if self.isnull(self._fcn_node_):
            self._fcn_node_ = fcn_node
            self.uname = fcn_node.get_name()
        else:
            print("Warning: fail to update the non-null fcn_node of a gnode!")
            return False
        
    def update_from_gnode(self, gnode_ext):
        '''update attrs from the same node'''
        if self.get_tlcfile() == False:
            if gnode_ext.get_tlcfile() != False:
                pass
            else:
                self.update_tlcfile(gnode_ext.get_tlcfile())
        elif gnode_ext.isnull(gnode_ext.get_tlcfile()):
            pass        # do nothing if ext. gnode have empty tlc file
        else:            
            if self.get_tlcfile().isidentical(gnode_ext.get_tlcfile()):
                return True
            else:        # inconsistent values of two nodes
                print("Contradictory gnodes' tlc_file value, to be seen as the same gnode")
                print(self.get_fcnnode().get_name(), '    ', gnode_ext.get_fcnnode().get_name())
                print(self.get_fcnnode().get_path(), '    ', gnode_ext.get_fcnnode().get_path())
                print(self.get_uname(), '    ', gnode_ext.get_uname())
                print('-------------')
        if self.get_fcnnode() == False:
            if gnode_ext.get_fcnnode() == False:
                pass
            else:
                self.update_fcnnode(gnode_ext.get_fcnnode())
        elif gnode_ext.isnull(gnode_ext.get_fcnnode()):
            pass        # do nothing if ext. gnode have empty tlc file
        else:            
                
            if    self.get_fcnnode().isidentical(gnode_ext.get_fcnnode()): 
                return True
            else:    # inconsistent values of two nodes
                print("Contradictory gnodes' tlc_file value, to be seen as the same gnode")
                print(self.get_fcnnode().get_name(), '    ', gnode_ext.get_fcnnode().get_name())
                print(self.get_fcnnode().get_path(), '    ', gnode_ext.get_fcnnode().get_path())
                print(self.get_uname(), '    ', gnode_ext.get_uname())
                print('-------------')
                return False
        # unnecessary to update uname
        return True
    
    def update_from_to(self, from_nodes=[], to_nodes=[]):
        self.from_nodes += from_nodes
        self.to_nodes += to_nodes
        

### Class call_graph
class call_graph(object):
    def __init__(self):
        self._gnode_list_ = []
        self._call_graph_ = []
    
    def __node__(self, gnode_ext):
        # return the node in call_graph mostly like gnode_ext , if not, create a new one.
        if self.isnodein(gnode_ext):
            return gnode_ext
        for ii in range(len(self._gnode_list_)):
            if self._gnode_list_[ii].get_uname() == gnode_ext.get_uname():    # same gnode ?
                if False == self._gnode_list_[ii].update_from_gnode(gnode_ext):
                    print("Error: fail to update a existing gnode in call_graph!")
                return self._gnode_list_[ii]
        # new gnode
        self._gnode_list_.append(gnode_ext)
        return gnode_ext
    
    def get_gnode_list(self):
        return self._gnode_list_
        
    def get_call_graph(self):
        return self._call_graph_
        
    def _isnodein_deep_(self, gnode_ext):
        for ii in range(len(self._gnode_list_)):
            if self._gnode_list_[ii].get_uname() == gnode_ext.get_uname():    # same gnode ?
                if False == self._gnode_list_[ii].update_from_gnode(gnode_ext):
                    print("Error: fail to update a existing gnode in call_graph!")
                return True
        return False
        
    def isnodein(self, gnode_ext):
        ''' is gnode_ext in the call graph '''
        if gnode_ext in self._gnode_list_:
            return True
        else: 
            if self._isnodein_deep_(gnode_ext):
                return True
            else:
                return False
        
    def isdirected(self, from_node, to_node):
        if self.isnodein(from_node):
            return False
        if self.isnodein(to_node):
            return False
        if (from_node.get_uname(), to_node.get_uname()) in \
        [(xx.get_uname, yy.get_uname) for (xx, yy) in self._call_graph_]:
            return True
        else:
            return False
    
    def add_connection(self, from_node, to_node):
        #todo : advanced node_in_list judgement 
        gfrom_node = self.__node__(from_node)
        gto_node = self.__node__(to_node)
        if (gfrom_node, gto_node) not in self._call_graph_:
            self._call_graph_.append((gfrom_node, gto_node))
    
    def rm_connection(self, from_node, to_node):
        gfrom_node = self.__node__(from_node)
        gto_node = self.__node__(to_node)
        if (gfrom_node, gto_node) in self._call_graph_:
            self._call_graph_.remove((gfrom_node, gto_node))
    
    def add_connection_from_tlcfile(self, tlc_file):
        for fcn_node in tlc_file.get_fcn_node_list():
            for fcn_name in fcn_node.get_call_names():
                if fcn_name in tlc_file.get_fcn_name_list():
                    # fcn_node in the same tlc file
                    to_fcn_node = tlc_file.get_fcn_by_name(fcn_name)    #not False
                    from_gnode = gnode({'tlc_file':tlc_file, 'fcn_node':fcn_node})
                    to_gnode = gnode({'tlc_file':tlc_file, 'fcn_node':to_fcn_node})
                else:    # fcn outof this tlc file
                    from_gnode = gnode({'tlc_file':tlc_file, 'fcn_node':fcn_node})
                    to_gnode = gnode({'uname': fcn_name})
                self.add_connection(from_gnode, to_gnode)
                
### simulink tlc system object
class sltlc(object):
    def __init__(self, tlc_dir_list):
        ''' init with dirs that contains tlc files '''
        ''' recommand dirs: <MATLAB_ROOT>/rtw <MATLAB_ROOT>/toolbox '''
        self.tlc_file_list = []
        self.tlc_function_list = []
        self.exclude_dirs = []
        # find each tlc files under the tlc_dir_list
        for rootdir in tlc_dir_list:
            for root, subfolders, files  in os.walk(rootdir):
                if root in self.exclude_dirs:
                    continue
                for filename in files:
                    dirname = root.split('\\')[-1]
                    if filename.endswith('tlc'):
                        ''' if it is a tlc file '''
                        filepath = os.path.join(root, filename)
                        dirandfile = dirname+'\n'+filename
                        # filename, filename_full, lastdir+name
                        self.tlc_file_list.append([filename, filepath, dirandfile])
        
        # find all tlc functions of all tlc files
        for efile in self.tlc_file_list:
            tlc_node = tlc_file(efile[1])   # init a tlc node with full filename
            for fnode in tlc_node.get_fcn_node_list():
                fnode_name = fnode.get_name()
                tlc_name = tlc_node.get_name()
                tlc_path = tlc_node.get_path()
                bfound = False
                for ii in range(0, len(self.tlc_function_list)):
                    if fnode_name == self.tlc_function_list[ii]['func']:
                        self.tlc_function_list[ii]['tlc'].append((tlc_name, tlc_path))
                        bfound = True
                        break
                if bfound == False:
                    dd = {'func': fnode_name, 'tlc': [(tlc_name, tlc_path)]}
                    self.tlc_function_list.append(dd)
        '''tlc_function_list is a list of all tlc functions in simulink
        each item is a dictionary with 'func' KV & 'tlc' KV,
        'tlc' value is tuple of ( tlc_filename, tlc_full_filename )
        '''
    
    def get_files_by_called_functions(self, tlc_file_path):
        ''' Find all called functions in tlc_file_path,
        return the tlc files that contains these called functions'''
        ret_file_list = []
        if os.path.isfile(tlc_file_path) and os.access(tlc_file_path, os.R_OK):
            pass # the file exists and readable
        else:
            print("ERROR: Either ", tlc_file_path, " is missing or not readable")
            return 
        tlc_node = tlc_file(tlc_file_path)
        fcn_nodes = tlc_node.get_fcn_node_list()
        for fnode in fcn_nodes:
            # for each function in the tlc file
            funcs_called = fnode.get_call_names()   
            #print(funcs_called)
            for called in funcs_called:
                bfound = False
                for ii in range(len(self.tlc_function_list)):    
                    if called.strip() in self.tlc_function_list[ii]['func']:
                        bfound = True
                        tlc_list = [tlc[1] for tlc in self.tlc_function_list[ii]['tlc']]
                        closest_idx = tlc_node.choose_cloest_tlc(tlc_list)
                        ret_file_list.append(self.tlc_function_list[ii]['tlc'][closest_idx])
                        break
                if(bfound == False):
                    print("ERROR: function is >",called,"< cannnot find its location")
        ret_file_list = list(set(ret_file_list))
        # return is a list of tuple (filename, full_filename)
        return ret_file_list
        
    def get_file_list(self):
        ''' get all tlc files '''
        ''' each item is a tuple of (filename, filename_full, lastdir+name) '''
        return self.tlc_file_list
        
    def get_function_list(self):
        ''' get all functions in tlc files '''     
        return self.tlc_function_list
        


### Class tlc_file represents a .tlc file
class tlc_file(object):
    def __init__(self, tlc_path):
        ''' init a tlc_file with file path(tlc_path) '''
        if os.path.isfile(tlc_path) and os.access(tlc_path, os.R_OK):
            pass # the file exists and readable
        else:
            print("ERROR: Either the file is missing or not readable")
            return 
        self.content_raw = ''
        self.path = os.path.realpath(tlc_path).strip()
        self.filename = os.path.basename(self.path).strip()
        self.fcn_node_list = []
        self.file_description = ''    # description before any function or tlc sentences
        if self.__parse__() == False:
            print("ERROR: fail to init ", tlc_path)
        
    def __parse__(self):
        '''try to read from tlc filepath & parse '''
        try:
            with open(self.path, 'r') as f:
                self.content_raw = f.read()
        except:
            print("read file %s error!" % self.path)
            traceback.print_exc()
            exit()
        self.__parse_content__()
        
    def __parse_content__(self):
        '''parse the content in the tlc file(self.content_raw) '''
        fcn_part_list = []
        is_file_discription = True
        for line in self.content_raw.split('\n'):
            cline = line.strip()
            if is_file_discription:
                if cline.startswith('%%') or cline == '':
                    if cline == '' or cline == '%%' or cline.startswith('%% Copyright '):
                        continue
                    else:
                        self.file_description += cline+'\n'
                else:
                    is_file_discription = False    # executing the following 
            if cline.startswith('%function'):
                fcn_part_list = []
                fcn_part_list.append(cline)
            elif cline.startswith('%endfunction'):
                fcn_part_list.append(cline)
                fcn_raw = '\n'.join(fcn_part_list)
                ''' parse each function node '''
                self.fcn_node_list.append(fcn_node(self, fcn_raw))
                fcn_part_list = []
            else:
                fcn_part_list.append(cline)        
    
    def get_name(self):
        ''' return tlc_file name '''
        return self.filename
    
    def isidentical(self, ob):
        ''' if ob has the same type and value, 
            then they are identical '''
        if self.__class__.__name__ == ob.__class__.__name__:
            if self.get_path() == ob.get_path():
                return True
        return False
    
    def isnull(self, arg):
        if arg == False:
            return True
        if isinstance(arg, str):
            if arg == '':
                return True
            else:
                return False
        if arg.__class__.__name__ not in self.__dict__:    # if arg is not an attribute
            return False
            print("Warning: %s has no value %s"%(type(self), type(arg)))
        return False
        
    def get_file_description(self):
        return self.file_description
        
    def get_fcn_node_list(self):
        return self.fcn_node_list
        
    def get_fcn_name_list(self):
        return [x.get_name for x in self.fcn_node_list]
            
    def get_path(self):
        return self.path
        
    def isin_fcn_node(self, fcn):
        fcn_name_list = [x.get_name() for x in self.fcn_node_list]
        if isinstance(fcn, str):
            if fcn in fcn_name_list:
                return True
            else:
                return False
        elif isinstance(fcn, fcn_node):
            if fcn.filepath == self.path and fcn.get_name in fcn_name_list:
                return True
            else:
                return False
        else:
            print(">>Error: unsupported type: ", type(fcn))
            
    def get_fcn_by_name(self, fcn_name):
        ''' return fcn_node object by fcn_name '''
        for fcn_node in self.fcn_node_list:
            if fcn_name == fcn_node.get_name():
                return fcn_node
        return False
        
    def isin_by_fcn_name(self, fcn_name):
        ''' is this function(by name) in the tlc file '''
        if fcn_name in [n.get_name() for n in self.fcn_node_list]:
            return True
        else:
            return False
        
    def print_inside_call_tree(self):
        print("+ %s" % self.filename)
        for fcn_node in self.fcn_node_list:
            print("|-- %s"%fcn_node.get_name())
            for fcn_name in fcn_node.get_call_names():
                if self.isin_by_fcn_name(fcn_name):
                    print("|   |--%s (in )"%fcn_name)
                else:
                    print("|   |--%s (out)"%fcn_name)
        print("L--------------------------------")
                    
    def choose_cloest_tlc(self, tlc_list):
        len_common_prefix = [0]*len(tlc_list)
        for ii in range(len(tlc_list)):
            tlc = tlc_list[ii]
            if os.path.isfile(tlc) and os.access(tlc, os.R_OK):
                pass # the file exists and readable
            else:
                print("ERROR: Either", tlc ," is missing or not readable")
                return 
            tlc_realpath = os.path.realpath(tlc)
            len_common_prefix[ii] = os.path.commonprefix([tlc_realpath, self.get_name()])
        # return the ii of the longest common prefix path
        if len_common_prefix == []:
            print("Error")
            exit()
        return len_common_prefix.index(max(len_common_prefix))
    
    
### Class fcn_node
class fcn_node(object):
    ''' init function node by this raw content'''
    def __init__(self, tlc_file, fcn_raw):
        self.owner = tlc_file                    # tlc file belonged to
        self.filepath = tlc_file.get_path()        # tlc filepath
        self.name = ''                            # function name
        self.call_name_list = []                # function names called by this function
        self.__parse__(fcn_raw)
    
    def __parse__(self, fcn_raw):
        '''parse the content of a function'''
        infcn = False
        for line in fcn_raw.split('\n'):
            if(infcn == False):
                ret = re.findall('\%function\ +([A-Z|a-z|0-9|_]+)\ {0,99}[\(|\ +\.\.\.]', line)
                if(len(ret) > 0):
                    self.name = ret[0].strip()            # get name
                    infcn = True
                    continue
                else:
                    print("Can't find function name from this line")
                    print(line)
                    print(self.owner.get_path())
                    print("------------- fcn_node content -------------")
                    print(fcn_raw)
                    print("------------- fcn_node content -------------")
                    exit()
            if self.name == '' or self.owner.get_path() == '':
                print(fcn_raw)
                exit()
            if re.match(r'^[ ]{0,100}\%[a-zA-Z_<-]+', line) != None:
                # find call functions in lines that begin with %,
                fcn_call_list_line = re.findall('([A-Za-z0-9_]+)\ {0,99}\(', line)
                for fcn in fcn_call_list_line:
                    function_name = fcn.strip()
                    if function_name in BI_functions:
                        continue
                    self.add_call_fcn(function_name)        # add function called
            else:
                pass

    def isidentical(self, ob):
        # same type with the same value
        if self.__class__.__name__ == ob.__class__.__name__:
            if self.get_filepath() == ob.get_filepath():
                if self.get_name() == ob.get_name():
                    return True
        return False

    def isnull(self, arg):
        if arg == False:
            return True
        if isinstance(arg, str):
            if arg == '':
                return True
            else:
                return False
        if arg.__class__.__name__ not in self.__dict__:    # if arg is not an attribute
            return False
            print("Warning: %s has no value %s"%(type(self), type(arg)))
        return False
        
    def get_name(self):
        return self.name
        
    def get_filepath(self):
        return self.filepath
        
    def set_name(self, new_name):
        self.name = new_name.strip()
        return True
        
    def add_call_fcn(self, name_call_fcn):
        if name_call_fcn in self.call_name_list:
            return False
        elif name_call_fcn == self.name:
            return False
        else:
            self.call_name_list.append(name_call_fcn)
            return True
        
    def get_call_names(self):
        return self.call_name_list
        
