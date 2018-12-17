import os
import subprocess

def run(**args):
    print "[*] In sysinfo module."

    info = ""
    output = subprocess.check_output("id", stderr=subprocess.STDOUT, shell=True)
    info = "id:\t" + output + "\n\n"
    output = subprocess.check_output("ifconfig eth0", stderr=subprocess.STDOUT, shell=True)
    info += "ifconfig:\t" + output + "\n\n"
    output = subprocess.check_output("uname -a", stderr=subprocess.STDOUT, shell=True)
    info += "uname:\t" + output + "\n\n"

    return info

