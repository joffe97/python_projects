
# Theta(n)
def checkPalindrom(string):
    if len(string) == 0 or len(string) == 1:
        return True
    elif string[0] == string[-1]:
        return checkPalindrom(string[1:-1])
    else:
        return False


# Theta(n)
def checkPalindromIter(string):
    for k in range(len(string)//2+1):
        if string[k] != string[len(string)-1-k]:
            return False
    return True


if __name__ == '__main__':
    print(checkPalindrom("reer"))
    print(checkPalindromIter("regninger"))
