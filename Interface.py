import json
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]), relative_path)


userName = os.path.normpath(sys.argv[0]).split(os.path.sep)[2]
if not os.path.exists(f'/Users/{userName}/Library/Application Support/FileBreakerApp'):
    os.mkdir(f'/Users/{userName}/Library/Application Support/FileBreakerApp')
    with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'w') as json_file:
        json.dump({
            "pythonPath": '/usr/bin/python3.8',
            "downloadsFolder": None,
            "userName": userName,
            "botChannel": None
        }, json_file, indent=0)
elif not os.path.exists(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json'):
    with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'w') as json_file:
        json.dump({
            "pythonPath": '/usr/bin/python3.8',
            "downloadsFolder": None,
            "userName": userName,
            "botChannel": None
        }, json_file, indent=0)
with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)


def getFile():
    filename = filedialog.askopenfilename(title="Select file to upload:")
    goodFilePath = filename.replace(' ', '\ ')
    os.system(
        f"{userInfo['pythonPath']} {resource_path('Uploader.py')} {goodFilePath}")


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
    def __init__(self, parent, controller):
        tk, Frame.__init__(self, parent)
        self.controller = controller
        upload_label = Label(self, text='Select file to upload:')
        upload_button = Button(self, text="Upload", command=getFile)
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        upload_label.pack()
        upload_button.pack()


class DownloadPage(tk.Frame):
    def refreshList(self):
        if not userInfo['pythonPath'] == None:
            for i in self.buttonList:
                i.pack_forget()
            os.system(
                f"{userInfo['pythonPath']} {resource_path('Downloader.py')} query")
            currentChoicesPath = f'/Users/{userName}/Library/Application Support/FileBreakerApp/currentChoices.json'
            with open(currentChoicesPath, 'r') as json_file:
                fileList = json.load(json_file)
            self.buttonList = []
            for file in fileList:
                this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
                self.buttonList += [this_button]
            for button in self.buttonList:
                button.pack()

    def downloadFile(self, fileName: str, pieceNum):
        if not userInfo['pythonPath'] is None or not userInfo['downloadsFolder'] is None or not userInfo[
                                                                                                    'userName'] is None:
            os.system(
                f"{userInfo['pythonPath']} {resource_path('Downloader.py')} \"download\" \"{fileName.replace(' ', '_')}\" \"{pieceNum}\"")
            if not os.path.exists(f'{userInfo["downloadsFolder"]}/Discord File Pieces'):
                os.mkdir(f'{userInfo["downloadsFolder"]}/Discord File Pieces')
            filePieces = os.listdir(f'{userInfo["downloadsFolder"]}/Discord File Pieces')
            filePieces.sort()
            realFileName = filePieces[0][:filePieces[0].index('_piece')]
            fileBytes = b''
            for piece in filePieces:
                with open(f'{userInfo["downloadsFolder"]}/Discord File Pieces/{piece}', 'rb') as txt:
                    fileBytes += txt.read()
                    os.rename(f'{userInfo["downloadsFolder"]}/Discord File Pieces/{piece}',
                              f'/Users/{userInfo["userName"]}/.Trash/{piece}')
            with open(f'{userInfo["downloadsFolder"]}/{realFileName}', 'wb') as writer:
                writer.write(fileBytes)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Here's what you can download")
        if not userInfo['pythonPath'] == None: #make this an and
            if not os.system(
                    f"{userInfo['pythonPath']} {resource_path('Downloader.py')} query") == 4: #if certificates are already installed
                currentChoicesPath = f'/Users/{userName}/Library/Application Support/FileBreakerApp/currentChoices.json'
                with open(currentChoicesPath, 'r') as json_file:
                    fileList = json.load(json_file)
            else: #if certs aren't installed, the app isn't going to work
                fileList = []
                warning = Label(self, text="QUIT AND RELAUNCH THE APP BEFORE DOING ANYTHING ELSE. It isn't bad for your computer or anything, but the app won't work until you reopen.")
                warning.pack()
        self.buttonList = []
        for file in fileList:
            this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
            self.buttonList += [this_button]
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
    def get_filename(self):
        filename = filedialog.askopenfilename(title="Select file:")
        if filename == '':
            userInfo['pythonPath'] = '/usr/bin/python3.8'
        else:
            userInfo['pythonPath'] = filename

    def submit(self, botChannel, userInfo):
        userInfo["botChannel"] = botChannel
        userInfo["downloadsFolder"] = f'/Users/{userName}/Downloads'
        userInfo["userName"] = userName
        with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'w') as json_file:
            json.dump(userInfo, json_file, indent=0)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        userInfo = {}
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
        submit = Button(self, text="Submit", command=lambda: self.submit(channelID, userInfo))
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        explanation.pack()
        pyLabel.pack()
        pyPathButton.pack()
        channelIDLabel.pack()
        botChannel.pack()
        submit.pack()


if __name__ == "__main__":
    app = App()
    currentChoicesPath = f'/Users/{userName}/Library/Application Support/FileBreakerApp/currentChoices.json'
    with open(resource_path('currentChoices.json'), 'r') as txt:
        with open(currentChoicesPath, 'w') as json_file:
            json_file.write(txt.read())
    app.mainloop()
