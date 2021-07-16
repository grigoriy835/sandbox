import random
import time


tt = [
    ['say', 'said', 'said', ],
    ['make', 'made', 'made', ],
    ['go', 'went', 'gone', ],
    ['take', 'took', 'taken', ],
    ['come', 'came', 'come', ],
    ['see', 'saw', 'seen', ],
    ['know', 'knew', 'known', ],
    ['get', 'got', 'got/gotten (US)', ],
    ['give', 'gave', 'given', ],
    ['find', 'found', 'found', ],
    ['think', 'thought', 'thought', ],
    ['tell', 'told', 'told', ],
    ['become', 'became', 'become', ],
    ['show', 'showed', 'shown', ],
    ['leave', 'left', 'left', ],
    ['feel', 'felt', 'felt', ],
    ['put', 'put', 'put', ],
    ['bring', 'brought', 'brought', ],
    ['begin', 'began', 'begun', ],
    ['keep', 'kept', 'kept', ],
    ['hold', 'held', 'held', ],
    ['write', 'wrote', 'written', ],
    ['stand', 'stood', 'stood', ],
    ['hear', 'heard', 'heard', ],
    ['let', 'let', 'let', ],
    ['mean', 'meant', 'meant', ],
    ['set', 'set', 'set', ],
    ['meet', 'met', 'met', ],
    ['run', 'ran', 'run', ],
    ['pay', 'paid', 'paid', ],
    ['sit', 'sat', 'sat', ],
    ['speak', 'spoke', 'spoken', ],
    ['lie', 'lay', 'lain', ],
    ['lead', 'led', 'led', ],
    ['read', 'read', 'read', ],
    ['grow', 'grew', 'grown', ],
    ['lose', 'lost', 'lost', ],
    ['fall', 'fell', 'fallen', ],
    ['send', 'sent', 'sent', ],
    ['build', 'built', 'built', ],
    ['understand', 'understood', 'understood', ],
    ['draw', 'drew', 'drawn', ],
    ['break', 'broke', 'broken', ],
    ['spend', 'spent', 'spent', ],
    ['cut', 'cut', 'cut', ],
    ['rise', 'rose', 'risen', ],
    ['drive', 'drove', 'driven', ],
    ['buy', 'bought', 'bought', ],
    ['wear', 'wore', 'worn', ],
    ['choose', 'chose', 'chosen', ],
]

while tt:
    print(len(tt))
    word = tt[random.randint(0, len(tt) - 1)]
    tt.remove(word)
    input(word[0])
    print(f'{word[1]} {word[2]}')
    print('\n')
    time.sleep(1)
