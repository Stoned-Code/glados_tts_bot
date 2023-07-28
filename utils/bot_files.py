import os

def read_token(token):
    if not os.path.exists(token): # Checks if the token path exists.
        raise Exception('\'{}\' not defined.'.format(token)) # Raises an exception if the token doesn't exist.

    with open(token, 'r') as f:
        token = f.read() # Reads the token from the file path.

    return token # Returns the token.


def init_folder(path):
    if os.path.exists(path):
        return
    
    else:
        os.mkdir(path)
