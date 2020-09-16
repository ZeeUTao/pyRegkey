# pyRegkey
python script for save and load `{key:value}` data with customized units, 

and a data vault for saving experimental data. 




## Introduction

This codes provide the inter-conversion of dictionary (`.dict`) and a series of file with specific extension (e.g. `.key`). 

For example, a python dictionary for the experimental parameters, 

```python
paras = {'num':410,'f10': Value(5.623,'GHz'), 'type': 'transmon', 'xlist': [0.8, 1.2, 1.5]}
```

Here, we can get individual files `num.key`, `f10.key`, `type.key`, `xlist.key`, where the contents are the values of dictionary. 




## Registry

mainly in `regkey.py`, and import some codes in `util`

### sub-directory

You can access the sub-directory via  `folder['sub_folder']['sub_sub_folder']`  or `folder.sub_folder.sub_sub_folder`, to change any key in the main `Registry` folder. 

```python
folder.sub_folder.sub_sub_folder.key0 = value0
# or
folder['sub_folder']['sub_sub_folder']['key0'] = value0
```



We usually have a structure `Registry\\User.dir\\20XXXXSample.dir\\q1.dir` , and use

 `sample, qubits = loadQubits(write_access=False)`. 

Specially, `sample['q1'].f10 = 5.414*GHz` will change the original `.key`, `qubits` is a copy and `qubits[0]=5.414*GHz` will not change the saved file. 





### basic types

All the types in python expression are supported 

```python
# float/int
11.0,-45.0,1,-4 

# string
'ikuiku' 

# list
[1.14,5.14,1.5,1.5] 
[('xy','12','13'),('z','12','13')]

# ...
```

### Unit

You can write `11.4514*GHz` or `Value(11.4514,'GHz') ` to define a number with units. 

Transformation of the usual units are supported, for example, 

`Value(11.4514,'GHz')['MHz']=11451.4 `

Combined type is also okay

`"""[1.2 ns, 1.3 ns]""" `  in the saved file `.key`  --> `[Value(1.2,'ns'),Value(1.3,'ns')]` in the extracted `.dict`



### write_access

You can change the value in `RegistryWrapper()` as `paras.f10 = 5.414*GHz` , then the original file is also changed. 

If you do not want to change the original file, you can use a copy of `paras`. 



## DataVault

mainly in `dataVault.py`, and import some codes in `util`

- Example:

`run dataVault` in ipython

and input

```python
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
    data = [x,y]
    data = np.asarray(data)
    
    dv.add(ctx,data)
    time.sleep(0.001)
   
dv.close(ctx)
```



## TODO

UI interface for the key editing



now we still use Registry.exe, Grapher.exe from labrad (ucsb) as a temporal solution





