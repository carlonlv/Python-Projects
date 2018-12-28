import sys


def func(dict, string):
    list = {}
    for i in range(len(string)):
        list[i] = []
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            if string[i:j] in dict:
                list[j - 1].append(i)
    result = dfs(list, string, len(string) - 1, [])
    if result is None:
        return None
    else:
        result.reverse()
        return stringize(result)


def stringize(result):
    asd = ""
    for i in result:
        asd += i
        asd += ' '
    return asd[:-1]


def dfs(list, string, index, result):
    if index == -1:
        return result
    elif len(list[index]) == 0:
        return None
    else:
        current_len = len(result)
        for i in list[index]:
            result.append(string[i: index + 1])
            status = dfs(list, string, i - 1, result)
            if status is None:
                for i in range(len(result) - current_len):
                    result.pop()
            else:
                return result
        return None


def parse_input(datafile):
    string = ""
    dictionary = []
    line_num = 1
    for line in datafile:
        if line_num == 1:
            alist = line.split(',')
            alist[len(alist) - 1] = alist[len(alist) - 1][:-1]
            for s in alist:
                dictionary.append(s)
            line_num += 1
        else:
            string = line[:-1]
    return dictionary, string


if __name__ == '__main__':
    if len(sys.argv) == 2:
        datafile = open(sys.argv[1])
        dict, string = parse_input(datafile)
        output = func(dict, string)
        if output is not None:
            print(output)
