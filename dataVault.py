#!/usr/bin/env python
## -*- coding: utf-8 -*-
# Copyright (c) 2020, Ziyu Tao



from configparser import ConfigParser
import os
from datetime import datetime
from util import types as T
import numpy
from twisted.internet.reactor import callLater


try:
    import numpy
    useNumpy = True
except ImportError as e:
    print(e)
    print("Numpy not imported.  The DataVault will operate, but will be slower.")
    useNumpy = False
    
    
    
class ConfigFile(object):
    """Wrapper for configuration files."""
    def __init__(self, name, path):
        if not name.endswith('.ini'):
            name += '.ini'
        self.name = name
        self.fname = os.path.join(path, name)
        self.parser = ConfigParser()
        with open(self.fname) as f:
            self.parser.read_file(f)
        
    def save():
        with open(self.fname, 'w') as f:
            self.parser.write(f)
        
    def __getattr__(self, key):
        """Delegate everything else to the config parser."""
        return getattr(self.parser, key)





## setting parameters

cf = ConfigFile('data_vault', os.getcwd())
DATADIR = cf.get('config', 'repository')

PRECISION = 6
FILE_TIMEOUT = 60 # how long to keep datafiles open if not accessed
DATA_TIMEOUT = 300 # how long to keep data in memory if not accessed
TIME_FORMAT = '%Y-%m-%d, %H:%M:%S'
DATA_FORMAT = '%%.%dG' % PRECISION





## filename translation
        
encodings = [
    ('%','%p'),
    ('/','%f'),
    ('\\','%b'),
    (':','%c'),
    ('*','%a'),
    ('?','%q'),
    ('"','%Q'),
    ('<','%l'),
    ('>','%g'),
    ('|','%P')
]

def dsEncode(name):
    for char, code in encodings:
        name = name.replace(char, code)
    return name

def dsDecode(name):
    for char, code in encodings[1:] + encodings[0:1]:
        name = name.replace(code, char)
    return name

def filedir(path):
    return os.path.join(DATADIR, *[dsEncode(d) + '.dir' for d in path[1:]])





## time formatting
    
def timeToStr(t):
    return t.strftime(TIME_FORMAT)

def timeFromStr(s):
    return datetime.strptime(s, TIME_FORMAT)





## error messages

class NoDatasetError(T.Error):
    """Please open a dataset first."""
    code = 2

class DatasetNotFoundError(T.Error):
    code = 3
    def __init__(self, name):
        self.msg="Dataset '%s' not found!" % name

class DirectoryExistsError(T.Error):
    code = 4
    def __init__(self, name):
        self.msg = "Directory '%s' already exists!" % name

class EmptyNameError(T.Error):
    """Names of directories or keys cannot be empty"""
    code = 5
        
class ReadOnlyError(T.Error):
    """Points can only be added to datasets created with 'new'."""
    code = 6

class BadDataError(T.Error):
    code = 7
    def __init__(self, varcount):
        self.msg = 'Dataset requires %d values per datapoint.' % varcount

class BadParameterError(T.Error):
    code = 8
    def __init__(self, name):
        self.msg = "Parameter '%s' not found." % name

class ParameterInUseError(T.Error):
    code = 9
    def __init__(self, name):
        self.msg = "Already a parameter called '%s'." % name





