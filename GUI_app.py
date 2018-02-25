import os
import time
import threading
import tkMessageBox
import tkFileDialog
from ttk             import Style, Button, Label, Entry, Progressbar, Checkbutton
from Tkinter         import Tk, Frame, RIGHT, BOTH, RAISED
from Tkinter         import TOP, X, N, LEFT
from Tkinter         import END, Listbox, MULTIPLE
from Tkinter         import Toplevel, DISABLED
from Tkinter         import ACTIVE, NORMAL
from Tkinter         import StringVar, Scrollbar
from multiprocessing import Queue
from fbchat          import log, client

# encryption
import Encrypt


class GUI(Frame):
    """
        This is the root window
    """

    def __init__(self, parent, client):
        self.queue = Queue()
        # I got sick of filling in the login parameters repeatedly,
        # for the sake of testing I will leave it like this and clear it before finishing the gui
        self.email = "bel@cs.uoregon.edu"
        self.password = "Bob433"
        self.parent = parent
        self.initialized = False
        self.loadWindow  = None
        self.remember    = False
        self.client = None
        self.loginScreen()

    def centerWindow(self,notself=None):
        """
        This centers the window into place
        if notself is set, then it centers
        the notself window

        @param:
            notself - TKobject
        """

        if notself != None: # notself is primarly for progressbar
            sw = self.parent.winfo_screenwidth()
            sh = self.parent.winfo_screenheight()
            x = (sw - self.w/2) / 2
            y = (sh - self.h/2) / 2
            notself.geometry('%dx%d+%d+%d' % (self.w/1.8,self.h/1.8, x,y))
        else:
            sw = self.parent.winfo_screenwidth()
            sh = self.parent.winfo_screenheight()
            x = (sw - self.w) / 2
            y = (sh - self.h) / 2
            self.parent.geometry('%dx%d+%d+%d' % (self.w,self.h, x ,y))

    def startWindow(self):
        """
        This method starts/creates the window for
        the UI
        """
        Frame.__init__(self, self.parent, background="white")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        if(not self.initialized):
            self.centerWindow()
        else:
            self.parent.geometry('%dx%d' % (self.w,self.h))
        self.initialized = True

    def resetWindow(self):
        """
        Resets the window
        """
        if(self.initialized):
            self.destroy()
        if(self.loadWindow != None):
            self.loadWindow.destroy()

        self.startWindow()


    def loginScreen(self):
        """
            First screen that user will see, will require Facebook credentials to be inputted
        """

        # Resetting window
        self.h = 150
        self.w = 350
        self.resetWindow()
        self.parent.title("Welcome")

        # Creating frame that takes in email
        emailFrame = Frame(self)
        emailFrame.pack(fill=X, side=TOP)

        emailLabel = Label(emailFrame, text="Email:", background="white")
        emailLabel.pack(side=LEFT, padx=15, pady=10)

        self.emailEntry = Entry(emailFrame, width=30)
        self.emailEntry.insert(0, self.email)
        self.emailEntry.pack(side=LEFT, padx=35, pady=10)
        # Done with email frame

        # Creating password frame
        passwordFrame = Frame(self)
        passwordFrame.pack(fill=X, side=TOP)

        passwordLabel = Label(passwordFrame, text="Password:", background="white")
        passwordLabel.pack(side=LEFT, padx = 15, pady=10)

        self.passwordEntry = Entry(passwordFrame, show="*", width=30)
        self.passwordEntry.insert(0, self.password)
        self.passwordEntry.pack(side=LEFT, padx=35, pady=10)
        # Done with password frame

        # Creating bottom buttons
        frame = Frame(self, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        exitButton = Button(self, text="Exit", command=self.parent.destroy)
        exitButton.pack(side=RIGHT, padx=5, pady=5)
        self.loginButton = Button(self, text="Log In", command=self.start)
        self.loginButton.pack(side=RIGHT)
        # Done with bottom buttons

    def start(self):
        """
            Initiates login, starts loading screen.
        """
        thread1 = ThreadedTask(self.queue,self.login)
        thread2 = ThreadedTask(self.queue,self.loadingScreen)
        thread2.start()
        thread1.start()

        self.checkThread(thread1,self.chatUI)

    def loadingScreen(self):
        """
        This starts the loading screen
        and disables all buttons
        """
        for i in self.winfo_children():
            if Button == type(i):
                i.configure(state=DISABLED)

        self.loadWindow = Toplevel(self.parent)
        loadingstring   = "Logging in..."
        loadinglabel    = Label(self.loadWindow, text=loadingstring, background="white")
        progressbar     = Progressbar(self.loadWindow, orient= "horizontal", \
                                    length=300, mode="indeterminate")
        progressbar.pack(pady=self.h/10)
        loadinglabel.pack()

        self.centerWindow(self.loadWindow)
        self.loadWindow.title("Wait")
        progressbar.start()

    def login(self):
        """
            Login with the inputted credentials from the loginScreen
        """
        if(self.client is not None):
            if(self.client.isLoggedIn()):
                self.client.logout()
        self.email = self.emailEntry.get()
        self.password = self.passwordEntry.get()

        # This will log into Facebook with the given credentials
        self.client = client.Client(self.email, self.password)

        # NOTE: This is a working print test that will print conversations with latest users
        # users = self.client.fetchAllUsers()
        # for user in users:
        #     print(user.name, user.uid)
        #     messages = self.client.fetchThreadMessages(user.uid)
        #     for message in messages:
        #         print(self.client._fetchInfo(message.author)[message.author]["first_name"], message.text)

    def chatUI(self):
        """
            Chat GUI page
        """
        self.h = 400
        self.w = 700
        self.resetWindow()
        self.parent.title("Messenger")

        messages_frame = Frame(self)

        my_msg = StringVar() # For messages to be sent.
        my_msg.set("Type your messages HERE")

        scrollbar = Scrollbar(messages_frame) # Navigate through past messages

        # Following will contain the messages

        msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.config(command = msg_list.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        msg_list.pack(side=LEFT, fill=BOTH)
        msg_list.pack()
        messages_frame.pack()

        entry_field = Entry(self, textvariable=my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        exitButton = Button(self, text="Exit", command=self.parent.destroy)
        exitButton.pack(side=RIGHT, padx=5, pady=5)
        send_button = Button(self, text="Send", command=self.send)
        send_button.pack(side=RIGHT)

    def send(self):
        return 0

        # Creating frame that takes in email
        # emailFrame = Frame(self)
        # emailFrame.pack(fill=X, side=TOP)

        # emailLabel = Label(emailFrame, text="Email:", background="white")
        # emailLabel.pack(side=LEFT, padx=15, pady=10)

        # self.emailEntry = Entry(emailFrame, width=30)
        # self.emailEntry.insert(0, self.email)
        # self.emailEntry.pack(side=LEFT, padx=35, pady=10)
        # # Done with email frame


    def checkThread(self,thread,function):
        """
        This function checks to see if
        the given thread is dead, if it
        is not, it recalls a new checkThread.
        After the thread is dead, it calls the
        given function

        @param:
            thread   - ThreadedTask
            functoin - a function
        """
        if thread.is_alive():
            self.parent.after(1000, lambda: self.checkThread(thread,function))
        else:
            function()


class ThreadedTask(threading.Thread):
    """
    Used for creating a threaded task
    """
    def __init__(self,queue,function):
        """
        Starts the threaded task

        @param:
            queue    - Queue object
            function - a function
        """
        threading.Thread.__init__(self)
        self.queue    = queue
        self.function = function

    def run(self):
        """
        Runs the function
        """
        self.function()

if __name__ == "__main__":
    # connect to DB

    appPubKey, appPrivKey = Encrypt.genPrivatePublicPair()

    # create GUI
    root = Tk()
    root.resizable(width=False, height=False)
    ex = GUI(root, client)

    # make calls to api to load GUI with relavent information

    root.mainloop()
    # while (not done):
        # check if new message on current conversation
        # if new message:
            # update view

        # wait n units of time

    root.destroy()

