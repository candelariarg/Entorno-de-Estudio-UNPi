import wx
from database import DatabaseManager
from utils import aplicar_tema, COLOR_NAVY
from vistas.home import PanelHome
from vistas.apuntes import PanelApuntes
from vistas.materias import PanelMaterias
from vistas.planner import PanelPlanner
from vistas.mis_apuntes import PanelMisApuntes
from vistas.acerca_de import PanelAcercaDe

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="UNPi", size=(1200, 750))
        self.db = DatabaseManager()
        self.es_oscuro = False
        
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- Barra Superior (Entorno de Estudio UNPi) ---
        self.top_bar = wx.Panel(main_panel, style=wx.BORDER_NONE)
        self.top_bar.SetBackgroundColour(COLOR_NAVY)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.titulo_app = wx.StaticText(self.top_bar, label="Entorno de Estudio UNPi")
        self.titulo_app.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Botón de tema con Ícono Nativo
        self.btn_tema = wx.Button(self.top_bar, label=" Tema Oscuro")
        try:
            self.btn_tema.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_BUTTON, (16, 16)))
        except: pass
        self.btn_tema.Bind(wx.EVT_BUTTON, self.alternar_tema)
        
        # Ensamblaje de la barra superior con el espacio extra que habíamos logrado
        top_sizer.Add(self.titulo_app, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP | wx.BOTTOM, 15)
        top_sizer.Add(self.btn_tema, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        self.top_bar.SetSizer(top_sizer)
        
        # --- Pestañas Superiores (Con Íconos Nativos) ---
        self.notebook = wx.Notebook(main_panel)
        
        # 1. Creamos la lista de imágenes nativas del sistema operativo
        image_list = wx.ImageList(16, 16)
        idx_inicio = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, (16, 16)))
        idx_materias = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        idx_planner = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, (16, 16)))
        idx_editor = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        idx_mis_apuntes = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, (16, 16)))
        idx_acerca_de = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16)))

        # 2. Asignamos la lista de imágenes al notebook
        self.notebook.AssignImageList(image_list)
        
        self.tab_home = PanelHome(self.notebook, self.db, self)
        self.tab_materias = PanelMaterias(self.notebook, self.db, self)
        self.tab_planner = PanelPlanner(self.notebook, self.db)
        self.tab_apuntes = PanelApuntes(self.notebook, self.db) 
        self.tab_mis_apuntes = PanelMisApuntes(self.notebook, self.db, self)
        self.tab_acerca_de = PanelAcercaDe(self.notebook)

        # 3. Agregamos las páginas vinculando el ID de cada imagen
        self.notebook.AddPage(self.tab_home, "Inicio", imageId=idx_inicio)
        self.notebook.AddPage(self.tab_materias, "Materias", imageId=idx_materias)
        self.notebook.AddPage(self.tab_planner, "Planner", imageId=idx_planner)
        self.notebook.AddPage(self.tab_apuntes, "Editor / Estudio", imageId=idx_editor)
        self.notebook.AddPage(self.tab_mis_apuntes, "Mis Apuntes", imageId=idx_mis_apuntes)
        self.notebook.AddPage(self.tab_acerca_de, "Acerca de", imageId=idx_acerca_de)

        # Ensamblaje Principal
        main_sizer.Add(self.top_bar, 0, wx.EXPAND)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)
        main_panel.SetSizer(main_sizer)
        
        aplicar_tema(self, self.es_oscuro)
        self._forzar_colores_topbar()
        self.Maximize(True)
        self.Show()

    def _forzar_colores_topbar(self):
        self.top_bar.SetBackgroundColour(COLOR_NAVY)
        self.titulo_app.SetBackgroundColour(COLOR_NAVY)
        self.titulo_app.SetForegroundColour(wx.WHITE)
        self.top_bar.Refresh()

    def ir_a_apunte(self, apunte_id, titulo, metodo):
        self.notebook.SetSelection(3)
        self.tab_apuntes.cargar_apunte_desde_home(apunte_id, titulo, metodo)

    def actualizar_lista_apuntes(self):
        self.tab_mis_apuntes.cargar_lista()

    def alternar_tema(self, event):
        self.es_oscuro = not self.es_oscuro
        self.btn_tema.SetLabel(" Tema Claro" if self.es_oscuro else " Tema Oscuro")
        aplicar_tema(self, self.es_oscuro)
        self._forzar_colores_topbar()
        self.Refresh()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()