import wx
import os
import subprocess
import webbrowser  # NUEVO: Librería nativa de Python para abrir el navegador web

class PanelMaterias(wx.Panel):
    def __init__(self, parent, db, main_frame):
        super().__init__(parent)
        self.db = db
        self.main_frame = main_frame
        self.materia_actual_id = None
        
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE | wx.SP_3D)
        
        # --- Panel Izquierdo (Árbol) ---
        self.left_panel = wx.Panel(splitter)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        # TreeCtrl para mostrar materias
        self.tree = wx.TreeCtrl(self.left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_NO_LINES)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_materia_seleccionada)
        btn_nueva = wx.Button(self.left_panel, label="+ Añadir Materia")
        btn_nueva.Bind(wx.EVT_BUTTON, self.on_nueva_materia)
        
        left_sizer.Add(wx.StaticText(self.left_panel, label="Mis Materias"), 0, wx.ALL | wx.ALIGN_CENTER, 10)
        left_sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(btn_nueva, 0, wx.EXPAND | wx.ALL, 5)
        self.left_panel.SetSizer(left_sizer)
        
        # --- Panel Derecho (Archivos) ---
        self.right_panel = wx.Panel(splitter)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.lbl_titulo = wx.TextCtrl(self.right_panel, style=wx.TE_PROCESS_ENTER | wx.BORDER_NONE)
        self.lbl_titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        form_sizer = wx.FlexGridSizer(rows=4, cols=2, vgap=10, hgap=10)
        form_sizer.AddGrowableCol(1, 1)
        self.txt_profesor = wx.TextCtrl(self.right_panel)
        self.txt_horario = wx.TextCtrl(self.right_panel)
        self.combo_estado = wx.ComboBox(self.right_panel, choices=["Cursando", "Finalizada"], style=wx.CB_READONLY)
        
        # --- NUEVO: SISTEMA DE ENLACES CON BOTÓN ---
        # Le quitamos el formato multilínea para que sea una simple barra de URL
        self.txt_links = wx.TextCtrl(self.right_panel) 
        
        self.btn_abrir_link = wx.Button(self.right_panel, label="🌐 Ir al Link")
        self.btn_abrir_link.Bind(wx.EVT_BUTTON, self.on_abrir_link_web)
        
        link_sizer = wx.BoxSizer(wx.HORIZONTAL)
        link_sizer.Add(self.txt_links, 1, wx.EXPAND | wx.RIGHT, 5)
        link_sizer.Add(self.btn_abrir_link, 0)
        # ------------------------------------------
        
        form_sizer.Add(wx.StaticText(self.right_panel, label="Profesor/a:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.txt_profesor, 1, wx.EXPAND)
        form_sizer.Add(wx.StaticText(self.right_panel, label="Días y Horarios:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.txt_horario, 1, wx.EXPAND)
        form_sizer.Add(wx.StaticText(self.right_panel, label="Link (Zoom/Meet/Drive):"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(link_sizer, 1, wx.EXPAND) # Agregamos el Sizer combinado aquí
        form_sizer.Add(wx.StaticText(self.right_panel, label="Estado:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.combo_estado, 1, wx.EXPAND)
        
        btn_guardar_mat = wx.Button(self.right_panel, label="💾 Guardar Datos de Materia")
        btn_guardar_mat.Bind(wx.EVT_BUTTON, self.on_guardar_materia)
        
        toolbar_archivos = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_subir = wx.Button(self.right_panel, label="+ Adjuntar Archivo")
        self.btn_subir.Bind(wx.EVT_BUTTON, self.on_subir_archivo)
        toolbar_archivos.Add(wx.StaticText(self.right_panel, label="Material de Estudio"), 1, wx.ALIGN_CENTER_VERTICAL)
        toolbar_archivos.Add(self.btn_subir, 0)
        
        self.list_ctrl = wx.ListCtrl(self.right_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.InsertColumn(0, "Archivo", width=300)
        self.list_ctrl.InsertColumn(1, "Tipo", width=100)
        self.list_ctrl.InsertColumn(2, "Fecha", width=120)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir_archivo)
        
        # Diccionarios de datos para la lista
        self.rutas_archivos = {}
        self.ids_archivos = {}
        self.items_es_apunte = {}
        
        right_sizer.Add(self.lbl_titulo, 0, wx.EXPAND | wx.ALL, 15)
        right_sizer.Add(form_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        right_sizer.Add(btn_guardar_mat, 0, wx.ALIGN_RIGHT | wx.ALL, 15)
        right_sizer.Add(wx.StaticLine(self.right_panel), 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(toolbar_archivos, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        right_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        self.right_panel.SetSizer(right_sizer)
        self.right_panel.Disable()
        
        # Ensamblaje del splitter
        splitter.SplitVertically(self.left_panel, self.right_panel, 250)
        splitter.SetSashGravity(0.0) 
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        
        self.cargar_arbol()
        
        # FIX: Fuerza al Splitter a acomodarse al instante
        wx.CallAfter(self.finalizar_layout)

    def finalizar_layout(self):
        """Fuerza al panel a recalcular su tamaño inicial."""
        if not self: return 
        self.Layout()
        self.tree.Refresh()

    # --- NUEVO: FUNCIÓN PARA ABRIR NAVEGADOR ---
    def on_abrir_link_web(self, event):
        url = self.txt_links.GetValue().strip()
        if url:
            # Si el usuario olvidó poner 'http://' o 'https://', el código lo arregla por él
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url
            webbrowser.open(url)
        else:
            wx.MessageBox("No hay ningún link guardado en esta materia.", "Sin link", wx.OK | wx.ICON_INFORMATION)

    def cargar_arbol(self):
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Materias")
        for row in self.db.obtener_materias():
            mat = dict(row) # <-- CONVERTIMOS A DICCIONARIO AQUÍ
            es_oscuro = self.main_frame.es_oscuro
            color = wx.Colour(17, 46, 107) if mat.get('estado') == "Finalizada" else wx.Colour(0, 85, 150)
            if es_oscuro: 
                 color = wx.Colour(230, 235, 250) if mat.get('estado') == "Finalizada" else wx.Colour(108, 160, 209)
                 
            item = self.tree.AppendItem(self.root, mat['nombre'])
            self.tree.SetItemData(item, mat['id'])
            self.tree.SetItemTextColour(item, color)
        self.tree.ExpandAll()

    def on_nueva_materia(self, event):
        nombre = wx.GetTextFromUser("Nombre de la materia:", "Nueva Materia")
        if nombre.strip():
            # Pasamos valores vacíos iniciales
            self.db.agregar_materia(nombre, "", "", "", "Cursando")
            self.cargar_arbol()

    def on_materia_seleccionada(self, event):
        item = event.GetItem()
        if item == self.tree.GetRootItem() or item == self.root:
            self.right_panel.Disable()
            return
        self.materia_actual_id = self.tree.GetItemData(item)
        
        # <-- CONVERTIMOS A DICCIONARIO EN LA BÚSQUEDA -->
        materia_data = next((dict(m) for m in self.db.obtener_materias() if m['id'] == self.materia_actual_id), None)
        
        if materia_data:
            self.right_panel.Enable()
            self.lbl_titulo.SetValue(materia_data['nombre'])
            # Usamos 'or ""' para evitar que se escriba "None" si el campo está vacío en la base de datos
            self.txt_profesor.SetValue(materia_data.get('profesor') or '')
            self.txt_horario.SetValue(materia_data.get('horario') or '')
            self.txt_links.SetValue(materia_data.get('link_clases') or '')
            self.combo_estado.SetValue(materia_data.get('estado') or 'Cursando')
            self.cargar_archivos()

    def on_guardar_materia(self, event):
        if self.materia_actual_id:
            self.db.actualizar_materia(
                self.materia_actual_id,
                self.lbl_titulo.GetValue(),
                self.txt_profesor.GetValue(),
                self.txt_links.GetValue(),
                self.txt_horario.GetValue()
            )
            # Actualizamos también el estado de la materia
            estado_actual = self.combo_estado.GetValue()
            self.db.cursor.execute("UPDATE materias SET estado=? WHERE id=?", (estado_actual, self.materia_actual_id))
            self.db.conn.commit()
            
            self.cargar_arbol()
            wx.MessageBox("Datos guardados correctamente.", "Éxito")

    def on_subir_archivo(self, event):
        with wx.FileDialog(self, "Seleccionar Material", wildcard="*.*", style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                ruta = dlg.GetPath()
                # Tu db manager solo pide materia_id y ruta, él saca el nombre
                self.db.agregar_material(self.materia_actual_id, ruta)
                self.cargar_archivos()

    def cargar_archivos(self):
        self.list_ctrl.DeleteAllItems()
        self.rutas_archivos.clear()
        self.ids_archivos.clear()
        self.items_es_apunte = {}
        
        # FIX: Colores de alto contraste
        try:
            top_level = wx.GetTopLevelParent(self)
            es_oscuro = top_level.es_oscuro
            fg = wx.Colour(230, 235, 250) if es_oscuro else wx.Colour(17, 46, 107)
            bg = wx.Colour(28, 39, 70) if es_oscuro else wx.Colour(242, 245, 250)
        except AttributeError:
            fg = wx.Colour(17, 46, 107)
            bg = wx.Colour(242, 245, 250)

        try:
            indice_fila = 0
            
            # 1. Cargar Archivos Físicos
            for mat in self.db.obtener_materiales(self.materia_actual_id):
                self.list_ctrl.InsertItem(indice_fila, "📄 " + mat['nombre'])
                self.list_ctrl.SetItem(indice_fila, 1, mat['tipo'])
                fecha = mat['fecha_sub'] if 'fecha_sub' in mat.keys() else '-'
                self.list_ctrl.SetItem(indice_fila, 2, fecha)
                
                self.rutas_archivos[indice_fila] = mat['ruta']
                self.ids_archivos[indice_fila] = mat['id']
                self.items_es_apunte[indice_fila] = False
                
                self.list_ctrl.SetItemTextColour(indice_fila, fg)
                self.list_ctrl.SetItemBackgroundColour(indice_fila, bg)
                indice_fila += 1
                
            # 2. Cargar Apuntes de esta Materia
            self.db.cursor.execute("SELECT id, nombre, metodo, fecha_creacion FROM apuntes WHERE materia_id=?", (self.materia_actual_id,))
            for apunte in self.db.cursor.fetchall():
                self.list_ctrl.InsertItem(indice_fila, "📝 " + apunte['nombre'])
                self.list_ctrl.SetItem(indice_fila, 1, "Apunte (" + apunte['metodo'] + ")")
                self.list_ctrl.SetItem(indice_fila, 2, apunte['fecha_creacion'][:10])
                
                self.rutas_archivos[indice_fila] = apunte['id'] 
                self.items_es_apunte[indice_fila] = True
                
                self.list_ctrl.SetItemTextColour(indice_fila, fg)
                self.list_ctrl.SetItemBackgroundColour(indice_fila, bg)
                indice_fila += 1
                
        except Exception as e:
            wx.MessageBox(f"Ocurrió un error leyendo los archivos:\n{e}", "Error de Lectura", wx.OK | wx.ICON_ERROR)

    def on_abrir_archivo(self, event):
        idx = event.GetIndex()
        es_apunte = self.items_es_apunte.get(idx, False)

        if es_apunte:
            apunte_id = self.rutas_archivos.get(idx)
            titulo = self.list_ctrl.GetItemText(idx, 0).replace("📝 ", "")
            metodo = self.list_ctrl.GetItemText(idx, 1).replace("Apunte (", "").replace(")", "")
            
            self.main_frame.ir_a_apunte(apunte_id, titulo, metodo)
        else:
            ruta = self.rutas_archivos.get(idx)
            if ruta and os.path.exists(ruta):
                if os.name == 'nt': os.startfile(ruta)
                else: subprocess.Popen(['xdg-open', ruta])
            else:
                wx.MessageBox("El archivo físico no se encuentra en la ruta registrada.", "Error de Apertura", wx.OK | wx.ICON_ERROR)