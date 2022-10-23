from leitorCSV import LeitorCSV

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
    def rodar(self):
        dados = self.leitorCSV.lerCSV('employees.csv') 

        # %string% -> comeco = False, final = False
        # string% -> comeco = True, final = False
        # %string -> comeco = False, final = True
        
        selecao = dados['first_name'].like('Mai'.lower(),False,False)
        resultado = dados[selecao]
        pass
