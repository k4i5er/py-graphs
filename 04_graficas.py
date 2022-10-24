from __future__ import division
from tkinter import Tk, Canvas, StringVar
from tkinter.ttk import Frame, Combobox, Label, Entry
from math import sqrt
from webbrowser import get


class Punto():
    def __init__(self, canvas, x=0, y=0):
        self.x = x
        self.y = y
        self.canvas = canvas

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
        x_coord = params[0] * divisions[0]
        y_coord = params[1] * divisions[1]
        print('>>>>>', canvas)
        # Para graficar el modelo lineal
        if self.model == 'Lineal':
            for i in range(-self.dom_x, self.dom_x):
                origin = self.plane.get_origin()
                canvas.create_line(
                    i*divisions[0] + origin[0], origin[1]-(x_coord*i+y_coord), (i+1)*divisions[0]+origin[0], origin[1]-(x_coord*(i+1)+y_coord))
        elif self.model == 'Cuadrático':
            for i in range(-self.dom_x, self.dom_x):
                origin = self.plane.get_origin()
                canvas.create_line(
                    i*divisions[0] + origin[0], origin[1]-(x_coord*i+y_coord), (i+1)*divisions[0]+origin[0], origin[1]-(x_coord*(i+1)+y_coord))

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
        self.cmb_eq_list = Combobox(self.frm_eq_list)
        self.cmb_eq_list.pack()
        self.frm_eq_list.pack(ipady=10)
        self.frm_models = Frame(self.frm_eq)
        Label(self.frm_models, text='y =').pack(side='left')
        self.param1 = StringVar()
        self.entry_param1 = Entry(
            self.frm_models, textvariable=self.param1, width=4)
        self.entry_param1.pack(side='left')
        self.entry_param1.bind(
            '<Return>', lambda e: self.entry_param2.focus_set())
        Label(self.frm_models, text=' x + ').pack(side='left')
        self.param2 = StringVar()
        self.entry_param2 = Entry(
            self.frm_models, textvariable=self.param2, width=4)
        self.entry_param2.pack(side='left')
        self.entry_param2.bind('<Return>', lambda e: self.model_graph(
            self.cmb_eq_list.get()))
        self.frm_models.pack(ipady=10)
        self.frm_eq.pack(side='left', fill='both', expand=1, pady=10)

        # Props
        self.width = self.canvas.winfo_width()  # self.winfo_width()
        self.height = self.canvas.winfo_height()  # self.winfo_height()
        self.dom_x = 10
        self.dom_y = 14
        self.divisions = (10, 10)

        # Se inicializa el plano
        self.update()
        self.initialize()
        # Se monitorean los eventos de configuración de la ventana
        self.bind('<Configure>', self.on_resize)

    def on_resize(self, e):
        self.width = self.winfo_width()  # e.width
        self.height = self.winfo_height()  # e.height
        # Repintar el plano
        self.initialize()
        self.set_divisions(self.width, self.height)

        
    def initialize(self):
        self.canvas.delete('all')
        param = self.get_divisions()

        # Dibujo del plani.
        self.plane()

        self.cmb_eq_list['values'] = ['Lineal', 'Cuadrático', 'Cúbico',
                                      'Exponencial', 'Logístico', 'Logarítmico', 'Senoidal', 'Hiperbólico']

    def get_canvas(self):
        return self.canvas

    def get_origin(self, division_x, param_x, division_y, param_y):
        return (division_x*param_x, division_y*param_y)

    def plane(self):
        param = self.get_divisions()
        divisions = self.parametros_xy()
        print(divisions)
        origin = self.get_origin(divisions[0], param[0], divisions[1], param[3])
        self.canvas.create_line(0,origin[1],self.canvas.winfo_width(),origin[1])
        self.canvas.create_line(origin[0],0,origin[0], self.canvas.winfo_height())
        x2 = (param[0]+param[1])*divisions[0]
        for i in range(divisions[0],x2,divisions[0]):
            self.canvas.create_line(i,origin[1]-5,i,origin[1]+5)
        y2= (param[2]+param[3])*divisions[1]
        for i in range(divisions[1],y2,divisions[1]):
            self.canvas.create_line(origin[0]-5,i,origin[0]+5,i)
        
        self.canvas.create_line(origin[0],self.height,origin[0]-20,self.height-20)
        self.canvas.create_line(origin[0],self.height,origin[0]+20,self.height-20)

        self.canvas.create_line(0,origin[1],20,origin[1]-20,)
        self.canvas.create_line(0,origin[1],20,origin[1]+20)

        self.canvas.create_line(origin[0],0,origin[0]+20,20)
        self.canvas.create_line(origin[0],0,origin[0]-20,20)

        self.canvas.create_line(self.width,origin[1],self.width-5,origin[1]-5)
        self.canvas.create_line(self.width,origin[1],self.width-5,origin[1]+5)
            
    
    
    def parametros_xy(self):
        param = self.get_divisions()
        eje_x = param[0]+param[1]
        self.division_x = self.canvas.winfo_width()//eje_x
        eje_y = param[2]+param[3]
        self.division_y = self.canvas.winfo_height()//eje_y
        return (self.division_x, self.division_y)

    def get_divisions(self):
            self.x_inf = 3+1
            self.x_sup = 10+1
            self.y_inf = 2+1
            self.y_sup = 20+1
            
            return (self.x_inf, self.x_sup, self.y_inf, self.y_sup)

    def get_params(self):
        #############################################################
        if self.cmb_eq_list.selection_get() == 'Lineal':
            return (float(self.param1.get()), float(self.param2.get()))

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
