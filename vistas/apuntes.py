import wx
from vistas.editor import EditorEnriquecido
from vistas.metodo_sprint import PanelSprint
from vistas.metodo_matriz import PanelMatriz
from vistas.metodo_flashcards import PanelFlashcards

class PanelApuntes(wx.Panel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.apunte_actual_id = None
        
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        #Cabecera
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_titulo = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.txt_titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        self.lbl_metodo = wx.StaticText(self, label="Método: Ninguno")
        self.lbl_metodo.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        btn_guardar = wx.Button(self, label="💾 Guardar", size=(-1, 35))
        btn_guardar.Bind(wx.EVT_BUTTON, self.on_guardar)
        
        top_sizer.Add(self.txt_titulo, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        top_sizer.Add(self.lbl_metodo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        top_sizer.Add(btn_guardar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        #Contenedor Dinámico
        self.area_trabajo = wx.Panel(self)
        self.area_sizer = wx.BoxSizer(wx.VERTICAL) 
        
        #Cartel de bienvenida
        self.panel_vacio = wx.Panel(self.area_trabajo)
        vacio_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl_vacio = wx.StaticText(self.panel_vacio, label="👈 Ve a 'Inicio' o 'Mis Apuntes' y selecciona un tema para estudiar.")
        lbl_vacio.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_vacio.SetForegroundColour(wx.Colour(120, 120, 120))
        vacio_sizer.AddStretchSpacer()
        vacio_sizer.Add(lbl_vacio, 0, wx.ALIGN_CENTER)
        vacio_sizer.AddStretchSpacer()
        self.panel_vacio.SetSizer(vacio_sizer)
        
        #Instanciar todas las vistas
        self.v_libre = EditorEnriquecido(self.area_trabajo)
        self.v_sprint = PanelSprint(self.area_trabajo)
        self.v_matriz = PanelMatriz(self.area_trabajo)
        self.v_flash = PanelFlashcards(self.area_trabajo)
        
        self.v_libre.Hide()
        self.v_sprint.Hide()
        self.v_matriz.Hide()
        self.v_flash.Hide()
        
        #Agregar al Sizer
        self.area_sizer.Add(self.panel_vacio, 1, wx.EXPAND)
        self.area_sizer.Add(self.v_libre, 1, wx.EXPAND)
        self.area_sizer.Add(self.v_sprint, 1, wx.EXPAND)
        self.area_sizer.Add(self.v_matriz, 1, wx.EXPAND)
        self.area_sizer.Add(self.v_flash, 1, wx.EXPAND)
        self.area_trabajo.SetSizer(self.area_sizer)
        
        self.main_sizer.Add(top_sizer, 0, wx.EXPAND)
        self.main_sizer.Add(self.area_trabajo, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(self.main_sizer)

    def cargar_apunte_desde_home(self, apunte_id, titulo, metodo):
        self.apunte_actual_id = apunte_id
        self.txt_titulo.SetValue(titulo)
        self.lbl_metodo.SetLabel(f"Método: {metodo}")
        
        self.panel_vacio.Hide()
        self.v_libre.Hide()
        self.v_sprint.Hide()
        self.v_matriz.Hide()
        self.v_flash.Hide()
        
        data = next((a for a in self.db.obtener_apuntes() if a['id'] == apunte_id), None)
        contenido = data['contenido_xml'] if data else ""
        
        if metodo == "Sprint de Memoria":
            self.v_sprint.Show()
            self.v_sprint.editor.load_xml(contenido)
            self.v_sprint.btn_corregir.Hide()
            self.v_sprint.btn_materias.Hide()
            self.v_sprint.btn_iniciar.Enable()
            self.v_sprint.editor.bloquear_edicion(False)
        elif metodo == "Matriz de Análisis":
            self.v_matriz.Show()
            self.v_matriz.load_data(contenido)
        elif metodo == "Flashcards":
            self.v_flash.Show()
            self.v_flash.load_data(contenido)
        else:
            self.v_libre.Show()
            self.v_libre.load_xml(contenido)
            
        self.area_trabajo.Layout()
        self.main_sizer.Layout()

    def on_guardar(self, event):
        if self.apunte_actual_id:
            nuevo_titulo = self.txt_titulo.GetValue()
            metodo = self.lbl_metodo.GetLabel().replace("Método: ", "")
            
            if metodo == "Sprint de Memoria": xml = self.v_sprint.editor.get_xml()
            elif metodo == "Matriz de Análisis": xml = self.v_matriz.get_data()
            elif metodo == "Flashcards": xml = self.v_flash.get_data()
            else: xml = self.v_libre.get_xml()
                
            self.db.actualizar_apunte(self.apunte_actual_id, nuevo_titulo, xml)
            
            try:
                parent_notebook = self.GetParent()
                panel_home = parent_notebook.GetPage(0)
                panel_home.cargar_recientes()
                
                panel_mis_apuntes = parent_notebook.GetPage(4)
                panel_mis_apuntes.cargar_lista()
            except: pass
            
            wx.MessageBox("Documento guardado con éxito.", "Guardado", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Crea o selecciona un apunte primero.", "Aviso", wx.ICON_WARNING)