d = {}
string = input().split(' ')
for word in string:
    cnt = string.count(word)
    d[word] = cnt
print(d.items())