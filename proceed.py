import re
import time
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.color_definitions import colors
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFillRoundFlatButton, MDFillRoundFlatIconButton, \
    MDFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

email_page = '''
BoxLayout:
    orientation: "vertical"
    MDToolbar:
        title: "mRadix"
        

'''


class InnerBox(BoxLayout):

    def __init__(self, given, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 0]
        self.add_widget(MDLabel(text='Email: ', pos_hint={'x': 0.075}))
        self.email_text_box = TextInput(multiline=False, size_hint_y=0.55)
        self.email_text_box.bind(on_text_validate=given)
        self.add_widget(self.email_text_box)
        self.add_widget(Label())

        self.loginbutton = MDFillRoundFlatButton(text='Proceed ->', pos_hint={'x': 0.6, 'y': 0.1}, md_bg_color=colors['Green']['A700'])
        self.loginbutton.bind(on_press=given)
        self.add_widget(self.loginbutton)


class EmailPage(BoxLayout):
    """ Asks for the email address of the user.
    It is officially the first page of the app"""

    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.orientation = 'vertical'
        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)
        self.add_widget(Label())

        self.main_app = main_app
        self.md_bg_color = self.main_app.theme_cls.primary_color

        self.inner = InnerBox(self.loginbutton_function)
        self.add_widget(self.inner)
        # self.padding = [100, 200]

        self.add_widget(Label())

    def closeDialog(self, inst):
        self.popup.dismiss()

    def loginbutton_function(self, instance):

        print('proceed has been pressed')

        email_is_correct = check_email(self.inner.email_text_box.text)

        if not email_is_correct:
            self.popup = MDDialog(title='Invalid Email',
                             text='Please check the email address you have'
                                   ' entered',
                             buttons=[
                                 MDFlatButton(
                                     text="OK", on_release=self.closeDialog
                                 ),
                             ]
                             )
            self.popup.open()
            return

        url = f'https://obscure-harbor-86580.herokuapp.com/api/find_user/' \
              f'{self.inner.email_text_box.text}/ '

        req = UrlRequest(url, verify=False)
        print('waiting for url to respond')
        req.wait()
        print('url has responded')
        details = req.result
        password_got = details['password']

        print('we reached here 21', details, 'the password is ', password_got)
        if password_got == '':

            # adding the back button functionality
            current = self.main_app.screen_manager.current
            if current not in self.main_app.screen_list:
                self.main_app.screen_list.append(current)

            self.main_app.screen_manager.current = 'signup'
        else:
            password_in_database = password_got
            print(password_in_database)
            self.main_app.password_page.original_password = password_in_database
            print(self.main_app.password_page.original_password,
                  'we have set the password')

            # adding the back button functionality
            print('adding the back button functionality')
            current = self.main_app.screen_manager.current
            if current not in self.main_app.screen_list:
                self.main_app.screen_list.append(current)

            print('changing the screen manager current')
            print('this is the currrent screen',
                  self.main_app.screen_manager.current)

            self.main_app.screen_manager.current = 'password'

            print('this is the current screen',
                  self.main_app.screen_manager.current)
            print('passed the screen')


regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def check_email(email) -> bool:
    if re.search(regex, email):
        return True

    return False
