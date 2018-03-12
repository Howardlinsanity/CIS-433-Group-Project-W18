import os
import time
import sys
import threading
import requests
import tkMessageBox
import tkFileDialog
# encryption
import Encrypt
from ttk             import Style, Button, Label, Entry, Progressbar, Checkbutton
from Tkinter         import Tk, Frame, RIGHT, BOTH, RAISED
from Tkinter         import TOP, X, N, LEFT
from Tkinter         import END, Listbox, MULTIPLE
from Tkinter         import Toplevel, DISABLED
from Tkinter         import ACTIVE, NORMAL
from Tkinter         import StringVar, Scrollbar
from multiprocessing import Queue
from uuid            import uuid1
from random          import choice
from fbchat          import log, client
from fbchat.models   import *
from fbchat.utils    import *
from fbchat.graphql  import *


# Wrapper for the client class just in case we need to modify client to make it work
class gui_client(client.Client):
    def __init__(self, email, password, user_agent=None, max_tries=5, session_cookies=None, logging_level=logging.INFO):
        '''
        Initializes and logs in the client

        :param email: Facebook `email`, `id` or `phone number`
        :param password: Facebook account password
        :param user_agent: Custom user agent to use when sending requests. If `None`, user agent will be chosen from a premade list (see :any:`utils.USER_AGENTS`)
        :param max_tries: Maximum number of times to try logging in
        :param session_cookies: Cookies from a previous session (Will default to login if these are invalid)
        :param logging_level: Configures the `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`_. Defaults to `INFO`
        :type max_tries: int
        :type session_cookies: dict
        :type logging_level: int
        :raises: FBchatException on failed login
        '''

        self.sticky, self.pool = (None, None)
        self._session = requests.session()
        self.req_counter = 1
        self.seq = "0"
        self.payloadDefault = {}
        self.client = 'mercury'
        self.default_thread_id = None
        self.default_thread_type = None
        self.req_url = ReqUrl()
        self.most_recent_message = None
        self.most_recent_messages_queue = Queue()

        if not user_agent:
            user_agent = choice(USER_AGENTS)

        self._header = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : self.req_url.BASE,
            'Origin' : self.req_url.BASE,
            'User-Agent' : user_agent,
            'Connection' : 'keep-alive',
        }

        handler.setLevel(logging_level)

        # If session cookies aren't set, not properly loaded or gives us an invalid session, then do the login
        if not session_cookies or not self.setSession(session_cookies) or not self.isLoggedIn():
            self.login(email, password, max_tries)
        else:
            self.email = email
            self.password = password

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
        if(message_object is not None):
            self.most_recent_message = message_object
            self.most_recent_messages_queue.put(message_object)

    def stopListening(self):
        """Cleans up the variables from startListening"""
        print("Logging off... (This might take a little bit, we swear we're not stealing your info)")
        self.listening = False
        self.sticky, self.pool = (None, None)

    def listen(self, markAlive=True):
        """
        Initializes and runs the listening loop continually

        :param markAlive: Whether this should ping the Facebook server each time the loop runs
        :type markAlive: bool
        """
        self.startListening()
        self.onListening()

        while self.listening and self.doOneListen(markAlive):
            pass

        self.stopListening()

