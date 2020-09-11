# pyRegkey
python script for save and load `{key:value}` data with customized units




## Introduction

This codes provide the inter-conversion of dictionary (`.dict`) and a series of file with specific extension (e.g. `.key`). 

For example, a python dictionary for the experimental parameters, 

```python
paras = {'num':410,'f10': Value(5.623,'GHz'), 'type': 'transmon', 'xlist': [0.8, 1.2, 1.5]}
```

Here, we can get individual files `num.key`, `f10.key`, `type.key`, `xlist.key`, where the contents are the values of dictionary. 



## Property

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



## TODO

UI interface for the key editing



now we still use Registry.exe from labrad (ucsb) as a temporal solution





