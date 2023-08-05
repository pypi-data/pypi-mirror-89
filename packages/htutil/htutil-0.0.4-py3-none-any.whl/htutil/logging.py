import re
import inspect
import datetime


def p(value):
    info = inspect.getframeinfo(inspect.currentframe().f_back)
    line = inspect.getframeinfo(inspect.currentframe().f_back)[3][0]

    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    var_name = re.search(r'''(?<=\b\().+(?=\))''', line).group(0)

    string = f'{var_name} = {value};{t};{info.filename}:{info.lineno}'

    print(string, flush=True)


class bob():
    a = 3


def main():
    a = 3
    p(a)

    p(a-1)

    b = bob()
    p(b.a)


if __name__ == '__main__':
    main()
