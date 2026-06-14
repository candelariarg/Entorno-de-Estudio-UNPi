import wx
import json
import random

class PanelFlashcards(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.cards = []
        self.idx_actual = 0
        self.mostrando_respuesta = False
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolbar = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_modo_editar = wx.ToggleButton(self, label=" Modo Edición", size=(140, 35))
        self.btn_modo_editar.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_BUTTON, (16, 16)))
        
        self.btn_modo_repaso = wx.ToggleButton(self, label=" Modo Repaso", size=(140, 35))
        self.btn_modo_repaso.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_BUTTON, (16, 16)))
        
        self.btn_modo_editar.SetValue(True)
        
        self.btn_modo_editar.Bind(wx.EVT_TOGGLEBUTTON, self.on_modo_editar)
        self.btn_modo_repaso.Bind(wx.EVT_TOGGLEBUTTON, self.on_modo_repaso)
        
        self.toolbar.Add(self.btn_modo_editar, 0, wx.RIGHT, 10)
        self.toolbar.Add(self.btn_modo_repaso, 0)
        
        # MODO EDICIÓN
        self.panel_editar = wx.Panel(self)
        ed_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_q = wx.TextCtrl(self.panel_editar, style=wx.TE_PROCESS_ENTER)
        self.txt_q.SetHint("Frente (Pregunta/Concepto)")
        self.txt_a = wx.TextCtrl(self.panel_editar, style=wx.TE_PROCESS_ENTER)
        self.txt_a.SetHint("Dorso (Respuesta/Definición)")
        
        btn_add = wx.Button(self.panel_editar, label=" Agregar Tarjeta")
        btn_add.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_BUTTON, (16, 16)))
        btn_add.Bind(wx.EVT_BUTTON, self.on_add_card)
        
        form_sizer.Add(self.txt_q, 1, wx.RIGHT, 10)
        form_sizer.Add(self.txt_a, 1, wx.RIGHT, 10)
        form_sizer.Add(btn_add, 0)
        
        self.lista = wx.ListCtrl(self.panel_editar, style=wx.LC_REPORT)
        self.lista.InsertColumn(0, "Pregunta", width=300)
        self.lista.InsertColumn(1, "Respuesta", width=300)
        
        btn_del = wx.Button(self.panel_editar, label=" Eliminar Seleccionada")
        btn_del.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, (16, 16)))
        btn_del.Bind(wx.EVT_BUTTON, self.on_del_card)
        
        ed_sizer.Add(form_sizer, 0, wx.EXPAND | wx.ALL, 10)
        ed_sizer.Add(self.lista, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        ed_sizer.Add(btn_del, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        self.panel_editar.SetSizer(ed_sizer)
        
        # MODO REPASO
        self.panel_repaso = wx.Panel(self)
        rep_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tarjeta = wx.Panel(self.panel_repaso)
        t_sizer = wx.BoxSizer(wx.VERTICAL)
        self.lbl_tipo = wx.StaticText(self.tarjeta, label="FRENTE")
        
        # Color neutro para el label tipo (que se vea bien en claro y oscuro)
        self.lbl_tipo.SetForegroundColour(wx.Colour(120, 120, 120)) 
        
        self.lbl_texto_tarjeta = wx.StaticText(self.tarjeta, label="Agrega tarjetas primero.")
        self.lbl_texto_tarjeta.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        t_sizer.Add(self.lbl_tipo, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        t_sizer.AddStretchSpacer()
        t_sizer.Add(self.lbl_texto_tarjeta, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        t_sizer.AddStretchSpacer()
        self.tarjeta.SetSizer(t_sizer)
        
        self.btn_girar = wx.Button(self.panel_repaso, label=" Girar Tarjeta", size=(-1, 40))
        self.btn_girar.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_BUTTON, (16, 16)))
        self.btn_girar.Bind(wx.EVT_BUTTON, self.on_girar)
        
        self.box_botones_juego = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_mal = wx.Button(self.panel_repaso, label=" No lo sabía", size=(120, 40))
        btn_mal.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_BUTTON, (16, 16)))
        
        btn_bien = wx.Button(self.panel_repaso, label=" Lo sabía", size=(120, 40))
        btn_bien.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_BUTTON, (16, 16)))
        
        btn_mal.Bind(wx.EVT_BUTTON, lambda e: self.siguiente_tarjeta(False))
        btn_bien.Bind(wx.EVT_BUTTON, lambda e: self.siguiente_tarjeta(True))
        
        self.box_botones_juego.Add(btn_mal, 0, wx.RIGHT, 20)
        self.box_botones_juego.Add(btn_bien, 0)
        
        rep_sizer.Add(self.tarjeta, 1, wx.EXPAND | wx.ALL, 30)
        rep_sizer.Add(self.btn_girar, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        rep_sizer.Add(self.box_botones_juego, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        self.panel_repaso.SetSizer(rep_sizer)
        self.panel_repaso.Hide()
        
        self.sizer.Add(self.toolbar, 0, wx.EXPAND | wx.BOTTOM, 10)
        self.sizer.Add(self.panel_editar, 1, wx.EXPAND)
        self.sizer.Add(self.panel_repaso, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def on_add_card(self, event):
        q = self.txt_q.GetValue().strip()
        a = self.txt_a.GetValue().strip()
        if q and a:
            self.cards.append({"q": q, "a": a})
            self.txt_q.Clear(); self.txt_a.Clear()
            self.actualizar_lista()

    def on_del_card(self, event):
        sel = self.lista.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        if sel != -1:
            del self.cards[sel]
            self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        
        # Recuperamos la paleta de modo oscuro desde el frame principal
        try:
            top_level = wx.GetTopLevelParent(self)
            es_oscuro = top_level.es_oscuro
            fg = wx.Colour(230, 230, 230) if es_oscuro else wx.Colour(30, 30, 30)
            bg = wx.Colour(50, 50, 50) if es_oscuro else wx.Colour(255, 255, 255)
        except AttributeError:
            fg = wx.Colour(30, 30, 30)
            bg = wx.Colour(255, 255, 255)
            
        for i, c in enumerate(self.cards):
            self.lista.InsertItem(i, c["q"])
            self.lista.SetItem(i, 1, c["a"])
            
            # Colorear la fila para evadir el bug de GTK en modo oscuro
            self.lista.SetItemTextColour(i, fg)
            self.lista.SetItemBackgroundColour(i, bg)

    def on_modo_editar(self, event):
        self.btn_modo_repaso.SetValue(False)
        self.panel_repaso.Hide()
        self.panel_editar.Show()
        self.Layout()

    def on_modo_repaso(self, event):
        self.btn_modo_editar.SetValue(False)
        self.panel_editar.Hide()
        self.panel_repaso.Show()
        self.Layout()
        
        if not self.cards:
            self.lbl_texto_tarjeta.SetLabel("No hay tarjetas. Ve al modo edición.")
            self.btn_girar.Hide()
            self.ShowBotones(False)
            return
            
        random.shuffle(self.cards)
        self.idx_actual = 0
        self.mostrar_frente()

    def get_colores_tema(self):
        """Devuelve los colores correctos para la tarjeta según el tema."""
        try:
            es_oscuro = wx.GetTopLevelParent(self).es_oscuro
        except AttributeError:
            es_oscuro = False
            
        if es_oscuro:
            return wx.Colour(60, 60, 60), wx.Colour(80, 80, 60) # Gris oscuro / Gris amarillento
        else:
            return wx.WHITE, wx.Colour(255, 255, 230) # Blanco / Amarillito claro

    def mostrar_frente(self):
        self.mostrando_respuesta = False
        color_frente, _ = self.get_colores_tema()
        self.tarjeta.SetBackgroundColour(color_frente)
        
        self.lbl_tipo.SetLabel("FRENTE (PREGUNTA)")
        self.lbl_texto_tarjeta.SetLabel(self.cards[self.idx_actual]["q"])
        self.btn_girar.Show()
        self.ShowBotones(False)
        
        self.tarjeta.Refresh()
        self.panel_repaso.Layout()

    def on_girar(self, event):
        self.mostrando_respuesta = True
        _, color_dorso = self.get_colores_tema()
        self.tarjeta.SetBackgroundColour(color_dorso)
        
        self.lbl_tipo.SetLabel("DORSO (RESPUESTA)")
        self.lbl_texto_tarjeta.SetLabel(self.cards[self.idx_actual]["a"])
        self.btn_girar.Hide()
        self.ShowBotones(True)
        
        self.tarjeta.Refresh()
        self.panel_repaso.Layout()

    def ShowBotones(self, show):
        self.box_botones_juego.ShowItems(show)

    def siguiente_tarjeta(self, sabia):
        if not sabia:
            self.cards.append(self.cards[self.idx_actual])
        self.idx_actual += 1
        if self.idx_actual >= len(self.cards):
            wx.MessageBox("¡Has completado todas las tarjetas!", "Fin del Repaso")
            self.btn_modo_editar.SetValue(True)
            self.on_modo_editar(None)
        else:
            self.mostrar_frente()

    def get_data(self):
        return json.dumps(self.cards)

    def load_data(self, data_str):
        self.cards = []
        if data_str:
            try: self.cards = json.loads(data_str)
            except: pass
        self.actualizar_lista()
        self.btn_modo_editar.SetValue(True)
        self.on_modo_editar(None)