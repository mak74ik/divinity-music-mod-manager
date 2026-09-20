# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

BASE_DIR = os.path.abspath(os.getcwd())

datas = [
    (os.path.join(BASE_DIR, 'web'), 'web'),
    (os.path.join(BASE_DIR, 'assets'), 'assets'),
    (os.path.join(BASE_DIR, 'core', 'tracks_data.json'), 'core'),
    (os.path.join(BASE_DIR, 'bin'), 'bin'),
]

hiddenimports = [
    'bottle',
    'lz4',
    'lz4.block',
    'pywebview',
    'proxy_tools',
    'core',
    'core.taxonomy',
    'core.convert_ogg_to_wem',
    'core.wem_encoder',
    'core.lspk_packer',
]

if sys.platform == 'darwin':
    hiddenimports.append('pywebview.platforms.cocoa')
elif sys.platform == 'win32':
    hiddenimports.extend(['pywebview.platforms.winforms', 'pywebview.platforms.edgechromium', 'clr'])
else:
    hiddenimports.extend(['pywebview.platforms.gtk', 'pywebview.platforms.qt'])

a = Analysis(
    ['app.py'],
    pathex=[BASE_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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

exe_icon = os.path.join(BASE_DIR, 'assets', 'app_icon.icns') if sys.platform == 'darwin' else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DivinityMusicManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=exe_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DivinityMusicManager',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Divinity Music Mod Manager.app',
        icon=os.path.join(BASE_DIR, 'assets', 'app_icon.icns'),
        bundle_identifier='com.mizuqa.divinitymusicmanager',
        info_plist={
            'CFBundleDisplayName': 'Divinity Music Mod Manager',
            'CFBundleName': 'Divinity Music Mod Manager',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '11.0.0',
        }
    )
