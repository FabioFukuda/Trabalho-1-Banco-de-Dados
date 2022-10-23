from leitorCSV import LeitorCSV

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
    def rodar(self):
        dadosJoao = self.leitorCSV.lerCSV('testeA.csv') 
        dadosMaria = self.leitorCSV.lerCSV('testeB.csv') 

        # %string% -> comeco = False, final = False
        # string% -> comeco = True, final = False
        # %string -> comeco = False, final = True
        
        selecao = dadosJoao['nome'].contido(dadosMaria['nome'])
        pass

if __name__ == '__main__':  
    app = Aplicacao()
    app.rodar()
