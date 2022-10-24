from tkinter import Tk, Canvas, StringVar
from tkinter.ttk import Frame, Combobox, Label, Entry
from math import sqrt


class Punto():
    def __init__(self, canvas, x=0, y=0):
        self.x = x
        self.y = y
        self.canvas = canvas

    def cuadrante(self):
        if self.x > 0 and self.y > 0:
            return 'Cuadrante positivo (Primer cuadrante)'
        elif self.x < 0 and self.y > 0:
            return 'Cuarto cuadrante'
        elif self.x > 0 and self.y < 0:
            return 'Segundo cuadrante'
        elif self.x < 0 and self.y < 0:
            return 'Tercer cuadrante'
        elif self.x == 0 and self.y != 0:
            return 'Punto sobre el eje vertical (y)'
        elif self.y == 0 and self.x != 0:
            return 'Punto sobre el eje horizontal (x)'
        else:
            return 'Punto en el origen'

    # Encapsulamiento

    def get_coordenadas(self):
        return (self.x, self.y)
    ##################

    def vector(self, p):
        # self.origin = self.canvas.get_origin()
        # print("##", self.canvas)
        self.canvas.get_canvas().create_line(
            self.x, self.y, p.get_coordenadas()[0], p.get_coordenadas()[1])


class Model():
    def __init__(self, model, dom_x, dom_y, plane):
        self.dom_x = dom_x
        self.dom_y = dom_y
        self.model = model
        self.plane = plane

    def graph(self):
        self.plane.initialize()
        params = self.plane.get_params()
        canvas = self.plane.get_canvas()
        divisions = self.plane.get_divisions()
        origin = self.plane.get_origin()
        print(origin)
        print(361//divisions[0])
        print('>>>>>', canvas)
        # Para graficar el modelo lineal
        if self.model == 'Lineal':
            x_coord = params[0] * divisions[1]
            y_coord = params[1] * divisions[1]
            for i in range(-self.dom_x, self.dom_x):
                origin = self.plane.get_origin()
                canvas.create_line(
                    i*divisions[0] + origin[0], origin[1]-(x_coord*i+y_coord), (i+1)*divisions[0]+origin[0], origin[1]-(x_coord*(i+1)+y_coord))
        elif self.model == 'Cuadrático':
            a = params[0]  * divisions[1]
            b = params[1]  * divisions[1]
            c = params[2]  * divisions[1]
            i = -self.dom_x
            while i <= self.dom_x:
                x_coord = i*divisions[0]
                x_coord2 = (i+1)*divisions[0]
                k = x_coord2 - x_coord
                for j in range(k):
                    canvas.create_line(
                        j + x_coord + origin[0], origin[1]-(a*(i+j/k)**2+b*(i+j/k)+c), (j+1) + x_coord + origin[0], origin[1]-(a*(i + (j+1)/k)**2+b*(i + (j+1)/k)+c))
                i += 1
                

            # canvas.create_line(0, 0, 300, 600)
            # print('Graficando... (próximamente)')


class Draw(Tk):
    def __init__(self):  # Constructor
        super().__init__()
        self.geometry('300x600')
        self.title('Canvas drawing example')
        # Creamos el Frame
        self.frm_canvas = Frame(
            self,
            relief='sunken')
        # Creamos el canvas
        self.canvas = Canvas(self.frm_canvas)
        self.canvas.pack(fill='both', expand=1)
        self.frm_canvas.pack(side='left', fill='both', expand=1)

        # Widgets
        self.frm_eq = Frame(self, relief='sunken')
        self.frm_eq_list = Frame(self.frm_eq)
        self.cmb_eq_list = Combobox(self.frm_eq_list, state='readonly')
        self.cmb_eq_list.pack()
        self.frm_eq_list.pack(ipady=10)
        self.frm_eq.pack(side='left', fill='both', expand=1, pady=10)     
        self.cmb_eq_list.bind('<<ComboboxSelected>>', lambda event: self.get_graf(self.cmb_eq_list))

        # Props
        
        self.width = self.canvas.winfo_width()  # self.winfo_width()
        self.height = self.canvas.winfo_height()  # self.winfo_height()
        self.dom_x = 10
        self.dom_y = 14

        # Se inicializa el plano
        self.update()
        self.initialize()
        # Se monitorean los eventos de configuración de la ventana
        self.bind('<Configure>', self.on_resize)

    def on_resize(self, e):
        self.width = self.winfo_width()  # e.width
        self.height = self.winfo_height() # e.height
    

        # Repintar el plano
        self.initialize()

    def initialize(self):
        self.canvas.delete('all')
        origin = self.get_origin()
        self.xscale = 0
        self.yscale = 0
        self.canvas.create_line(origin[0], 0, origin[0], origin[1]*2)  # Eje y
        self.canvas.create_line(0, origin[1], origin[0]*2, origin[1])  # Eje x
        self.canvas.create_line(0, origin[1], 10, origin[1]-5)
        self.canvas.create_line(0, origin[1], 10, origin[1]+5)
        self.canvas.create_line(
            origin[0]*2, origin[1], origin[0]*2-10, origin[1]-5)
        self.canvas.create_line(
            origin[0]*2, origin[1], origin[0]*2-10, origin[1]+5)

        self.canvas.create_line(origin[0], 0, origin[0]-5, 10)

        self.canvas.create_line(origin[0], 0, origin[0]+5, 10)

        self.canvas.create_line(
            origin[0], origin[1]*2, origin[0]-5, origin[1]*2-10)

        self.canvas.create_line(
            origin[0], origin[1]*2, origin[0]+5, origin[1]*2-10)

        # self.set_divisions(5, 'y')
        self.set_divisions(self.divisions)

        self.cmb_eq_list['values'] = ['Lineal', 'Cuadrático', 'Cúbico',
                                      'Exponencial', 'Logístico', 'Logarítmico', 'Senoidal', 'Hiperbólico']

    def get_canvas(self):
        return self.canvas

    def get_origin(self):
        return (self.canvas.winfo_width()//2, self.canvas.winfo_height()//2)

    def set_divisions(self):
        self.x_inf = 6
        self.x_sup = 7
        self.y_inf = 8
        self.y_sup = 9
        eje_x = self.x_inf+self.x_sup
        eje_y = self.y_inf+self.y_sup
    
        return

    def get_divisions(self):
        origin = self.get_origin()
        return(origin[0]//self.divisions[0], origin[1]//self.divisions[1])

    def get_params(self):
        #############################################################
        if self.cmb_eq_list.selection_get() == 'Lineal':
            return (float(self.param1.get()), float(self.param2.get()))
        elif self.cmb_eq_list.selection_get() == 'Cuadrático':
            self.param1 = StringVar()
            self.param2 = StringVar()
            self.param3 = StringVar()
            self.param1.set('-1')
            self.param2.set('0')
            self.param3.set('0')
            return (float(self.param1.get()), float(self.param2.get()), float(self.param3.get()))
   
    def get_graf(self, opc):
        self.frm_models = Frame(self.frm_eq)
        self.frm_models.pack(ipady= 10)

        self.label = Label(self.frm_models)
        self.label.pack(side='left')

        self.param1= StringVar()
        self.entry_param1 = Entry(self.frm_models, textvariable=self.param1, width=4)
        self.entry_param1.pack(side='left')
        self.entry_param1.bind('<Return>', lambda e: self.entry_param2.focus_set())

        self.label_1 = Label(self.frm_models)
        self.label_1.pack(side='left')

        self.param2= StringVar()
        self.entry_param2 = Entry(self.frm_models, textvariable=self.param2, width=4)
        self.entry_param2.pack(side='left')  
        self.entry_param2.bind('<Return>', lambda e: self.model_graph(self.cmb_eq_list.get() ) )

        self.label_2 = Label(self.frm_models)
        self.label_2.pack(side='left')

        if opc.get() == 'Lineal':
            self.label.config(text='y =') 
            self.label_1.config(text='x + ') 

        if opc.get() == 'Cuadrático':
            pass
       
    def model_graph(self, model_name):
        # params = self.get_params()
        # Creamos una instancia de la clase Model
        model = Model(model_name, self.dom_x, self.dom_y, self)
        model.graph()


if __name__ == '__main__':
    app = Draw()  # Instancia para crear una ventana
    # app.set_divisions(10, 'x')
    p1 = Punto(app, 3, 4)
    p2 = Punto(app, 9, 200)
    # p1.vector(p2)
    app.mainloop()