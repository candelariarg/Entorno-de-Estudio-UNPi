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
        
        # --- Barra Superior (UNPi Manager) ---
        self.top_bar = wx.Panel(main_panel, style=wx.BORDER_NONE)
        self.top_bar.SetBackgroundColour(COLOR_NAVY)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.titulo_app = wx.StaticText(self.top_bar, label="UNPi Study Manager")
        self.titulo_app.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Botón de tema con Ícono Nativo
        self.btn_tema = wx.Button(self.top_bar, label=" Tema Oscuro")
        try:
            self.btn_tema.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_BUTTON, (16, 16)))
        except: pass
        self.btn_tema.Bind(wx.EVT_BUTTON, self.alternar_tema)
        
        # FIX PARA DAR MÁS ESPACIO ARRIBA/ABAJO A UNPi MANAGER:
        # Agregamos los márgenes verticales (wx.TOP | wx.BOTTOM) dentro de la barra azul.
        # Usamos un padding de 15 píxeles para que la barra azul sea más alta y respire.
        top_sizer.Add(self.titulo_app, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP | wx.BOTTOM, 15)
        top_sizer.Add(self.btn_tema, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        
        self.top_bar.SetSizer(top_sizer)
        
        # --- Pestañas Superiores ---
        self.notebook = wx.Notebook(main_panel)
        
        self.tab_home = PanelHome(self.notebook, self.db, self)
        self.tab_materias = PanelMaterias(self.notebook, self.db, self)
        self.tab_planner = PanelPlanner(self.notebook, self.db)
        self.tab_apuntes = PanelApuntes(self.notebook, self.db) # Asegúrate de pasar db si lo requiere
        self.tab_mis_apuntes = PanelMisApuntes(self.notebook, self.db, self)
        
        self.notebook.AddPage(self.tab_home, "Inicio")
        self.notebook.AddPage(self.tab_materias, "Materias")
        self.notebook.AddPage(self.tab_planner, "Planner")
        self.notebook.AddPage(self.tab_apuntes, "Editor / Estudio")
        self.notebook.AddPage(self.tab_mis_apuntes, "Mis Apuntes")
        
        # Ensamblaje Principal
        main_sizer.Add(self.top_bar, 0, wx.EXPAND)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)
        main_panel.SetSizer(main_sizer)
        
        # Aplicamos tema y maximizamos
        aplicar_tema(self, self.es_oscuro)
        self._forzar_colores_topbar()
        self.Maximize(True)
        self.Show()

    def _forzar_colores_topbar(self):
        """Mantiene los colores forzados para evitar que el 'modo claro' pinte de blanco la barra azul"""
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