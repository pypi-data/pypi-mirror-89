# write2list

A simple python package which accepts a Tuple of Lists and converts it to a List. I wrote this to learn how custom packages work in Python. Here is the quick difference between a Tuple and a List-

| Tuple              | List                          |
|:------------------:|:-----------------------------:|
| Immutable bindings | Mutable via Append and Extend |

### How to use?

```bash
pip install write2list
```

```Python
# test.py
import write2list

exampleTuple=(["Hi I am the first example list"], ["123456"], ["Wow these are one too many lists for a simple example. Let's end this object here."])

resultList=write2list.create(exampleTuple)

print(resultList)
```

```bash
python test.py
['Hi I am the first example list', '123456', "Wow these are one too many lists for a simple example. Let's end this object here."]
```