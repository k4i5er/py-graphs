from tkinter import Tk, Canvas, StringVar, IntVar
from tkinter.ttk import Frame, Combobox, Label, Entry, Labelframe


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
        divisions_2 = self.plane.parametros_xy()
        origin = self.plane.get_origin(divisions_2[0], divisions[0], divisions_2[1], divisions[3])
        print(origin)
        print(361//divisions[0])
        print('>>>>>', canvas)
        # Para graficar el modelo lineal
        if self.model == 'Lineal':
            x_coord = params[0] * divisions_2[1]
            y_coord = params[1] * divisions_2[1]
            for i in range(-self.dom_x, self.dom_x):
                origin = self.plane.get_origin(divisions_2[0], divisions[0], divisions_2[1], divisions[3])
                canvas.create_line(
                    i*divisions_2[0] + origin[0], origin[1]-(x_coord*i+y_coord), (i+1)*divisions_2[0]+origin[0], origin[1]-(x_coord*(i+1)+y_coord))
        elif self.model == 'Cuadrático':
            a = params[0]  * divisions_2[1]
            b = params[1]  * divisions_2[1]
            c = params[2]  * divisions_2[1]

            i = -self.dom_x
            while i <= self.dom_x:
                x_coord = i*divisions_2[0]
                x_coord2 = (i+1)*divisions_2[0]
                k = x_coord2 - x_coord
                for j in range(k):
                    canvas.create_line(
                        j + x_coord + origin[0], origin[1]-(a*(i+j/k)**2+b*(i+j/k)+c), (j+1) + x_coord + origin[0], origin[1]-(a*(i + (j+1)/k)**2+b*(i + (j+1)/k)+c))
                i += 1

class Draw(Tk):
    def __init__(self):  # Constructor
        super().__init__()
        self.geometry('300x600')
        self.title('Canvas drawing example')
        # Creamos el Frame
        self.frm_canvas = Frame(
            self,
            relief='sunken')
        # Create canvas
        self.canvas = Canvas(self.frm_canvas)
        self.canvas.pack(fill='both', expand=1)
        self.frm_canvas.pack(side='left', fill='both', expand=1)

        # Widgets
        self.frm_eq = Frame(self, relief='sunken')
        self.frm_sca = Frame(self, relief='sunken')
        self.frm_sca.pack(side='bottom')
        self.frm_eq_list = Frame(self.frm_eq)
        self.cmb_eq_list = Combobox(self.frm_eq_list, state='readonly')
        self.cmb_eq_list.pack()
        self.frm_eq_list.pack(ipady=10)
        self.frm_eq.pack(side='left', fill='both', expand=1, pady=10)
        self.cmb_eq_list.bind('<<ComboboxSelected>>',
                              lambda event: self.get_graf(self.cmb_eq_list))

        # Props

        self.width = self.canvas.winfo_width()  # self.winfo_width()
        self.height = self.canvas.winfo_height()  # self.winfo_height()
        self.dom_x = 10
        self.dom_y = 14

        self.sup_x = IntVar()
        self.inf_x = IntVar()
        self.sup_y = IntVar()
        self.inf_y = IntVar()
        self.sup_x.set(10)
        self.inf_x.set(10)
        self.sup_y.set(10)
        self.inf_y.set(10)

        # Initialize the plane
        self.update()
        self.initialize()
        self.get_scalar()
        # Se monitorean los eventos de configuración de la ventana
        self.bind('<Configure>', self.on_resize)

    def on_resize(self, e):
        self.width = self.winfo_width()  # e.width
        self.height = self.winfo_height()  # e.height
        
        
        # Repintar el plano
        self.initialize()

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
        variables = self.get_variables()
        if variables[0].get() == None and variables[0].get() == None and variables[0].get() == None and variables[0].get() == None:
            self.sup_x.set(10)
            self.inf_x.set(10)
            self.sup_y.set(10)
            self.inf_y.set(10)
        
        self.canvas.delete('all')
        param = self.get_divisions()
        divisions = self.parametros_xy()
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
        variables = self.get_variables()
        self.x_sup = variables[0].get() +1
        self.x_inf = variables[1].get() +1
        self.y_sup = variables[2].get() +1
        self.y_inf = variables[3].get() +1
        return (self.x_inf, self.x_sup, self.y_inf, self.y_sup)

    def get_params(self):
        #############################################################
        if self.cmb_eq_list.selection_get() == 'Lineal':
            return (float(self.param1.get()), float(self.param2.get()))
        elif self.cmb_eq_list.selection_get() == 'Cuadrático':
            return (float(self.param1.get()), float(self.param2.get()), float(self.param3.get()))

    def get_graf(self, opc):
        

        self.frm_models = Frame(self.frm_eq)
        self.frm_models.pack(ipady=10)

        # Labels
        self.lbl = Label(self.frm_models)
        self.lbl_1 = Label(self.frm_models)
        self.lbl_2 = Label(self.frm_models)
        self.lbl_3 = Label(self.frm_models)

        #Entrys 
        self.param1= StringVar()
        self.entry_param1 = Entry(self.frm_models, textvariable=self.param1, width=4)
        self.entry_param1.bind('<Return>', lambda e: self.entry_param2.focus_set())

        self.param2= StringVar()
        self.entry_param2 = Entry(self.frm_models, textvariable=self.param2, width=4)
        
        self.param3= StringVar()
        self.entry_param3 = Entry(self.frm_models, textvariable=self.param3, width=4)
        
        self.param4= StringVar()
        self.entry_param4 = Entry(self.frm_models, textvariable=self.param3, width=4)

        #Pack forget 
        
        self.cmb_eq_list.bind('<<ComboboxSelected>>', lambda event: self.pack_forget())

        if opc.get() == 'Lineal':
            self.lbl.pack(side='left')
            self.entry_param1.pack(side='left')
            self.lbl_1.pack(side='left')
            self.entry_param2.pack(side='left')
            self.lbl.config(text='y =') 
            self.lbl_1.config(text='x + ') 
            self.entry_param2.bind('<Return>', lambda e: self.model_graph(self.cmb_eq_list.get() ) )

        elif opc.get() == 'Cuadrático':
            self.lbl.pack(side='left') 
            self.lbl.config(text='f(x) = ')
            self.entry_param1.pack(side='left')
            self.lbl_1.pack(side='left')
            self.lbl_1.config(text='x**2 +') 
            self.entry_param2.pack(side='left')
            self.lbl_2.pack(side='left')
            self.lbl_2.config(text='x + ')
            self.entry_param3.pack(side='left')
            self.entry_param2.bind('<Return>', lambda e: self.entry_param3.focus_set())
            self.entry_param3.bind('<Return>', lambda e: self.model_graph(self.cmb_eq_list.get() ) )

        elif opc.get() == 'Cúbico':
            self.lbl.pack(side='left') 
            self.lbl.config(text='f(x) = ')
            self.entry_param1.pack(side='left')
            self.lbl_1.pack(side='left')
            self.lbl_1.config(text='x**3 +')
            self.entry_param2.pack(side='left')
            self.lbl_2.pack(side='left')
            self.lbl_2.config(text='x**2 + ')
            self.entry_param3.pack(side='left')
            self.lbl_3.pack(side='left')
            self.lbl_3.config(text='x +')
            self.entry_param4.pack(side='left')
            self.entry_param2.bind('<Return>', lambda e: self.entry_param3.focus_set())
            self.entry_param3.bind('<Return>', lambda e: self.model_graph(self.cmb_eq_list.get() ) )
            
        elif opc.get() == 'Exponencial':
            
            self.lbl.pack(side='left')
            self.lbl.config(text='f(x) = ') 
            self.entry_param1.pack(side='left')
            self.entry_param2.pack(side='left')
            self.lbl_1.pack(side='left')
            self.lbl_1.config(text='** (') 
            self.entry_param3.pack(side='left')
            self.lbl_2.pack(side='left')
            self.lbl_2.config(text='x +')
            self.entry_param4.pack(side='left')
            self.lbl_3.pack(side='left')
            self.lbl_3.config(text=')')
            self.entry_param2.bind('<Return>', lambda e: self.entry_param3.focus_set())
            self.entry_param3.bind('<Return>', lambda e: self.model_graph(self.cmb_eq_list.get() ) )

        elif opc.get() == 'Logístico':
            
            self.lbl.pack(side='left')
            self.lbl.config(text='P(t) =')
            self.lbl_1.pack(side='left')
            self.lbl_1.config(text=' 1 / 1 + e ** - ')
            self.entry_param1.pack(side='left')

        elif opc.get() == 'Logarítmico' :
            
            self.lbl.pack(side='left')
            self.lbl.config(text='f(x) = Log')
            self.entry_param1.pack(side='left')
            self.lbl_1.pack(side='left')
            self.lbl_1.config(text='(')
            self.entry_param2.pack(side='left')
            self.lbl_2.pack(side='left')
            self.lbl_2.config(text=')')
            
        elif opc.get() == 'Senoidal':
            pass
        elif opc.get() == 'Hiperbólico':
            pass


    def get_variables(self,):
        return(self.sup_x, self.inf_x, self.sup_y, self.inf_y )

    def get_scalar(self):
        
        var  = self.get_variables()
        self.frm_scalar = Frame( self.frm_sca)
        self.frm_scalar.pack(fill= 'both', side='bottom')

        # Eje X
        self.frm_x = Labelframe(self.frm_scalar, text='Eje X:')
        self.frm_x.pack(fill= 'both', expand=1, side='left')
        
        self.frm_x_labels = Frame(self.frm_x)
        self.frm_x_labels.pack(
        side='left', expand=True, ipadx=5, ipady=5)
        self.lbl_x_1 = Label( self.frm_x_labels, text='Limite superior:')
        self.lbl_x_1.pack( pady= 5)
        self.lbl_x_2 = Label( self.frm_x_labels, text='Limite inferior:')
        self.lbl_x_2.pack( pady= 5)

        self.frm_x_entrys = Frame(self.frm_x)
        self.frm_x_entrys.pack(
        side='right', expand=True, ipadx=5, ipady=5)
        self.entry_x_1 = Entry(self.frm_x_entrys, width= 20, textvariable= var[0])
        self.entry_x_1.pack(pady= 5)
        self.entry_x_1.delete(0, 'end')
        self.entry_x_1.bind('<Return>', lambda e: self.entry_x_2.focus_set())
        self.entry_x_2 = Entry(self.frm_x_entrys, width= 20, textvariable= var[1])
        self.entry_x_2.pack( pady= 5)
        self.entry_x_2.delete(0, 'end')
        self.entry_x_2.bind('<Return>', lambda e: self.entry_y_1.focus_set())

        # Eje Y
        self.frm_y = Labelframe(self.frm_scalar, text='Eje Y:')
        self.frm_y.pack(fill= 'both', expand=1, side='left')
        
        self.frm_y_labels = Frame(self.frm_y)
        self.frm_y_labels.pack(
            side='left', expand=True, ipadx=5, ipady=5)
        self.lbl_y_1 = Label( self.frm_y_labels, text='Limite superior:')
        self.lbl_y_1.pack(fill='both', pady= 5)
        self.lbl_y_2 = Label( self.frm_y_labels, text='Limite inferior:')
        self.lbl_y_2.pack(fill='both', pady= 5)
        
        self.frm_y_entrys = Frame(self.frm_y)
        self.frm_y_entrys.pack(
            side='right', expand=True, ipadx=5, ipady=5)
        self.entry_y_1 = Entry(self.frm_y_entrys, width= 20, textvariable= var[2])
        self.entry_y_1.pack(pady= 5)
        self.entry_y_1.delete(0, 'end')
        self.entry_y_1.bind('<Return>', lambda e: self.entry_y_2.focus_set())
        self.entry_y_2 = Entry(self.frm_y_entrys, width= 20, textvariable= var[3])
        self.entry_y_2.pack( pady= 5)
        self.entry_y_2.delete(0, 'end')
        self.entry_y_2.bind('<Return>', lambda e: self.plane())

    def pack_forget(self):
        self.frm_models.pack_forget()
        self.get_graf(self.cmb_eq_list)

    def model_graph(self, model_name):
        # Create a instance for the model class
        model = Model(model_name, self.dom_x, self.dom_y, self)
        model.graph()


if __name__ == '__main__':
     app = Draw()  # Instance for create a window
     app.mainloop()

