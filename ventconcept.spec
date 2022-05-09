# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew


block_cipher = None

a = Analysis(['ventconcept.py'],
             pathex=['C:\\Users\\rafap\\Documents\\Studium\\Master\\VentPython', 'C:\\Users\\rafap\\Documents\\Studium\\Master\\VentPython\\venv\\Lib\\site-packages'],
             binaries=[],
             datas=[('ventconcept.kv', '.'), ('ventconcept.ico', '.'), ('./images/button_logos/*.png', r'\images\button_logos'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\epw_files', r'\epw_files'), ('./images/*.png', 'image_compass'), ('./epw_files', '.'), ('./images/*.png', 'images'), ('./experimental_results', r'\results'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\ladybug\config.json', r'\venv\Lib\site-packages\ladybug'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_energy\config.json', r'\venv\Lib\site-packages\honeybee_energy'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee\config.json', r'\venv\Lib\site-packages\honeybee'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_standards', r'\venv\Lib\site-packages\honeybee_standards'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_standards\schedules\user_library.json', r'\venv\Lib\site-packages\honeybee_standards\schedules'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_standards\programtypes\user_library.json', r'\venv\Lib\site-packages\honeybee_standards\programtypes'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_standards\energy_default.json', r'\venv\Lib\site-packages\honeybee_standards'), (r'C:\Users\rafap\Documents\Studium\Master\VentPython\venv\Lib\site-packages\honeybee_energy\measures\honeybee_openstudio_gem\lib', r'\venv\Lib\site-packages\honeybee_energy\measures\honeybee_openstudio_gem\lib')],
             hiddenimports=['win32file','win32timezone'],
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
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='VentConcept',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='ventconcept.ico' )

