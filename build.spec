# -*- mode: python ; coding: utf-8 -*-
import shutil

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/octopod/code/octogon-panel'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

for folder in ["assets", "output", "templates", "style", "queries"]:
    try:
        shutil.copytree(f"./{folder}", f"{DISTPATH}/{folder}")
    except Exception:
        pass