class Session(object):
    """Stores information about a directory on disk.
    
    One session object is created for each data directory accessed.
    The session object manages reading from and writing to the config
    file, and manages the datasets in this directory.
    """
    
    # keep a dictionary of all created session objects
    _sessions = {}
    
    @staticmethod
    def exists(path):
        """Check whether a session exists on disk for a given path.
        This does not tell us whether a session object has been
        created for that path.
        """
        return os.path.exists(filedir(path))
    
    def __new__(cls, path, parent):
        """Get a Session object.
        
        If a session already exists for the given path, return it.
        Otherwise, create a new session instance.
        """
        path = tuple(path)
        if path in cls._sessions:
            return cls._sessions[path]
        inst = super(Session, cls).__new__(cls)
        inst._init(path, parent)
        cls._sessions[path] = inst
        return inst

    def _init(self, path, parent):
        """Initialization that happens once when session object is created."""
        self.path = path
        self.parent = parent
        self.dir = filedir(path)
        self.infofile = os.path.join(self.dir, 'session.ini')
        self.listeners = []
        self.datasets = {}

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            
            # notify listeners about this new directory
            parent_session = Session(path[:-1], parent)
            parent.onNewDir(path[-1], parent_session.listeners)
           
        if os.path.exists(self.infofile):
            self.load()
        else:
            self.counter = 1
            self.created = self.modified = datetime.now()

        self.access() # update current access time and save
        self.listeners = set()
            
    def load(self):
        """Load info from the session.ini file."""
        S = ConfigParser()
        S.read(self.infofile)

        sec = 'File System'
        self.counter = S.getint(sec, 'Counter')

        sec = 'Information'
        self.created = timeFromStr(S.get(sec, 'Created'))
        self.accessed = timeFromStr(S.get(sec, 'Accessed'))
        self.modified = timeFromStr(S.get(sec, 'Modified'))

    def save(self):
        """Save info to the session.ini file."""
        S = ConfigParser()

        sec = 'File System'
        S.add_section(sec)
        S.set(sec, 'Counter', repr(self.counter))

        sec = 'Information'
        S.add_section(sec)
        S.set(sec, 'Created',  timeToStr(self.created))
        S.set(sec, 'Accessed', timeToStr(self.accessed))
        S.set(sec, 'Modified', timeToStr(self.modified))

        with open(self.infofile, 'w') as f:
            S.write(f)

    def access(self):
        """Update last access time and save."""
        self.accessed = datetime.now()
        self.save()

    def listContents(self):
        """Get a list of directory names in this directory."""
        files = os.listdir(self.dir)
        dirs = [dsDecode(s[:-4]) for s in files if s.endswith('.dir')]
        datasets = [dsDecode(s[:-4]) for s in files if s.endswith('.csv')]
        return dirs, datasets
            
    def listDatasets(self):
        """Get a list of dataset names in this directory."""
        files = os.listdir(self.dir)
        return [dsDecode(s[:-4]) for s in files if s.endswith('.csv')]
    
    def newDataset(self, title, independents, dependents):
        num = self.counter
        self.counter += 1
        self.modified = datetime.now()

        name = '%05d - %s' % (num, title)
        dataset = Dataset(self, name, title, create=True)
        for i in independents:
            dataset.addIndependent(i)
        for d in dependents:
            dataset.addDependent(d)
        self.datasets[name] = dataset
        self.access()
        
        # notify listeners about the new dataset
        # self.parent.onNewDataset(name, self.listeners)
        return dataset
        
    def openDataset(self, name):
        # first lookup by number if necessary
        if isinstance(name, (int)):
            for oldName in self.listDatasets():
                num = int(oldName[:5])
                if name == num:
                    name = oldName
                    break
        # if it's still a number, we didn't find the set
        if isinstance(name, (int)):
            raise DatasetNotFoundError(name)

        filename = dsEncode(name)
        if not os.path.exists(os.path.join(self.dir, filename + '.csv')):
            raise DatasetNotFoundError(name)

        if name in self.datasets:
            dataset = self.datasets[name]
            dataset.access()
        else:
            # need to create a new wrapper for this dataset
            dataset = Dataset(self, name)
            self.datasets[name] = dataset
        self.access()
        
        return dataset





