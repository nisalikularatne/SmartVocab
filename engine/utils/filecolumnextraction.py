import os
import inspect

filepath = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../resources/")))
with open(filepath + '/c2-vocab.txt') as fp:
    lines = fp.readlines()
    new_lines = []
    for line in lines:
        # - Strip white spaces
        line = line.strip().split()[-1]

        new_lines.append(line)
for i,e in enumerate(new_lines):

    print(1.,'\t',e,'\t',0.,'\t',1.)
