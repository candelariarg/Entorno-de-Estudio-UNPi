import wx

class PanelMisApuntes(wx.Panel):
    def __init__(self, parent, db, main_frame):
        super().__init__(parent)
        self.db = db
        self.main_frame = main_frame
        
        #Sizer principal con margen estándar
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_titulo = wx.StaticText(self, label="Mis Apuntes Guardados")
        lbl_titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        #Toolbar
        toolbar = wx.BoxSizer(wx.HORIZONTAL)
        btn_abrir = wx.Button(self, label="✏️ Abrir Apunte")
        btn_renombrar = wx.Button(self, label="🔄 Renombrar")
        btn_eliminar = wx.Button(self, label="🗑️ Eliminar")
        toolbar.Add(btn_abrir, 0, wx.RIGHT, 10)
        toolbar.Add(btn_renombrar, 0, wx.RIGHT, 10)
        toolbar.Add(btn_eliminar, 0, wx.RIGHT, 10)
        
        #Lista estándar
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lista.InsertColumn(0, "Título", width=400)
        self.lista.InsertColumn(1, "Método Utilizado", width=150)
        self.lista.InsertColumn(2, "Fecha de Creación", width=150)
        
        #Layout base que sabemos que funciona en los otros paneles
        main_sizer.Add(lbl_titulo, 0, wx.ALL, 20)
        main_sizer.Add(toolbar, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        main_sizer.Add(self.lista, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        
        self.SetSizer(main_sizer)
        
        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir)
        btn_abrir.Bind(wx.EVT_BUTTON, self.on_abrir)
        btn_renombrar.Bind(wx.EVT_BUTTON, self.on_renombrar)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.cargar_lista()

    def cargar_lista(self):
        self.lista.DeleteAllItems()
        es_oscuro = self.main_frame.es_oscuro
        fg = wx.Colour(230, 235, 250) if es_oscuro else wx.Colour(17, 46, 107)
        bg = wx.Colour(28, 39, 70) if es_oscuro else wx.Colour(242, 245, 250)

        for i, ap in enumerate(self.db.obtener_apuntes()):
            self.lista.InsertItem(i, ap['nombre'])
            self.lista.SetItem(i, 1, ap['metodo'])
            self.lista.SetItem(i, 2, ap['fecha_creacion'][:10])
            self.lista.SetItemData(i, ap['id'])
            self.lista.SetItemTextColour(i, fg)
            self.lista.SetItemBackgroundColour(i, bg)

    def on_abrir(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            self.main_frame.ir_a_apunte(self.lista.GetItemData(idx), self.lista.GetItemText(idx, 0), self.lista.GetItemText(idx, 1))

    def on_renombrar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            ap_id = self.lista.GetItemData(idx)
            viejo = self.lista.GetItemText(idx, 0)
            nuevo = wx.GetTextFromUser("Nuevo nombre:", "Renombrar", viejo, self)
            if nuevo.strip():
                self.db.renombrar_apunte(ap_id, nuevo.strip())
                self.cargar_lista()

    def on_eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            ap_id = self.lista.GetItemData(idx)
            if wx.MessageBox("¿Eliminar?", "Confirmar", wx.YES_NO) == wx.YES:
                self.db.eliminar_apunte(ap_id)
                self.cargar_lista()