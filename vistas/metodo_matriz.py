import wx
import json

class PanelMatriz(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # GridSizer para dividir la pantalla en 4 partes iguales
        sizer = wx.GridSizer(rows=2, cols=2, hgap=15, vgap=15)
        
        # Se reemplazaron los paneles de colores planos por "StaticBox" nativos del sistema
        self.t1 = self.crear_cuadrante(sizer, "1. Conocimiento Previo", "¿Qué sé ya sobre este tema antes de leer?")
        self.t2 = self.crear_cuadrante(sizer, "2. Dudas Iniciales", "¿Qué quiero aprender o averiguar hoy?")
        self.t3 = self.crear_cuadrante(sizer, "3. Síntesis (Apunte Real)", "Escribe aquí tu resumen luego de estudiar los materiales...")
        self.t4 = self.crear_cuadrante(sizer, "4. Dudas Pendientes", "Lo que no entendí y debo preguntarle al profesor...")
        
        self.SetSizer(sizer)

    def crear_cuadrante(self, main_sizer, titulo, hint):
        # Crear la caja nativa con su título incorporado
        caja = wx.StaticBox(self, label=titulo)
        caja.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Sizer especial para elementos StaticBox
        box_sizer = wx.StaticBoxSizer(caja, wx.VERTICAL)
        
        # El área de texto ocupa toda la caja
        txt = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.BORDER_NONE)
        txt.SetHint(hint)
        
        # Ensamblamos la caja y la agregamos al Grid principal
        box_sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 8)
        main_sizer.Add(box_sizer, 1, wx.EXPAND | wx.ALL, 5)
        
        return txt

    def get_data(self):
        return json.dumps({
            "1": self.t1.GetValue(), 
            "2": self.t2.GetValue(),
            "3": self.t3.GetValue(), 
            "4": self.t4.GetValue()
        })

    def load_data(self, data_str):
        self.t1.Clear()
        self.t2.Clear()
        self.t3.Clear()
        self.t4.Clear()
        
        if not data_str: 
            return
            
        try:
            data = json.loads(data_str)
            self.t1.SetValue(data.get("1", ""))
            self.t2.SetValue(data.get("2", ""))
            self.t3.SetValue(data.get("3", ""))
            self.t4.SetValue(data.get("4", ""))
        except:
            # Por si acaso la data vieja no estaba en formato JSON
            self.t3.SetValue(data_str)