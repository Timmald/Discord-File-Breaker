import datetime
import os
import json
import sys
from zoneinfo import ZoneInfo


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]),relative_path)

userName=os.path.normpath(sys.argv[0]).split(os.path.sep)[2]
with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)

class SplitFile:
    def __init__(self,path:os.PathLike):
        self.path=path
        self.name=os.path.basename(path)
        self.chunks=self.splitFile()
        self.writeSplitFile()
        self.fullName=json.dumps([f'{self.name}; Uploaded at {datetime.datetime.now(tz=ZoneInfo("America/New_York")).strftime("%c")}',len(self.chunks)])
        self.chunkNames=[f'{self.name} piece #{i+1}.txt' for i in range(len(self.chunks))]
    def splitFile(self):
        with open(self.path, 'rb') as img:
            bytesboi = img.read()
            filePieceList = []
            index=0
            for i in range(int(len(bytesboi) / 8000000)):
                filePieceList += [bytesboi[8000000 * i:8000000 * (i + 1)]]
                index=i
            filePieceList += [bytesboi[8000000 * (index + 1):]]
            return filePieceList

    def writeSplitFile(self):
        index = 0
        for i in self.chunks:
            with open(f'/Users/{userInfo["userName"]}/Library/Application Support/FileBreakerApp/filePieces/{self.name} piece #{index+1}.txt', 'wb') as txt:
                txt.write(i)
            index += 1