import time

i = 1

# NOTE: Not using threading or anything, will have to manually exec into pod and start process

while True:
    with open("counter.txt", "a") as f:
        f.write(f'{i}\n')
    i += 1
    time.sleep(1)