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
            'testeA':dadosA,
            'testeB':dadosB
        }

        '''
        >	Maior que
        >=	Maior ou igual
        <	Menor que
        <=	Menor ou igual
        <> ou !=	Diferente de
        =	Igual
        '''
            
        query = 'select ta.nome from testeA as ta order by Id asc'

        self.g.executarQuery(query,tabelas)

        # %string% -> comeco = False, final = False
        # string% -> comeco = True, final = False
        # %string -> comeco = False, final = True


if __name__ == '__main__':  
    app = Aplicacao()
    app.rodar()
