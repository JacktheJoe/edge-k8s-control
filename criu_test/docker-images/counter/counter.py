import time

i = 1
numbers = []
'''
while True:
    with open("counter.txt", "a") as f:
        f.write(f'{i}\n')
    i += 1
    time.sleep(1)
'''
while True:
    numbers.append(i)
    i += 1
    time.sleep(0.001)
