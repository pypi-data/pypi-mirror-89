from tkdesinger import myasker, dnd

__author__ = 'FotonPC'
__license__ = 'MIT'
__doc__ = \
    """
This module use modify tkinter.dnd as dnd.py in program directory - Drag And Drop
Supported:
Label
Button
Entry
Listbox
Text
Canvas

This program is not best!!!
And this can generate no right code!

WARNING: Height and width is not const value! It can be in px and pt!
"""

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
from tkinter import colorchooser
import tkfontchooser


def ask_font() :
    # open the font chooser and get the font selected by the user
    font = tkfontchooser.askfont ( root )
    # font is "" if the user has cancelled
    if font :
        # spaces in the family name need to be escaped
        fontka = [font['family'], font['size'], font['weight'], font['slant']]
        try :
            if font['underline'] : fontka += ['underline']
        except :
            pass
        try :
            if font['overstrike'] : fontka += ['overstrike']
        except :
            pass
        return tuple ( fontka )


widAs = {'Label' : dnd.DndLabel,
         'Button' : dnd.DndButton,
         'Entry' : dnd.DndEntry,
         'Listbox' : dnd.DndListbox,
         'Text' : dnd.DndText,
         'Canvas' : dnd.DndCanvas,
         'Radiobutton' : dnd.DndRadiobutton,
         'ttk.Combobox' : dnd.DndTtkCombobox,
         'ttk.Progressbar' : dnd.DndTtkProgressbar,
         'Checkbutton': dnd.DndCheckbutton}
widNotText = {'Listbox', 'Canvas', 'Text', 'Entry', 'ttk.Combobox', 'ttk.Progressbar'}
widFonted = {'Listbox', 'Text', 'Entry', 'ttk.Combobox', 'Radiobutton', 'Label', 'Entry', 'Button', 'Checkbutton'}
IDS = {}
WIDobjects = []
lasttop = None


def del_lasttop(event=None) :
    try :
        lasttop.destroy ()
    except :
        pass


root = tk.Tk ()
root.geometry('1000x60')
root.resizable(True, False)
root.withdraw()
root.wm_deiconify()
root.title ( 'FotonTkDesinger' )
root.iconbitmap ( 'icon.ico' )
toolbar = tk.Frame ( root )
toolbar.pack ( fill='x', padx = (10,5) )
desing_frame = tk.Toplevel (root )
desing_frame.title('Foton TkDesinger - New form')
desing_frame.config(bg = 'lightblue')
desing_frame.lift()
desing_frame.transient(root)
combowid = ttk.Combobox ( toolbar )
combowid['values'] = (
'Label', 'Button', 'Entry', 'Listbox', 'Text', 'Canvas', 'Radiobutton','Checkbutton' ,'ttk.Combobox', 'ttk.Progressbar')
combowid.grid ( row=0, column=0 )


