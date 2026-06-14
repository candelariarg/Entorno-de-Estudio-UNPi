import wx

class PanelMisApuntes(wx.Panel):
    def __init__(self, parent, db, main_frame):
        super().__init__(parent)
        self.db = db
        self.main_frame = main_frame
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_titulo = wx.StaticText(self, label="Mis Apuntes Guardados")
        lbl_titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_titulo.SetMinSize((-1, 30))
        
        toolbar = wx.BoxSizer(wx.HORIZONTAL)
        
        # --- ÍCONOS NATIVOS EN LUGAR DE EMOJIS ---
        btn_abrir = wx.Button(self, label=" Abrir Apunte")
        btn_abrir.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16, 16)))
        
        btn_renombrar = wx.Button(self, label=" Renombrar")
        btn_renombrar.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_BUTTON, (16, 16)))
        
        btn_eliminar = wx.Button(self, label=" Eliminar")
        btn_eliminar.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, (16, 16)))
        
        toolbar.Add(btn_abrir, 0, wx.RIGHT, 10)
        toolbar.Add(btn_renombrar, 0, wx.RIGHT, 10)
        toolbar.Add(btn_eliminar, 0, wx.RIGHT, 10)
        
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lista.InsertColumn(0, "Título", width=400)
        self.lista.InsertColumn(1, "Método Utilizado", width=150)
        self.lista.InsertColumn(2, "Fecha de Creación", width=150)
        
        sizer.Add(lbl_titulo, 0, wx.ALL | wx.EXPAND, 15)
        sizer.Add(toolbar, 0, wx.LEFT | wx.BOTTOM, 15)
        sizer.Add(self.lista, 1, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(sizer)
        
        # Bindings
        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir)
        btn_abrir.Bind(wx.EVT_BUTTON, self.on_abrir)
        btn_renombrar.Bind(wx.EVT_BUTTON, self.on_renombrar)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        
        self.cargar_lista()

    def cargar_lista(self):
        self.lista.DeleteAllItems()
        
        # Extraer variables de color según si el modo oscuro está activo en el MainFrame
        es_oscuro = self.main_frame.es_oscuro
        fg = wx.Colour(230, 230, 230) if es_oscuro else wx.Colour(30, 30, 30)
        bg = wx.Colour(50, 50, 50) if es_oscuro else wx.Colour(255, 255, 255)
        
        try:
            for i, ap in enumerate(self.db.obtener_apuntes()):
                self.lista.InsertItem(i, ap['nombre'])
                self.lista.SetItem(i, 1, ap['metodo'])
                self.lista.SetItem(i, 2, ap['fecha_creacion'][:10])
                self.lista.SetItemData(i, ap['id'])
                
                # ¡Magia! Pintamos la fila insertada para burlar el fallo de GTK
                self.lista.SetItemTextColour(i, fg)
                self.lista.SetItemBackgroundColour(i, bg)
        except Exception as e:
            print(f"Error cargando lista: {e}")

    def on_abrir(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            ap_id = self.lista.GetItemData(idx)
            titulo = self.lista.GetItemText(idx, 0)
            metodo = self.lista.GetItemText(idx, 1)
            self.main_frame.ir_a_apunte(ap_id, titulo, metodo)

    def on_renombrar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            ap_id = self.lista.GetItemData(idx)
            viejo = self.lista.GetItemText(idx, 0)
            nuevo = wx.GetTextFromUser("Nuevo nombre del apunte:", "Renombrar", viejo, self)
            
            if nuevo.strip() and nuevo != viejo:
                self.db.renombrar_apunte(ap_id, nuevo.strip())
                self.cargar_lista()
                self.sincronizar_home()

    def on_eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx != -1:
            ap_id = self.lista.GetItemData(idx)
            if wx.MessageBox("¿Eliminar este apunte definitivamente?", "Confirmar", wx.YES_NO | wx.ICON_WARNING) == wx.YES:
                self.db.eliminar_apunte(ap_id)
                self.cargar_lista()
                self.sincronizar_home()

    def sincronizar_home(self):
        """Le avisa al Home que actualice su lista de recientes para que no queden datos viejos"""
        try:
            notebook = self.GetParent()
            panel_home = notebook.GetPage(0)
            panel_home.cargar_recientes()
        except Exception as e:
            pass