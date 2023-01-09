from xml.dom import minidom
import tkinter as tk
from tkinter import ttk
from tkinter import END
import os
import sys
import importlib

class App(object):
    """
    """
    def __init__(self)->None:
        self.__path = os.path.abspath(os.path.dirname(sys.argv[0]))
        sys.path.insert(0, os.path.join(self.__path))
        self.root = tk.Tk()
        self.stack = []

    def get_name(self):
        """
        """
        #m = importlib.import_module(self.__module__)
        return os.path.basename(sys.argv[0]).replace('.py', '')

    def path(self)->str:
        """
        """
        return self.__path

    def open(self, controller:str):
        app_path = self.path()
        sys.path.insert(0, os.path.join(app_path, 'controller'))
        ctrl = __import__(controller)
        c = ctrl.Controller(app=self)
        self.stack.append(c)
        c.view.build()
        return c

    def run(self):
        """
        """
        app_path = self.path()
        print("Aplicacao rodando em: {}".format(app_path))
        self.open(controller=self.get_name())
        self.root.mainloop()


class Controller(object):

    def __init__(self, app)->None:
        self.app = app
        self.view = self.load_view(self.get_name()) 
        self.model = self.load_model()

    def load_view(self, view:str):
        """
        """
        return View(view, self) 

    def load_model(self):
        """
        """
        #app_path = self.app.path()
        #sys.path.insert(0, os.path.join(app_path, 'model'))
        #print("AAAA:" + os.path.join(app_path, 'model'))
        #print("NOME CONTROLLER:"+self.get_name())
        print('model.' + self.get_name())
        name = self.get_name()
        try:
            mdl = __import__('model.' + name)
        except:
            return
        m = getattr(mdl, name).Model()
        return m

    def get_name(self):
        """
        """
        m = importlib.import_module(self.__module__)
        return os.path.basename(m.__file__).replace('.py', '')

class View(object):
    def __init__(self, view:str, controller)->None:
        """
        """
        self.controller = controller
        self.elements = {}
        self.view = view
        self.window = None

    def get_action(self, action:str):
        return getattr(self.controller, action)

    def get_viewfile(self):
        """
        Pelo nome da view, retorna o caminho para
        o XML que define ela.
        """
        app_path = self.controller.app.path()
        view_path = os.path.join(app_path, 'view', '{}.xml'.format(self.view))
        return view_path

    def gen_id(self, tagname:str):
        """
        """
        i = 1
        for k, _ in self.elements.items():
            if tagname in k:
                i+=1
        return tagname + str(i)

    def __set_element(self, obj, id:str):
        """
        """
        self.elements[id] = obj
        return self
    
    def element(self, id):
        """
        """
        return self.elements.get(id, None)

    def build(self):
        """
        """
        # parse an xml file by name
        doc = minidom.parse(self.get_viewfile())
        #print(doc.nodeName)
        #print(doc.childNodes)
        #print(doc.firstChild.tagName)
        for el in doc.childNodes:
            self.__build(el)

    def __build(self, el, parent=None):
        """
        """
        if el.nodeType==el.TEXT_NODE:
            text=el.data.strip()
            if text:
                lbl = tk.Label(parent, text=text).pack()
                self.__set_element(lbl, self.gen_id('label'))
            return
        tagname = el.tagName
        id = None if 'id' not in el.attributes else el.attributes['id'].value
        if tagname=="window":
            title = 'Title' if 'title' not in el.attributes else el.attributes['title'].value
            width = '300' if 'width' not in el.attributes else el.attributes['width'].value
            height = '200' if 'height' not in el.attributes else el.attributes['height'].value
            parent = None
            #print(el.attributes['title'].value)
            if self.controller.app.stack[0]==self.controller:
                self.controller.app.root.wm_title(title)
                self.controller.app.root.geometry('{}x{}'.format(width, height))
                self.window=self.controller.app.root
            else:
                newWindow = tk.Toplevel(self.controller.app.root)
                newWindow.title(title)
                newWindow.geometry('{}x{}'.format(width, height))
                self.window=newWindow
            for sel in el.childNodes:
                print(sel)
                self.__build(el=sel, parent=self.window)
        # divisoria horizontal
        elif tagname=='hr':
            width = 1 if 'width' not in el.attributes else el.attributes['width'].value
            e = ttk.Separator(parent, orient='horizontal')
            e.pack(fill='x')
        # lista
        elif tagname=='list':
            background = 'white' if 'background' not in el.attributes else el.attributes['background'].value
            color = 'black' if 'color' not in el.attributes else el.attributes['color'].value
            options = []
            i = 1
            for sel in el.childNodes:
                if sel.nodeType!=el.TEXT_NODE:
                    text = 'Option {}'.format(i) if 'text' not in sel.attributes else sel.attributes['text'].value
                    value = text if 'value' not in sel.attributes else sel.attributes['value'].value
                    options.append(text)
                    i+=1
            var = tk.Variable(value=options)
            e = tk.Listbox(
                parent,
                #listvariable=var,
                height=6,
                selectmode=tk.EXTENDED, bg=background, fg=color
            )
            for sel in el.childNodes:
                if sel.nodeType!=el.TEXT_NODE:
                    text = 'Option {}'.format(i) if 'text' not in sel.attributes else sel.attributes['text'].value
                    value = text if 'value' not in sel.attributes else sel.attributes['value'].value
                    e.insert(i, text)
            onclick = el.attributes['onclick'].value if 'onclick' in el.attributes else None
            if onclick:
                e.bind('<<ListboxSelect>>', self.get_action(onclick))
            self.__set_element(e, id if id else self.gen_id('list'))
            e.pack()
        # label
        elif tagname=='label':
            text=el.data.strip()
            if text:
                e = tk.Label(parent, text=text).pack()
                self.__set_element(e, self.gen_id('label'))
            return
        # input
        elif tagname=='input':
            background = 'white' if 'background' not in el.attributes else el.attributes['background'].value
            color = 'black' if 'color' not in el.attributes else el.attributes['color'].value
            text = '' if 'text' not in el.attributes else el.attributes['text'].value
            e = tk.Entry(parent, bg=background, fg=color)
            self.__set_element(e, id if id else self.gen_id('input'))
            if text:
                e.delete(0,END)
                e.insert(0,text)
            e.pack()
        elif tagname=='frame':
            bg = None if 'bg' not in el.attributes else el.attributes['bg'].value
            fr = tk.Frame(parent, bg=bg)
            self.__set_element(fr, id if id else self.gen_id('frame'))
            fr.pack()
            for sel in el.childNodes:
                self.__build(el=sel, parent=fr)
        elif tagname=='button':
            text = 'text' if 'text' not in el.attributes else el.attributes['text'].value
            onclick = el.attributes['onclick'].value if 'onclick' in el.attributes else None
            if onclick:
                print(self.get_action(onclick), onclick)
            btn = tk.Button(parent, text=text, command=self.get_action(onclick))
            self.__set_element(btn, id if id else self.gen_id('button'))
            btn.pack()
        else:
            return

if __name__=="__main__":
    raise Exception("The init file module was not created to be called directly.")