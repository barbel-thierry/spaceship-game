from kivy.app import App

import frame


class AVoidApp(App):
    def build(self):
        return frame.Screen()


if __name__ == '__main__':
    AVoidApp().run()
