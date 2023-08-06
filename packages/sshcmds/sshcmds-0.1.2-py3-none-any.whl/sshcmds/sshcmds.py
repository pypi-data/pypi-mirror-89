"""
The sshcmds class establishes an ssh connection 
and runs commands. 
"""

import hvac
import json
import paramiko
import getpass
import sys 
import os
class sshcmds:

    def __init__(self, user=None, password=None, host=None):
        self.user = user
        self.password = password
        self.host = host
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.login() 
        try:
            self.ssh.connect(self.host, port=22, username=self.user, password=self.password)
        except paramiko.ssh_exception.AuthenticationException:
            print("Authentication failed.")
        except paramiko.ssh_exception.BadAuthenticationType:
            print("The server does not allow this authentication type.")
        except:
            print("Cannot connect to the SSH Server.")
    
    def login(self):
        confname = "sshcmds.json"
        if os.path.exists(confname):
            with open(confname) as f:
                try:
                    data = json.load(f)
                    self.host = data['host'] 
                    self.user = data['user']
                    client = hvac.Client(url=data['vaultURL'], token=data['token'])
                    sshpass = client.read(data['keypath'])
                    self.password = sshpass['data']['password']
                except:
                    print("Error reading in " + confname)
        
        if self.host is None:
            self.host = input("Please enter the host: ")
        if self.user is None:
            self.user = input("Please enter your username: ")
        if self.password is None:
            self.password = getpass.getpass(prompt='Please enter your password : ', stream=None) 

    def execute_command(self, command):
        stdin, stdout, sterr = self.ssh.exec_command(command)
        lines = stdout.readlines()
        return lines
    