def popup_des(event, obj) :
    global lasttop
    label = obj.label
    lab_id = IDS[label]
    x = event.x_root
    y = event.y_root
    top = tk.Toplevel ( root )
    lasttop = top
    top.geometry ( '+' + str ( x ) + '+' + str ( y ) )
    def ask_fg():
        try :
            label['fg'] = colorchooser.askcolor()[1]
        except Exception as E :
            print ( E.__class__.__name__, E.args )
        top.destroy ()
    def ask_bg():
        try :
            label['bg'] = colorchooser.askcolor()[1]
        except Exception as E :
            print ( E.__class__.__name__, E.args )
        top.destroy ()
    def ask_fnt_() :
        try :
            label.config ( font=ask_font () )
            print ( label['font'] )
        except Exception as E :
            print ( E.__class__.__name__, E.args )
        top.destroy ()

    def ask_text() :
        try :
            label['text'] = simpledialog.askstring ( 'Задать текст', 'Задайте текст!' )
        except :
            pass
        top.destroy ()

    def ask_img() :
        try :
            fn = filedialog.askopenfilename ()
            imga = Image.open ( fn )
            obj.image_path = fn
            label.image_data = ImageTk.PhotoImage ( imga )
            label.config ( image=label.image_data )
        except :
            pass
        top.destroy ()

    def del_id() :
        desinger.canvas.delete ( lab_id )
        top.destroy ()

        WIDobjects.remove ( obj )
    def cnf_length() :
        try :
            label['length'] = simpledialog.askinteger ( 'Выбрать длину', 'Задайте длину!' )
        except :
            pass
        top.destroy ()
    def cnf_value() :
        try :
            label['value'] = simpledialog.askinteger ( 'Выбрать значение', 'Задайте значение!' )
        except :
            pass
        top.destroy ()
    def cnf_width() :
        try :
            label['width'] = simpledialog.askinteger ( 'Выбрать ширину', 'Задайте ширину!' )
        except :
            pass
        top.destroy ()

    def cnf_height() :
        try :
            label['height'] = simpledialog.askinteger ( 'Выбрать высоту', 'Задайте высоту!' )
        except :
            pass
        top.destroy ()
    def ask_values() :
        try:
            if obj.name == 'ttk.Combobox':
                label['values'] = myasker.asklist( root )
            elif obj.name == 'ttk.Listbox':
                x = myasker.asklist( root )
                label.delete('1.0', 'end')
                for el in x:
                    label.insert('end', el)
                obj.listbox_values = x
        except:
            pass
        top.destroy()
    tk.Button ( top, text='Удалить', command=del_id, relief='groove' ).pack ( fill='x', ipadx=10 )

    if obj.name == 'ttk.Progressbar':
        tk.Button ( top, text='Задать длину', command=cnf_length, relief='groove' ).pack ( fill='x', ipadx=10 )
        tk.Button ( top, text='Задать значение', command=cnf_value, relief='groove' ).pack ( fill='x', ipadx=10 )
    else:
        tk.Button ( top, text='Задать ширину', command=cnf_width, relief='groove' ).pack ( fill='x', ipadx=10 )
        tk.Button ( top, text='Задать высоту', command=cnf_height, relief='groove' ).pack ( fill='x', ipadx=10 )
        tk.Button ( top, text='Цвет фона', command=ask_bg, relief='groove' ).pack ( fill='x', ipadx=10 )
    if obj.name == 'ttk.Combobox':
        tk.Button ( top, text='Задать список', command=ask_values, relief='groove' ).pack ( fill='x', ipadx=10 )
    if not obj.name in widNotText :
        tk.Button ( top, text='Цвет текста', command=ask_fg, relief='groove' ).pack ( fill='x', ipadx=10 )
        tk.Button ( top, text='Задать тект', command=ask_text, relief='groove' ).pack ( fill='x', ipadx=10 )
        tk.Button ( top, text='Задать изображение', command=ask_img, relief='groove' ).pack ( fill='x', ipadx=10 )
    if obj.name in widFonted :
        tk.Button ( top, text='Выбрать шрифт', command=ask_fnt_, relief='groove' ).pack ( fill='x', ipadx=10 )
    tk.Button ( top, text='Закрыть меню', command=lambda : top.destroy (), relief='groove' ).pack ( fill='x', ipadx=10 )
    top.overrideredirect ( True )
    lasttop = top


def add_wid() :
    title = combowid.get ()
    objcls = widAs[title]
    if title == 'Canvas' :
        newobj = objcls ( bg='white' )
    elif title == 'Listbox':
        newobj = objcls( )
        newobj.listbox_values = []
    elif title == 'ttk.Progressbar':
        newobj = objcls ( mode='determinate' )
    elif title in widNotText :
        newobj = objcls ()
    else :
        newobj = objcls ( text=title + str ( len ( WIDobjects ) ) )
    newobj.attach ( desinger.canvas, x=0, y=0 )
    newobj.y_orig = 0
    newobj.x_orig = 0
    IDS[newobj.label] = newobj.id
    newobj.label.bind ( '<Button-3>', lambda event : popup_des ( event, newobj ) )
    WIDobjects.append ( newobj )


