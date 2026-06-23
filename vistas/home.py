import wx

class PanelHome(wx.Panel):
    def __init__(self, parent, db, main_frame):
        super().__init__(parent)
        self.db = db
        self.main_frame = main_frame
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_saludo = wx.StaticText(self, label="Ingresa el tema de estudio:")
        lbl_saludo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.txt_tema = wx.TextCtrl(self, size=(500, 35))
        self.txt_tema.SetHint("Título del apunte (ej. Repaso Lógica, Proyecto Java)...")
        self.txt_tema.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        # Obtener la lista de materias desde la base de datos y crear el ComboBox
        self.lista_materias = self.db.obtener_materias()
        opciones = ["Ninguna (Apunte suelto)"] + [m['nombre'] for m in self.lista_materias]
        
        self.combo_materia = wx.ComboBox(self, choices=opciones, style=wx.CB_READONLY, size=(500, 35))
        self.combo_materia.SetSelection(0) # Por defecto "Ninguna"

        lbl_tecnicas = wx.StaticText(self, label="Elige una técnica de estudio para arrancar:")
        lbl_tecnicas.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        grid_botones = wx.GridSizer(rows=2, cols=2, vgap=15, hgap=15)
        
        # --- BOTONES CON ÍCONOS NATIVOS ---
        btn_libre = self.crear_boton(grid_botones, " Apunte Libre\n (Editor clásico)", wx.ART_NORMAL_FILE)
        btn_sprint = self.crear_boton(grid_botones, " Sprint de Memoria\n (Escribir contra reloj)", wx.ART_REDO)
        btn_matriz = self.crear_boton(grid_botones, " Matriz de Análisis\n (4 Cuadrantes CQA)", wx.ART_REPORT_VIEW)
        btn_flash = self.crear_boton(grid_botones, " Flashcards\n (Tarjetas de Repaso)", wx.ART_COPY)
        
        # --- BINDINGS ---
        btn_libre.Bind(wx.EVT_BUTTON, lambda e: self.crear_apunte("Apunte Libre"))
        btn_sprint.Bind(wx.EVT_BUTTON, lambda e: self.crear_apunte("Sprint de Memoria"))
        btn_matriz.Bind(wx.EVT_BUTTON, lambda e: self.crear_apunte("Matriz de Análisis"))
        btn_flash.Bind(wx.EVT_BUTTON, lambda e: self.crear_apunte("Flashcards"))
        
        # --- NUEVO ENSAMBLAJE (ALINEADO) ---
        # Agrupamos los inputs para que compartan el mismo margen
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer.Add(self.txt_tema, 0, wx.BOTTOM, 10)
        input_sizer.Add(self.combo_materia, 0, wx.BOTTOM, 0)
        
        # Agregamos todo al sizer principal
        sizer.Add(lbl_saludo, 0, wx.TOP | wx.LEFT, 40)
        sizer.Add(input_sizer, 0, wx.LEFT | wx.TOP, 20) # <-- Ahora ambos tienen margen 20
        sizer.Add(lbl_tecnicas, 0, wx.LEFT | wx.TOP, 40)
        sizer.Add(grid_botones, 0, wx.LEFT | wx.TOP, 20)
        
        self.SetSizer(sizer)

    def crear_boton(self, sizer, label, art_id):
        btn = wx.Button(self, label=label, size=(240, 90))
        btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        # Obtener el ícono nativo del sistema operativo (tamaño 32x32 para que destaque)
        bmp = wx.ArtProvider.GetBitmap(art_id, wx.ART_BUTTON, (32, 32))
        if bmp.IsOk():
            btn.SetBitmap(bmp)
            btn.SetBitmapPosition(wx.LEFT) # Acomoda el ícono a la izquierda del texto
            
        sizer.Add(btn, 1, wx.EXPAND)
        return btn

    def crear_apunte(self, metodo):
        titulo = self.txt_tema.GetValue().strip()
        if not titulo:
            wx.MessageBox("Escribí un título o tema primero, por favor.", "Falta título")
            return
            
        # Determinar el ID de la materia seleccionada (si es que se seleccionó alguna)
        idx_seleccionado = self.combo_materia.GetSelection()
        materia_id_seleccionada = None
        if idx_seleccionado > 0:
            # Restamos 1 porque el índice 0 es "Ninguna"
            materia_id_seleccionada = self.lista_materias[idx_seleccionado - 1]['id']
            
        # Pasa un string vacío al XML inicial, y el ID de la materia
        apunte_id = self.db.guardar_apunte(titulo, metodo, "", materia_id=materia_id_seleccionada)
        
        self.txt_tema.Clear()
        self.combo_materia.SetSelection(0) # Reiniciar selector
        
        self.main_frame.actualizar_lista_apuntes()
        self.main_frame.ir_a_apunte(apunte_id, titulo, metodo)