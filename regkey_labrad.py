#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2020, Ziyu Tao


import os
from functools import reduce
import re

# from util.units import Unit,Value
from util.sweeptools import RangeCreator
from labrad.units import Unit,Value

_unitSpace = ('V', 'mV', 'us', 'ns', 'GHz', 'MHz','kHz','Hz', 'dBm', 'rad','None')
V, mV, us, ns, GHz, MHz,kHz,Hz,dBm, rad,_l  = [Unit(s) for s in _unitSpace]

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
        if any([u in g0 for u in _unitSpace]) and g0 is not None:
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
    """Accesses the labrad registry with a dict-like interface.
    
    Keys or directories in the registry can be accesed using either
    dict-like notation d["key"] or attribute access d.key.  Obviously
    the former is required if you want to compute the string name of
    an element to access and then pass the key as a variable.
    
    For every packet that gets sent to the registry, we first cd
    into the directory wrapped by this wrapper, then at the end
    cd back into the root directory.  That way this directory
    (and any subdirectories that we visit which get wrapped) can
    always be deleted because there is not a stray context hanging
    out in any particular directory.
    
    The copy method returns a local copy of this registry directory,
    including recursive copies of all subdirectories. 
    """
    def __init__(self, cxn, dir='', ctx=None):
        if isinstance(dir, str):
            dir = [dir]
        else:
            dir = list(dir)
        if '' in dir[1:]:
            raise Exception('Empty string is invalid subdirectory name')
        if dir[0] != '':
            dir = [''] + dir
        if ctx is None:
            ctx = cxn.context()
        srv = cxn.registry
            
        object.__setattr__(self, '_dir', dir)
        object.__setattr__(self, '_cxn', cxn)
        object.__setattr__(self, '_srv', srv)
        object.__setattr__(self, '_ctx', ctx)
        
        # make sure the directory gets created
        self._send(self._packet())
        
    def _subdir(self, name):
        """Create a wrapper for a subdirectory, reusing our connection."""
        if name == '':
            raise Exception('Empty string is invalid subdirectory name')
        return RegistryWrapper(self._cxn, self._dir + [name], self._ctx)
        
    def _packet(self):
        """Create a packet with the correct context and directory."""
        return self._srv.packet(context=self._ctx).cd(self._dir, True)
    
    def _send(self, pkt):
        """Change back into the root directory after each request."""
        return pkt.cd(['']).send()
    
    def _get_list(self):
        """Get current directory listing (dirs and keys)."""
        return self._send(self._packet().dir()).dir
        
    ## dict interface
    def __getitem__(self, name):
        dirs, keys = self._get_list()
        if name in dirs:
            return self._subdir(name)
        elif name in keys:
            return self._send(self._packet().get(name)).get
        else:
            raise KeyError(name)

    def __setitem__(self, name, value):
        if isinstance(value, (dict, RegistryWrapper)):
            subdir = self._subdir(name)
            for element in value:
                subdir[element] = value[element]
        else:
            self._send(self._packet().set(name, value))

    def __delitem__(self, name):
        dirs, keys = self._get_list()
        if name in dirs:
            subdir = self._subdir(name)
            for k in subdir:
                del subdir[k]
            self._send(self._packet().rmdir(name))
        elif name in keys:
            self._send(self._packet()['del'](name))
        else:
            raise KeyError(name)

    ## attribute interface
    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __delattr__(self, name):
        try:
            return self.__delitem__(name)
        except KeyError:
            raise AttributeError(name)

    def copy(self):
        """Make a local copy, recursively copying subdirs as well."""
        dirs, keys = self._get_list()
        d = AttrDict()
        object.__setattr__(d, '_dir', self._dir)
        object.__setattr__(d, '__name__', self._dir[-1])
        for name in dirs:
            d[name] = self._subdir(name).copy()
        if len(keys):
            p = self._packet()
            for name in keys:
                p.get(name, key=name)
            ans = self._send(p)
            for name in keys:
                d[name] = ans[name]
        return d

    def __contains__(self, name):
        dirs, keys = self._get_list()
        return name in keys or name in dirs
    
    def keys(self):
        dirs, keys = self._get_list()
        return list(dirs) + list(keys)
    
    def __iter__(self):
        return iter(self.keys())
    
    def __repr__(self):
        return '<RegistryWrapper: %r>' % (self._dir,)
        
          


#userPath = 'Registry' ## default at current directory 

 
def loadQubits(cxn,user='Ziyu',session=None,write_access=False):
    """Get local copies of the sample configuration stored in the registry.
    
    Returns the local sample config, and also extracts the individual
    qubit configurations, as specified by the sample['config'] list.  If
    write_access is True, also returns the qubit registry wrappers themselves,
    so that updates can be saved back into the registry.
    """
    userPath = ['', user]
    reg = RegistryWrapper(cxn, userPath)
    
    if session is None:
        samplePath = reg['sample']
        session = samplePath[-1]
        print('Sample Path is', samplePath)
    else:
        prefix, oldSession = reg['sample'][:-1], reg['sample'][-1]
        samplePath = prefix + [session]
        reg['sample'] = samplePath
        print('Sample Path changed to', samplePath)
    #Wrap only the last registry directory in samplePath
    for dir in samplePath[:-1]:
        reg = reg[dir]
    #Error if session doesn't exist at the end of the sample path
    if session is not None and session not in reg:
        print('Session "%s" not found.  Copying from "%s"...' % (session, oldSession),)
        reg[session] = reg[oldSession]
        print('Done.')
    sample = reg[session]
    
    Qubits = [sample[q] for q in sample['config']]
    sample_copy = sample.copy()
    qubits = [sample_copy[q] for q in sample_copy['config']]
    
    # only return original qubit objects if requested
    if write_access:
        return sample, qubits, Qubits
    else:
        return sample, qubits
    
def loadInfo(cxn,paths=['Servers','devices']):
    reg = RegistryWrapper(cxn, ['']+paths)
    # for path in paths:
        # reg = reg[path]
    # dev = reg[user]
    return reg.copy()

