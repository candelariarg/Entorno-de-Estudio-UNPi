import wx
from utils import exportar_planner_pdf, HORARIOS

class DraggableBlock(wx.Panel):
    def __init__(self, parent, db_id, label, col, row, color, db_manager):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.db_id = db_id
        self.color_hex = color
        self.label = label
        self.col = col
        self.row = row
        self.db = db_manager
        
        self.SetBackgroundColour(wx.Colour(color))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label=label)
        self.text.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #Mantenemos el texto negro para contrastar con los colores que elige el usuario
        self.text.SetForegroundColour(wx.BLACK)
        sizer.Add(self.text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)
        self.SetSizer(sizer)
        
        self.dragging = False
        self.offset = (0, 0)
        
        for el in (self, self.text):
            el.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
            el.Bind(wx.EVT_LEFT_UP, self.OnUp)
            el.Bind(wx.EVT_MOTION, self.OnMotion)
            el.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

    def OnRightClick(self, event):
        """Elimina la tarea tanto de la pantalla como de la base de datos."""
        if wx.MessageBox(f"¿Quieres eliminar la actividad '{self.label}'?", "Eliminar Bloque", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.db.borrar_bloque_planner(self.db_id)
            self.Destroy()

    def OnDown(self, event):
        self.dragging = True
        self.Raise()
        obj = event.GetEventObject()
        if obj == self.text:
            pos_in_screen = self.text.ClientToScreen(event.GetPosition())
            self.offset = self.ScreenToClient(pos_in_screen)
        else:
            self.offset = event.GetPosition()
        if not self.HasCapture(): self.CaptureMouse()

    def OnUp(self, event):
        """Ajusta el bloque de forma inteligente dentro de los límites horarios lógicos."""
        if self.dragging:
            self.dragging = False
            if self.HasCapture(): self.ReleaseMouse()
            
            parent = self.GetParent()
            w, h = parent.GetSize()
            
            margin_left = 60
            margin_top = 30
            col_w = (w - margin_left) // 7
            row_h = (h - margin_top) // len(HORARIOS)
            
            x, y = self.GetPosition()
            
            self.col = max(0, min(round((x - margin_left) / col_w), 6))
            self.row = max(0, min(round((y - margin_top) / row_h), len(HORARIOS) - 1))
            
            self.ajustar_posicion_grilla(col_w, row_h, margin_left, margin_top)
            self.db.actualizar_bloque_planner(self.db_id, self.col, self.row)

    def ajustar_posicion_grilla(self, col_w, row_h, margin_left, margin_top):
        snap_x = margin_left + (self.col * col_w) + 2
        snap_y = margin_top + (self.row * row_h) + 2
        self.SetSize((col_w - 4, row_h - 4))
        self.SetPosition((snap_x, snap_y))
        self.Layout()

    def OnMotion(self, event):
        if self.dragging and event.Dragging() and event.LeftIsDown():
            screen_pos = event.GetEventObject().ClientToScreen(event.GetPosition())
            parent_pos = self.GetParent().ScreenToClient(screen_pos)
            self.SetPosition((parent_pos.x - self.offset.x, parent_pos.y - self.offset.y))


class PanelPlanner(wx.Panel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        toolbar = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_nuevo = wx.Button(self, label=" Crear Bloque Actividad")
        btn_nuevo.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_BUTTON, (16, 16)))
        
        btn_pdf = wx.Button(self, label=" Exportar a PDF")
        btn_pdf.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_BUTTON, (16, 16)))
        
        lbl_info = wx.StaticText(self, label=" (Clic derecho sobre un bloque para eliminarlo)")
        lbl_info.SetForegroundColour(wx.Colour(120, 120, 120))
        
        toolbar.Add(btn_nuevo, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        toolbar.Add(btn_pdf, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        toolbar.Add(lbl_info, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.canvas = wx.Panel(self)
        self.canvas.Bind(wx.EVT_PAINT, self.on_paint)
        self.canvas.Bind(wx.EVT_SIZE, self.on_resize)
        #Evita el parpadeo en Windows/Linux al redibujar
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        self.sizer.Add(toolbar, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
        
        btn_nuevo.Bind(wx.EVT_BUTTON, self.on_nuevo_bloque)
        btn_pdf.Bind(wx.EVT_BUTTON, self.on_exportar_pdf)
        
        wx.CallAfter(self.cargar_bloques_desde_bd)

    def cargar_bloques_desde_bd(self):
        w, h = self.canvas.GetSize()
        margin_left = 60
        margin_top = 30
        col_w = (w - margin_left) // 7
        row_h = (h - margin_top) // len(HORARIOS)
        
        for b in self.db.obtener_bloques_planner():
            bloque = DraggableBlock(self.canvas, b['id'], b['titulo'], b['columna'], b['fila'], b['color'], self.db)
            bloque.ajustar_posicion_grilla(col_w, row_h, margin_left, margin_top)
        self.canvas.Refresh()

    def on_resize(self, event):
        w, h = self.canvas.GetSize()
        margin_left = 60
        margin_top = 30
        col_w = (w - margin_left) // 7
        row_h = (h - margin_top) // len(HORARIOS)
        
        for child in self.canvas.GetChildren():
            if isinstance(child, DraggableBlock):
                child.ajustar_posicion_grilla(col_w, row_h, margin_left, margin_top)
        event.Skip()
        self.canvas.Refresh()

    def on_paint(self, event):
        #Usamos AutoBufferedPaintDC para evitar el parpadeo negro
        dc = wx.AutoBufferedPaintDC(self.canvas)
        
        #Detectar de forma segura si estamos en modo oscuro
        try:
            es_oscuro = wx.GetTopLevelParent(self).es_oscuro
        except AttributeError:
            es_oscuro = False
            
        #Paleta de colores según el modo
        bg_grid = wx.Colour(35, 35, 35) if es_oscuro else wx.WHITE
        bg_header = wx.Colour(50, 60, 80) if es_oscuro else wx.Colour(230, 240, 255)
        bg_time = wx.Colour(45, 45, 45) if es_oscuro else wx.Colour(240, 240, 240)
        line_color = wx.Colour(70, 70, 70) if es_oscuro else wx.Colour(220, 220, 220)
        text_color = wx.Colour(230, 230, 230) if es_oscuro else wx.BLACK
        
        #Pintar el fondo base
        w, h = self.canvas.GetSize()
        dc.SetBrush(wx.Brush(bg_grid))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0, 0, w, h)
        
        margin_left = 60
        margin_top = 30
        
        col_w = (w - margin_left) // 7
        row_h = (h - margin_top) // len(HORARIOS)
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.SetTextForeground(text_color)
        
        #Dibujar cabeceras de días
        for i, dia in enumerate(dias):
            x = margin_left + i * col_w
            dc.SetBrush(wx.Brush(bg_header))
            dc.SetPen(wx.Pen(line_color, 1))
            dc.DrawRectangle(x, 0, col_w, margin_top)
            dc.DrawText(dia, x + 15, 8)
            dc.DrawLine(x, margin_top, x, h)

        #Dibujar columna de referencia de horas
        for j, hora in enumerate(HORARIOS):
            y = margin_top + j * row_h
            dc.SetBrush(wx.Brush(bg_time))
            dc.DrawRectangle(0, y, margin_left, row_h)
            dc.DrawText(hora, 10, y + (row_h // 2) - 6)
            
            dc.SetPen(wx.Pen(line_color, 1))
            dc.DrawLine(margin_left, y, w, y)

    def on_nuevo_bloque(self, event):
        titulo = wx.GetTextFromUser("Asignar Nombre a la Actividad:", "Nueva Actividad")
        if titulo.strip():
            color_elegido = wx.GetColourFromUser(self, wx.Colour(108, 160, 209))
            if not color_elegido.IsOk(): return
            
            color_hex = color_elegido.GetAsString(wx.C2S_HTML_SYNTAX)
            
            w, h = self.canvas.GetSize()
            margin_left = 60
            margin_top = 30
            col_w = (w - margin_left) // 7
            row_h = (h - margin_top) // len(HORARIOS)
            
            db_id = self.db.guardar_bloque_planner(titulo, 0, 0, color_hex)
            
            b = DraggableBlock(self.canvas, db_id, titulo, 0, 0, color_hex, self.db)
            b.ajustar_posicion_grilla(col_w, row_h, margin_left, margin_top)
            self.canvas.Refresh()

    def on_exportar_pdf(self, event):
        with wx.FileDialog(self, "Exportar Cronograma en PDF", wildcard="PDF (*.pdf)|*.pdf", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                bloques_lista = []
                for child in self.canvas.GetChildren():
                    if isinstance(child, DraggableBlock):
                        bloques_lista.append({
                            'titulo': child.label,
                            'columna': child.col,
                            'fila': child.row,
                            'color': child.color_hex
                        })
                
                exportar_planner_pdf(dlg.GetPath(), bloques_lista)
                wx.MessageBox("Tu archivo PDF se ha descargado y coincide exactamente con tu diseño.", "Éxito")