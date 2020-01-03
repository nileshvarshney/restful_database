x = -123
rev = 0
while x != 0:
    pop = x % 10
    x /= 10
    if x == 0:
        rev = rev * 10 + pop

print(rev)
