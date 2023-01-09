from gui import Controller as CBase

class Controller(CBase):

    def teste(self):
        print("Acorda Berenice!")
        #self.view.element('botao').text="A"

    def about(self):
        self.app.open('about')

    def seleciona_lista(self, event):
        print("Lista selecionada.")
