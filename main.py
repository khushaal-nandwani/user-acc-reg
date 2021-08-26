# management modules
from kivymd.color_definitions import colors
from kivymd.uix.toolbar import MDToolbar

from proceed import EmailPage
from already_exists_email import LoginPasswordPage, NewPassword, ForgetPassBox
from signup_pages import SignUpPage, ManualSignUp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout



class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign='center', valign='middle', font_size=30,
                             text='You have successfully Logged In! \n Welcome!')
        self.add_widget(self.message)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.on_back_button)
        self.screen_list = []


    def on_back_button(self, window, key, *args):
        # user presses back button
        if key == 27:
            # if there are screens to return to
            if self.screen_list:
                print('backed')
                self.screen_manager.current = self.screen_list.pop()
                return True
            return False


    def build(self):

        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Indigo"

        self.screen_manager = ScreenManager()
        print('screen has been created')

        self.email_page = EmailPage(main_app)
        screen = Screen(name='email')
        screen.add_widget(self.email_page)
        self.screen_manager.add_widget(screen)

        # adding password page
        self.password_page = LoginPasswordPage(main_app)
        screen = Screen(name='password')
        screen.add_widget(self.password_page)
        self.screen_manager.add_widget(screen)

        # adding infopage
        self.info_page = InfoPage()
        screen = Screen(name='info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        # adding signup page
        self.signup = SignUpPage(main_app)
        screen = Screen(name='signup')
        screen.add_widget(self.signup)
        self.screen_manager.add_widget(screen)

        # adding signup manual page
        self.manual = ManualSignUp(main_app)
        screen = Screen(name='manual')
        screen.add_widget(self.manual)
        self.screen_manager.add_widget(screen)

        self.otp_view = ForgetPassBox(main_app)
        screen = Screen(name='otp view')
        screen.add_widget(self.otp_view)
        self.screen_manager.add_widget(screen)

        self.new_password = NewPassword(main_app)
        screen = Screen(name='new password')
        screen.add_widget(self.new_password)
        self.screen_manager.add_widget(screen)

        self.verification_otp = ForgetPassBox(main_app)
        screen = Screen(name='verification otp')
        screen.add_widget(self.verification_otp)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


def back_button(selfe) -> bool:
    """ Checks if back button can be used to go back to the previous page or
    exit the application"""
    out_list = selfe.main_app.email_page.screen_list

    if out_list:
        selfe.main_app.screen_manager.current = out_list.pop()
        return True
    return False


if __name__ == '__main__':
    main_app = MainApp()
    main_app.run()
