import wx
import wx.grid as gridlib
from modo_oscuro import LIGHT_THEME, DARK_THEME

COLOR_NAVY  = wx.Colour(17, 46, 107)
COLOR_BLUE  = wx.Colour(0, 85, 150)
COLOR_LIGHT = wx.Colour(108, 160, 209)
COLOR_BG    = wx.Colour(245, 245, 245)
COLOR_WHITE = wx.Colour(255, 255, 255)


# ══════════════════════════════════════════════════════
#  PANEL 1 — Inicio ("¿Qué vas a estudiar hoy?")
# ══════════════════════════════════════════════════════
class PanelInicio(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(COLOR_BG)
        sizer = wx.BoxSizer(wx.VERTICAL)

        card = wx.Panel(self)
        card.SetBackgroundColour(COLOR_WHITE)
        card_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_title = wx.StaticText(card, label="¡Hola! ¿Qué vas a estudiar hoy?")
        lbl_title.SetForegroundColour(COLOR_BLUE)
        font_title = lbl_title.GetFont()
        font_title.SetPointSize(18)
        font_title.MakeBold()
        lbl_title.SetFont(font_title)

        lbl_inst = wx.StaticText(card, label="Ingresá el tema para iniciar tu sesión de aprendizaje activo.")
        lbl_inst.SetForegroundColour(wx.Colour(100, 100, 100))

        self.txt_tema = wx.TextCtrl(card, size=(400, 35))
        self.txt_tema.SetHint("Ej: Leyes de Newton, Anatomía del corazón...")

        btn_start = wx.Button(card, label="Comenzar Diagnóstico (Paso 1)", size=(250, 40))
        btn_start.SetBackgroundColour(COLOR_BLUE)
        btn_start.SetForegroundColour(COLOR_WHITE)
        btn_start.Bind(wx.EVT_BUTTON, self.on_start_study)

        card_sizer.Add(lbl_title,     0, wx.ALL, 15)
        card_sizer.Add(lbl_inst,      0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        card_sizer.Add(self.txt_tema, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)
        card_sizer.Add(btn_start,     0, wx.ALL | wx.ALIGN_RIGHT, 15)
        card.SetSizer(card_sizer)

        sizer.Add(card, 0, wx.ALL | wx.EXPAND, 40)
        self.SetSizer(sizer)

    def on_start_study(self, event):
        tema = self.txt_tema.GetValue().strip()
        if not tema:
            wx.MessageBox("Por favor, ingresá un tema primero.", "Atención",
                          wx.OK | wx.ICON_WARNING)
            return
        from vistas.editor import EditorEstudio
        editor = EditorEstudio(self, tema)
        editor.Show()


# ══════════════════════════════════════════════════════
#  PANEL 2 — Materiales
# ══════════════════════════════════════════════════════
class PanelMateriales(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(COLOR_BG)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        # Panel izquierdo — árbol de materias
        left_panel = wx.Panel(splitter)
        left_panel.SetBackgroundColour(COLOR_WHITE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_materias = wx.StaticText(left_panel, label="Mis Materias")
        lbl_materias.SetForegroundColour(COLOR_NAVY)
        font_titulo = lbl_materias.GetFont()
        font_titulo.SetPointSize(12)
        font_titulo.MakeBold()
        lbl_materias.SetFont(font_titulo)

        self.tree = wx.TreeCtrl(left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        root = self.tree.AddRoot("Materias")

        materias = {
            "Programación Fullstack": ["Teoría", "Trabajos Prácticos", "Exámenes Anteriores"],
            "Matemática Discreta":    ["Apuntes", "Guías de Ejercicios"],
            "Inglés":                 ["Grammar", "Listening Audio"],
            "Portugués":              ["Material de Lectura", "Ejercicios"],
        }
        for mat, carpetas in materias.items():
            mat_item = self.tree.AppendItem(root, mat)
            for carpeta in carpetas:
                self.tree.AppendItem(mat_item, carpeta)
        self.tree.ExpandAll()

        btn_nueva = wx.Button(left_panel, label="+ Añadir Materia")

        left_sizer.Add(lbl_materias, 0, wx.ALL, 10)
        left_sizer.Add(self.tree,    1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        left_sizer.Add(btn_nueva,    0, wx.EXPAND | wx.ALL, 10)
        left_panel.SetSizer(left_sizer)

        # Panel derecho — detalle de la materia
        right_panel = wx.Panel(splitter)
        right_panel.SetBackgroundColour(COLOR_BG)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        info_card = wx.Panel(right_panel)
        info_card.SetBackgroundColour(COLOR_WHITE)
        info_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo_materia = wx.StaticText(info_card, label="Programación Fullstack")
        font_h1 = lbl_titulo_materia.GetFont()
        font_h1.SetPointSize(16)
        font_h1.MakeBold()
        lbl_titulo_materia.SetFont(font_h1)
        lbl_titulo_materia.SetForegroundColour(COLOR_BLUE)

        datos_grid = wx.GridSizer(rows=2, cols=2, hgap=20, vgap=10)
        datos_grid.Add(wx.StaticText(info_card, label="👨‍🏫 Profesor: Pérez, Juan"))
        datos_grid.Add(wx.StaticText(info_card, label="🔗 Link: meet.google.com/abc-def"))
        datos_grid.Add(wx.StaticText(info_card, label="📅 Horario: Jueves 18:00hs"))
        datos_grid.Add(wx.StaticText(info_card, label="⭐ Estado: Cursando"))

        info_sizer.Add(lbl_titulo_materia, 0, wx.ALL, 15)
        info_sizer.Add(datos_grid,         0, wx.LEFT | wx.BOTTOM, 15)
        info_card.SetSizer(info_sizer)

        lbl_archivos = wx.StaticText(right_panel, label="Archivos Descargados (Carpeta Local)")
        lbl_archivos.SetFont(font_titulo)

        self.list_ctrl = wx.ListCtrl(right_panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "Nombre del Archivo", width=300)
        self.list_ctrl.InsertColumn(1, "Tipo",               width=100)
        self.list_ctrl.InsertColumn(2, "Fecha",              width=150)

        self.list_ctrl.InsertItem(0, "Guia_Ejercicios_01.pdf")
        self.list_ctrl.SetItem(0, 1, "PDF")
        self.list_ctrl.SetItem(0, 2, "20/05/2026")
        self.list_ctrl.InsertItem(1, "Diapositivas_Clase_3.pptx")
        self.list_ctrl.SetItem(1, 1, "Presentación")
        self.list_ctrl.SetItem(1, 2, "18/05/2026")

        btn_abrir = wx.Button(right_panel, label="📂 Abrir Carpeta")
        btn_abrir.Bind(wx.EVT_BUTTON, self.on_abrir_carpeta)

        right_sizer.Add(info_card,      0, wx.EXPAND | wx.ALL, 15)
        right_sizer.Add(lbl_archivos,   0, wx.LEFT | wx.TOP, 15)
        right_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        right_sizer.Add(btn_abrir,      0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 15)
        right_panel.SetSizer(right_sizer)

        splitter.SplitVertically(left_panel, right_panel, 220)
        splitter.SetMinimumPaneSize(180)

        main_sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def on_abrir_carpeta(self, event):
        import os, subprocess
        carpeta = os.path.expanduser("~/Documents")
        if os.path.exists(carpeta):
            if os.name == 'nt':
                os.startfile(carpeta)
            else:
                subprocess.Popen(['xdg-open', carpeta])
        else:
            wx.MessageBox("La carpeta no existe.", "Error", wx.OK | wx.ICON_ERROR)


# ══════════════════════════════════════════════════════
#  PANEL 3 — Planner Semanal
# ══════════════════════════════════════════════════════
class PanelPlanner(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(COLOR_BG)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Panel izquierdo — bloques de actividades
        left_panel = wx.Panel(self)
        left_panel.SetBackgroundColour(COLOR_WHITE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo = wx.StaticText(left_panel, label="Mis Bloques")
        lbl_titulo.SetForegroundColour(COLOR_NAVY)
        font_titulo = lbl_titulo.GetFont()
        font_titulo.SetPointSize(14)
        font_titulo.MakeBold()
        lbl_titulo.SetFont(font_titulo)
        left_sizer.Add(lbl_titulo, 0, wx.ALL, 15)

        actividades = [
            ("Clases UNPilar",    wx.Colour(0, 85, 150)),
            ("Tutorías Privadas", wx.Colour(46, 139, 87)),
            ("Turno Trabajo",     wx.Colour(210, 105, 30)),
            ("Gimnasio",          wx.Colour(138, 43, 226)),
            ("Estudio App",       wx.Colour(220, 20, 60)),
        ]
        for nombre, color in actividades:
            bloque = wx.Panel(left_panel, size=(180, 40))
            bloque.SetBackgroundColour(color)
            bs = wx.BoxSizer(wx.VERTICAL)
            texto = wx.StaticText(bloque, label=nombre)
            texto.SetForegroundColour(COLOR_WHITE)
            bs.Add(texto, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            bloque.SetSizer(bs)
            left_sizer.Add(bloque, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        btn_nuevo = wx.Button(left_panel, label="+ Nuevo Bloque")
        left_sizer.Add(btn_nuevo, 0, wx.ALL | wx.EXPAND, 10)
        left_panel.SetSizer(left_sizer)

        # Panel derecho — grilla semanal
        right_panel = wx.Panel(self)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        top_bar = wx.BoxSizer(wx.HORIZONTAL)
        lbl_semana = wx.StaticText(right_panel, label="Planificación de la Semana")
        lbl_semana.SetFont(font_titulo)
        lbl_semana.SetForegroundColour(COLOR_NAVY)

        btn_exportar = wx.Button(right_panel, label="📥 Descargar PDF")
        btn_exportar.SetBackgroundColour(COLOR_BLUE)
        btn_exportar.SetForegroundColour(COLOR_WHITE)
        btn_exportar.Bind(wx.EVT_BUTTON, self.on_exportar)

        top_bar.Add(lbl_semana,  1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        top_bar.Add(btn_exportar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        self.grid = gridlib.Grid(right_panel)
        self.grid.CreateGrid(15, 7)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, dia in enumerate(dias):
            self.grid.SetColLabelValue(i, dia)
            self.grid.SetColSize(i, 100)

        for i, hora in enumerate(f"{h}:00" for h in range(8, 23)):
            self.grid.SetRowLabelValue(i, hora)

        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        self.grid.SetCellValue(2, 0, "UNPilar")
        self.grid.SetCellBackgroundColour(2, 0, wx.Colour(0, 85, 150))
        self.grid.SetCellTextColour(2, 0, COLOR_WHITE)
        self.grid.SetCellValue(10, 1, "Gimnasio")
        self.grid.SetCellBackgroundColour(10, 1, wx.Colour(138, 43, 226))
        self.grid.SetCellTextColour(10, 1, COLOR_WHITE)

        right_sizer.Add(top_bar,    0, wx.EXPAND)
        right_sizer.Add(self.grid,  1, wx.ALL | wx.EXPAND, 15)
        right_panel.SetSizer(right_sizer)

        main_sizer.Add(left_panel,  0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(main_sizer)

    def on_exportar(self, event):
        wx.MessageBox("Aquí se conectaría ReportLab para generar el PDF.",
                      "Exportar PDF", wx.OK | wx.ICON_INFORMATION)


# ══════════════════════════════════════════════════════
#  VENTANA PRINCIPAL — contenedor con navegación
# ══════════════════════════════════════════════════════
class StudyApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Entorno de Estudio UNPilar", size=(1000, 650))

        self.is_dark    = False
        self.historial  = []   # pila de navegación para el botón "Volver"

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ── Sidebar ──────────────────────────────────────
        self.sidebar = wx.Panel(self)
        self.sidebar.SetBackgroundColour(COLOR_NAVY)
        sidebar_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_menu = wx.StaticText(self.sidebar, label="MI ESPACIO")
        lbl_menu.SetForegroundColour(COLOR_LIGHT)
        font_menu = lbl_menu.GetFont()
        font_menu.SetPointSize(12)
        font_menu.MakeBold()
        lbl_menu.SetFont(font_menu)

        self.btn_volver   = wx.Button(self.sidebar, label="← Volver")
        self.btn_inicio   = wx.Button(self.sidebar, label="🏠 Inicio")
        self.btn_apuntes  = wx.Button(self.sidebar, label="Mis Apuntes")
        self.btn_planner  = wx.Button(self.sidebar, label="Planner Semanal")
        self.btn_campus   = wx.Button(self.sidebar, label="Materiales")

        self.btn_volver.Bind(wx.EVT_BUTTON,  self.ir_atras)
        self.btn_inicio.Bind(wx.EVT_BUTTON,  lambda e: self.navegar("inicio"))
        self.btn_apuntes.Bind(wx.EVT_BUTTON, self.abrir_apuntes)
        self.btn_planner.Bind(wx.EVT_BUTTON, lambda e: self.navegar("planner"))
        self.btn_campus.Bind(wx.EVT_BUTTON,  lambda e: self.navegar("materiales"))

        self.btn_tema = wx.Button(self.sidebar, label="☽ Modo Oscuro")
        self.btn_tema.Bind(wx.EVT_BUTTON, self.toggle_tema)

        sidebar_sizer.Add(lbl_menu,        0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sidebar_sizer.Add(self.btn_volver, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sidebar_sizer.Add(self.btn_inicio, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sidebar_sizer.Add(self.btn_apuntes,0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sidebar_sizer.Add(self.btn_planner,0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sidebar_sizer.Add(self.btn_campus, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sidebar_sizer.AddStretchSpacer()
        sidebar_sizer.Add(self.btn_tema,   0, wx.EXPAND | wx.ALL, 15)
        self.sidebar.SetSizer(sidebar_sizer)

        # ── Área de contenido (stack de paneles) ─────────
        self.content_area = wx.Panel(self)
        self.content_area.SetBackgroundColour(COLOR_BG)
        self.stack_sizer = wx.BoxSizer(wx.VERTICAL)

        # Instanciar los tres paneles (solo uno visible a la vez)
        self.panel_inicio     = PanelInicio(self.content_area)
        self.panel_materiales = PanelMateriales(self.content_area)
        self.panel_planner    = PanelPlanner(self.content_area)

        self.stack_sizer.Add(self.panel_inicio,     1, wx.EXPAND)
        self.stack_sizer.Add(self.panel_materiales, 1, wx.EXPAND)
        self.stack_sizer.Add(self.panel_planner,    1, wx.EXPAND)

        self.content_area.SetSizer(self.stack_sizer)

        # ── Ensamblaje ────────────────────────────────────
        main_sizer.Add(self.sidebar,      1, wx.EXPAND)
        main_sizer.Add(self.content_area, 4, wx.EXPAND)
        self.SetSizer(main_sizer)

        # Mostrar inicio al arrancar
        self._mostrar_panel(self.panel_inicio)
        self._actualizar_boton_volver()

        self.Center()
        self.Show()

    # ── Navegación ───────────────────────────────────────
    def _mostrar_panel(self, panel_destino):
        """Oculta todos los paneles y muestra solo el indicado."""
        for p in (self.panel_inicio, self.panel_materiales, self.panel_planner):
            p.Hide()
        panel_destino.Show()
        self.content_area.Layout()

    def navegar(self, destino):
        """Guarda el panel actual en el historial y navega al destino."""
        actual = self._panel_actual()
        if actual is not None:
            self.historial.append(actual)
        panel = {
            "inicio":      self.panel_inicio,
            "materiales":  self.panel_materiales,
            "planner":     self.panel_planner,
        }[destino]
        self._mostrar_panel(panel)
        self._actualizar_boton_volver()

    def ir_atras(self, event):
        if self.historial:
            panel_anterior = self.historial.pop()
            self._mostrar_panel(panel_anterior)
        self._actualizar_boton_volver()

    def _panel_actual(self):
        for p in (self.panel_inicio, self.panel_materiales, self.panel_planner):
            if p.IsShown():
                return p
        return None

    def _actualizar_boton_volver(self):
        self.btn_volver.Enable(len(self.historial) > 0)

    def abrir_apuntes(self, event):
        wx.MessageBox("Módulo Mis Apuntes: próximamente.", "Info", wx.OK | wx.ICON_INFORMATION)

    # ── Modo Oscuro ──────────────────────────────────────
    def toggle_tema(self, event):
        self.is_dark = not self.is_dark
        tema = DARK_THEME if self.is_dark else LIGHT_THEME
        self.btn_tema.SetLabel("☀ Modo Claro" if self.is_dark else "☽ Modo Oscuro")
        self.aplicar_tema(tema)

    def aplicar_tema(self, tema):
        self.SetBackgroundColour(tema["bg"])
        for widget in self.GetChildren():
            widget.SetBackgroundColour(tema["bg_panel"])
            widget.SetForegroundColour(tema["fg"])
            for hijo in widget.GetChildren():
                hijo.SetBackgroundColour(tema["bg_panel"])
                hijo.SetForegroundColour(tema["fg"])
        self.Refresh()
        self.Update()


if __name__ == '__main__':
    app = wx.App()
    frame = StudyApp()
    app.MainLoop()