from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior
Builder.load_file("design.kv")

class LoginScreen(Screen):

    def forgot_pass(self):
        self.manager.transition.direction= "left"
        self.manager.current = "forgot_pass_screen"

    def sign_up(self):
        self.manager.transition.direction= "left"
        self.manager.current = "signup_screen"

    def login(self, username, password):

        with open('user.json', 'r') as file:
            users = json.load(file)
            if username in users and users[username]['password'] == password :
                self.manager.transition.direction= "left"
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong username or password!"

class ForgotPassScreen(LoginScreen):

    def update_user(self, username, password):
        with open("user.json", 'r') as file:
            users = json.load(file)
        
        users[username] = {'username': username, 'password': password,
        'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}

        with open('user.json', 'w') as file:
            json.dump(users, file)

        self.manager.transition.direction= "left"
        self.manager.current = 'forgot_pass_screen_success'

    def goto_login(self):
        self.manager.transition.direction= "right"
        self.manager.current = 'login_screen'

class ForgotPassScreenSuccess(Screen):
    
    def goto_login(self):
        self.manager.transition.direction= "right"
        self.manager.current = 'login_screen'

class SignUpScreen(LoginScreen):

    def add_user(self, username, password):
        with open("user.json", 'r') as file:
            users = json.load(file)
        
        users[username] = {'username': username, 'password': password,
        'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}

        with open('user.json', 'w') as file:
            json.dump(users, file)
        
        self.manager.transition.direction= "left"
        self.manager.current = 'signup_screen_success'

    def goto_login(self):
        self.manager.transition.direction= "right"
        self.manager.current = 'login_screen'

class SignUpScreenSuccess(Screen):
    
    def goto_login(self):
        self.manager.transition.direction= "right"
        self.manager.current = 'login_screen'

class LoginScreenSuccess(Screen):
    
    def log_out(self):
        self.ids.quote.text = ""
        self.ids.feeling.text = ""
        self.manager.transition.direction= "right"
        self.manager.current = 'login_screen'

    def get_quote(self, feel):

        feel = feel.lower()

        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()

            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try some another feeling or stop Feeling man, its not neccessary."

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()