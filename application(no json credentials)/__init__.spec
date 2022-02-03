# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\danie\\Documents\\computerscience\\SpeechRecognition\\application'],
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
a.datas += [('app_logo.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\app_logo.png', 'DATA'),
('centre_align.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\centre_align.png', 'DATA'),
('left_align.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\left_align.png', 'DATA'),
(r'right_align.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\right_align.png', 'DATA'),
(r'justify_align.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\justify_align.png', 'DATA'),
(r'redo.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\redo.png', 'DATA'),
(r'undo.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\undo.png', 'DATA'),
(r'text_bold.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\text_bold.png', 'DATA'),
(r'text_colour.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\text_colour.png', 'DATA'),
(r'text_fontcolour.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\text_fontcolour.png', 'DATA'),
(r'text_italics.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\text_italics.png', 'DATA'),
(r'text_underline.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\text_underline.png', 'DATA'),
(r'indent.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\indent.png', 'DATA'),
(r'unindent.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\unindent.png', 'DATA'),
(r'microphone.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\microphone.png', 'DATA'),
(r'font_highlight.png', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\font_highlight.png', 'DATA'),
(r'credentials.json', r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\credentials.json', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='__init__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon=r'C:\Users\danie\Documents\computerscience\SpeechRecognition\application\app_logo.ico')
