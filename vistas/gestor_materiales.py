import wx

# --- PALETA DE COLORES UNP ---
COLOR_NAVY = wx.Colour(17, 46, 107)    
COLOR_BLUE = wx.Colour(0, 85, 150)     
COLOR_BG = wx.Colour(245, 245, 245)    
COLOR_WHITE = wx.Colour(255, 255, 255)

class MaterialesPanel(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Gestor de Campus y Materiales", size=(1000, 600))
        
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour(COLOR_BG)
        
        # Usamos un SplitterWindow para poder arrastrar y cambiar el tamaño de los paneles
        splitter = wx.SplitterWindow(main_panel, style=wx.SP_LIVE_UPDATE)
        
        # ==========================================
        # 1. PANEL IZQUIERDO: ÁRBOL DE MATERIAS
        # ==========================================
        left_panel = wx.Panel(splitter)
        left_panel.SetBackgroundColour(COLOR_WHITE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_materias = wx.StaticText(left_panel, label="Mis Materias")
        lbl_materias.SetForegroundColour(COLOR_NAVY)
        font_titulo = lbl_materias.GetFont()
        font_titulo.SetPointSize(12)
        font_titulo.MakeBold()
        lbl_materias.SetFont(font_titulo)
        
        # El componente estrella para organizar carpetas
        self.tree = wx.TreeCtrl(left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        root = self.tree.AddRoot("Materias")
        
        # Añadiendo datos de ejemplo realistas
        materias = {
            "Programación Fullstack": ["Teoría", "Trabajos Prácticos", "Exámenes Anteriores"],
            "Matemática Discreta": ["Apuntes", "Guías de Ejercicios"],
            "Inglés": ["Grammar", "Listening Audio"],
            "Portugués": ["Material de Lectura", "Ejercicios"]
        }
        
        for mat, carpetas in materias.items():
            mat_item = self.tree.AppendItem(root, mat)
            for carpeta in carpetas:
                self.tree.AppendItem(mat_item, carpeta)
                
        self.tree.ExpandAll()
        
        btn_nueva_materia = wx.Button(left_panel, label="+ Añadir Materia")
        
        left_sizer.Add(lbl_materias, 0, wx.ALL, 10)
        left_sizer.Add(self.tree, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        left_sizer.Add(btn_nueva_materia, 0, wx.EXPAND | wx.ALL, 10)
        left_panel.SetSizer(left_sizer)
        
        # ==========================================
        # 2. PANEL DERECHO: DASHBOARD DE LA MATERIA
        # ==========================================
        right_panel = wx.Panel(splitter)
        right_panel.SetBackgroundColour(COLOR_BG)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # -- Tarjeta de Información (Info SIU/Campus) --
        info_card = wx.Panel(right_panel)
        info_card.SetBackgroundColour(COLOR_WHITE)
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_titulo_materia = wx.StaticText(info_card, label="Programación Fullstack")
        font_h1 = lbl_titulo_materia.GetFont()
        font_h1.SetPointSize(16)
        font_h1.MakeBold()
        lbl_titulo_materia.SetFont(font_h1)
        lbl_titulo_materia.SetForegroundColour(COLOR_BLUE)
        
        # Datos rápidos
        datos_grid = wx.GridSizer(rows=2, cols=2, hgap=20, vgap=10)
        datos_grid.Add(wx.StaticText(info_card, label="👨‍🏫 Profesor: Pérez, Juan"))
        datos_grid.Add(wx.StaticText(info_card, label="🔗 Link Clases: meet.google.com/abc-def"))
        datos_grid.Add(wx.StaticText(info_card, label="📅 Horario: Jueves 18:00hs"))
        datos_grid.Add(wx.StaticText(info_card, label="⭐ Estado: Cursando"))
        
        info_sizer.Add(lbl_titulo_materia, 0, wx.ALL, 15)
        info_sizer.Add(datos_grid, 0, wx.LEFT | wx.BOTTOM, 15)
        info_card.SetSizer(info_sizer)
        
        # -- Lista de Archivos Locales --
        lbl_archivos = wx.StaticText(right_panel, label="Archivos Descargados (Carpeta Local)")
        lbl_archivos.SetFont(font_titulo)
        
        # Un ListCtrl para mostrar los PDFs y documentos
        self.list_ctrl = wx.ListCtrl(right_panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "Nombre del Archivo", width=300)
        self.list_ctrl.InsertColumn(1, "Tipo", width=100)
        self.list_ctrl.InsertColumn(2, "Fecha", width=150)
        
        # Archivos de ejemplo
        self.list_ctrl.InsertItem(0, "Guia_Ejercicios_01.pdf")
        self.list_ctrl.SetItem(0, 1, "PDF")
        self.list_ctrl.SetItem(0, 2, "20/05/2026")
        
        self.list_ctrl.InsertItem(1, "Diapositivas_Clase_3.pptx")
        self.list_ctrl.SetItem(1, 1, "Presentación")
        self.list_ctrl.SetItem(1, 2, "18/05/2026")
        
        btn_abrir_carpeta = wx.Button(right_panel, label="📂 Abrir Carpeta")
        btn_abrir_carpeta.Bind(wx.EVT_BUTTON, self.on_abrir_carpeta)
        
        right_sizer.Add(info_card, 0, wx.EXPAND | wx.ALL, 15)
        right_sizer.Add(lbl_archivos, 0, wx.LEFT | wx.TOP, 15)
        right_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        right_sizer.Add(btn_abrir_carpeta, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 15)
        right_panel.SetSizer(right_sizer)
        
        # Ensamblar el Splitter
        splitter.SplitVertically(left_panel, right_panel, 250)
        splitter.SetMinimumPaneSize(200)
        
        # Sizer principal
        main_layout = wx.BoxSizer(wx.VERTICAL)
        main_layout.Add(splitter, 1, wx.EXPAND)
        main_panel.SetSizer(main_layout)
        
        self.Center()
        self.Show()

def on_abrir_carpeta(self, event):
    import os, subprocess
    carpeta = os.path.expanduser("~/Documents")  #Cambiá esta ruta a la que uses
    if os.path.exists(carpeta):
        if os.name == 'nt':  #Windows
            os.startfile(carpeta)
        else:  #Mac/Linux
            subprocess.Popen(['xdg-open', carpeta])
    else:
        wx.MessageBox("La carpeta no existe.", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = MaterialesPanel()
    app.MainLoop()