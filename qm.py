#!/usr/bin/env python3
# coding=utf-8

import sys
import getopt
import signal
import subprocess
import json
import getpass
from os.path import expanduser, ismount

def signal_handler(signal, frame):
    print('\n')
    raise SystemExit

def display_server_list(servers):
    for index, server in enumerate(servers):
        line = '[' + str(index) + ']'
        if server['mounted']:
            line += ' [mounted]'
        line += ' ' + server['name']
        print(line)

def connect_to(server):
    ssh_command = 'ssh ' + server['user'] + '@' + server['host'] + ' -p ' + str(server['port'])
    subprocess.call(ssh_command, shell = True)

def mount_from(server):

    if server['mounted']:
        print('Unmounting', server['name'], 'from', server['mount'])

        umount_command = 'fusermount -uz ' + server['mount']
        subprocess.call(umount_command, shell = True)
        
    else:
        print('Mounting', server['name'], 'at', server['mount'])

        mkdir_command = 'mkdir -p ' + server['mount']
        sshfs_command = 'sshfs -o ' + config['options'] + ' -p ' + str(server['port'])
        sshfs_command += ' ' + server['user'] + '@' + server['host'] + ':' + server['dir']
        sshfs_command += ' ' + server['mount']

        subprocess.call(mkdir_command, shell = True)
        subprocess.call(sshfs_command, shell = True)

def main(argv):
    with open(expanduser('~') + '/.qm/config.json') as f:
        config = json.load(f)

    for server in config['servers']:
        server['mounted'] = ismount(server['mount'].replace('~', expanduser('~')))

    if len(argv):
        try:
            opts, _ = getopt.getopt(argv,"lm:u:s:")
        except getopt.GetoptError:
            print('Invalid arguments!')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-l':
                display_server_list(config['servers'])
                sys.exit()
            elif opt == '-m':
                server = config['servers'][int(arg)]
                if server['mounted']:
                    print(server['mount'], 'is already a mount point!')
                else:
                    mount_from(server)
            elif opt == '-u':
                server = config['servers'][int(arg)]
                if server['mounted']:
                    mount_from(server)
                else:
                    print(server['mount'], 'is not a mount point!')
            elif opt == '-s':
                server = config['servers'][int(arg)]
                connect_to(server)
    else:
        display_server_list(config['servers'])
        
        selected_server = input('Choose server to mount / unmount: ')
        server = config['servers'][int(selected_server)]
        mount_from(server)
    

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main(sys.argv[1:])
