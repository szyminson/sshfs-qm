#!/usr/bin/env python3
# coding=utf-8

import signal
import subprocess
import json
import getpass
from os.path import expanduser, ismount

def signal_handler(signal, frame):
    print('\n')
    raise SystemExit

def main():
    with open(expanduser('~') + '/.qm/config.json') as f:
        config = json.load(f)

    for index, server in enumerate(config['servers']):
        server['mounted'] = ismount(server['mount'].replace('~', expanduser('~')))
        line = '[' + str(index) + ']'
        if server['mounted']:
            line += ' [mounted]'
        line += ' ' + server['name']
        print(line)
    
    server = input('Choose server to mount / unmount: ')
    server = config['servers'][int(server)]

    if server['mounted']:
        print('Unmounting', server['name'], 'from', server['mount'])

        umount_command = 'umount ' + server['mount']
        subprocess.call(umount_command, shell = True)
        
    else:
        print('Mounting', server['name'], 'at', server['mount'])

        mkdir_command = 'mkdir -p ' + server['mount']
        sshfs_command = 'sshfs -o ' + config['options'] + ' -p ' + str(server['port'])
        sshfs_command += ' ' + server['user'] + '@' + server['host'] + ':' + server['dir']
        sshfs_command += ' ' + server['mount']

        subprocess.call(mkdir_command, shell = True)
        subprocess.call(sshfs_command, shell = True)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
