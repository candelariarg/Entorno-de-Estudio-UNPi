import wx
import wx.adv

manualTexto = (
    'Manual de Usuario - Entorno de Estudio UNPi\n'

    'Pestañas Principales:\n\n'

    '1. Inicio:\n'
    'Acá arrancás cada sesión. Escribí el título o tema del apunte, '
    'elegí de qué materia es (opcional) y seleccioná uno de los cuatro '
    'métodos de estudio. Al hacer clic en un método, el apunte se crea y se '
    'abre automáticamente en la pestaña Editor/Estudio.\n\n'

    '2. Materias:\n'
    'Registrá tus materias con nombre, docente, días y horarios, link de clase '
    '(Zoom, Meet, Drive) y estado (Cursando/Finalizada). Desde el botón '
    '"Ir al Link" abrís la URL directamente en tu navegador. '
    'También podés adjuntar archivos a cada materia (PDFs, presentaciones, '
    'imágenes) y ver los apuntes que vinculaste. Doble clic sobre un ítem de la '
    'lista lo abre con el programa correspondiente de tu pc.\n\n'

    '3. Planner:\n'
    'Grilla visual de lunes a domingo con franjas horarias. Creá bloques de '
    'actividad con nombre y color, y arrastralos hasta el día y horario que '
    'corresponda. Clic derecho sobre un bloque para eliminarlo. '
    'Podés exportar tu semana a PDF con el botón "Exportar a PDF".\n\n'

    '4. Editor/Estudio:\n'
    'El área de trabajo central de la aplicación. Se activa al seleccionar un apunte. '
    'Podés editar el título directamente y  guardar con el botón Guardar. '
    'La aplicación NO guarda automáticamente.\n\n'

    '5. Mis Apuntes:\n'
    'Biblioteca con todos tus apuntes guardados. Seleccioná uno y usá los '
    'botones para Abrir, Renombrar o Eliminar. '
    'También podés hacer doble clic para abrirlo directamente.\n\n'

    'Métodos de Estudio:\n\n'

    '1. Apunte Libre:\n'
    'Editor para tomar apuntes con formato: negrita, cursiva, '
    'subrayado, colores, listas y alineación. '
    'Ideal para apuntes de clase y resúmenes.\n\n'

    '2. Sprint de Memoria:\n'
    'Elegí cuántos minutos querés y hacé clic en "Empezar Reto". '
    'Escribí todo lo que recordás del tema sin consultar nada. '
    'Al terminar el tiempo, el editor se bloquea. Luego podés revisar tus '
    'materiales y volver a activar el modo corrección para marcar en rojo '
    'lo que faltó o estaba mal.\n\n'

    '3. Matriz de Análisis:\n'
    'Cuatro cuadrantes para estudiar en profundidad:\n'
    '  1. Conocimiento previo: ¿qué sé antes de empezar?\n'
    '  2. Dudas iniciales: ¿qué quiero aprender hoy?\n'
    '  3. Síntesis: tu resumen real luego de estudiar.\n'
    '  4. Dudas pendientes: lo que quedó sin resolver.\n\n'

    '4. Flashcards:\n'
    'Creá tarjetas con pregunta (frente) y respuesta (dorso). '
    'En Modo Edición agregás y eliminás tarjetas. '
    'En Modo Repaso las tarjetas se mezclan al azar: leés el frente, '
    'pensás la respuesta y girás la tarjeta. '
    '"Lo sabía" avanza; "No lo sabía" devuelve la tarjeta al final del mazo '
    'para repasar de nuevo. El repaso termina cuando acertás todas.\n\n'

    '¡Gracias por usar Entorno de Estudio UNPi!\n'
    'Nyx y Candelaria.'
)

class PanelAcercaDe(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        #Sizer externo: centra verticalmente
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        #Sizer medio: centra horizontalmente
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Sizer del contenido
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        content_sizer.SetMinSize((620, -1))

        #Nombre y versión
        nombre = wx.StaticText(self, label="'Entorno de Estudio UNPi'")
        font_titulo = nombre.GetFont()
        font_titulo.SetPointSize(24)
        font_titulo.SetWeight(wx.FONTWEIGHT_BOLD)
        nombre.SetFont(font_titulo)
        content_sizer.Add(nombre, 0, wx.ALIGN_CENTER_HORIZONTAL, 18)

        version = wx.StaticText(self, label="Versión: 1.0")
        font_version = version.GetFont()
        font_version.SetPointSize(13)
        version.SetFont(font_version)
        content_sizer.Add(version, 0, wx.ALIGN_CENTER_HORIZONTAL, 15)


        #Repositorio en GitHub
        web = wx.adv.HyperlinkCtrl(
            self, label="Repositorio en GitHub",
            url="https://github.com/candelariarg/Entorno-de-Estudio-UNPi.git"
        )
        font_web = web.GetFont()
        font_web.SetPointSize(15)
        web.SetFont(font_web)
        content_sizer.Add(web, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        #Desarrolladoras
        devs = wx.StaticText(self, label="Desarrolladoras:\n~ Nyx Margot Paez\n~ Candelaria Ruggieri")
        font_devs = devs.GetFont()
        font_devs.SetPointSize(15)
        devs.SetFont(font_devs)
        content_sizer.Add(devs, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        content_sizer.Add(wx.StaticLine(self, size=(620, -1)), 0, wx.ALL, 8)

        #Botón Manual
        self.btn_manual = wx.Button(self, label="Manual de Usuario", size=(170, 40))
        font_btn = self.btn_manual.GetFont()
        font_btn.SetPointSize(12)
        self.btn_manual.SetFont(font_btn)
        content_sizer.Add(self.btn_manual, 0, wx.ALL | wx.BOTTOM, 15)


        #Texto del Manual
        self.manual_scroll = wx.TextCtrl(
            self,
            value=manualTexto,
            size=(600, 300),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP | wx.BORDER_SIMPLE
        )
        font_manual = self.manual_scroll.GetFont()
        font_manual.SetPointSize(11)
        self.manual_scroll.SetFont(font_manual)
        self.manual_scroll.Hide()
        content_sizer.Add(self.manual_scroll, 0, wx.ALL | wx.BOTTOM, 15)

        #Ensamblaje
        h_sizer.AddStretchSpacer(1)
        h_sizer.Add(content_sizer, 0, wx.EXPAND)
        h_sizer.AddStretchSpacer(1)

        outer_sizer.AddStretchSpacer(1)
        outer_sizer.Add(h_sizer, 0, wx.EXPAND)
        outer_sizer.AddStretchSpacer(1)

        self.SetSizer(outer_sizer)
        self.Bind(wx.EVT_BUTTON, self.on_manual, self.btn_manual)

        #Copyright
        copyright = wx.StaticText(
            self, label="(c) 2026 Equipo de desarrollo de Entorno de Estudio UNPi"
        )
        font_copy = copyright.GetFont()
        font_copy.SetPointSize(12)
        copyright.SetFont(font_copy)
        content_sizer.Add(copyright, 0, wx.ALL | wx.CENTER, 15)

    def on_manual(self, evt):
        if self.manual_scroll.IsShown():
            self.manual_scroll.Hide()
            self.btn_manual.SetLabel("Manual de Usuario")
        else:
            self.manual_scroll.Show()
            self.btn_manual.SetLabel("Cerrar manual")
        self.Layout()
        self.GetParent().Layout()