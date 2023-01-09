from gui import Controller as CBase

class Controller(CBase):

    def fechar(self):
        self.view.window.destroy()
        self.view.window.update()
        print("Acorda Berenice!")
        #self.view.element('botao').text="A"


