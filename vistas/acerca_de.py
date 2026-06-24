import wx
from wx.lib.wordwrap import wordwrap
import wx.adv

manualTexto = (
    'Bienvenido al manual de usuario de "Entorno de Estudio UNPi".\n\n'
    
)

class PanelAcercaDe(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        # --- Sizer externo: centra verticalmente ---
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Sizer medio: centra horizontalmente ---
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # --- Sizer del contenido ---
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        content_sizer.SetMinSize((620, -1))

        # --- Nombre y versión ---
        nombre = wx.StaticText(self, label="'Entorno de Estudio UNPi'")
        font_titulo = nombre.GetFont()
        font_titulo.SetPointSize(24)
        font_titulo.SetWeight(wx.FONTWEIGHT_BOLD)
        nombre.SetFont(font_titulo)
        content_sizer.Add(nombre, 0, wx.ALIGN_CENTER_HORIZONTAL, 18)

        version = wx.StaticText(self, label="Versión: 1.0")
        font_version = version.GetFont()
        font_version.SetPointSize(13)
        version.SetFont(font_version)
        content_sizer.Add(version, 0, wx.ALIGN_CENTER_HORIZONTAL, 15)


        # --- Sitio web ---
        web = wx.adv.HyperlinkCtrl(
            self, label="Repositorio en GitHub",
            url="https://github.com/candelariarg/Entorno-de-Estudio-UNPi.git"
        )
        font_web = web.GetFont()
        font_web.SetPointSize(15)
        web.SetFont(font_web)
        content_sizer.Add(web, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        # --- Desarrolladoras ---
        devs = wx.StaticText(self, label="Desarrolladoras:\n~ Paez Nyx Margot\n~ Ruggieri Candelaria")
        font_devs = devs.GetFont()
        font_devs.SetPointSize(15)
        devs.SetFont(font_devs)
        content_sizer.Add(devs, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        content_sizer.Add(wx.StaticLine(self, size=(620, -1)), 0, wx.ALL, 8)

        # --- Botón Manual ---
        self.btn_manual = wx.Button(self, label="Manual de Usuario", size=(170, 40))
        font_btn = self.btn_manual.GetFont()
        font_btn.SetPointSize(12)
        self.btn_manual.SetFont(font_btn)
        content_sizer.Add(self.btn_manual, 0, wx.ALL | wx.BOTTOM, 15)


        # --- Texto del Manual (oculto al inicio) ---
        texto_wrapeado = wordwrap(manualTexto, 580, wx.ClientDC(self))
        self.manual_text = wx.StaticText(self, label=texto_wrapeado)
        font_manual = self.manual_text.GetFont()
        font_manual.SetPointSize(15)
        self.manual_text.SetFont(font_manual)
        self.manual_text.Hide()
        content_sizer.Add(self.manual_text, 0, wx.ALL | wx.BOTTOM, 15)

        # --- Ensamblaje ---
        h_sizer.AddStretchSpacer(1)
        h_sizer.Add(content_sizer, 0, wx.EXPAND)
        h_sizer.AddStretchSpacer(1)

        outer_sizer.AddStretchSpacer(1)
        outer_sizer.Add(h_sizer, 0, wx.EXPAND)
        outer_sizer.AddStretchSpacer(1)

        self.SetSizer(outer_sizer)
        self.Bind(wx.EVT_BUTTON, self.on_manual, self.btn_manual)

        # --- Copyright ---
        copyright = wx.StaticText(
            self, label="(c) 2026 Equipo de desarrollo de Entorno de Estudio UNPi"
        )
        font_copy = copyright.GetFont()
        font_copy.SetPointSize(12)
        copyright.SetFont(font_copy)
        content_sizer.Add(copyright, 0, wx.ALL | wx.CENTER, 15)

    def on_manual(self, evt):
        if self.manual_text.IsShown():
            self.manual_text.Hide()
        else:
            self.manual_text.Show()
        self.Layout()
        self.GetParent().Layout()
