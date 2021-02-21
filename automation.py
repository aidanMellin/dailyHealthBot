from datetime import date
import datetime as dt
from time import sleep
import sys

from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def main(run_now):
    '''
    Check if user has already entered their account information. If not, open the pane for entering info, otherwise,
    run automation
    '''    
    credList = []
    with open("secrets.txt","r") as fd:
        if "//" in fd.readline():
                lf.mainloop()

    if not run_now:
            for _ in range(60*60*24):  # loop the whole day
                if dt.datetime.now().hour == 8:  # 24 hour format
                    print("Running Daily Health Screen")
                    break
                else:
                    print("Not time yet, waiting for 30 minutes before checking again")
                sleep(60*30)

    with open("secrets.txt","r") as fd:
        for line in fd:
            line = line.strip().split()
            credList.append(line[2].replace('"',''))
        healthBot(credList[0],credList[1],credList[2])

class healthBot(object):

    def __init__(self,username,password,browser):
        """
        init function for overall class establishing base rules for window as well as driver
        :param username:
        :type username:
        :param password:
        :type password:
        """
        print("Initializing variables")
        super().__init__()
        self.username = username
        self.password = password
        self.browser = browser
        self.browser_options = Options()
        self.browser_options.add_experimental_option("detach", True)  # Make it so the browser doesn't close upon finish
        self._run()

    def _run(self):
        """
        Boot the window, and start login (Separated in case I should implement a GUI pane)
        :return:
        :rtype:
        """
        ffOP = None
        #should probably add the time check here. incorporate progress bar as well?

        if self.browser == "Chrome":
            self.driver = webdriver.Chrome(options=self.browser_options)
        elif self.browser == "Safari":
            self.driver = webdriver.Safari()
        elif self.browser == "Firefox":
            ffOP = webdriver.FirefoxOptions()
            ffOP.set_headless()
            self.driver = webdriver.Firefox(firefox_options = ffOP)
        elif self.browser == "Opera":
            self.driver = webdriver.Opera()

        print("\nBooting Browser")
        sleep(2)
        self.login()

    def login(self):
        """
        logs in using RIT credentials   
        """
        self.driver.get('https://dailyhealth.rit.edu/')
        print("Navigating to dailyhealth.rit.edu\n")
        sleep(3)
        url = self.driver.current_url
        if 'https://shibboleth.main.ad.rit.edu/' in url:
            print("Entering credentials")

            userin = self.driver.find_element_by_xpath('//*[@id="username"]')  # Enter username
            userin.send_keys(self.username)
            print("Username Entered:", self.username)

            pwordin = self.driver.find_element_by_xpath('//*[@id="password"]')  # Enter pword
            pwordin.send_keys(self.password)
            print('Password Entered', ('*' * len(self.password)))

            submitbtn = self.driver.find_element_by_xpath('//*[@id="userInput"]/form/button')  # Submit
            submitbtn.click()
            print("Submitted Login form\n")
            sleep(2)

        self.assessment()

    def assessment(self):
        """
        The thing that actually completes the assessment
        """
        url = self.driver.current_url
        if "https://dailyhealth.rit.edu/?login=true" in url:
            sleep(1)
            print("Beginning Daily Health Assessment")
            agree = self.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[1]/div[2]/div/div/a')
            agree.click()
            print("Clicked Agree")
            sleep(2)
            #div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div
            self.driver.execute_script("window.scrollTo(0, 400)")
            #For some reason noButton (below) does not work when run in headless mode, and as a result, can't be run
            # as such. The noButton has a dynamic css selector, but the Xpath points to supposedly the wrong thing...
            noButton = self.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div')
            noButton.click()
            print("Clicked 'NO'\n")
            sleep(2)

        url = self.driver.current_url
        if 'https://dailyhealth.rit.edu/pass' in url:
            """
            Takes a screenshot if test is successful
            """
            print("Assessment Successful, taking screenshot")
            today = date.today()
            d1 = today.strftime("%d-%m-%Y")
            screen = "screens/"+d1+".png"
            self.driver.save_screenshot(screen)
            print("Screenshot successfully saved as", d1 + ".png")
        else:
            print("Unable to successfully complete daily health test. No screenshot stored")

class LoginFrame(Frame):
    show = False
    pShow = "*"
    
    def __init__(self, master):
        '''
        Initialize entire window, name it, and give the user entry fields for new account information
        :param master:
        '''
        super().__init__(master)

        root.title("Credentials")
        root.geometry("350x150")

        self.var = IntVar()

        Label(self, text="Please enter RIT Account Details\n").grid(row=0, column=1, sticky=E)
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show=self.pShow)
        
        self.showButton = Checkbutton(self, text="show password", variable=self.var, command=self.cb).grid(row=2, column=2)
    
        OptionList = [
        "Chrome",
        "Firefox",
        "Opera",
        "Safari"
        ] 

        self.dropVar = StringVar(root)
        self.dropVar.set(OptionList[0])
        self.opt = OptionMenu(root, self.dropVar, *OptionList)
        self.opt.config(width=90, font=('Helvetica', 12))
        
        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.opt.pack()

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(row=4, columnspan=2)
        self.pack()
        
    def cb(self):
        '''
        Checkbutton event to show / hide password
        :return: None
        :rtype: None
        '''
        if self.pShow == "": #Hide the text
            self.pShow = "*"
        elif self.pShow == "*": #Show the text
            self.pShow = ""
        self.entry_password.config(show=self.pShow) #Configure to show text
    
    def _login_btn_clicked(self):
        '''
        Event after the user submits account information
        :return: None
        :rtype: None
        '''
        username = self.entry_username.get()
        password = self.entry_password.get()
        browser = self.dropVar.get()
        root.destroy()
        self.writeDetails(username, password,browser)
        # print("Browser is",self.dropVar.get())

    def writeDetails(self, u, p,b):
        '''
        Write the new information to secrets.txt file
        :param u: username
        :type u: String
        :param p: password
        :type p: String
        :return: None
        :rtype: None
        '''
        with open("secrets.txt", 'w') as fw:
            fw.write('usernameStudent = "' + u + '"')
            fw.write('\npwordStudent = "' + p + '"')
            fw.write('\nbrowser = "'+b+'"')

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        if "True" in sys.argv[1].title():
            run_now = True
        else:
            run_now = False
    else:
        run_now = False
    while True:
        with open("secrets.txt","r+") as fd:
            if "//" in fd.readline():
                    root = Tk()
                    lf = LoginFrame(root)
        main(run_now)
        run_now = False
        items = list(range(0, 100)) #List of numbers for counting for progress bar
        for item in progressBar(items, prefix = 'Progress:', suffix = 'Complete', length = 100):
            now = dt.datetime.now()
            time_sleep = (dt.timedelta(hours=24) - (now - now.replace(hour=8, minute=30, second=0, microsecond=0))).total_seconds() % (24 * 3600)
            sleep(time_sleep/100) #Progress bar fills by 1% every 1/100 of time_sleep