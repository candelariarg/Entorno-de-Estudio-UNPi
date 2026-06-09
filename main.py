import wx
from vistas.home import StudyApp

if __name__ == '__main__':
    app = wx.App()
    frame = StudyApp()
    app.MainLoop()