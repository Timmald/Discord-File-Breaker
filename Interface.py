import asyncio as aio
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import GlobalVars  # So I can modify globals
from Downloader import query, download
from GlobalVars import *  # So I can use globals
from Uploader import uploader
from installCerts import installCerts
import certifi

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)
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


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        uPage = Button(self, text="Upload Stuff", command=lambda: controller.show_frame("UploadPage"))
        dPage = Button(self, text="Download Stuff", command=lambda: controller.show_frame("DownloadPage"))
        refresh = Button(self, text="Refresh Downloads List",
                         command=lambda: self.controller.frames["DownloadPage"].refreshList())
        settings = Button(self, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        aPage = Button(self, text="About the App", command=lambda: self.controller.show_frame("AboutPage"))
        uPage.pack()
        dPage.pack()
        refresh.pack()
        aPage.pack()
        settings.pack()


class UploadPage(Frame):
    @staticmethod
    def uploadFile():
        filename = askopenfilename(title="Select file to upload:")
        aio.run(uploader(filename))

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        upload_label = Label(self, text='Select file to upload:')
        upload_button = Button(self, text="Upload", command=self.uploadFile)
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        upload_label.pack()
        upload_button.pack()


class DownloadPage(Frame):
    def refreshList(self):
        for i in self.buttonList:
            i.pack_forget()
        aio.run(query())
        self.buttonList = []
        for file in GlobalVars.fileList:
            this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
            self.buttonList += [this_button]
        for button in self.buttonList:
            button.pack()

    @staticmethod
    def downloadFile(fileName: str, pieceNum):
        aio.run(download(fileName.replace(" ", "_"), pieceNum))

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Here's what you can download")
        aio.run(query())
        self.buttonList = []
        for file in GlobalVars.fileList:
            this_button = Button(self, text=file[0], command=lambda: self.downloadFile(file[0], file[1]))
            self.buttonList.append(this_button)
        label.pack(side="top", fill="x", pady=10)
        for button in self.buttonList:
            button.pack()
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()


class AboutPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        aboutText = Label(self,
                          text="How to use:\nTo upload file, go to upload page and select a file to upload.\nYou can download any of the 10 most recent files from the downloads menu (if needed I'll reship the app with search capability, but it would b SLOW\nIMPORTANT: If someone just uploaded a file and you want to download it, you have to go back to main menu and refresh downloads list.\nAnd don't worry if it freezes for a bit, discord is slow when dealing with files. Shouldn't be more than 30 seconds, unless u r uploading or downloading something huge")
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        aboutText.pack()


class SettingsPage(Frame):
    @staticmethod
    def submit(newBotChannel):
        channelID = int(newBotChannel.get("1.0", "end-1c"))
        userInfo["botChannel"] = channelID
        with open(userInfoPath, 'w') as json_file:
            json.dump(userInfo, json_file, indent=0)
        GlobalVars.botChannelID = channelID

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        channelIDLabel = Label(self,
                               text="If you're not on Nick's server, enter the channel ID of the bot channel here. Otherwise, leave blank\n(click below to type)")
        botChannel = Text(self, height=1, borderwidth=1)
        submit = Button(self, text="Submit", command=lambda: self.submit(botChannel))
        back_button = Button(self, text="<-", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()
        channelIDLabel.pack()
        botChannel.pack()
        submit.pack()


if __name__ == "__main__":
    if isFirstTime:
        installCerts()
        os.mkdir(appSupportFolder)  # folder is made
        userInfo = {
            "botChannel": 939234547906777139
        }
        GlobalVars.botChannelID = userInfo["botChannel"]
        with open(userInfoPath, 'w') as info_writer:
            json.dump(userInfo, info_writer, indent=0)
        os.mkdir(f'{appSupportFolder}/filePieces')
    else:
        os.environ["SSL_CERT_FILE"] = certifi.where()
        with open(userInfoPath, 'r') as info_reader:
            userInfo = json.load(info_reader)
        GlobalVars.botChannelID = userInfo["botChannel"]
    app = App()
    app.mainloop()
