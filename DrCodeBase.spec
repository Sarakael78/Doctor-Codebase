from PyInstaller.utils.hooks import collect_all
import os

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collect data, binaries, and hidden imports for gradio and PyYAML
gradio_data, gradio_binaries, gradio_hiddenimports = collect_all('gradio')
pyyaml_data, pyyaml_binaries, pyyaml_hiddenimports = collect_all('PyYAML')

# Analysis section: Specify the main script and paths
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=gradio_binaries,
    datas=[
        *gradio_data,  # Include gradio data files
        *pyyaml_data,  # Include PyYAML data files
        ('config.yaml', '.'),
        ('modules/', 'modules/'),
        # Using the original os.path.join(...) expression 
        # to include types.json from your virtual environment
        (os.path.join(os.environ.get('VIRTUAL_ENV', ''),
                     'Lib', 'site-packages', 'gradio_client', 'types.json'),
         'gradio_client'),  
    ],
    hiddenimports=[
        *gradio_hiddenimports,  # Include gradio hidden imports
        *pyyaml_hiddenimports,  # Include PyYAML hidden imports
        'gradio',  # Explicitly include gradio
        'gradio.routes',
        'gradio.blocks',
        'gradio.components', 
        'gradio.themes',
        'gradio.utils',
        'gradio.blocks_events',  
        'debugpy',
        'yaml',   # Add this for PyYAML
        'PyYAML',
        'multiprocessing.Lock',  # Add this for multiprocessing.Lock 
        # Add any other missing modules here if needed
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Create Python ZIP archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable build configuration
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DrCodeBase',
    debug=False,  # Set to False for a smaller final build 
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True  
)

# Collect files and dependencies into the distribution directory
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DrCodeBase'
)