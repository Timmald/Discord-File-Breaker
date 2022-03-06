import datetime
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]), relative_path)


homeDir = str(Path.home())
appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
with open(f'{appSupportFolder}/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)


class SplitFile:
    def __init__(self, path: os.PathLike):
        self.path = path
        self.name = os.path.basename(path)
        self.chunks = self.splitFile()
        self.writeSplitFile()
        self.fullName = json.dumps(
            [f'{self.name}; Uploaded at {datetime.now().strftime("%c")}',
             len(self.chunks)])
        self.chunkNames = [f'{self.name} piece #{i + 1}.txt' for i in range(len(self.chunks))]

    def splitFile(self) -> list:
        with open(self.path, 'rb') as img:
            bytesboi = img.read()
            filePieceList = []
            for i in range(int(len(bytesboi) / 8000000)):
                filePieceList += [bytesboi[8000000 * i:8000000 * (i + 1)]]
            filePieceList += [bytesboi[8000000 * (i + 1):]]
            return filePieceList

    def writeSplitFile(self):
        index = 0
        for i in self.chunks:
            with open(
                    f'{appSupportFolder}/filePieces/{self.name} piece #{index + 1}.txt',
                    'wb') as txt:
                txt.write(i)
            index += 1
