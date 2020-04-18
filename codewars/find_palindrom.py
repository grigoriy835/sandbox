# https://www.codewars.com/kata/5dcde0b9fcb0d100349cb5c0/train/python
def longest_palindrome(s):
    current = ''
    for index in range(0, len(s)):
        center = [index, index]
        i = 1
        while index+i < len(s):
            if s[index+i] == s[index]:
                if index >= i and s[index-i] == s[index]:
                    i += 1
                else:
                    center[1] = index+1
                    break
            else:
                break
        for i in range(0, center[0]+1 if len(s) - center[1] > center[0] else len(s) - center[1]):
            if s[center[0]-i] != s[center[1]+i]:
                i -= 1
                break
        if i*2+1+int(center[0] != center[1]) > len(current):
            current = s[center[0]-i:center[1]+i+1]

    return current


# print(longest_palindrome('s d h d g g'))
# print(longest_palindrome('asdfsadfggfdtr'))
# print(longest_palindrome('asdf kuy'))
# print(longest_palindrome('55567765855'))
# print(longest_palindrome('#$%^$##$#'))
# print(longest_palindrome('dde'))
print(longest_palindrome('ababbab'))
