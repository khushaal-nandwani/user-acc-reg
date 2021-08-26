from urllib import parse, request
import urllib.request
import urllib
import smtplib
import random

from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.color_definitions import colors
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDIconButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar


class GoogleBox(FloatLayout):
    def __init__(self, given, **kwargs):
        super().__init__(**kwargs)
        self.manual = MDFillRoundFlatButton(text='Sign Up Manually', md_bg_color=colors['Blue']['600'], pos_hint={'x': 0.32, 'y': 0.3})
        self.manual.bind(on_press=given)
        self.add_widget(self.manual)
        self.google_label = MDLabel(text='Sign Up through', pos_hint={'x': 0.32, 'y': 0.4})
        self.add_widget(self.google_label)
        self.add_widget(MDIconButton(icon='icon.png', user_font_size="64sp", pos_hint={'x': 0.3, 'y': 0.7}))

        self.add_widget(MDLabel(text='OR', pos_hint={'x': 0.45, 'y': 0.05}))



class SignUpPage(BoxLayout):
    """ Asks whether to sign up manually or sign up through gmail"""
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_app = main_app
        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)
        self.google_box = GoogleBox(self.manual_signup)
        self.add_widget(self.google_box)

    def manual_signup(self, instance):

        # setting the default email
        new_email = self.main_app.email_page.email_text_box.text
        self.main_app.manual.email_set.text = new_email

        # sending an OTP for verification
        otp = self.send_verification_otp()
        self.main_app.verification_otp.verification = True
        self.main_app.verification_otp.otp = otp

        # adding the back button functionality
        current = self.main_app.screen_manager.current
        if current not in self.main_app.screen_list:
            self.main_app.screen_list.append(current)

        self.main_app.screen_manager.current = 'verification otp'

    def send_verification_otp(self) -> int:
        port = 587
        password = 'a4173e869e71049900c68faa9b24325d-1d8af1f4-a0089450'
        username = 'postmaster@sandboxfb88fbcd0c3e40008753504ede9f44f4' \
                   '.mailgun.org '

        # context = ssl.create_default_context()
        otp = random.randint(1000, 9999)

        sender_email = "tripta@admin.in"

        message = f"""\
        Subject: Email Verification

        Your One Time Password is {otp} to verify your email associated with
        your account at mRadix
        """
        print(otp)
        self.main_app.otp_view.otp = otp
        receiver_email = self.main_app.email_page.email_text_box.text

        s = smtplib.SMTP(host='smtp.mailgun.org', port=587)

        s.starttls()
        s.login(username, password)
        s.sendmail(sender_email, receiver_email, message)
        s.quit()

        return otp




def check_mobile_number(mobile_number) -> bool:
    if (isinstance(mobile_number, int)
            and 6000000000 < mobile_number < 9999999999):
        return True
    return False

class ManualSignUp(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.main_app = main_app
        self.popup = None
        self.orientation = 'vertical'
        toolbar = MDToolbar(title='mRadix', elevation=12)
        self.add_widget(toolbar)
        self.default_email = 'empty string'

        self.add_widget(Label())

        self.add_widget(MDLabel(text='Email', pos_hint={'x': 0.2}))
        self.email_set = TextInput(text=self.default_email, readonly=True,
                                   size_hint_y=0.7,
                                   size_hint_x=0.7,
                                   pos_hint={'x': 0.2})
        self.add_widget(self.email_set)
        self.add_widget(Label())

        self.add_widget(MDLabel(text='Password', pos_hint={'x': 0.2}))
        self.password = TextInput(multiline=False,
                                  password=True,
                                  write_tab=False,
                                  size_hint_y=0.7,
                                  size_hint_x=0.7,
                                  pos_hint={'x': 0.2})
        self.add_widget(self.password)
        self.add_widget(Label())
        self.add_widget(MDLabel(text='Verify Password', pos_hint={'x': 0.2}))
        self.p_verify = TextInput(multiline=False,
                                  password=True,
                                  write_tab=False,
                                  size_hint_y=0.7,
                                  size_hint_x=0.7,
                                  pos_hint={'x': 0.2})
        self.add_widget(self.p_verify)

        self.add_widget(Label())
        self.add_widget(MDLabel(text='Mobile Number', pos_hint={'x': 0.2}))
        self.mobile_no_text_box = TextInput(multiline=False, write_tab=False,
                                            size_hint_y=0.7,
                                            size_hint_x=0.7,
                                            pos_hint={'x': 0.2})

        self.add_widget(self.mobile_no_text_box)

        self.add_widget(Label())
        self.signup_button = MDFillRoundFlatButton(text='Sign Up', md_bg_color=colors['Green']['900'], pos_hint={'x':0.4})
        self.signup_button.bind(on_press=self.signup_button_function)
        self.add_widget(self.signup_button)
        self.add_widget(Label())

    def closeDialog(self, inst):
        self.popup.dismiss()

    def signup_button_function(self, instance):
        if self.mobile_no_text_box.text.isnumeric():
            mobile_is_correct = check_mobile_number(
                int(self.mobile_no_text_box.text))
        else:
            mobile_is_correct = False

        if not mobile_is_correct:
            self.popup = MDDialog(title='Invalid Mobile Number',
                              text='Please check the mobile number you have entered',
                             buttons=[
                                 MDFlatButton(
                                     text="OK", text_color=colors['Purple']['900'], on_release=self.closeDialog
                                 ),
                             ])
            self.popup.open()
            return

        if self.password.text != self.p_verify.text:
            self.popup = MDDialog(title='The Passwords do not match',
                             text='Please verify the password correctly',
                             buttons=[
                                 MDFlatButton(
                                     text="OK",
                                     on_release=self.closeDialog
                                 ),
                             ])
            self.popup.open()
            return



        # doing a POST request to the database
        data_dict = {"email": self.email_set.text,
                     "password": self.password.text,
                     "mobile_no": int(self.mobile_no_text_box.text),
                     }
        data = parse.urlencode(data_dict).encode()

        url = 'http://obscure-harbor-86580.herokuapp.com/api/users/create/'
        response = urllib.request.urlopen(url, data)
        req = request.Request(url, data=data)

        # adding the back button functionality
        current = self.main_app.screen_manager.current
        if current not in self.main_app.screen_list:
            self.main_app.screen_list.append(current)

        self.main_app.screen_manager.current = 'info'

    def closeDialog(self, inst):
        self.popup.dismiss()

#alreadyexists.py

