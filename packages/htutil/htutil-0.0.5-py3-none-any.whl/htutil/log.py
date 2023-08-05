import re
import inspect
import datetime

_format = '${var_name} = ${value};${time};${file_name}:${line_number}'


def config(format: str):
    _format = format


def register_p_callback(func_call_back):
    list_p_call_back_func.append(func_call_back)


list_p_call_back_func = []


def p(value) -> str:
    info = inspect.getframeinfo(inspect.currentframe().f_back)

    file_name = info.filename
    line_number = str(info.lineno)

    line = inspect.getframeinfo(inspect.currentframe().f_back)[3][0]
    var_name = re.search(r'''(?<=\b\().+(?=\))''', line).group(0)

    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    d = {'${file_name}': file_name, '${line_number}': line_number,
         '${var_name}': var_name, '${time}': t, '${value}': str(value)}

    string = _format

    for s in d:
        string = string.replace(s, d[s])

    print(string, flush=True)
    for func in list_p_call_back_func:
        func(string)

    return string


class bob():
    a = 3


def callback_example(string: str):
    print('callback', string)


def main():
    a = 3
    p(a)

    p(a-1)

    register_p_callback(callback_example)

    b = bob()
    p(b.a)


if __name__ == '__main__':
    main()
