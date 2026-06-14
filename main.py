import wx
from database import DatabaseManager
from utils import aplicar_tema, COLOR_NAVY
from vistas.home import PanelHome
from vistas.apuntes import PanelApuntes
from vistas.materias import PanelMaterias
from vistas.planner import PanelPlanner
from vistas.mis_apuntes import PanelMisApuntes

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Entorno de Estudio UNPi", size=(1200, 750))
        self.db = DatabaseManager()
        self.es_oscuro = False
        
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- Barra Superior ---
        top_bar = wx.Panel(main_panel)
        top_bar.SetBackgroundColour(COLOR_NAVY)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titulo = wx.StaticText(top_bar, label="UNPi Study Manager")
        titulo.SetForegroundColour(wx.WHITE)
        titulo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.btn_tema = wx.Button(top_bar, label="🌙 Modo Oscuro")
        self.btn_tema.Bind(wx.EVT_BUTTON, self.alternar_tema)
        
        top_sizer.Add(titulo, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        top_sizer.Add(self.btn_tema, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        top_bar.SetSizer(top_sizer)
        
        # --- Pestañas Superiores ---
        self.notebook = wx.Notebook(main_panel)
        
        self.tab_home = PanelHome(self.notebook, self.db, self)
        self.tab_materias = PanelMaterias(self.notebook, self.db)
        self.tab_planner = PanelPlanner(self.notebook, self.db)
        self.tab_apuntes = PanelApuntes(self.notebook, self.db)
        self.tab_mis_apuntes = PanelMisApuntes(self.notebook, self.db, self)
        
        self.notebook.AddPage(self.tab_home, "🏠 Inicio")
        self.notebook.AddPage(self.tab_materias, "📚 Materias")
        self.notebook.AddPage(self.tab_planner, "📅 Planner")
        self.notebook.AddPage(self.tab_apuntes, "📝 Editor / Estudio")
        self.notebook.AddPage(self.tab_mis_apuntes, "🗂 Mis Apuntes")
        
        main_sizer.Add(top_bar, 0, wx.EXPAND)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)
        main_panel.SetSizer(main_sizer)
        
        aplicar_tema(self, self.es_oscuro)
        top_bar.SetBackgroundColour(COLOR_NAVY)
        self.Center()
        self.Show()

    def ir_a_apunte(self, apunte_id, titulo, metodo):
        self.notebook.SetSelection(3)
        self.tab_apuntes.cargar_apunte_desde_home(apunte_id, titulo, metodo)

    def actualizar_lista_apuntes(self):
        self.tab_mis_apuntes.cargar_lista()

    def alternar_tema(self, event):
        self.es_oscuro = not self.es_oscuro
        self.btn_tema.SetLabel("☀️ Modo Claro" if self.es_oscuro else "🌙 Modo Oscuro")
        aplicar_tema(self, self.es_oscuro)
        self.GetChildren()[0].GetChildren()[0].SetBackgroundColour(COLOR_NAVY)
        self.Refresh()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()