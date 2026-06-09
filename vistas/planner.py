import wx
import wx.grid as gridlib

# --- PALETA DE COLORES ---
COLOR_NAVY = wx.Colour(17, 46, 107)    
COLOR_BLUE = wx.Colour(0, 85, 150)     
COLOR_BG = wx.Colour(245, 245, 245)    
COLOR_WHITE = wx.Colour(255, 255, 255)

class PlannerPanel(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Planner Semanal", size=(1000, 650))
        
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour(COLOR_BG)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # ==========================================
        # 1. PANEL IZQUIERDO: CAJA DE BLOQUES (TUS ACTIVIDADES)
        # ==========================================
        left_panel = wx.Panel(main_panel)
        left_panel.SetBackgroundColour(COLOR_WHITE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_titulo = wx.StaticText(left_panel, label="Mis Bloques")
        lbl_titulo.SetForegroundColour(COLOR_NAVY)
        font_titulo = lbl_titulo.GetFont()
        font_titulo.SetPointSize(14)
        font_titulo.MakeBold()
        lbl_titulo.SetFont(font_titulo)
        left_sizer.Add(lbl_titulo, 0, wx.ALL, 15)
        
        # Simulación de los bloques de colores arrastrables
        actividades = [
            ("Clases UNPilar", wx.Colour(0, 85, 150)),       # Azul
            ("Tutorías Privadas", wx.Colour(46, 139, 87)),   # Verde
            ("Turno Trabajo", wx.Colour(210, 105, 30)),    # Naranja
            ("Gimnasio", wx.Colour(138, 43, 226)),           # Violeta
            ("Estudio App", wx.Colour(220, 20, 60))          # Rojo
        ]
        
        for nombre, color in actividades:
            bloque = wx.Panel(left_panel, size=(180, 40))
            bloque.SetBackgroundColour(color)
            bloque_sizer = wx.BoxSizer(wx.VERTICAL)
            texto = wx.StaticText(bloque, label=nombre)
            texto.SetForegroundColour(COLOR_WHITE)
            bloque_sizer.Add(texto, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            bloque.SetSizer(bloque_sizer)
            left_sizer.Add(bloque, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
            
        # Botón para añadir nuevo bloque
        btn_nuevo = wx.Button(left_panel, label="+ Nuevo Bloque")
        left_sizer.Add(btn_nuevo, 0, wx.ALL | wx.EXPAND, 10)
        
        left_panel.SetSizer(left_sizer)
        
        # ==========================================
        # 2. PANEL DERECHO: LA GRILLA SEMANAL Y EXPORTACIÓN
        # ==========================================
        right_panel = wx.Panel(main_panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Barra superior con el botón de exportar
        top_bar = wx.BoxSizer(wx.HORIZONTAL)
        lbl_semana = wx.StaticText(right_panel, label="Planificación de la Semana")
        lbl_semana.SetFont(font_titulo)
        lbl_semana.SetForegroundColour(COLOR_NAVY)
        
        btn_exportar = wx.Button(right_panel, label="📥 Descargar PDF")
        btn_exportar.SetBackgroundColour(COLOR_BLUE)
        btn_exportar.SetForegroundColour(COLOR_WHITE)
        btn_exportar.Bind(wx.EVT_BUTTON, self.on_exportar)
        
        top_bar.Add(lbl_semana, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        top_bar.Add(btn_exportar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        # La Grilla del Calendario
        self.grid = gridlib.Grid(right_panel)
        self.grid.CreateGrid(15, 7) # 15 filas (horarios), 7 columnas (días)
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, dia in enumerate(dias):
            self.grid.SetColLabelValue(i, dia)
            self.grid.SetColSize(i, 100) # Ancho de columnas
            
        horarios = [f"{h}:00" for h in range(8, 23)] # De 8hs a 22hs
        for i, hora in enumerate(horarios):
            self.grid.SetRowLabelValue(i, hora)
            
        # Configuraciones estéticas de la grilla
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        
        # Ejemplo: Pintando un bloque manualmente (simulando que se arrastró algo ahí)
        self.grid.SetCellValue(2, 0, "UNPilar") # Lunes 10:00
        self.grid.SetCellBackgroundColour(2, 0, wx.Colour(0, 85, 150))
        self.grid.SetCellTextColour(2, 0, COLOR_WHITE)
        
        self.grid.SetCellValue(10, 1, "Gimnasio") # Martes 18:00
        self.grid.SetCellBackgroundColour(10, 1, wx.Colour(138, 43, 226))
        self.grid.SetCellTextColour(10, 1, COLOR_WHITE)

        right_sizer.Add(top_bar, 0, wx.EXPAND)
        right_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 15)
        
        right_panel.SetSizer(right_sizer)
        
        # ==========================================
        # ENSAMBLAJE FINAL
        # ==========================================
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)
        
        main_panel.SetSizer(main_sizer)
        self.Center()
        self.Show()

def on_exportar(self, event):
    from reportlab.pdfgen import canvas
    import os

    ruta = os.path.expanduser("~/Desktop/planner_semanal.pdf")
    c = canvas.Canvas(ruta)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Planificación de la Semana")
    c.setFont("Helvetica", 10)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    x_inicio = 100
    ancho_col = 70
    for i, dia in enumerate(dias):
        c.drawString(x_inicio + i * ancho_col, 770, dia)

    # Iterar sobre la grilla para exportar los valores
    for fila in range(self.grid.GetNumberRows()):
        hora = self.grid.GetRowLabelValue(fila)
        for col in range(self.grid.GetNumberCols()):
            valor = self.grid.GetCellValue(fila, col)
            if valor:
                x = x_inicio + col * ancho_col
                y = 750 - fila * 20
                c.drawString(x, y, f"{hora}: {valor}")

    c.save()
    wx.MessageBox(f"PDF guardado en:\n{ruta}", "Exportación exitosa", wx.OK | wx.ICON_INFORMATION)
    
if __name__ == '__main__':
    app = wx.App()
    frame = PlannerPanel()
    app.MainLoop()