def pycode() :

    if varPillow.get() == 0:
        code = 'import tkinter\nimport tkinter.ttk\nroot = tkinter.Tk()\n'
    else:
        code = 'import PIL\nimport PIL.Image\nimport PIL.ImageTk\nimport tkinter\nimport tkinter.ttk\nroot = tkinter.Tk()\n'
    code += 'root.title("'+desingtitle.replace('\\', '\\\\').replace('"', '\\"')+'")\n'
    for i, widget in enumerate ( WIDobjects ) :
        x, y = widget.canvas.coords ( widget.id )
        if widget.name == 'Checkbutton':
            try:
                code += 'boolvar'+str(i)+' = tkinter.BooleanVar()\nboolvar'+str(i)+'.set(0)\n'
            except:
                pass
        suffix = ''
        if widget.name == 'Label' or widget.name == 'Radiobutton':
            try :
                suffix = ', text = "' + widget.label['text'].replace ( '"', '\\"' ) + '", bg = "' + widget.label[
                    'bg'] + '", fg = "' + \
                         widget.label['fg'] + '", width = ' + str ( widget.label['width'] ) + ', height = ' + str (
                    widget.label['height'] ) + ', image = "' + widget.image_data_name.replace ( '/', '\\\\' ) + '"'
            except :
                suffix = ', text = "' + widget.label['text'].replace ( '"', '\\"' ) + '", bg = "' + widget.label[
                    'bg'] + '", fg = "' + \
                         widget.label['fg'] + '", width = ' + str ( widget.label['width'] ) + ', height = ' + str (
                    widget.label['height'] )
        if widget.name == 'Checkbutton':
            try:
                suffix = ', text = "'+widget.label['text'].replace('\\','\\\\').replace('"','\\\\"')+'", variable = '+'boolvar'+str(i)
            except:
                pass
        if widget.name == 'ttk.Progressbar':
            try:
                suffix = ', length = ' + str(widget.label['length']) + ', mode = "determinate"'
            except: pass
        if widget.name == 'Button' :
            try :
                suffix = ', text = "' + widget.label['text'].replace ( '"', '\\"' ) + '", bg = "' + widget.label[
                    'bg'] + '", fg = "' + \
                         widget.label['fg'] + '", width = ' + str ( widget.label['width'] ) + ', height = ' + str (
                    widget.label['height'] ) + ', image = "' + widget.image_data_name.replace ( '/', '\\\\' ) + '"'
            except :
                suffix = ', text = "' + widget.label['text'].replace ( '"', '\\"' ) + '", bg = "' + widget.label[
                    'bg'] + '", fg = "' + \
                         widget.label['fg'] + '", width = ' + str ( widget.label['width'] ) + ', height = ' + str (
                    widget.label['height'] )
        if widget.name == 'Entry' :
            suffix = ', bg = "' + widget.label['bg'] + '", fg = "' + widget.label['fg'] + '", width = ' + str (
                widget.label['width'] )
        if widget.name == 'Canvas' :
            suffix = ', bg = "' + widget.label['bg'] + '", width = ' + str (
                widget.label['width'] ) + ', height = ' + str ( widget.label['height'] )
        if widget.name == 'Text' :
            suffix = ', bg = "' + widget.label['bg'] + '", fg = "' + widget.label['fg'] + '", width = ' + str (
                widget.label['width'] ) + ', height = ' + str ( widget.label['height'] )
        if widget.name == 'Listbox' :
            suffix = ', bg = "' + widget.label['bg'] + '", fg = "' + widget.label['fg'] + '", width = ' + str (
                widget.label['width'] ) + ', height = ' + str ( widget.label['height'] )

        name = 'tkinter.' + widget.name + '( root ' + suffix + ')'
        code += widget.name.split ( '.' )[-1] + str ( i ) + '=' + name
        code += '\n'
        code += widget.name.split ( '.' )[-1] + str ( i ) + '.place( x=' + str ( x ) + ', y=' + str ( y ) + ')'
        code += '\n'
        if widget.name == 'ttk.Combobox' :
            code += widget.name.split ( '.' )[-1] + str ( i ) + '["values"] = ' + '("'+'","'.join(widget.label["values"]).replace('\\','\\\\')+'")\n'
        if varPillow.get() == 0:
            try:
                x = widget.image_path
                code += 'image_'+str(i)+' = tkinter.PhotoImage( file="'+x.replace('/','\\\\')+'")\n'
                code += str(widget.name.split ( '.' )[-1]) + str ( i ) + '.config( image = image_'+str(i)+')\n'
            except Exception as E:
                print(E.__class__.__name__, E.args)
        else:
            try:
                x = widget.image_path
                code += 'image_'+str(i)+' = PIL.ImageTk.PhotoImage(PIL.Image.open("'+x.replace('/','\\\\')+ '"))\n'
                code += str(widget.name.split ( '.' )[-1]) + str ( i ) + '.config( image = image_'+str(i)+')\n'
            except Exception as E:
                print(E.__class__.__name__, E.args)
        if widget.name == 'ttk.Progressbar':
            code += widget.name.split ( '.' )[-1] + str ( i ) + '["value"] = '+str(widget.label['value'])+'\n'
    code += 'root.mainloop()'

    def copy_a() :
        t.event_generate ( '<<Copy>>' )

    menuha = tk.Menu ()
    menuha.add_command ( label='Копировать', command=copy_a )

    def popup(event) :
        menuha.post ( event.x_root, event.y_root )

    a = tk.Toplevel ( root )
    a.title ( 'Код' )

    t = tk.Text ( a )
    t.pack ( fill='both', expand=1 )
    t.insert ( tk.END, code )
    t.config(state = tk.DISABLED)
    t.bind ( '<Button-3>', popup )
    a.transient(root)
    a.lift()
    root.wait_window(a)

buttplus = tk.Button ( toolbar, relief='groove', text='+ Добавить - Add ', command=add_wid )
buttplus.grid ( row=0, column=1, padx=20 )

