# main.spec
# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None


def create_launcher():
    dist_dir = os.path.join(os.getcwd(), 'dist', 'main')
    if sys.platform.startswith('win'):
        batch_content = """@echo off
        "%~dp0\\main.exe" %*
        """
        batch_file = os.path.join(dist_dir, 'codeharvester.bat')
        with open(batch_file, 'w') as f:
            f.write(batch_content)
    else:
        shell_content = """#!/bin/bash
        /usr/local/codeharvester/main "$@"
        """
        shell_file = os.path.join(dist_dir, 'codeharvester')
        with open(shell_file, 'w') as f:
            f.write(shell_content)
        os.chmod(shell_file, 0o755)  # Asegúrate de que el script sea ejecutable

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('static', 'static')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

coll_post_hook = create_launcher()