class Dataset:
    def __init__(self, session, name, title=None, num=None, create=False):
        self.parent = session.parent
        self.name = name
        file_base = os.path.join(session.dir, dsEncode(name))
        self.datafile = file_base + '.csv'
        self.infofile = file_base + '.ini'
        self.file # create the datafile, but don't do anything with it
        self.listeners = set() # contexts that want to hear about added data
        self.param_listeners = set()
        self.comment_listeners = set()
        
        if create:
            self.title = title
            self.created = self.accessed = self.modified = datetime.now()
            self.independents = []
            self.dependents = []
            self.parameters = []
            self.comments = []
            self.save()
        else:
            self.load()
            self.access()

    def load(self):
        S = ConfigParser()
        S.read(self.infofile)

        gen = 'General'
        self.title = S.get(gen, 'Title', raw=True)
        self.created = timeFromStr(S.get(gen, 'Created'))
        self.accessed = timeFromStr(S.get(gen, 'Accessed'))
        self.modified = timeFromStr(S.get(gen, 'Modified'))

        def getInd(i):
            sec = 'Independent %d' % (i+1)
            label = S.get(sec, 'Label', raw=True)
            units = S.get(sec, 'Units', raw=True)
            return dict(label=label, units=units)
        count = S.getint(gen, 'Independent')
        self.independents = [getInd(i) for i in range(count)]

        def getDep(i):
            sec = 'Dependent %d' % (i+1)
            label = S.get(sec, 'Label', raw=True)
            units = S.get(sec, 'Units', raw=True)
            categ = S.get(sec, 'Category', raw=True)
            return dict(label=label, units=units, category=categ)
        count = S.getint(gen, 'Dependent')
        self.dependents = [getDep(i) for i in range(count)]

        def getPar(i):
            sec = 'Parameter %d' % (i+1)
            label = S.get(sec, 'Label', raw=True)
            # TODO: big security hole! eval can execute arbitrary code
            data = T.evalLRData(S.get(sec, 'Data', raw=True))
            return dict(label=label, data=data)
        count = S.getint(gen, 'Parameters')
        self.parameters = [getPar(i) for i in range(count)]

        # get comments if they're there
        if S.has_section('Comments'):
            def getComment(i):
                sec = 'Comments'
                time, user, comment = eval(S.get(sec, 'c%d' % i, raw=True))
                return timeFromStr(time), user, comment
            count = S.getint(gen, 'Comments')
            self.comments = [getComment(i) for i in range(count)]
        else:
            self.comments = []
        
    def save(self):
        S = ConfigParser()
        
        sec = 'General'
        S.add_section(sec)
        S.set(sec, 'Created',  timeToStr(self.created))
        S.set(sec, 'Accessed', timeToStr(self.accessed))
        S.set(sec, 'Modified', timeToStr(self.modified))
        S.set(sec, 'Title',       self.title)
        S.set(sec, 'Independent', repr(len(self.independents)))
        S.set(sec, 'Dependent',   repr(len(self.dependents)))
        S.set(sec, 'Parameters',  repr(len(self.parameters)))
        S.set(sec, 'Comments',    repr(len(self.comments)))

        for i, ind in enumerate(self.independents):
            sec = 'Independent %d' % (i+1)
            S.add_section(sec)
            S.set(sec, 'Label', ind['label'])
            S.set(sec, 'Units', ind['units'])

        for i, dep in enumerate(self.dependents):
            sec = 'Dependent %d' % (i+1)
            S.add_section(sec)
            S.set(sec, 'Label',    dep['label'])
            S.set(sec, 'Units',    dep['units'])
            S.set(sec, 'Category', dep['category'])

        for i, par in enumerate(self.parameters):
            sec = 'Parameter %d' % (i+1)
            S.add_section(sec)
            S.set(sec, 'Label', par['label'])
            # TODO: smarter saving here, since eval'ing is insecure
            S.set(sec, 'Data', repr(par['data']))

        sec = 'Comments'
        S.add_section(sec)
        for i, (time, user, comment) in enumerate(self.comments):
            time = timeToStr(time)
            S.set(sec, 'c%d' % i, repr((time, user, comment)))
            
        with open(self.infofile, 'w') as f:
            S.write(f)

    def access(self):
        """Update time of last access for this dataset."""
        self.accessed = datetime.now()
        self.save()

    @property
    def file(self):
        """Open the datafile on demand.

        The file is also scheduled to be closed
        if it has not accessed for a while.
        """
        if not hasattr(self, '_file'):
            self._file = open(self.datafile, 'a+') # append data
            self._fileTimeoutCall = callLater(FILE_TIMEOUT, self._fileTimeout)
        else:
            self._fileTimeoutCall.reset(FILE_TIMEOUT)
        return self._file
        
    def _fileTimeout(self):
        self._file.close()
        del self._file
        del self._fileTimeoutCall
    
    def _fileSize(self):
        """Check the file size of our datafile."""
        # does this include the size before the file has been flushed to disk?
        return os.fstat(self.file.fileno()).st_size
    
    @property
    def data(self):
        """Read data from file on demand.
        
        The data is scheduled to be cleared from memory unless accessed."""
        if not hasattr(self, '_data'):
            self._data = []
            self._datapos = 0
            self._dataTimeoutCall = callLater(DATA_TIMEOUT, self._dataTimeout)
        else:
            self._dataTimeoutCall.reset(DATA_TIMEOUT)
        f = self.file
        f.seek(self._datapos)
        lines = f.readlines()
        self._data.extend([float(n) for n in line.split(',')] for line in lines)
        self._datapos = f.tell()
        return self._data
    
    def _dataTimeout(self):
        del self._data
        del self._datapos
        del self._dataTimeoutCall
    
    def _saveData(self, data):
        f = self.file
        for row in data:
            f.write(', '.join(DATA_FORMAT % v for v in row) + '\n')
        f.flush()
    
    def addIndependent(self, label):
        """Add an independent variable to this dataset."""
        if isinstance(label, tuple):
            label, units = label
        else:
            label, units = parseIndependent(label)
        d = dict(label=label, units=units)
        self.independents.append(d)
        self.save()

    def addDependent(self, label):
        """Add a dependent variable to this dataset."""
        if isinstance(label, tuple):
            label, legend, units = label
        else:
            label, legend, units = parseDependent(label)
        d = dict(category=label, label=legend, units=units)
        self.dependents.append(d)
        self.save()

    def addParameter(self, name, data, saveNow=True):
        self._addParam(name, data)
        if saveNow:
            self.save()
        
        # notify all listening contexts
