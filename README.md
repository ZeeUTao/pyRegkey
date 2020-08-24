# pyRegkey
Inter-conversion of python dictionary (.dict) and a series of file with extension (e.g. ".key")




## example

a python dictionary for the experimental parameters

```python
paras = {'f10': 5.623, 'type': 'transmon', 'xlist': [0.8, 1.2, 1.5]}
```

This codes provide the inter-conversion of dictionary (.dict) and a series of file with specific extension (e.g. ".key"). 

Here, we can get three files *f10.key, type.key, xlist.key*, where the contents are the values of dictionary. 



We can use it as following

```python
print(paras.f10)
# 5.623
## or as traditional dict
print(paras['f10'])
```



### types

- float
- string
- list

are supported 





## TODO

UI interface for the key editing





