import wx
import os
import subprocess
import sqlite3

# ==========================================
# DIÁLOGO DE CONFIGURACIÓN DE MATERIA
# ==========================================
class DialogoMateria(wx.Dialog):
    def __init__(self, parent, titulo="Nueva Materia", datos=None):
        super().__init__(parent, title=titulo, size=(450, 300))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.txt_nombre = self.crear_campo(sizer, "Nombre de la Materia:")
        self.txt_profesor = self.crear_campo(sizer, "Profesor:")
        self.txt_link = self.crear_campo(sizer, "Link de Clases:")
        self.txt_horario = self.crear_campo(sizer, "Horario de Cursada:")
        
        if datos:
            self.txt_nombre.SetValue(datos['nombre'])
            self.txt_profesor.SetValue(datos['profesor'])
            self.txt_link.SetValue(datos['link_clases'])
            self.txt_horario.SetValue(datos['horario'])
        
        btn_sizer = wx.StdDialogButtonSizer()
        # Al usar wx.ID_OK, Linux le pone el ícono nativo de "Aceptar/Guardar" automáticamente
        btn_ok = wx.Button(self, wx.ID_OK, label="Guardar")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, label="Cancelar")
        btn_sizer.AddButton(btn_ok)
        btn_sizer.AddButton(btn_cancel)
        btn_sizer.Realize()
        
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 15)
        self.SetSizer(sizer)

    def crear_campo(self, sizer, label):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label, size=(140, -1))
        txt = wx.TextCtrl(self)
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(txt, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        return txt

# ==========================================
# PANEL PRINCIPAL DE MATERIAS
# ==========================================
class PanelMaterias(wx.Panel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.materia_actual_id = None
        
        self.rutas_archivos = {}
        self.ids_archivos = {}
        
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        
        # --- PANEL IZQUIERDO (Árbol de navegación) ---
        self.left_panel = wx.Panel(splitter)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_materias = wx.StaticText(self.left_panel, label="Mis Materias")
        lbl_materias.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.tree = wx.TreeCtrl(self.left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_materia_seleccionada)
        
        btn_nueva_materia = wx.Button(self.left_panel, label=" Añadir Materia")
        btn_nueva_materia.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_BUTTON, (16, 16)))
        btn_nueva_materia.Bind(wx.EVT_BUTTON, self.on_nueva_materia)
        
        left_sizer.Add(lbl_materias, 0, wx.ALL, 10)
        left_sizer.Add(self.tree, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        left_sizer.Add(btn_nueva_materia, 0, wx.EXPAND | wx.ALL, 10)
        self.left_panel.SetSizer(left_sizer)
        
        # --- PANEL DERECHO (Contenedor dual) ---
        self.right_panel = wx.Panel(splitter)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Vista A: Estado vacío
        self.panel_vacio = wx.Panel(self.right_panel)
        vacio_sizer = wx.GridSizer(rows=1, cols=1, hgap=0, vgap=0)
        lbl_vacio = wx.StaticText(self.panel_vacio, label="Selecciona una materia o crea una nueva para ver su espacio de estudio.")
        lbl_vacio.SetForegroundColour(wx.Colour(120, 120, 120))
        vacio_sizer.Add(lbl_vacio, 0, wx.ALIGN_CENTER)
        self.panel_vacio.SetSizer(vacio_sizer)
        
        # Vista B: Panel de contenido activo
        self.panel_contenido = wx.Panel(self.right_panel)
        contenido_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Cabecera con título y acciones de la materia
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_titulo_materia = wx.StaticText(self.panel_contenido, label="-")
        self.lbl_titulo_materia.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.btn_editar_mat = wx.Button(self.panel_contenido, label=" Editar")
        self.btn_editar_mat.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_BUTTON, (16, 16)))
        
        self.btn_borrar_mat = wx.Button(self.panel_contenido, label=" Borrar")
        self.btn_borrar_mat.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, (16, 16)))
        
        self.btn_editar_mat.Bind(wx.EVT_BUTTON, self.on_editar_materia)
        self.btn_borrar_mat.Bind(wx.EVT_BUTTON, self.on_borrar_materia)
        
        header_sizer.Add(self.lbl_titulo_materia, 1, wx.ALIGN_CENTER_VERTICAL)
        header_sizer.Add(self.btn_editar_mat, 0, wx.RIGHT, 5)
        header_sizer.Add(self.btn_borrar_mat, 0)
        
        # Tarjeta informativa
        info_card = wx.Panel(self.panel_contenido)
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        self.datos_grid = wx.GridSizer(rows=2, cols=2, hgap=20, vgap=10)
        self.lbl_profesor = wx.StaticText(info_card, label="Profesor: -")
        self.lbl_link = wx.StaticText(info_card, label="Link Clases: -")
        self.lbl_horario = wx.StaticText(info_card, label="Horario: -")
        self.lbl_estado = wx.StaticText(info_card, label="Estado: -")
        
        for lbl in [self.lbl_profesor, self.lbl_link, self.lbl_horario, self.lbl_estado]:
            lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
        self.datos_grid.AddMany([self.lbl_profesor, self.lbl_link, self.lbl_horario, self.lbl_estado])
        info_sizer.Add(self.datos_grid, 1, wx.EXPAND | wx.ALL, 10)
        info_card.SetSizer(info_sizer)
        
        # Barra de herramientas de archivos
        toolbar_archivos = wx.BoxSizer(wx.HORIZONTAL)
        lbl_seccion_archivos = wx.StaticText(self.panel_contenido, label="Material de Estudio Descargado")
        lbl_seccion_archivos.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.btn_subir = wx.Button(self.panel_contenido, label=" Adjuntar Archivo")
        self.btn_subir.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16, 16)))
        
        self.btn_eliminar_archivo = wx.Button(self.panel_contenido, label=" Eliminar Archivo")
        self.btn_eliminar_archivo.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_BUTTON, (16, 16)))
        
        self.btn_subir.Bind(wx.EVT_BUTTON, self.on_subir_archivo)
        self.btn_eliminar_archivo.Bind(wx.EVT_BUTTON, self.on_eliminar_archivo)
        
        toolbar_archivos.Add(lbl_seccion_archivos, 1, wx.ALIGN_CENTER_VERTICAL)
        toolbar_archivos.Add(self.btn_subir, 0, wx.RIGHT, 5)
        toolbar_archivos.Add(self.btn_eliminar_archivo, 0)
        
        # Listado de archivos
        self.list_ctrl = wx.ListCtrl(self.panel_contenido, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.InsertColumn(0, "Nombre del Archivo", width=280)
        self.list_ctrl.InsertColumn(1, "Tipo", width=80)
        self.list_ctrl.InsertColumn(2, "Fecha", width=120)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir_archivo)
        
        # Estructurar Vista B
        contenido_sizer.Add(header_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        contenido_sizer.Add(info_card, 0, wx.EXPAND | wx.BOTTOM, 15)
        contenido_sizer.Add(toolbar_archivos, 0, wx.EXPAND | wx.BOTTOM, 10)
        contenido_sizer.Add(self.list_ctrl, 1, wx.EXPAND)
        self.panel_contenido.SetSizer(contenido_sizer)
        self.panel_contenido.Hide() 
        
        # Añadir ambas vistas al sizer del panel derecho
        self.right_sizer.Add(self.panel_vacio, 1, wx.EXPAND | wx.ALL, 20)
        self.right_sizer.Add(self.panel_contenido, 1, wx.EXPAND | wx.ALL, 15)
        self.right_panel.SetSizer(self.right_sizer)
        
        splitter.SplitVertically(self.left_panel, self.right_panel, 250)
        splitter.SetMinimumPaneSize(200)
        
        main_layout = wx.BoxSizer(wx.VERTICAL)
        main_layout.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(main_layout)
        
        self.cargar_arbol()

    def cargar_arbol(self):
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("Materias")
        for mat in self.db.obtener_materias():
            item = self.tree.AppendItem(root, mat['nombre'])
            self.tree.SetItemData(item, mat['id'])
        self.tree.ExpandAll()

    def on_nueva_materia(self, event):
        dlg = DialogoMateria(self, "Añadir Nueva Materia")
        if dlg.ShowModal() == wx.ID_OK:
            nombre = dlg.txt_nombre.GetValue().strip()
            if nombre:
                try:
                    self.db.agregar_materia(
                        nombre=nombre,
                        profesor=dlg.txt_profesor.GetValue().strip() or "No asignado",
                        link=dlg.txt_link.GetValue().strip() or "-",
                        horario=dlg.txt_horario.GetValue().strip() or "-",
                        estado="Cursando"
                    )
                    self.cargar_arbol()
                except Exception as e:
                    wx.MessageBox(f"Error al guardar materia:\n{e}", "Error", wx.ICON_ERROR)
        dlg.Destroy()

    def on_materia_seleccionada(self, event):
        item = event.GetItem()
        if item == self.tree.GetRootItem() or not item.IsOk():
            self.panel_contenido.Hide()
            self.panel_vacio.Show()
            self.right_sizer.Layout()
            return
        
        self.materia_actual_id = self.tree.GetItemData(item)
        self.actualizar_dashboard_materia()

    def actualizar_dashboard_materia(self):
        materia_data = next((m for m in self.db.obtener_materias() if m['id'] == self.materia_actual_id), None)
        if materia_data:
            self.lbl_titulo_materia.SetLabel(materia_data['nombre'])
            self.lbl_profesor.SetLabel(f"Profesor: {materia_data['profesor']}")
            self.lbl_link.SetLabel(f"Link Clases: {materia_data['link_clases']}")
            self.lbl_horario.SetLabel(f"Horario: {materia_data['horario']}")
            self.lbl_estado.SetLabel(f"Estado: {materia_data['estado']}")
            
            self.panel_vacio.Hide()
            self.panel_contenido.Show()
            self.right_sizer.Layout()
            self.cargar_archivos()

    def on_editar_materia(self, event):
        materia_data = None
        for m in self.db.obtener_materias():
            if m['id'] == self.materia_actual_id:
                materia_data = m
                break
                
        if not materia_data: return
        
        datos_previos = {
            'nombre': materia_data['nombre'],
            'profesor': materia_data['profesor'],
            'link_clases': materia_data['link_clases'],
            'horario': materia_data['horario']
        }
        
        dlg = DialogoMateria(self, "Editar Configuración de Materia", datos_previos)
        if dlg.ShowModal() == wx.ID_OK:
            nombre = dlg.txt_nombre.GetValue().strip()
            if nombre:
                self.db.actualizar_materia(
                    self.materia_actual_id,
                    nombre,
                    dlg.txt_profesor.GetValue().strip(),
                    dlg.txt_link.GetValue().strip(),
                    dlg.txt_horario.GetValue().strip()
                )
                self.cargar_arbol()
                self.actualizar_dashboard_materia()
        dlg.Destroy()

    def on_borrar_materia(self, event):
        if wx.MessageBox("¿Estás seguro de que deseas eliminar esta materia?\nSe borrarán permanentemente todos sus registros y referencias a archivos vinculados.", 
                          "Confirmar Eliminación", wx.YES_NO | wx.ICON_WARNING) == wx.YES:
            self.db.eliminar_materia(self.materia_actual_id)
            self.materia_actual_id = None
            self.panel_contenido.Hide()
            self.panel_vacio.Show()
            self.right_sizer.Layout()
            self.cargar_arbol()

    def on_subir_archivo(self, event):
        with wx.FileDialog(self, "Seleccionar Archivo", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    self.db.agregar_material(self.materia_actual_id, dlg.GetPath())
                    self.cargar_archivos()
                except Exception as e:
                    wx.MessageBox(f"Error al guardar en base de datos:\n{e}", "Error Interno", wx.OK | wx.ICON_ERROR)

    def on_eliminar_archivo(self, event):
        sel = self.list_ctrl.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        if sel == -1:
            wx.MessageBox("Por favor, selecciona un archivo de la lista para eliminarlo.", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
            
        file_id = self.ids_archivos.get(sel)
        if file_id and wx.MessageBox("¿Deseas desvincular este archivo de la materia?", "Eliminar Archivo", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.db.eliminar_material(file_id)
            self.cargar_archivos()

    def cargar_archivos(self):
        self.list_ctrl.DeleteAllItems()
        self.rutas_archivos.clear()
        self.ids_archivos.clear()
        
        # Recuperamos los colores de la paleta actual para pintar la lista
        try:
            top_level = wx.GetTopLevelParent(self)
            es_oscuro = top_level.es_oscuro
            fg = wx.Colour(230, 230, 230) if es_oscuro else wx.Colour(30, 30, 30)
            bg = wx.Colour(50, 50, 50) if es_oscuro else wx.Colour(255, 255, 255)
        except AttributeError:
            fg = wx.Colour(30, 30, 30)
            bg = wx.Colour(255, 255, 255)

        try:
            for index, mat in enumerate(self.db.obtener_materiales(self.materia_actual_id)):
                self.list_ctrl.InsertItem(index, mat['nombre'])
                self.list_ctrl.SetItem(index, 1, mat['tipo'])
                
                fecha = mat['fecha_sub'] if 'fecha_sub' in mat.keys() else '-'
                self.list_ctrl.SetItem(index, 2, fecha)
                
                self.rutas_archivos[index] = mat['ruta']
                self.ids_archivos[index] = mat['id']
                
                # Coloreado dinámico para evadir el bug de GTK
                self.list_ctrl.SetItemTextColour(index, fg)
                self.list_ctrl.SetItemBackgroundColour(index, bg)
                
        except Exception as e:
            wx.MessageBox(f"Ocurrió un error leyendo los archivos:\n{e}", "Error de Lectura", wx.OK | wx.ICON_ERROR)

    def on_abrir_archivo(self, event):
        ruta = self.rutas_archivos.get(event.GetIndex())
        if ruta and os.path.exists(ruta):
            if os.name == 'nt': os.startfile(ruta)
            else: subprocess.Popen(['xdg-open', ruta])
        else:
            wx.MessageBox("El archivo físico no se encuentra en la ruta original registrada.", "Error de Apertura", wx.OK | wx.ICON_ERROR)