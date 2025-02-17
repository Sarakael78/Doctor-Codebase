# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Analysis section: Specify the main script and paths
a = Analysis(
    ['main.py'],  # Entry point of your application
    pathex=[],    # Additional paths if required
    binaries=[],  # Add binary files if necessary
    datas=[       # Include data files or folders explicitly
        ('config.yaml', '.'),  # Copies `config.yaml` to the same location as the executable
        ('modules/', 'modules/'),  # Ensure the `modules` directory is included
    ],
    hiddenimports=[
        'gradio',  # Explicitly include hidden imports
        'debugpy',
        'PyYAML',
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
    name='DB-Doctor-Codebase',  # Name of the generated executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression for smaller file size
    console=True  # Set to False for a GUI application
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
    name='DB-Doctor-Codebase'
)