tk.Button ( toolbar, text='Показать код! View code!', command=pycode, relief='groove' ).grid ( row=0, column=2, padx=20 )
varPillow = tk.BooleanVar()
varPillow.set(0)
pillowPowerImg = tk.PhotoImage(file = 'pillow-power.png')
check_PIL = tk.Checkbutton(toolbar,  text = 'Использовать pillow для поддержки других форматов изображения\nUse pillow to support others images formats',cursor = 'hand2', selectcolor = '#fffff0',overrelief = 'groove',offrelief = 'raised', variable=varPillow, onvalue=1, offvalue=0)
check_PIL.grid(row=0, column = 3, padx = (0, 10))

def helpPIL():
    a = tk.Toplevel()
    a.title('О использовании Pillow - About using Pillow')
    a['bg'] = 'white'
    tk.Label(a, bg = 'white', compound = 'bottom', image = pillowPowerImg, text = 'Pillow используется для поддержки форматов изображений которых нет в стандартом tkinter.\nЕсли версия tkinter меньше 8.5 то будет поддерживатся только GIF, иначе еще и PNG.\nPillow нужно устанавливать через pip командой:\n pip install pillow\n А импортировать как PIL, так как это форк PIL!').pack()
    a.resizable(False, False)
    a.lift()
    a.transient(root)
def re_title():
    global desingtitle
    desingtitle = entryTitle.get()
    desing_frame.title(desingtitle)
tk.Button(toolbar, text = '?', font='arial 12 bold', command = helpPIL, height= 0, fg = 'blue').place(rely = 0 , relx = 1, anchor = 'ne')
titleframe = tk.Frame(desing_frame)
titleframe.pack(fill = 'x')
desingtitle = 'Foton TkDesinger - New form'
entryTitle = ttk.Entry(titleframe)
entryTitle.pack(side = tk.LEFT, padx = (0, 5), fill = 'x', expand = 1, ipady = 1.5)
entryTitle.insert('end', 'Foton TkDesinger - New form')
tk.Button(titleframe, relief = 'groove',  text = 'Поменять название! Rename form!', command = re_title).pack(side=tk.LEFT, ipadx = 5, padx= (2,4))
desinger = dnd.DNDField ( desing_frame )
desinger.top.pack ( fill='both', expand=1, pady=7, padx=3 )
desinger.canvas.pack ( fill='both', expand=1 )
desinger.canvas.bind ( '<Button-1>', del_lasttop )
### Root menu


def new_desing():
    global entryTitle, desing_frame, desinger, titleframe, lasttop, IDS, WIDobjects, desingtitle
    IDS = {}
    WIDobjects = []
    lasttop = None
    if not desing_frame.destroyed:
        return

    desing_frame = tk.Toplevel ( root )
    desing_frame.config ( bg='lightblue' )
    desing_frame.lift ()
    desing_frame.title('Foton TkDesinger - New form')
    desing_frame.transient ( root )
    titleframe = tk.Frame ( desing_frame )
    titleframe.pack ( fill='x' )
    entryTitle = ttk.Entry ( titleframe )
    entryTitle.pack ( side=tk.LEFT, padx=(0, 5), fill='x', expand=1, ipady=1.5 )
    entryTitle.insert ( 'end', 'Foton TkDesinger - New form' )
    tk.Button(titleframe, relief = 'groove',  text = 'Поменять название! Rename form!', command = re_title).pack(side=tk.LEFT, ipadx = 5, padx= (2,4))
    desinger = dnd.DNDField ( desing_frame )
    desinger.top.pack ( fill='both', expand=1, pady=7, padx=3 )
    desinger.canvas.pack ( fill='both', expand=1 )
    desinger.canvas.bind ( '<Button-1>', del_lasttop )
    desing_frame.wm_attributes ( '-alpha', 0.93 )
    desing_frame.destroyed = False
    desing_frame.protocol('WM_DELETE_WINDOW', close_des)
menu_root = tk.Menu(root)
filemenu = tk.Menu(menu_root, tearoff = 0)
newform_img = tk.PhotoImage(file = 'newform.png')
filemenu.add_command(label = 'Новая заготовка - New form', command = new_desing, image = newform_img, compound = 'left')
menu_root.add_cascade(menu = filemenu, label = 'Файл - File')
root.config(menu = menu_root)
desing_frame.wm_attributes('-alpha', 0.93)
desing_frame.destroyed = False
def close_des(event= None):
    desing_frame.destroyed =  True
    desing_frame.destroy()
desing_frame.protocol('WM_DELETE_WINDOW', close_des)
root.deiconify()
root.mainloop ()