#         self.parent.onNewParameter(None, self.param_listeners)
        self.param_listeners = set()
        return name

    def addParameters(self, params, saveNow=True):
        for name, data in params:
            self._addParam(name, data)
        if saveNow:
            self.save()
        
        # notify all listening contexts
#         self.parent.onNewParameter(None, self.param_listeners)
        self.param_listeners = set()
        
    def _addParam(self, name, data):
        for p in self.parameters:
            if p['label'] == name:
                raise ParameterInUseError(name)
        d = dict(label=name, data=data)
        self.parameters.append(d)
        
    def getParameter(self, name, case_sensitive=True):
        for p in self.parameters:
            if case_sensitive:
                if p['label'] == name:
                    return p['data']
            else:
                if p['label'].lower() == name.lower():
                    return p['data']
        raise BadParameterError(name)
        
    def addData(self, data):
        varcount = len(self.independents) + len(self.dependents)
        if not len(data) or not isinstance(data[0], list):
            data = [data]
        if len(data[0]) != varcount:
            raise BadDataError(varcount, len(data[0]))
            
        # append the data to the file
        self._saveData(data)
        
        # notify all listening contexts
#         self.parent.onDataAvailable(None, self.listeners)
        self.listeners = set()
    
    def getData(self, limit, start):
        if limit is None:
            data = self.data[start:]
        else:
            data = self.data[start:start+limit]
        return data, start + len(data)
        
    def keepStreaming(self, context, pos):
        if pos < len(self.data):
            if context in self.listeners:
                self.listeners.remove(context)
#             self.parent.onDataAvailable(None, context)
        else:
            self.listeners.add(context)
            
    def addComment(self, user, comment):
        self.comments.append((datetime.now(), user, comment))
        self.save()
        
        # notify all listening contexts
        self.parent.onCommentsAvailable(None, self.comment_listeners)
        self.comment_listeners = set()

    def getComments(self, limit, start):
        if limit is None:
            comments = self.comments[start:]
        else:
            comments = self.comments[start:start+limit]
        return comments, start + len(comments)
        
    def keepStreamingComments(self, context, pos):
        if pos < len(self.comments):
            if context in self.comment_listeners:
                self.comment_listeners.remove(context)
            self.parent.onCommentsAvailable(None, context)
        else:
            self.comment_listeners.add(context)





class NumpyDataset(Dataset):
    def _get_data(self):
        """Read data from file on demand.
        
        The data is scheduled to be cleared from memory unless accessed."""
        if not hasattr(self, '_data'):
            try:
                # if the file is empty, this line can barf in certain versions
                # of numpy.  Clearly, if the file does not exist on disk, this
                # will be the case.  Even if the file exists on disk, we must
                # check its size
                if self._fileSize() > 0:
                    self._data = numpy.loadtxt(self.file, delimiter=',')
                else:
                    self._data = numpy.array([[]])
                if len(self._data.shape) == 1:
                    self._data.shape = (1, len(self._data))
            except ValueError:
                # no data saved yet
                # this error is raised by numpy <=1.2
                self._data = numpy.array([[]])
            except IOError:
                # no data saved yet
                # this error is raised by numpy 1.3
                self.file.seek(0)
                self._data = numpy.array([[]])
            self._dataTimeoutCall = callLater(DATA_TIMEOUT, self._dataTimeout)
        else:
            self._dataTimeoutCall.reset(DATA_TIMEOUT)
        return self._data

    def _set_data(self, data):
        self._data = data
        
    data = property(_get_data, _set_data)
    
    def _saveData(self, data):
        f = self.file
        numpy.savetxt(f, data, fmt=DATA_FORMAT, delimiter=',')
        f.flush()
    
    def _dataTimeout(self):
        del self._data
        del self._dataTimeoutCall
        
    def addData(self, data):
        varcount = len(self.independents) + len(self.dependents)
        data = numpy.asarray(data)
        
        # reshape single row
        if len(data.shape) == 1:
            data.shape = (1, data.size)
        
        # check row length
        if data.shape[-1] != varcount:
            raise BadDataError(varcount, data.shape[-1])
        
        # append data to in-memory data
        if self.data.size > 0:
            self.data = numpy.vstack((self.data, data))
        else:
            self.data = data
            
        # append data to file
        self._saveData(data)
        
        # notify all listening contexts
