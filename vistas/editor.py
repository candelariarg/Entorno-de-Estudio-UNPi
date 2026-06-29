import wx
import wx.richtext as rt
import io

rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

#Dialogo para ajustar el tamaño de la imagen antes de insertarla:

class DialogoAjusteImagen(wx.Dialog):
    def __init__(self, parent, img):
        super().__init__(parent, title="Ajustar Tamaño de Imagen")
        self.img = img
        self.escala = 100
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        lbl_titulo = wx.StaticText(self, label="Ajusta la imagen antes de insertarla:")
        lbl_titulo.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(lbl_titulo, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        
        self.lbl_info = wx.StaticText(self, label=f"Tamaño original: {img.GetWidth()} x {img.GetHeight()} px")
        sizer.Add(self.lbl_info, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        self.slider = wx.Slider(self, value=100, minValue=10, maxValue=300, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slide)
        sizer.Add(self.slider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        self.lbl_preview = wx.StaticText(self, label=f"Tamaño final: {img.GetWidth()} x {img.GetHeight()} px")
        self.lbl_preview.SetForegroundColour(wx.Colour(0, 100, 200))
        self.lbl_preview.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(self.lbl_preview, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL, label="❌ Cancelar")
        self.btn_ok = wx.Button(self, wx.ID_OK, label="✔️ Insertar Imagen")
        btn_sizer.Add(self.btn_cancel, 0, wx.RIGHT, 15)
        btn_sizer.Add(self.btn_ok, 0)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        
        self.SetSizer(sizer)
        self.Fit()
        self.Center()
        
    def on_slide(self, event):
        self.escala = self.slider.GetValue()
        nw = int(self.img.GetWidth() * (self.escala / 100.0))
        nh = int(self.img.GetHeight() * (self.escala / 100.0))
        self.lbl_preview.SetLabel(f"Tamaño final: {nw} x {nh} px")
        self.Layout()


#Editor con barra de herramientas y funcionalidades de formato de texto, imágenes y tablas:
class EditorEnriquecido(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- FILA 1: Estilos de Texto, Alineación y Elementos ---
        self.toolbar1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_bold = wx.Button(self, label="N", size=(35, 35))
        self.btn_bold.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btn_italic = wx.Button(self, label="C", size=(35, 35))
        self.btn_italic.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.btn_under = wx.Button(self, label="S", size=(35, 35))
        self.btn_under.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True))
        
        self.btn_hl = wx.Button(self, label="🖍 Resaltar", size=(-1, 35))
        self.btn_color = wx.Button(self, label="🎨 Letra", size=(-1, 35))
        self.btn_font = wx.Button(self, label="abc Tipografía", size=(-1, 35))
        
        self.btn_align_l = wx.Button(self, label="⇤ Izq", size=(-1, 35))
        self.btn_align_c = wx.Button(self, label="↔ Centro", size=(-1, 35))
        self.btn_align_r = wx.Button(self, label="⇥ Der", size=(-1, 35))

        self.btn_undo = wx.Button(self, label="↩ Deshacer", size=(-1, 35))
        self.btn_redo = wx.Button(self, label="↪ Rehacer", size=(-1, 35))
        
        self.btn_img = wx.Button(self, label="📷 Imagen", size=(-1, 35))
        self.btn_table = wx.Button(self, label="▦ Tabla", size=(-1, 35))


        for b in [self.btn_bold, self.btn_italic, self.btn_under]:
            self.toolbar1.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.toolbar1.AddSpacer(10)
        for b in [self.btn_undo, self.btn_redo]:
            self.toolbar1.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.toolbar1.AddSpacer(10)
        for b in [self.btn_hl, self.btn_color, self.btn_font]:
            self.toolbar1.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.toolbar1.AddSpacer(10)
        for b in [self.btn_align_l, self.btn_align_c, self.btn_align_r]:
            self.toolbar1.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.toolbar1.AddStretchSpacer()
        for b in [self.btn_img, self.btn_table]:
            self.toolbar1.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        #Sangrías y Espaciados (de la demo)
        self.toolbar2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_ind_less = wx.Button(self, label="⬅️ - Sangría", size=(-1, 35))
        self.btn_ind_more = wx.Button(self, label="+ Sangría ➡️", size=(-1, 35))
        
        self.btn_ls_1 = wx.Button(self, label="↕️ Línea x1.0", size=(-1, 35))
        self.btn_ls_15 = wx.Button(self, label="↕️ Línea x1.5", size=(-1, 35))
        self.btn_ls_2 = wx.Button(self, label="↕️ Línea x2.0", size=(-1, 35))
        
        self.btn_ps_less = wx.Button(self, label="⬆️ - Párrafo", size=(-1, 35))
        self.btn_ps_more = wx.Button(self, label="⬇️ + Párrafo", size=(-1, 35))

        for b in [self.btn_ind_less, self.btn_ind_more]:
            self.toolbar2.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.toolbar2.AddSpacer(15)
        for b in [self.btn_ls_1, self.btn_ls_15, self.btn_ls_2]:
            self.toolbar2.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.toolbar2.AddSpacer(15)
        for b in [self.btn_ps_less, self.btn_ps_more]:
            self.toolbar2.Add(b, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        #Area de texto
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.BORDER_SUNKEN)
        self.rtc.SetMargins(15, 15)
        
        # Ensamblar Sizers
        self.sizer.Add(self.toolbar1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.sizer.Add(self.toolbar2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.sizer.Add(self.rtc, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
        
        #Bindeos
        self.btn_bold.Bind(wx.EVT_BUTTON, lambda e: self.rtc.ApplyBoldToSelection())
        self.btn_italic.Bind(wx.EVT_BUTTON, lambda e: self.rtc.ApplyItalicToSelection())
        self.btn_under.Bind(wx.EVT_BUTTON, lambda e: self.rtc.ApplyUnderlineToSelection())

        self.btn_undo.Bind(wx.EVT_BUTTON, self.OnUndo)
        self.btn_redo.Bind(wx.EVT_BUTTON, self.OnRedo)
        
        self.btn_color.Bind(wx.EVT_BUTTON, self.OnColour)
        self.btn_hl.Bind(wx.EVT_BUTTON, self.OnHighlight)
        self.btn_font.Bind(wx.EVT_BUTTON, self.OnFont)
        
        self.btn_align_l.Bind(wx.EVT_BUTTON, self.OnAlignLeft)
        self.btn_align_c.Bind(wx.EVT_BUTTON, self.OnAlignCenter)
        self.btn_align_r.Bind(wx.EVT_BUTTON, self.OnAlignRight)
        
        self.btn_ind_more.Bind(wx.EVT_BUTTON, self.OnIndentMore)
        self.btn_ind_less.Bind(wx.EVT_BUTTON, self.OnIndentLess)
        
        self.btn_ls_1.Bind(wx.EVT_BUTTON, self.OnLineSpacingSingle)
        self.btn_ls_15.Bind(wx.EVT_BUTTON, self.OnLineSpacingHalf)
        self.btn_ls_2.Bind(wx.EVT_BUTTON, self.OnLineSpacingDouble)
        
        self.btn_ps_more.Bind(wx.EVT_BUTTON, self.OnParagraphSpacingMore)
        self.btn_ps_less.Bind(wx.EVT_BUTTON, self.OnParagraphSpacingLess)
        
        self.btn_img.Bind(wx.EVT_BUTTON, self.OnInsertImage)
        self.btn_table.Bind(wx.EVT_BUTTON, self.OnInsertTable)



    #Funciones de Formato de Texto y Alineación (de la demo)

    def OnUndo(self, evt):
        if self.rtc.CanUndo():
            self.rtc.Undo()

    def OnRedo(self, evt):
        if self.rtc.CanRedo():
            self.rtc.Redo()
            
    def OnAlignLeft(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

    def OnAlignRight(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

    def OnAlignCenter(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

    def OnIndentMore(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnIndentLess(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            if attr.GetLeftIndent() >= 100:
                attr.SetLeftIndent(attr.GetLeftIndent() - 100)
                attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
                self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingMore(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20)
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingLess(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20)
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)

    def OnLineSpacingSingle(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingHalf(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingDouble(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection(): r = self.rtc.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)

    #Funciones de Formato de Color, Fuente, Imágenes y Tablas
    def OnHighlight(self, event):
        colorData = wx.ColourData()
        dlg = wx.ColourDialog(self, colorData)
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()
            attr = rt.RichTextAttr()
            attr.SetFlags(wx.TEXT_ATTR_BACKGROUND_COLOUR)
            attr.SetBackgroundColour(color)
            if self.rtc.HasSelection(): self.rtc.SetStyle(self.rtc.GetSelectionRange(), attr)
            else: self.rtc.SetDefaultStyle(attr)
        dlg.Destroy()

    def OnColour(self, event):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            if not self.rtc.HasSelection(): self.rtc.BeginTextColour(colour)
            else:
                r = self.rtc.GetSelectionRange()
                attr = wx.TextAttr()
                attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                attr.SetTextColour(colour)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnFont(self, event):
        if not self.rtc.HasSelection(): return
        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            font = dlg.GetFontData().GetChosenFont()
            if font:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    #Cambiar la ruta para que detecte automáticamente la carpeta "Imágenes" del sistema
    def OnInsertImage(self, event):
        import os
        
        #Obtener la carpeta principal del usuario
        home_dir = os.path.expanduser("~")
        
        #Lista de posibles nombres que el sistema operativo le da a la carpeta
        posibles_nombres = ["Imágenes", "Imagenes", "Pictures", "Mis imágenes", "My Pictures"]
        
        #Si no encuentra la carpeta, abrirá en la carpeta principal del usuario
        carpeta_img = home_dir 
        
        #Buscar cuál de esas carpetas existe realmente en la PC
        for nombre in posibles_nombres:
            ruta_prueba = os.path.join(home_dir, nombre)
            if os.path.exists(ruta_prueba) and os.path.isdir(ruta_prueba):
                carpeta_img = ruta_prueba
                break #Encontramos la correcta, dejamos de buscar

        #Abrir el cuadro de diálogo en la carpeta detectada
        with wx.FileDialog(self, "Seleccionar Imagen", defaultDir=carpeta_img, wildcard="Imágenes (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg", style=wx.FD_OPEN) as dlg_file:
            if dlg_file.ShowModal() == wx.ID_OK:
                img = wx.Image(dlg_file.GetPath())
                dlg_ajuste = DialogoAjusteImagen(self, img)
                if dlg_ajuste.ShowModal() == wx.ID_OK:
                    escala = dlg_ajuste.escala
                    if escala != 100:
                        nw = int(img.GetWidth() * (escala / 100.0))
                        nh = int(img.GetHeight() * (escala / 100.0))
                        img = img.Scale(nw, nh, wx.IMAGE_QUALITY_HIGH)
                    self.rtc.WriteImage(img)
                dlg_ajuste.Destroy()

    def OnInsertTable(self, event):
        filas = wx.GetNumberFromUser("Número de Filas", "Filas:", "Crear Tabla", 3, 1, 20, self)
        if filas <= 0: return
        cols = wx.GetNumberFromUser("Número de Columnas", "Columnas:", "Crear Tabla", 3, 1, 10, self)
        if cols <= 0: return
        self.rtc.WriteTable(filas, cols)

    #Utilidades para bloquear la edición, activar modo corrección y obtener/cargar contenido en formato XML (formato que conserva el estilo y formato del texto, incluyendo imágenes y tablas)
    def bloquear_edicion(self, bloquear):
        self.rtc.SetEditable(not bloquear)
        for toolbar in [self.toolbar1, self.toolbar2]:
            for child in toolbar.GetChildren():
                widget = child.GetWindow()
                if widget and isinstance(widget, wx.Button):
                    widget.Enable(not bloquear)

    def activar_modo_correccion(self):
        self.bloquear_edicion(False)
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        attr.SetTextColour(wx.Colour(180, 0, 0))
        self.rtc.SetDefaultStyle(attr)
        self.rtc.SetFocus()

    def get_xml(self):
        buffer = io.BytesIO()
        handler = rt.RichTextXMLHandler()
        handler.SaveFile(self.rtc.GetBuffer(), buffer)
        return buffer.getvalue().decode('utf-8')

    def load_xml(self, xml_string):
        self.rtc.Clear()
        if xml_string:
            buffer = io.BytesIO(xml_string.encode('utf-8'))
            handler = rt.RichTextXMLHandler()
            try: handler.LoadFile(self.rtc.GetBuffer(), buffer)
            except: pass
        self.rtc.Refresh()