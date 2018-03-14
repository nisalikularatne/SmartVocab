import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4]
y = [ [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [9, 8, 7, 6, 5] ]
labels = ['foo', 'bar', 'baz']

for y_arr, label in zip(y, labels):
    print(y_arr)


