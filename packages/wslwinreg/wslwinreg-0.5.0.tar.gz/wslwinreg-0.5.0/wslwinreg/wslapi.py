#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that implements winreg for Windows Subsystem for Linux
"""

## \package wslwinreg.wslapi

import os
import subprocess
import socket

_TCP_IP = '127.0.0.1'
_BUFFER_SIZE = 1024
_WIN_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)),
    'src',
    'bin')

print(_WIN_DIR)
_WIN_EXE = os.path.join(_WIN_DIR, 'backendv19w64ltc.exe')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((_TCP_IP, 0))
port = s.getsockname()[1]
s.listen(1)
tempfp = subprocess.Popen(
    (_WIN_EXE, '-p', str(port)),
    cwd=_WIN_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    universal_newlines=True)
conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(_BUFFER_SIZE)
    if not data:
        break
    print("received data:", data)
    conn.send(data)  # echo
conn.close()
