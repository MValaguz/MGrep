# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\sorgenti\\MGrep.py'],
             pathex=['MGrep18\\compila'],
             binaries=[],
             datas=[
					('..\\sorgenti\\icons\\*.*','icons'),
					('..\\help\\*.*','help'),
					('..\\sorgenti\\risorse\\*.*','risorse')
			       ],
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
          [],
          exclude_binaries=True,
          name='MGrep',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='..\\sorgenti\\qtdesigner\\icons\\MGrep.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MGrep')