class GUI(Frame):
    '''
    This is the root window
    '''

    def __init__(self, parent, client):
        self.queue = Queue()
        # I got sick of filling in the login parameters repeatedly,
        # for the sake of testing I will leave it like this and clear it before finishing the gui
        self.email = "linnyflow@gmail.com"
        self.password = "AwesomeSauce1997"
        self.name = ""
        self.parent = parent
        self.initialized = False
        self.loadWindow  = None
        self.remember    = False
        self.client = None
        self.msg_list = None
        self.changingConvo = False
        self.loginScreen()

    def centerWindow(self,notself=None):
        '''
        This centers the window into place
        if notself is set, then it centers
        the notself window

        @param:
            notself - TKobject
        '''

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
        '''
        This method starts/creates the window for
        the UI
        '''
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
        '''
        Resets the window
        '''
        if(self.initialized):
            self.destroy()
        if(self.loadWindow != None):
            self.loadWindow.destroy()

        self.startWindow()


    def loginScreen(self):
        '''
        First screen that user will see, will require Facebook credentials to be inputted
        '''

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
        self.passwordEntry.bind("<Return>", self.start)
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

    def start(self,opt=""):
        '''
        Initiates login, starts loading screen.
        '''
        thread1 = ThreadedTask(self.queue,self.login)
        thread2 = ThreadedTask(self.queue,self.loadingScreen)
        thread2.start()
        thread1.start()

        self.checkThread(thread1,self.chatUI)

    def loadingScreen(self):
        '''
        This starts the loading screen
        and disables all buttons
        '''
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
        '''
        Login with the inputted credentials from the loginScreen
        '''
        if(self.client is not None):
            if(self.client.isLoggedIn()):
                self.client.logout()
        self.email = self.emailEntry.get()
        self.password = self.passwordEntry.get()

        # This will log into Facebook with the given credentials
        self.client = gui_client(self.email, self.password)
        print(self.client._fetchInfo(self.client.uid)[self.client.uid].get('first_name'))
        self.thread3 = ThreadedTask(self.queue, self.listen)
        self.thread3.start()

    def listen(self):
        '''
        We start the listening loop 
        '''
        self.client.listen()

    def chatUI(self):
        '''
        Chat GUI page
        '''
        self.h = 350
        self.w = 700
        self.resetWindow()
        self.parent.title("Messenger")

        # We make the chat side of the UI
        self.right_frame = Frame(self)
        self.right_frame.pack(side=RIGHT, fill='y')
        self.messages_frame = Frame(self.right_frame)
        self.messages_frame.pack(side=TOP)

        self.my_msg = StringVar() # For messages to be sent.
        self.my_msg.set("")

        self.msg_scrollbar = Scrollbar(self.messages_frame) # Navigate through past messages

        # Following will contain the messages

        self.msg_list = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.msg_scrollbar.set)
        self.msg_scrollbar.config(command = self.msg_list.yview)
        self.msg_scrollbar.pack(side=RIGHT, fill='y', padx=5)
        self.msg_list.pack(side=RIGHT)

        self.entry_field = Entry(self.right_frame, textvariable=self.my_msg)
        self.send_button = Button(self.right_frame, text="Send", command=self.send)
        self.entry_field.pack(side="top", fill=X, padx=5, pady=5)
        self.send_button.pack(side="top")

        self.exitButton = Button(self.right_frame, text="Exit", command=self.exit)
        self.exitButton.pack(side="bottom", padx=5, pady=5)

        # We make the the side that contains the other users.
        self.left_frame = Frame(self)
        self.left_frame.pack(side=LEFT, fill='y')

        self.usr_scrollbar = Scrollbar(self.left_frame)        
        self.usr_list = Listbox(self.left_frame, height=15, width=50, yscrollcommand=self.usr_scrollbar.set)
        self.usr_scrollbar.config(command = self.usr_list.yview)
        self.usr_search_bar = Entry(self.left_frame, textvariable="")
        self.usr_search_button = Button(self.left_frame, text="Search", command=self.search)

        self.usr_search_bar.pack(side="top", fill=X, pady=2, padx=1)
        self.usr_search_button.pack(side="top", fill=X, pady=2,padx=1)
        self.usr_scrollbar.pack(side=RIGHT, fill='y', padx=5)
        self.usr_list.pack(side=RIGHT, fill='y')

        # The user loading logic is in the search function
        self.search()

        self.usr_list.bind('<Double-1>', self.changeConvo)

    def search(self):
        fresh_users = self.client.fetchAllUsers()
        self.users = []
        if(self.usr_search_bar.get() is not ""):
            for user in fresh_users:
                if(self.usr_search_bar.get() in user.name):
                    self.users.append(user)
        else:
            self.users = fresh_users

        if(self.usr_list.size() is not 0):
            self.usr_list.delete(0,END)

        for user in self.users:
            self.usr_list.insert(END, " " + user.name)

        # By default I would just take the first conversation
        self.currentUser = self.users[0]
        self.usr_search_bar.delete(0, END)

        # print(self.currentUser)
        # messages = self.client.fetchThreadMessages(self.currentUser.uid)
        # self.client.most_recent_message = messages[0]
        # for message in messages:
        #     self.msg_list.insert(0, self.client._fetchInfo(message.author)[message.author]["first_name"] + ": " + message.text)
        # self.msg_list.see(END)

    def send(self):
        '''
        Send messages, will send whatever is in the message field and then clear it
        '''
        message = Message(text=self.entry_field.get())
        self.client.send(message,self.currentUser.uid)
        self.entry_field.delete(0, END)
        self.client.most_recent_message = message
        self.msg_list.insert(0, self.name + ": " + message.text)
        self.msg_list.see(END)

    def changeConvo(self, param):
        '''
        When you click on another user in the chat we update the page
        '''
        print("CHANGING CONVO")
        selectionIndex = self.usr_list.curselection()
        self.currentUser = self.users[selectionIndex[0]]
        self.changingConvo = True
        self.updateConversation()

    def updateConversation(self):
        '''
        Clear the conversation box, reupdate with new conversation, pings facebook server if they got anything
        '''
        if(self.changingConvo):
            print("[updateConversation] we are changing conversation")
            messages = self.client.fetchThreadMessages(self.currentUser.uid)
            self.msg_list.delete(0, END)
            for message in messages:
                self.msg_list.insert(0, self.client._fetchInfo(message.author)[message.author]["first_name"] + ": " + message.text)
            self.msg_list.see(END)
            self.changingConvo = False
        else:
            last_message = self.msg_list.get(END)
            if(self.client is not None and self.client.isLoggedIn() and self.client.most_recent_message is not None):
                msg_object = self.client.most_recent_message
                msg_author = self.client.most_recent_message.author
                name = ""
                if(msg_author is None):
                    msg_author = self.name
                else:
                    name = self.client._fetchInfo(msg_author)[msg_author]["first_name"]

                new_last_message = name + ": " + msg_object.text
                if(last_message != new_last_message):
                    # This is checking if were updating the current convo or refreshing convo
                    if(name + ": " in last_message):
                        while(self.client.most_recent_messages_queue.empty() is not True):
                            message = self.client.most_recent_messages_queue.get()
                            self.msg_list.insert(END, self.client._fetchInfo(message.author)[message.author]["first_name"] + ": " + message.text)
                            self.msg_list.see(END)
                    else:
                        messages = self.client.fetchThreadMessages(self.currentUser.uid)
                        self.msg_list.delete(0, END)
                        for message in messages:
                            self.msg_list.insert(0, self.client._fetchInfo(message.author)[message.author]["first_name"] + ": " + message.text)
                        self.msg_list.see(END)
                        self.client.most_recent_message = messages[0]


    def exit(self):
        '''
        Stops listening and ends GUI
        '''
        self.client.stopListening()
        self.parent.destroy()

    def checkThread(self,thread,function):
        '''
        This function checks to see if
        the given thread is dead, if it
        is not, it recalls a new checkThread.
        After the thread is dead, it calls the
        given function

        @param:
            thread   - ThreadedTask
            functoin - a function
        '''
        if thread.is_alive():
            self.parent.after(1000, lambda: self.checkThread(thread,function))
        else:
            function()

    


class ThreadedTask(threading.Thread):
    '''
    Used for creating a threaded task
    '''
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

def tk_loop(root, ex):
    '''
    Checks for messages every half a second
    '''
    if(ex.msg_list is not None):
        ex.updateConversation()
    root.after(2000, tk_loop, root, ex)

def initiate_tk_loop(root, ex):
    '''
    I honestly don't know how to thread this other than doing this terrible piece of code
    '''
    root.after(2000, tk_loop, root, ex)
    

if __name__ == "__main__":
    # connect to DB

    appPubKey, appPrivKey = Encrypt.genPrivatePublicPair()

    # create GUI
    root = Tk()
    root.resizable(width=False, height=False)
    ex = GUI(root, client)


    # make calls to api to load GUI with relavent information
    initiate_tk_loop(root, ex)
    root.mainloop()


