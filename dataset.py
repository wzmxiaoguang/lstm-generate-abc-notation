import random

input = open('.\\data\\original.txt', 'r').read().split('X:')
with open('.\\data\\input.txt', 'w') as f:
    for i in range(1000):
        f.write('X:' + input[random.randint(1,len(input)-1)] + '_______________________\n')
