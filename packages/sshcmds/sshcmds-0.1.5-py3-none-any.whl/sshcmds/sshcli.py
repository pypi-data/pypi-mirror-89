"""
This main function calls upon sshcmds to execute a command and print the result.
"""
from sshcmds import SSHCmds
import sys 
import os

def main():
    ssh = SSHCmds() 
    command = str(input("What command would you like to execute? "))
    print("executing command...")
    info = ssh.execute_command(command)
    print(info)
    
if __name__ == "__main__":
    main()