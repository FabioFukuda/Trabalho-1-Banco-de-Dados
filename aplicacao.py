from leitorCSV import LeitorCSV
from gerenciadorQuery import GerenciadorQuery

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
        self.g = GerenciadorQuery()

    def rodar(self):
        dadosA = self.leitorCSV.lerCSV('testeA.csv') 
        dadosB = self.leitorCSV.lerCSV('testeB.csv') 

        tabelas = {
            'tabelaA':dadosA,
            'tabelaB':dadosB
        }

        query = 'select * from tabelaA as ta,tabelaB as tb where ta.Id = tb.Id'

        self.g.executarQuery(query,tabelas)

        # %string% -> comeco = False, final = False
        # string% -> comeco = True, final = False
        # %string -> comeco = False, final = True
        
        selecao = dadosA['nome'].contido(dadosB['nome'])
        if selecao.nome == 'relacao':
            novaTabela = dadosA.juntar(dadosB,selecao)
        else:
            novaTaela = dadosA[selecao]
        pass

if __name__ == '__main__':  
    app = Aplicacao()
    app.rodar()
