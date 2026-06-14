import wx
from vistas.editor import EditorEnriquecido

class PanelSprint(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.panel_timer = wx.Panel(self)
        t_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.lbl_info = wx.StaticText(self.panel_timer, label="Sprint: Escribe sin parar.")
        self.lbl_info.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.spin_mins = wx.SpinCtrl(self.panel_timer, value="5", min=1, max=60, size=(60, -1))
        lbl_min = wx.StaticText(self.panel_timer, label="minutos")
        
        self.btn_iniciar = wx.Button(self.panel_timer, label=" Empezar Reto")
        self.btn_iniciar.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_BUTTON, (16, 16)))
        self.btn_iniciar.Bind(wx.EVT_BUTTON, self.on_iniciar)
        
        self.lbl_reloj = wx.StaticText(self.panel_timer, label="00:00")
        self.lbl_reloj.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_reloj.SetMinSize((100, -1)) 
        
        self.btn_materias = wx.Button(self.panel_timer, label=" Buscar Apuntes")
        self.btn_materias.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_BUTTON, (16, 16)))
        
        self.btn_corregir = wx.Button(self.panel_timer, label=" Corregir (Rojo)")
        self.btn_corregir.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_BUTTON, (16, 16)))
        
        self.btn_materias.Bind(wx.EVT_BUTTON, self.on_ir_materias)
        self.btn_corregir.Bind(wx.EVT_BUTTON, self.on_corregir)
        self.btn_materias.Hide()
        self.btn_corregir.Hide()
        
        t_sizer.Add(self.lbl_info, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        t_sizer.Add(self.spin_mins, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        t_sizer.Add(lbl_min, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        t_sizer.Add(self.btn_iniciar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        t_sizer.AddStretchSpacer()
        t_sizer.Add(self.btn_materias, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        t_sizer.Add(self.btn_corregir, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        t_sizer.Add(self.lbl_reloj, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        self.panel_timer.SetSizer(t_sizer)
        
        self.editor = EditorEnriquecido(self)
        
        self.sizer.Add(self.panel_timer, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.sizer.Add(self.editor, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_tick, self.timer)
        self.tiempo_restante = 0

        # Asignar un color inicial seguro y luego leer el tema real
        self.panel_timer.SetBackgroundColour(wx.Colour(230, 240, 255))
        wx.CallAfter(self.ajustar_colores)

    def ajustar_colores(self):
        """Asigna el color a la franja superior dependiendo del modo seleccionado."""
        try:
            es_oscuro = wx.GetTopLevelParent(self).es_oscuro
            bg_color = wx.Colour(60, 60, 60) if es_oscuro else wx.Colour(230, 240, 255)
        except AttributeError:
            bg_color = wx.Colour(230, 240, 255)
            
        self.panel_timer.SetBackgroundColour(bg_color)
        self.panel_timer.Refresh()

    def on_iniciar(self, event):
        minutos = self.spin_mins.GetValue()
        self.tiempo_restante = minutos * 60
        self.actualizar_reloj()
        self.editor.bloquear_edicion(False)
        self.btn_materias.Hide()
        self.btn_corregir.Hide()
        self.btn_iniciar.Disable()
        self.spin_mins.Disable()
        self.panel_timer.Layout()
        self.timer.Start(1000)

    def on_tick(self, event):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.actualizar_reloj()
        else:
            self.timer.Stop()
            self.actualizar_reloj()
            wx.CallAfter(self.mostrar_fin_sprint)

    def mostrar_fin_sprint(self):
        try: 
            wx.Sound.PlaySound("SystemAsterisk", wx.SOUND_SYNC)
        except: 
            pass
        self.editor.bloquear_edicion(True)
        self.btn_materias.Show()
        self.btn_corregir.Show()
        self.panel_timer.Layout()
        wx.MessageBox("¡Tiempo agotado! El documento ha sido bloqueado.\nVe a revisar tus materiales antes de corregir.", "Fin del Sprint", wx.ICON_WARNING)

    def actualizar_reloj(self):
        mins, secs = divmod(self.tiempo_restante, 60)
        self.lbl_reloj.SetLabel(f"{mins:02d}:{secs:02d}")

    def on_ir_materias(self, event):
        try:
            notebook = self.GetTopLevelParent().notebook
            # El índice 1 corresponde a la pestaña "Materias"
            notebook.SetSelection(1)
        except: 
            pass

    def on_corregir(self, event):
        self.editor.activar_modo_correccion()
        self.btn_corregir.Hide()
        self.btn_materias.Hide()
        self.btn_iniciar.Enable()
        self.spin_mins.Enable()
        self.panel_timer.Layout()