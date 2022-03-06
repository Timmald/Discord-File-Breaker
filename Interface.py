import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import sys
from shutil import copyfile
from Downloader import query, download
from Uploader import uploader
from ssl import SSLCertVerificationError
import asyncio as aio


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]), relative_path)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title('Discord FileBreaker')
        self.frames = {}
        for F in (StartPage, UploadPage, DownloadPage, AboutPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        uPage = tk.Button(self, text="Upload Stuff", command=lambda: controller.show_frame("UploadPage"))
        dPage = tk.Button(self, text="Download Stuff", command=lambda: controller.show_frame("DownloadPage"))
        refresh = Button(self, text="Refresh Downloads List",
                         command=lambda: self.controller.frames["DownloadPage"].refreshList())
        settings = Button(self, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        aPage = Button(self, text="About the App", command=lambda: self.controller.show_frame("AboutPage"))
        uPage.pack()
        dPage.pack()
        refresh.pack()
        aPage.pack()
        settings.pack()


class UploadPage(tk.Frame):
    @staticmethod
    def uploadFile():
        filename = filedialog.askopenfilename(title="Select file to upload:")
        loop = aio.new_event_loop()
        loop.run_until_complete(uploader(filename))
        loop.close()

    def __init__(self, parent, controller):
        tk, Frame.__init__(self, parent)
        self.controller = controller
        upload_label = Label(self, text='Select file to upload:')
        upload_button = Button(self, text="Upload", command=self.uploadFile)
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        upload_label.pack()
        upload_button.pack()


class DownloadPage(tk.Frame):
    def refreshList(self):
        for i in self.buttonList:
            i.pack_forget()
        loop = aio.new_event_loop()
        loop.run_until_complete(query())
        loop.close()
        with open(currentChoicesPath, 'r') as json_file:
            fileList = json.load(json_file)
        self.buttonList = []
        for file in fileList:
            this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
            self.buttonList += [this_button]
        for button in self.buttonList:
            button.pack()

    @staticmethod
    def downloadFile(fileName: str, pieceNum):
        loop = aio.new_event_loop()
        loop.run_until_complete(download(fileName.replace(" ", "_"), pieceNum))
        loop.close()
        filePieceFolderPath = f'{userInfo["downloadsFolder"]}/Discord File Pieces'
        filePieces = os.listdir(filePieceFolderPath)
        filePieces.sort()
        realFileName = filePieces[0][:filePieces[0].index('_piece')]
        fileBytes = b''
        for piece in filePieces:
            piecePath = f'{filePieceFolderPath}/{piece}'
            with open(piecePath, 'rb') as txt:
                fileBytes += txt.read()
                os.rename(piecePath,
                          f'{homeDir}/.Trash/{piece}')
        with open(f'{userInfo["downloadsFolder"]}/{realFileName}', 'wb') as writer:
            writer.write(fileBytes)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Here's what you can download")
        try:
            loop = aio.new_event_loop()
            loop.run_until_complete(query())
            loop.close()
            with open('currentChoices.json', 'r') as choices_reader:
                fileList = json.load(choices_reader)
        except SSLCertVerificationError:
            fileList = []
            warning = Label(self,
                            text="QUIT AND RELAUNCH THE APP BEFORE DOING ANYTHING ELSE. It isn't bad for your computer or anything, but the app won't work until you reopen.")
            warning.pack()
            popUp = Toplevel(self)
            Label(popUp,
                  text='CLOSE APP NOW. It isn\'t serious, but you need to restart the app for it to work.').pack()
        self.buttonList = []
        for file in fileList:
            this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
            self.buttonList.append(this_button)
        label.pack(side="top", fill="x", pady=10)
        for button in self.buttonList:
            button.pack()
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        aboutText = Label(self,
                          text="How to use:\nTo upload file, go to upload page and select a file to upload.\nYou can download any of the 10 most recent files from the downloads menu (if needed I'll reship the app with search capability, but it would b SLOW\nIMPORTANT: If someone just uploaded a file and you want to download it, you have to go back to main menu and refresh downloads list.\nAnd don't worry if it freezes for a bit, discord is slow when dealing with files. Shouldn't be more than 30 seconds, unless u r uploading or downloading something huge")
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        aboutText.pack()


class SettingsPage(tk.Frame):
    @staticmethod
    def get_filename():
        filename = filedialog.askopenfilename(title="Select file:")
        if not filename == '':
            userInfo['pythonPath'] = filename

    @staticmethod
    def submit(botChannel):
        userInfo["botChannel"] = botChannel
        with open(userInfoPath, 'w') as json_file:
            json.dump(userInfo, json_file, indent=0)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        explanation = Label(self,
                            text="You only need this page once, to be used before you use the main app for the first time. Quit and reopen the app after you submit")
        pyLabel = Label(self,
                        text="Find where your version of python3.9 is located.\nIf you don't know how to find it, go to top menu of finder -> go -> go to folder and then enter /usr\n It is most likely either in /usr/local/bin or /usr/bin\n just look for a file literally called python3.9\nAnd get Nathan to send it to you and put it in /usr/bin if you don't have it, but you still have to enter that here\n if you only have 3.8, use that and nothing should go wrong")
        pyPathButton = Button(self, text="Find python3.9", command=lambda: self.get_filename())
        channelIDLabel = Label(self,
                               text="If you're not on Nick's server, enter the channel ID of the bot channel here. Otherwise, leave blank\n(click below to type)")
        botChannel = Text(self, height=1, borderwidth=1)
        try:
            channelID = int(botChannel.get("1.0", "end-1c"))
        except ValueError:
            channelID = 746803793408163898
        submit = Button(self, text="Submit", command=lambda: self.submit(channelID))
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        explanation.pack()
        pyLabel.pack()
        pyPathButton.pack()
        channelIDLabel.pack()
        botChannel.pack()
        submit.pack()


if __name__ == "__main__":
    homeDir = str(Path.home())  # homeDir, for example, is /Users/nathanwolf
    AppSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
    userInfoPath = f'{AppSupportFolder}/userInfo.json'
    currentChoicesPath = f'{AppSupportFolder}/currentChoices.json'
    isFirstTime = not os.path.exists(AppSupportFolder)
    if isFirstTime:
        os.mkdir(AppSupportFolder)  # folder is made
        copyfile(resource_path('currentChoices.json'),
                 f'{AppSupportFolder}/currentChoices.json')  # currentChoices is in folder
        with open(f'{AppSupportFolder}/userInfo.json', 'w') as info_writer:
            if homeDir == '/Users/nathanwolf':
                userInfo = {
                    "pythonPath": '/usr/local/bin/python3.8',
                    "downloadsFolder": f'{homeDir}/Downloads',
                    "botChannel": 939234547906777139
                }
            else:
                userInfo = {
                    "pythonPath": '/usr/bin/python3.8',
                    "downloadsFolder": f'{homeDir}/Downloads',
                    "botChannel": 939234547906777139
                }
            json.dump(userInfo, info_writer, indent=0)
        # dump all the default values for stuff into the userInfo.json
        # just a fun note, once u eliminate all the os.systems, the userInfo can just be a variable in one file that gets imported
        os.mkdir(f'{AppSupportFolder}/filePieces')
    else:
        with open(f'{AppSupportFolder}/userInfo.json', 'r') as info_reader:
            userInfo = json.load(info_reader)
    app = App()
    app.mainloop()
