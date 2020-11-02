from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import cv2
import numpy as np
import pyautogui

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""    

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
    def fileshow(self,**kwargs):
        sm.current = "file"

class FileWindow(Screen):
    # Have to get a default path and store in db for using it next time,
    #  So that he dont wan't to open from root folder
    
    file_selected = ObjectProperty(None)
    # path = 'C:\\Users\\ALBIN\Desktop\\school\\'
    # if file_selected:
    # self.x_val = 2.2
    def select(self,path,selection, *args):
        self.start_rec_button.disabled=False
        # if file_selected:
            # self.x_val = 0.2
        # print("************************")
        # print(path,selection)
        # root_folder = self.user_data_dir
        # print(root_folder,"#############")
        # print(self.FileChooserListView.path)
        try:
            self.label.text = args[1][0]
        except: 
            pass
    def start_recording(self,path,selection,**args):
        if self.start_rec_button.text == "Start Recording":
            
            self.recording = True
            from threading import Thread
            from multiprocessing import Process
            # print(selection[0])
            self.thread = Thread(target=self.do_record, args=[selection[0]])
            self.thread.start()
        if self.start_rec_button.text=="Stop Recording" and self.recording==True:
            self.recording=False
            self.thread.join()
            print("Thread ended")
            self.start_rec_button.text="Start Recording"
            # display screen resolution, get it from your OS settings
            # SCREEN_SIZE = (1920, 1080)
            

        if self.start_rec_button.text == "Start Recording" and self.recording==True:
            self.start_rec_button.text = "Stop Recording"
    def do_record(self,args):
        # print(args)
        path = args+"\\"
        # print(self.recording)
        SCREEN_SIZE = pyautogui.size()
        # define the codec
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        # create the video write object
        # print(selection)
        # print(path)
        out = cv2.VideoWriter(path+"demo.avi", fourcc, 20.0, (SCREEN_SIZE))
        # make a screenshot
        while self.recording:
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            out.write(frame)
            # print(self.recording)
        # print(self.recording)
        # show the frame
        # cv2.imshow("screenshot", frame)q
        # if the user clicks q, it exits
        # if cv2.waitKey(1) == ord("q"):
        #     break

    def stop_recording(self,path,selection,**args):
        pass
    
class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"),FileWindow(name="file")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
