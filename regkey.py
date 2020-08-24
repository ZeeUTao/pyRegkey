#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2020, Ziyu Tao
# All rights reserved.

import os,json


# dict to files (keys)
dict_example = {'f10': 5.6883, 'type': 'transmon1', 'xlist': [0.8, 1.2, 1.5]}
folder = r'Registry\example_keys.dir'

for (k,v) in  dict_example.items():
    path_save = os.path.join(folder,k+'.key')
    f=open(path_save,"w")
    if type(v) is str:
        v_write = '"{0}"'.format(v)
    else:
        v_write = str(v)
    f.write(v_write)
    f.close()


# files (keys) to dict
def key2dict(folder,key=0,value=1):
    keys,values = [],[]
    f_list = (fn for fn in os.listdir(folder+'//') if fn.endswith('.key'))
    for f in f_list:
        keys.append(os.path.splitext(f)[0])
        f_open = open(os.path.join(folder,f))
        value0 = f_open.read().strip()
        f_open.close()
        # transfer from .str to appropriate type
        value = json.loads(value0)
        values.append(value)
    dict_res = dict(zip(keys,values))
    return dict_res


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


folder = r'Registry\example_keys.dir'
q1 = AttrDict(key2dict(folder))


print(q1)




