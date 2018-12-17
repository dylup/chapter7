import os

def run(**args):
    print "[*] In shadow module"

    with open('/etc/shadow', 'r') as file:
        data = file.read()

    file.close()
    return data