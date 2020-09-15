#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2020, Ziyu Tao


import os
from functools import reduce
import re

from util.units import Unit,Value
from util.sweeptools import RangeCreator

unitSpace = ('V', 'mV', 'us', 'ns', 'GHz', 'MHz', 'dBm', 'rad')
V, mV, us, ns, GHz, MHz, dBm, rad = [Unit(s) for s in unitSpace]

ar = RangeCreator()



def MatchString(string):
    string_new = None
    
    # if the string is in python expression
    try:
        eval(string)
    except:pass
    else:
        string_new = eval(string)
        return string_new
    
    # Now, the string is not a python expression
    # If it has Units
    
    def space_repl(matchobj):
        g0 = matchobj.group()
        unitSpace = ('V', 'mV', 'us', 'ns', 'GHz', 'MHz', 'dBm', 'rad')
        if any([u in g0 for u in unitSpace]) and g0 is not None:
            return g0.replace(' ','*')
        else:
            return g0
    try:
        string1 = re.sub('\-?[0-9]+(\.[0-9]*)?\s[A-Za-z]*', space_repl,string)
        eval(string1)
    except:pass
    else:
        string1 = re.sub('\-?[0-9]+(\.[0-9]*)?\s[A-Za-z]*', space_repl,string)
        string_new = eval(string1)
        return string_new
        
    # If the type is not considered, return None
    if string_new == None:
        print(string)
        print('Registry Type error, use default value')
    return string_new
    
    
class AttrDict(dict):
    """A dict whose entries can also be accessed as attributes.
    
    The copy method returns a copy, including recursive copies of
    any sub directories as AttrDict's.  Note that mutable values of
    other types, such as lists, are not copied.
    
    The where method returns a copy with updates passed as a dictionary
    or keyword parameters.  This also allows updates to be made to
    keys in subdirectories by passing dotted names (or, when using
    keyword parameters, by using '__' in place of '.').
    """
    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        dict.__setitem__(self, name, value)
    
    def __delattr__(self, name):
        try:
            dict.__delitem__(self, name)
        except KeyError:
            raise AttributeError(name)
    
    def copy(self):
        d = AttrDict(self)
        object.__setattr__(d, '_dir', self._dir)
        object.__setattr__(d, '__name__', self.__name__)
        for k, v in d.iteritems():
            if isinstance(v, AttrDict):
                d[k] = v.copy()
        return d
    
    def where(self, dict={}, **kwds):
        d = self.copy()
        def add_all(updates):
            for k, v in updates.iteritems():
                k = k.replace('__', '.')
                if '.' in k:
                    path = k.split('.')
                    path, k = path[:-1], path[-1]
                    subdir = d
                    for dir in path:
                        subdir = subdir[dir]
                    subdir[k] = v
                else: # just set the key
                    d[k] = v
        add_all(dict)
        add_all(kwds)
        return d

class RegistryWrapper(object):
    def __init__(self, dir=''):
        if isinstance(dir, str):
            dir = [dir]
        else:
            dir = list(dir)
        object.__setattr__(self, '_dir', dir)
        
        # 'registry\\xxx.dir\\xxx.dir'
        dir2 = [dir[0]] + [d+'.dir' for d in dir[1:]]
        dir_path = reduce(os.path.join,dir2)
        object.__setattr__(self, '_path', dir_path)
        
    def _subdir(self, name):
        """Create a wrapper for a subdirectory"""
        if name == '':
            raise Exception('Empty string is invalid subdirectory name')
        return RegistryWrapper(self._dir + [name])
    
    def _send(self,path,value):
        """Change back into the root directory after each request."""
        f=open(path,"w")
        if type(value) is str:
            v_write = "'{0}'".format(value)
        else:
            v_write = str(value)
        f.write(v_write)
        f.close()
    
    def _get_list(self):
        """Get current directory dirs and keys."""
        dirs,keys = [],[]
        d_list = (fn for fn in os.listdir(self._path) if fn.endswith('.dir'))
        k_list = (fn for fn in os.listdir(self._path) if fn.endswith('.key'))
        for d in d_list:
            dirs.append(os.path.splitext(d)[0])
        for k in k_list:
            keys.append(os.path.splitext(k)[0])
        return dirs,keys
    
    def _get_value(self,key):
        """get the value of a key"""
        f_open = open(os.path.join(self._path,key+'.key'))
        value0 = f_open.read().strip().replace("'", '"')
        f_open.close()
                
        # transfer from .str to float/string/list...
        value = MatchString(value0)
        return value
    
    ## dict interface
    def __getitem__(self, name):
        dirs, keys = self._get_list()
        if name in dirs:
            return self._subdir(name)
        elif name in keys:
            return self._get_value(name)
        else:
            raise KeyError(name)
            
    def __setitem__(self, name, value):
        dirs, keys = self._get_list()
        if name in dirs:
            pass
        elif name in keys:
            """Change back into the root directory after each request."""
            self._send(self._path+'//'+name+'.key',value)

    ## attribute interface
    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)
        
    def copy(self):
        """Make a local copy, recursively copying subdirs as well."""
        dirs, keys = self._get_list()
        d = AttrDict()
        object.__setattr__(d, '_dir', self._dir)
        object.__setattr__(d, '__name__', self._dir[-1])
        for name in dirs:
            d[name] = self._subdir(name).copy()
        if len(keys):
            for name in keys:
                d[name] = self[name]
        return d
        
        
def loadQubits(write_access=False):
    """Get local copies of the sample configuration stored in the registry.
    
    Returns the local sample config, and also extracts the individual
    qubit configurations, as specified by the sample['config'] list.  If
    write_access is True, also returns the qubit registry wrappers themselves,
    so that updates can be saved back into the registry.
    """
    
    userPath = r'Registry'
    user = 'Ziyu'
    reg = RegistryWrapper(userPath)
    reg = reg[user]
    sample = reg[reg['sample'][0]]
    
    
    Qubits = [sample[q] for q in sample['config']]
    sample_copy = sample.copy()
    qubits = [sample_copy[q] for q in sample_copy['config']]
    
    # only return original qubit objects if requested
    if write_access:
        return sample, qubits, Qubits
    else:
        return sample, qubits
    


# sample, qubits = loadQubits(write_access=False)





