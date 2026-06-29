import wx
import wx.richtext as rt
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor

#Constantes de color para la exportación PDF
COLOR_NAVY = wx.Colour(17, 46, 107)
COLOR_BLUE = wx.Colour(0, 85, 150)
COLOR_LIGHT = wx.Colour(108, 160, 209)

HORARIOS = [f"{h:02d}:00" for h in range(8, 21)] #08:00 a 20:00

#Paleta de colores para los modos claro y oscuro
class Paleta:
    #Modo claro "UNPi LIGHT BLUE"
    #Reemplazamos el blanco genérico por un blanco más puro y brillante
    FONDO_CLARO = wx.Colour(255, 255, 255)
    TEXTO_CLARO = wx.Colour(17, 46, 107)         #Reemplaza el gris oscuro por el azul UNPi
    PANEL_SECUNDARIO_CLARO = wx.Colour(242, 245, 250) 
    
    #Modo oscuro "UNPi DARK BLUE"
    #Reemplazamos los grises genéricos por un azul marino extremadamente profundo y elegante
    FONDO_OSCURO = wx.Colour(15, 22, 40)       
    TEXTO_OSCURO = wx.Colour(230, 235, 250)      #Blanco con un sutil tinte azul para descansar la vista
    PANEL_SECUNDARIO_OSCURO = wx.Colour(28, 39, 70) 

def aplicar_tema(window, es_oscuro):
    """Inyecta los estilos CSS-like a todos los componentes de la app."""
    bg_color = Paleta.FONDO_OSCURO if es_oscuro else Paleta.FONDO_CLARO
    fg_color = Paleta.TEXTO_OSCURO if es_oscuro else Paleta.TEXTO_CLARO
    bg_secundario = Paleta.PANEL_SECUNDARIO_OSCURO if es_oscuro else Paleta.PANEL_SECUNDARIO_CLARO

    window.SetBackgroundColour(bg_color)
    window.SetForegroundColour(fg_color)

    _actualizar_hijos(window, bg_color, fg_color, bg_secundario, es_oscuro)
    window.Refresh()
def _actualizar_hijos(window, bg, fg, bg_sec, es_oscuro):
    for child in window.GetChildren():
        
        #Dejamos que Linux los dibuje con su motor nativo 
        if isinstance(child, (wx.Button, wx.ToggleButton, wx.SpinCtrl)):
            pass 
            
        #Arregla las "Letras negras en fondo negro"
        elif isinstance(child, rt.RichTextCtrl):
            child.SetBackgroundColour(bg_sec)
            
            #Armamos el atributo de color
            attr = wx.TextAttr()
            attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
            attr.SetTextColour(fg)
            child.SetDefaultStyle(attr)
            
            #Le aplicamos el color a todo el texto que ya esté escrito
            try:
                r = rt.RichTextRange(0, child.GetLastPosition())
                child.SetStyle(r, attr)
            except Exception:
                pass
            
        #Arregla la cabecera blanca invisible
        elif isinstance(child, wx.ListCtrl):
            child.SetBackgroundColour(bg_sec)
            child.SetForegroundColour(wx.NullColour) 
            
            for i in range(child.GetItemCount()):
                child.SetItemTextColour(i, fg)
                child.SetItemBackgroundColour(i, bg_sec)

        #Arregla el bug de GTK que hace que los TreeCtrl se vean mal en modo oscuro
        elif isinstance(child, wx.TreeCtrl):
            child.SetBackgroundColour(bg_sec)
            child.SetForegroundColour(fg)
            if child.GetRootItem().IsOk():
                child.SetItemTextColour(child.GetRootItem(), fg)

        #Arregla el bug de GTK que hace que los TextCtrl y ListBox se vean mal en modo oscuro
        elif isinstance(child, (wx.TextCtrl, wx.ListBox)):
            child.SetBackgroundColour(bg_sec)
            child.SetForegroundColour(fg)
            
        #Arregla el bug de GTK que hace que los ComboBox se vean mal en modo oscuro
        else:
            child.SetBackgroundColour(bg)
            child.SetForegroundColour(fg)

        # Recursividad: Buscar dentro de los paneles internos
        _actualizar_hijos(child, bg, fg, bg_sec, es_oscuro)

#Función para exportar la cuadrícula horaria a PDF
def exportar_planner_pdf(ruta_guardado, bloques_data):
    """Genera una copia exacta de la cuadrícula horaria de la app en formato PDF."""
    c = pdf_canvas.Canvas(ruta_guardado, pagesize=landscape(A4))
    w_pdf, h_pdf = landscape(A4)
    
    #Encabezado principal
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#112e6b"))
    c.drawString(40, h_pdf - 35, "Planificación Semanal de Cursada")
    
    margin_left = 70
    margin_top = 60
    grid_w = w_pdf - margin_left - 40
    grid_h = h_pdf - margin_top - 50
    
    col_w = grid_w / 7
    row_h = grid_h / len(HORARIOS)
    
    #Dibujar cabecera de días
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    c.setFont("Helvetica-Bold", 10)
    for i, dia in enumerate(dias):
        x = margin_left + (i * col_w)
        c.setFillColor(HexColor("#112e6b"))
        c.rect(x, h_pdf - margin_top, col_w, 20, fill=1, stroke=0)
        c.setFillColor(HexColor("#ffffff"))
        c.drawCentredString(x + col_w/2, h_pdf - margin_top + 6, dia)

    #Dibujar horarios y líneas de la grilla
    c.setFont("Helvetica-Bold", 9)
    for j, hora in enumerate(HORARIOS):
        y = h_pdf - margin_top - (j * row_h)
        c.setFillColor(HexColor("#333333"))
        c.drawString(25, y - row_h/2 - 3, hora)
        
        c.setStrokeColor(HexColor("#dddddd"))
        c.setLineWidth(0.5)
        c.line(margin_left, y, margin_left + grid_w, y)
    
    #Última línea horizontal inferior
    c.line(margin_left, h_pdf - margin_top - (len(HORARIOS) * row_h), margin_left + grid_w, h_pdf - margin_top - (len(HORARIOS) * row_h))

    #Líneas verticales divisorias
    for i in range(8):
        x = margin_left + (i * col_w)
        c.line(x, h_pdf - margin_top, x, h_pdf - margin_top - (len(HORARIOS) * row_h))

    #Dibujar los bloques dinámicos del usuario
    c.setFont("Helvetica-Bold", 8)
    for b in bloques_data:
        col = b['columna']
        fil = b['fila']
        
        #Calcular posición exacta dentro de la celda de destino
        bx = margin_left + (col * col_w) + 2
        by = h_pdf - margin_top - ((fil + 1) * row_h) + 2
        bw = col_w - 4
        bh = row_h - 4
        
        #Fondo del bloque con su color original
        c.setFillColor(HexColor(b['color']))
        c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=1)
        
        #Texto centrado dentro del bloque del PDF
        c.setFillColor(HexColor("#000000"))
        texto_recortado = b['titulo'][:14] + ".." if len(b['titulo']) > 14 else b['titulo']
        c.drawCentredString(bx + bw/2, by + bh/2 - 3, texto_recortado)

    c.save()