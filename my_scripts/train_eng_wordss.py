import random
import time

eng_rus = False


tt = [
    ['postpone', 'переносить, откладывать', ],
    ['convenient', 'удобный', ],
]

while tt:
    print(len(tt))
    word = tt[random.randint(0, len(tt) - 1)]
    tt.remove(word)
    if eng_rus:
        input(word[0])
        print(f'{word[1]} {word[2] if len(word) > 2 else ""}')
    else:
        input(word[1])
        print(f'{word[0]} {word[2] if len(word) > 2 else ""}')
    print('\n')
    time.sleep(1)
