#
def getMode():
    while True:
        print('Do you wish to encrypt or decrypt or brute-force a message?')
        mode = input().lower()

        if mode in ['encrypt', 'e', 'decrype', 'd', 'brute', 'b']:
            return mode
        else:
            print('Enter either "encrypt" or "e" or "decrypt" or "d" or "brute" or "b".')

def getMessage():
    print('Enter your message:')
    return input()

def getKey():
    key = 0
    while True:
        print('Enter the key number (1-%s)' % (MAX_KEY_SIZE))
        key = int(input())
        if (key >= 1 and key <=  MAX_KEY_SIZE):
            return key

def getTranslatedMsg(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = '' #containS the string of the result:

    for symbol in message:
        symbolIndex = SYMBOLS.find(symbol)
        if symbolIndex == -1: # Symbol not found in SYMBOLS.
            translated +=  symbol # Just add this symbol without any change.
        else:
            symbolIndex += key

            # wrap around to the beginning of the list at 0
            if symbolIndex >= len(SYMBOLS):
                symbolIndex -= len(SYMBOLS)
            elif symbolIndex < 0:
                symbolIndex +=  len(SYMBOLS)

            translated += SYMBOLS[symbolIndex]

    return translated
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
#SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890!@#$%^&*()'
MAX_KEY_SIZE = len(SYMBOLS)
mode = getMode()
message = getMessage()

if mode[0] != 'b':
    key = getKey()

print('Your translated text is:')
if mode[0] != 'b':
    print(getTranslatedMsg(mode, message, key))
else:
    for key in range(1, MAX_KEY_SIZE + 1):
        print(key, getTranslatedMsg('decrypt', message, key))