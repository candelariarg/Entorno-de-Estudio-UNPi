import wx
from wx.lib.wordwrap import wordwrap
import wx.adv

manualTexto = (
    "Bienvenido al manual de Entorno de Estudio UNPi.\n\n"
)

class PanelAcercaDe(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Nombre y versión ---
        nombre = wx.StaticText(self, label="Entorno de Estudio UNPi")
        font_titulo = nombre.GetFont()
        font_titulo.SetPointSize(16)
        font_titulo.SetWeight(wx.FONTWEIGHT_BOLD)
        nombre.SetFont(font_titulo)
        sizer.Add(nombre, 0, wx.ALL, 10)

        version = wx.StaticText(self, label="Versión: 1.0")
        sizer.Add(version, 0, wx.LEFT | wx.BOTTOM, 10)

        # --- Copyright ---
        copyright = wx.StaticText(
            self, label="(c) 2026 Equipo de desarrollo de Entorno de Estudio UNPi"
        )
        sizer.Add(copyright, 0, wx.LEFT | wx.BOTTOM, 10)

        # --- Sitio web ---
        web = wx.adv.HyperlinkCtrl(
            self, label="Repositorio en GitHub",
            url="https://github.com/candelariarg/Entorno-de-Estudio-UNPi.git"
        )
        sizer.Add(web, 0, wx.LEFT | wx.BOTTOM, 10)

        # --- Desarrolladores ---
        devs = wx.StaticText(self, label="Desarrolladores:\n  Paez Nyx\n  Ruggieri Candelaria")
        sizer.Add(devs, 0, wx.LEFT | wx.BOTTOM, 10)

        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        # --- Botón Manual ---
        self.btn_manual = wx.Button(self, label="Manual")
        sizer.Add(self.btn_manual, 0, wx.ALL, 10)

        # --- Texto del Manual (oculto al inicio) ---
        texto_wrapeado = wordwrap(manualTexto, 450, wx.ClientDC(self))
        self.manual_text = wx.StaticText(self, label=texto_wrapeado)
        self.manual_text.Hide()
        sizer.Add(self.manual_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.on_manual, self.btn_manual)

    def on_manual(self, evt):
        if self.manual_text.IsShown():
            self.manual_text.Hide()
        else:
            self.manual_text.Show()
        self.Layout()
        self.GetParent().Layout()
