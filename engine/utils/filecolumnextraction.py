import os
import inspect

filepath = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../resources/")))
with open(filepath + '/a1-vocab.txt') as fp:
    lines = fp.readlines()
    new_lines = []
    for line in lines:
        # - Strip white spaces
        line = line.strip().split()[0]
        if line not in new_lines:
            new_lines.append(line)
for i in new_lines:
    print(i)