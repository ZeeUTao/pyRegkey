# pyRegkey
python script for save and load `{key:value}` data with customized units (optional)




## Introduction

This codes provide the inter-conversion of dictionary (`.dict`) and a series of file with specific extension (e.g. `.key`). 

For example, a python dictionary for the experimental parameters, 

```python
paras = {'num':410,'f10': Value(5.623,'GHz'), 'type': 'transmon', 'xlist': [0.8, 1.2, 1.5]}
```

Here, we can get individual files `num.key`, `f10.key`, `type.key`, `xlist.key`, where the contents are the values of dictionary. 



## Property

### Types

- float/int
- string
- list
- float/int + units

are supported 

```python
# float/int
11.0,-45.0,1,-4 

# string
'ikuiku' 

# list
[1.14,5.14,1.5,1.5] 

# float/int + units
11.4514*GHz, Value(11.4514,'GHz') 


```

### Unit

You can write `11.4514*GHz` or `Value(11.4514,'GHz') ` to define a number with units. 

Transformation of the usual units are supported, for example, 

`Value(11.4514,'GHz')['MHz']=11451.4 `



## Getting started

`run regkey` and enter 

```python
sample, qubits = loadQubits(write_access=False)
```

The data in `\\Registry\\` is given for test. 



## TODO

UI interface for the key editing



now we still use Registry.exe from labrad (ucsb) as a temporal solution





