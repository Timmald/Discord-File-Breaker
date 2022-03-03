import PyInstaller.__main__

PyInstaller.__main__.run(pyi_args=[
    'Interface.py',
    '-w',
    '--add-data=Uploader.py:.',
    '--add-data=Downloader.py:.',
    '--add-data=SplitFile.py:.',
    '--add-data=currentChoices.json:.'
])