import tkinter
import tkinter.ttk
root = tkinter.Tk()
root.title("Foton TkDesinger - New form")
Entry0=tkinter.Entry( root , bg = "SystemWindow", fg = "SystemWindowText", width = 20)
Entry0.place( x=32.0, y=106.0)
Combobox1=tkinter.ttk.Combobox( root )
Combobox1.place( x=28.0, y=46.0)
Combobox1["values"] = ("")
Radiobutton2=tkinter.Radiobutton( root , text = "Radiobutton2", bg = "SystemButtonFace", fg = "SystemWindowText", width = 0, height = 0)
Radiobutton2.place( x=25.0, y=73.0)
boolvar3 = tkinter.BooleanVar()
boolvar3.set(0)
Checkbutton3=tkinter.Checkbutton( root , text = "Checkbutton3", variable = boolvar3)
Checkbutton3.place( x=32.0, y=13.0)
Button4=tkinter.Button( root , text = "?", bg = "SystemButtonFace", fg = "#0000ff", width = 0, height = 0)
Button4.place( x=29.0, y=137.0)
Entry5=tkinter.Entry( root , bg = "SystemWindow", fg = "SystemWindowText", width = 20)
Entry5.place( x=197.0, y=54.0)
root.mainloop()

if __name__ == '__main__':
    pass