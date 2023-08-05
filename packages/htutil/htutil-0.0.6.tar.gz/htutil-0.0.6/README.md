# htutil

HaoTian's Python Util

## install

```sh
pip install htutil
```

## usage

### file

```python
from htutil import file
```

Refer to C# System.IO.File API, very simple to use.

```python
    s = 'hello'
    write_all_text('1.txt', s)
    # hello in 1.txt
    append_all_text('1.txt', 'world')
    # helloworld in 1.txt
    s = read_all_text('1.txt')
    print(s)  # helloworld

    s = ['hello', 'world']
    write_all_lines('1.txt', s)
    # hello\nworld in 1.txt
    append_all_lines('1.txt',['\npython'])
    # hello\nworld\npython in 1.txt
    s = read_all_lines('1.txt')
    print(s)  # ['hello', 'world', 'python']
```

### log

```python
from htutil import log
from htutil.log import p
```

A powerful logger, support var name output.

```python
a = 3
p(a)
p(a-1)

b = bob()
p(b.a)
```

The output is

```txt
a = 3;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:55
a-1 = 2;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:56
b.a = 3;2020-12-19 16:43:49;/Users/t117503445/Project/htutil/htutil/log.py:58
```

You could change the output format.

```python
config(format = '${var_name} = ${value} ### ${time} ### ${file_name}:${line_number}')
p(a)
```

then the output is

```txt
a = 3 ### 2020-12-19 16:46:56 ### /Users/t117503445/Project/htutil/htutil/log.py:60
```

The default format is ${var_name} = ${value};${time};${file_name}:${line_number}

If you want to save the log output to file, you could use callback.

```python
def callback_example(string: str):
    file.append_all_text('1.log',string)

register_p_callback(callback_example)
a = 3
p(a)
```