#         self.parent.onDataAvailable(None, self.listeners)
        self.listeners = set()
    
    def getData(self, limit, start):
        if limit is None:
            data = self.data[start:]
        else:
            data = self.data[start:start+limit]
        # nrows should be zero for an empty row
        nrows = len(data) if data.size > 0 else 0
        return data, start + nrows
        
    def keepStreaming(self, context, pos):
        # cheesy hack: if pos == 0, we only need to check whether
        # the filesize is nonzero
        if pos == 0:
            more = os.path.getsize(self.datafile) > 0
        else:
            nrows = len(self.data) if self.data.size > 0 else 0
            more = pos < nrows
        if more:
            if context in self.listeners:
                self.listeners.remove(context)
#             self.parent.onDataAvailable(None, context)
        else:
            self.listeners.add(context)
if useNumpy:
    Dataset = NumpyDataset





class DataVault(object):
    # context 
    # def __init__(self):
        
    def getSession(self, c):
        """Get a session object for the current path."""
        return Session(c['path'], self)

    def getDataset(self, c):
        """Get a dataset object for the current dataset."""
        if 'dataset' not in c:
            raise NoDatasetError()
        session = self.getSession(c)
        return session.datasets[c['dataset']]

    def dir(self, c, tagFilters=['-trash'], includeTags=None):
        """Get subdirectories and datasets in the current directory."""
        if isinstance(tagFilters, str):
            tagFilters = [tagFilters]
        sess = self.getSession(c)
        dirs, datasets = sess.listContents()
        if includeTags:
            dirs, datasets = sess.getTags(dirs, datasets)
        #print dirs, datasets
        return dirs, datasets

    def cd(self, c, path=None, create=False):
        """Change the current directory.
        
        The empty string '' refers to the root directory. If the 'create' flag
        is set to true, new directories will be created as needed.
        Returns the path to the new current directory.
        """
        if path is None:
            return c['path']
        
        temp = c['path'][:] # copy the current path
        if isinstance(path, (int, long)):
            if path > 0:
                temp = temp[:-path]
                if not len(temp):
                    temp = ['']
        else:
            if isinstance(path, str):
                path = [path]
            for dir in path:
                if dir == '':
                    temp = ['']
                else:
                    temp.append(dir)
                if not Session.exists(temp) and not create:
                    raise DirectoryNotFoundError(temp)
                session = Session(temp, self) # touch the session
        if c['path'] != temp:
            # stop listening to old session and start listening to new session
            Session(c['path'], self).listeners.remove(c.ID)
            Session(temp, self).listeners.add(c.ID)
            c['path'] = temp
        return c['path']
        
    def mkdir(self, c, name):
        """Make a new sub-directory in the current directory.
        
        The current directory remains selected.  You must use the
        'cd' command to select the newly-created directory.
        Directory name cannot be empty.  Returns the path to the
        created directory.
        """
        if name == '':
            raise EmptyNameError()
        path = c['path'] + [name]
        if Session.exists(path):
            raise DirectoryExistsError(path)
        sess = Session(path, self) # make the new directory
        return path
    

    def new(self, c, name, independents, dependents):
        """Create a new Dataset.

        Independent and dependent variables can be specified either
        as clusters of strings, or as single strings.  Independent
        variables have the form (label, units) or 'label [units]'.
        Dependent variables have the form (label, legend, units)
        or 'label (legend) [units]'.  Label is meant to be an
        axis label that can be shared among traces, while legend is
        a legend entry that should be unique for each trace.
        Returns the path and name for this dataset.
        """
        session = self.getSession(c)
        dataset = session.newDataset(name or 'untitled', independents, dependents)
        c['dataset'] = dataset.name # not the same as name; has number prefixed
        c['filepos'] = 0 # start at the beginning
        c['commentpos'] = 0
        c['writing'] = True
        return c['path'], c['dataset']
    
    def open(self, c, name):
        """Open a Dataset for reading.
        
        You can specify the dataset by name or number.
        Returns the path and name for this dataset.
        """
        session = self.getSession(c)
        dataset = session.openDataset(name)
        c['dataset'] = dataset.name # not the same as name; has number prefixed
        c['filepos'] = 0
        c['commentpos'] = 0
        c['writing'] = False
        dataset.keepStreaming(c.ID, 0)
        dataset.keepStreamingComments(c.ID, 0)
        return c['path'], c['dataset']
    

    def add(self, c, data):
        """Add data to the current dataset.
        
        The number of elements in each row of data must be equal
        to the total number of variables in the data set
        (independents + dependents).
        """
        dataset = self.getDataset(c)
        if not c['writing']:
            raise ReadOnlyError()
        dataset.addData(data)
    
    def get(self, c, limit=None, startOver=False):
        """Get data from the current dataset.
        
        Limit is the maximum number of rows of data to return, with
        the default being to return the whole dataset.  Setting the
        startOver flag to true will return data starting at the beginning
        of the dataset.  By default, only new data that has not been seen
        in this context is returned.
        """
        dataset = self.getDataset(c)
        c['filepos'] = 0 if startOver else c['filepos']
        data, c['filepos'] = dataset.getData(limit, c['filepos'])
        dataset.keepStreaming(c.ID, c['filepos'])
        return data
    
    def close(self,c):
        dataset = self.getDataset(c)
        dataset._fileTimeout()
        
    def variables(self, c):
        """Get the independent and dependent variables for the current dataset.
        
        Each independent variable is a cluster of (label, units).
        Each dependent variable is a cluster of (label, legend, units).
        Label is meant to be an axis label, which may be shared among several
        traces, while legend is unique to each trace.
        """
        ds = self.getDataset(c)
        ind = [(i['label'], i['units']) for i in ds.independents]
        dep = [(d['category'], d['label'], d['units']) for d in ds.dependents]
        return ind, dep

    def parameters(self, c):
        """Get a list of parameter names."""
        dataset = self.getDataset(c)
        return [par['label'] for par in dataset.parameters]

    def add_parameter(self, c, name, data):
        """Add a new parameter to the current dataset."""
        dataset = self.getDataset(c)
        dataset.addParameter(name, data)

    def add_parameters(self, c, params):
        """Add a new parameter to the current dataset."""
        dataset = self.getDataset(c)
        dataset.addParameters(params)
        
    def get_name(self, c):
        """Get the name of the current dataset."""
        dataset = self.getDataset(c)
        name = dataset.name
        return name

    def get_parameter(self, c, name, case_sensitive=True):
        """Get the value of a parameter."""
        dataset = self.getDataset(c)
        return dataset.getParameter(name, case_sensitive)

    def get_parameters(self, c):
        """Get all parameters.
        
        Returns a cluster of (name, value) clusters, one for each parameter.
        If the set has no parameters, nothing is returned (since empty clusters
        are not allowed).
        """
        dataset = self.getDataset(c)
        names = [par['label'] for par in dataset.parameters]
        params = tuple((name, dataset.getParameter(name)) for name in names)
        dataset.param_listeners.add(c.ID) # send a message when new parameters are added
        if len(params):
            return params





def num2name(c,num):
    sess = Session(c['path'],'')
    name = ''
    try:
        name = sess.listDatasets()[num]   
    except:
        print('num2name Error')
    return name





def init_context(path):
    context = {}
    context['path'] = path
    context['dataset'] = num2name(context,-1)
    context['ID'] = 0 # useless now, if only use a local datasaving
    context['writing'] = False
    return context





### following is example
### remove annotation to use

"""
path = ['XXX','Ziyu','peach']
ctx = init_context(path)
dv = DataVault()





import numpy as np
xs = np.arange(0.,101,1)
ys = np.sin(0.1*xs)





dv.new(ctx,'Test_x_y22', [('freq', 'value')], [('z','Test-Spectrum','a.u.')])
dv.add_parameter(ctx,'simu_eq22', ['ys=sin(xs)'])



import time

for i in range(len(xs)):
    
    x,y=xs[i],ys[i]
    print(i)
    data = [x+20,y**2]
    data = np.asarray(data)
    
    dv.add(ctx,data)
    time.sleep(0.001)

# 结束了要close掉，删除缓存    
dv.close(ctx)

"""





