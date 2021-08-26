import random
import smtplib
import urllib
from urllib import parse, request

from kivymd.color_definitions import colors
from kivymd.color_definitions import palette
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

class LoginPasswordPageInnerBox(FloatLayout):
    def __init__(self, f1, f2, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.spacing = 10

        # forget password BUTTON
        self.forget_password_button = MDFillRoundFlatButton(
            text='Forgot Password',
            pos_hint={"top": 0.5, "right": 0.5},
            md_bg_color=colors['Red']['A700']
        )
        self.forget_password_button.bind(on_press=f1)
        self.add_widget(self.forget_password_button)

        # login BUTTON
        self.password_button = MDFillRoundFlatButton(
            text='Login',
            pos_hint={"top": 0.5, "right": 0.8},
            md_bg_color=colors['Green']['A700']
        )
        self.password_button.bind(on_press=f2)
        self.add_widget(self.password_button)



class LoginPasswordPage(BoxLayout):
    """The email has already been entered. It now only asks for password"""

    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.popup = None
        self.orientation = 'vertical'
        self.original_password = None

        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)

        self.add_widget(Label())

        self.add_widget(MDLabel(text='Password', pos_hint={'x': 0.4}))

        self.password_text_box = TextInput(multiline=False,
                                           password=True,
                                           size_hint_y=0.2,
                                           size_hint_x=0.6,
                                           pos_hint={'top': 0.6, 'x': 0.2})
        self.password_text_box.bind(
            on_text_validate=self.password_button_function)
        self.add_widget(self.password_text_box)



        self.inner = LoginPasswordPageInnerBox(self.sent_otp_forgot,
                                               self.password_button_function)
        self.add_widget(self.inner)

        self.add_widget(Label())

    def closeDialog(self, inst):
        self.popup.dismiss()

    def password_button_function(self, instance):
        if self.inner.password.password_text_box.text == self.original_password:

            # adding the back button functionality
            current = self.main_app.screen_manager.current
            if current not in self.main_app.screen_list:
                self.main_app.screen_list.append(current)

            self.main_app.screen_manager.current = 'info'
        else:
            self.popup = MDDialog(title='Invalid Password',
                             text='The Password you have entered\n does not match with the email with\n which you signed in',
                             buttons=[
                                 MDFlatButton(
                                     text="OK",
                                     on_release=self.closeDialog
                                         ),
                                     ]
                                 )

            self.popup.open()

    def sent_otp_forgot(self, instance):
        password = 'password'
        username = 'username'

        # context = ssl.create_default_context()
        otp = random.randint(1000, 9999)

        sender_email = "tripta@admin.in"

        message = f"""\
        Subject: Forgot Password

        Your One Time Password is {otp} to reset your password of your account
        at mRadix
        """
        print(otp, 'the otp has been generated')
        self.main_app.otp_view.otp = otp
        receiver_email = self.main_app.email_page.inner.email_text_box.text
        print('we are sending an email to', receiver_email)

        s = smtplib.SMTP(host='smtp.mailgun.org', port=587)

        s.starttls()
        s.login(username, password)
        s.sendmail(sender_email, receiver_email, message)
        s.quit()

        current = self.main_app.screen_manager.current
        if current not in self.main_app.screen_list:
            self.main_app.screen_list.append(current)

        self.main_app.screen_manager.current = 'otp view'


class InnerBox(BoxLayout):

    def __init__(self, given, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 0]
        self.add_widget(
            MDLabel(text='Enter OTP from your email', pos_hint={'x': 0.17}))
        self.otp_text_box = TextInput(multiline=False, size_hint_y=0.55)
        self.otp_text_box.bind(on_text_validate=given)
        self.add_widget(self.otp_text_box)
        self.add_widget(Label())

        self.loginbutton = MDFillRoundFlatButton(text='Submit',
                                                 pos_hint={'x': 0.38, 'y': 0.1})
        self.loginbutton.bind(on_press=given)
        self.add_widget(self.loginbutton)


class ForgetPassBox(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.main_app = main_app
        self.orientation = 'vertical'
        self.decision = False
        self.verification = False
        self.otp = 0000
        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)
        self.add_widget(Label())
        self.md_bg_color = self.main_app.theme_cls.primary_color

        self.inner = InnerBox(self.submit_otp)
        self.add_widget(self.inner)

        self.add_widget(Label())

    def closeDialog(self, inst):
        self.popup.dismiss()

    def submit_otp(self, instance):
        if self.otp_text_box.text.isnumeric():
            print('the otp entered is an integer')
            if self.otp == int(self.otp_text_box.text):
                self.decision = True
                if self.verification:

                    # adding the back button functionality
                    current = self.main_app.screen_manager.current
                    if current not in self.main_app.screen_list:
                        self.main_app.screen_list.append(current)

                    self.main_app.screen_manager.current = 'manual'
                else:

                    # adding the back button functionality
                    current = self.main_app.screen_manager.current
                    if current not in self.main_app.screen_list:
                        self.main_app.screen_list.append(current)

                    self.main_app.screen_manager.current = 'new password'
        else:
            self.popup = MDDialog(title='Invalid OTP',
                                  text='Please enter the OTP sent at your email',
                                  buttons=[
                                      MDFlatButton(
                                          text="OK",
                                          on_release=self.closeDialog
                                      ),
                                  ]
                                  )

            self.popup.open()


class NewPassword(BoxLayout):
    """Shows the screen for entering the OTP and then creating a new password"""

    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.popup = None
        self.default_email = 'empty string'
        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)

        self.add_widget(Label())

        self.add_widget(MDLabel(text='New Password', pos_hint={'x': 0.3}))
        self.new_password = TextInput(multiline=False, password=True, size_hint_y=0.3, size_hint_x=0.7, pos_hint={'x': 0.2})
        self.add_widget(self.new_password)

        self.add_widget(MDLabel(text='Retype New Password', pos_hint={'x': 0.25}))
        self.retype = TextInput(multiline=False, password=True, size_hint_y=0.3, size_hint_x=0.7, pos_hint={'x': 0.2})
        self.add_widget(self.retype)

        self.add_widget(Label())
        self.change_password = MDFillRoundFlatButton(text='Change Password', md_bg_color=colors['Green']['A700'], pos_hint={'x': 0.35})
        self.change_password.bind(on_press=self.change_password_func)
        self.add_widget(self.change_password)

        self.add_widget(Label())

    def closeDialog(self, inst):
        self.popup.dismiss()

    def change_password_func(self, instance):
        if self.retype.text != self.new_password.text:
            self.popup = MDDialog(title='Invalid Passwords',
                          text='The passwords you entered do not match',
                          buttons=[
                              MDFlatButton(
                                  text="OK",
                                  on_release=self.closeDialog
                              ),
                          ]
                          )
            self.popup.open()
        else:
            email = self.main_app.email_page.email_text_box.text
            print(email)
            # call the api
            data_dict = {"email": email,
                         "password": self.new_password.text,
                         }
            print(data_dict)
            data = parse.urlencode(data_dict).encode()

            url = f'http://obscure-harbor-86580.herokuapp.com/api/find_user/{email}/'

            req = request.Request(url, data=data, method='PUT')
            with urllib.request.urlopen(req) as f:
                print(f.status)
                print(f.reason)
            print('successfully updated')
            self.main_app.password_page.original_password = self.retype.text

            # adding the back button functionality
            current = self.main_app.screen_manager.current
            if current not in self.main_app.screen_list:
                self.main_app.screen_list.append(current)

            self.main_app.screen_manager.current = 'password'
