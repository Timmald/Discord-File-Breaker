import asyncio as aio
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import GlobalVars  # So I can modify globals
from Downloader import query, download
from GlobalVars import *  # So I can use globals
from Uploader import upload
from installCerts import installCerts
import certifi


class App(Tk):
    """
    The interface of the app.
    It instantiates the window,
    and also fills the dict ``frames`` with all of the pages of the app for easy referncing and manipulation later.
    FYI, class ``Tk`` represents a ``tkinter`` app
    """
    def __init__(self, *args, **kwargs):
        """
        Called at the bottom of the file when ``app`` is instantiated

        I got most of this one from StackOverflow btw
        """
        Tk.__init__(self, *args, **kwargs)  # Inheritance! Instantiate a tkinter app
        self.container = Frame(self)  # This frame holds every other element in the app
        self.container.pack(side="top", fill="both", expand=True)  # the frame has now been placed in the window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Are these last two lines important? Probably
        self.title('Discord FileBreaker')
        # Now the blank window has been configured. time to get interesting!
        self.frames = {}
        for F in (StartPage, UploadPage, DownloadPage, AboutPage, SettingsPage):
            # Confusing, right? Well, in python, classes can be treated like variables.
            # Crazy, I know. So this just applies those things to all of those classes in the tuple
            # Each class in the tuple is a page of the app
            page_name = F.__name__  # Name of page should be name of class
            frame = F(parent=self.container, controller=self)  # Calls the constructor of class F, because they all take the same params
            self.frames[page_name] = frame  # Store tha page object so it can be accessed with its page name. Smort.
            frame.grid(row=0, column=0, sticky="nsew")  # place the page in the app
        self.show_frame("StartPage")  # Show the starting page

    def show_frame(self, page_name):
        """
        Raises the indicated page to the top of the pile such that the user can navigate to it

        :param page_name: The key of the page you want to navigate to (the name of the class of that page)
        """
        frame = self.frames[page_name]  # Get the desired page from the dictionary with the pages
        frame.tkraise()  # raise it above all the other pages so it can be interacted with
        # IMPORTANT: The pages aren't brought to life separately. They all exist at once, just stacked on top of each other. This method brings whichever one you want to the top to give the appearance of birthing it.


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
        aio.run(upload(filename))

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
    def generateButtons(self):
        aio.run(query())
        self.buttonList = []
        for file in GlobalVars.fileList:
            buttonName = f'{file["fileName"]}; Uploaded at {file["uploadDate"]}'
            this_button = Button(self, text=buttonName, command=lambda: aio.run(download(file["fileName"])))
            self.buttonList += [this_button]
        for button in self.buttonList:
            button.pack()

    def refreshList(self):
        for i in self.buttonList:
            i.pack_forget()
        self.generateButtons()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Here's what you can download")
        label.pack(side="top", fill="x", pady=10)
        self.generateButtons()
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
    # This is where the app starts
    if isFirstTime:
        # if the application support folder doesn't exist, we assume it's the first time you're using the app
        installCerts()  # go over to installCerts.py to see what that does
        os.mkdir(appSupportFolder)  # creates /Library/Application Support/FileBreakerApp
        userInfo = {
            "botChannel": 939234547906777139  # default is bot channel ID for the test server
        }
        # TODO: this can be one variable, also default to nick's in future versions
        GlobalVars.botChannelID = userInfo["botChannel"]  # modify runtime record of botChannelID
        with open(userInfoPath, 'w') as info_writer:
            json.dump(userInfo, info_writer, indent=0)
        # saves the botChannelID for future openings of the app
        # TODO: Rename the file and maybe just make it a txt file because it holds one thing
        os.mkdir(f'{appSupportFolder}/filePieces')
        # this folder stores chunks that get uploaded to discord
    else:
        # this code runs most of the time, assuming this isn't their first time opening the app
        os.environ["SSL_CERT_FILE"] = certifi.where()  # this environment variable has to be set so that when the SSL certificates are getting verified, it knows to look at certifi.where()
        # certifi.where() is where the imported SSL certs are stored
        with open(userInfoPath, 'r') as info_reader:
            userInfo = json.load(info_reader)
        GlobalVars.botChannelID = userInfo["botChannel"]
        # If it isn't their first opening, there is already a default botChannel ID saved, so read that and set the runtime record of it
    app = App()  # Documentation on top of file
    # the app class creates instances of all the pages of the app, basically
    app.mainloop()  # This runs the entire time the app is open. It is the main process that calls all the other functions as the user does stuff.
