import os
import subprocess

def run(**args):
    print "[*] In sysinfo module."

    info = ""
    output = subprocess.check_output("id", stderr=subprocess.STDOUT, shell=True)
    info = "id:" + output + "\n"
    output = subprocess.check_output("ifconfig eth0", stderr=subprocess.STDOUT, shell=True)
    info += "ifconfig:\n" + output + "\n"
    output = subprocess.check_output("uname -a", stderr=subprocess.STDOUT, shell=True)
    info += "uname:" + output + "\n"

    return info

