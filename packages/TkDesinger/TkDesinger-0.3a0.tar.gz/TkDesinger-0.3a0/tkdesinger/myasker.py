import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sdialog

class AskTuple(sdialog.Dialog):
    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = tk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel2)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()
        print('the end')
    def cancel2(self, event = None):
        self.canceled = True
        self.cancel()
    def body(self, parent):
        self.a = None
        self.frame = parent
        self.title('Выбрать список')
        self.canceled = False
        self.style = ttk.Style()
        ttk.Label(parent, text = 'Разделяется по переносу строки').pack()
        self.txt = tk.Text(parent, width = 20, height = 15)
        self.txt.pack()
    def show(self):
        if not self.canceled:
            return self.a[:-1]
    def validate(self):
        a = self.txt.get('1.0', 'end')
        self.a =  a.split('\n')
        return 1
class AskRelief ( sdialog.Dialog ) :
    def body(self, parent) :
        self.canceled =  False
        self.style = ttk.Style()
        self.dict = {0 : None, 1 : 'raised', 2 : 'flat', 3 : 'groove', 4 : 'solid', 5 : 'sunken', 6 : 'ridge'}
        ttk.Label ( parent, text='Выберите рельеф', font='arial 13' ).pack ()
        self.var = tk.IntVar ()
        self.var.set ( 0 )
        self.style.configure ( 'RAISED.TRadiobutton', relief = 'raised')
        self.style.configure ( 'FLAT.TRadiobutton', relief = 'flat' )
        self.style.configure ( 'GROOVE.TRadiobutton', relief = 'groove' )
        self.style.configure ( 'SOLID.TRadiobutton', relief = 'solid' )
        self.style.configure ( 'SUNKEN.TRadiobutton', relief = 'sunken' )
        self.style.configure ( 'RIDGE.TRadiobutton', relief = 'ridge')

        tk.Radiobutton ( parent, value = 1, relief = 'raised', variable = self.var, text = ' raised ' ).pack ( fill = 'x' )
        tk.Radiobutton ( parent, value = 2, relief = 'flat',   variable = self.var, text = ' flat '   ).pack ( fill = 'x' )
        tk.Radiobutton ( parent, value = 3, relief = 'groove', variable = self.var, text = ' groove ' ).pack ( fill = 'x' )
        tk.Radiobutton ( parent, value = 4, relief = 'solid',  variable = self.var, text = ' solid '  ).pack ( fill = 'x' )
        tk.Radiobutton ( parent, value = 5, relief = 'sunken', variable = self.var, text = ' sunken ' ).pack ( fill = 'x' )
        tk.Radiobutton ( parent, value = 6, relief = 'ridge',  variable = self.var, text = ' ridge '  ).pack ( fill = 'x' )
        self.geometry ( '270x250' )
        self.resizable ( False, False )
        self.title ( 'Выбрать рельеф' )
    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()
    def show(self) :
        return self.validate2()

    def validate2(self) :
        if self.canceled:
            return None
        else:
            return self.dict[self.var.get ()]


    def buttonbox(self) :
        buttbox = ttk.Frame ( self )
        ttk.Button ( buttbox, text =     'Ок', command = self.ok,     width = 10 ).pack ( side = tk.LEFT )
        ttk.Button ( buttbox, text = 'Отмена', command = self.cancel, width = 10 ).pack ( side = tk.LEFT )
        self.bind ( '<Return>', self.ok )
        self.bind ( '<Escape>', self.cancel )
        buttbox.pack (side = 'bottom')
    def cancel(self, event=None):

        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()
def askrelief(TK):
    return AskRelief(TK).show()
def asklist(TK):
    return AskTuple(TK).show()
if __name__ == '__main__':
    a= tk.Tk()
    print ( askrelief(a) )
    print ( asktuple(a))
