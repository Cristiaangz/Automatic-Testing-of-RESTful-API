import os

if not os.path.isfile("gorest_test/token.txt"):
    token = ''
    while token == '':
        token = input("\n\nToken file not found. Please enter gorest.co.in token:\n")
        if len(token) != 64:
            print("Error: Token must be 64 characters long")
            token = ''
    f = open("gorest_test/token.txt", "w")
    f.write(token)
    f.close()