from leitorCSV import LeitorCSV
from gerenciadorQuery import GerenciadorQuery
from tabelaOperacao import tabelaOperacao

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
        self.g = GerenciadorQuery()

    def rodar(self):
        '''
        dadosA = self.leitorCSV.lerCSV('testeA.csv') 
        dadosB = self.leitorCSV.lerCSV('testeB.csv') 
        dadosC = self.leitorCSV.lerCSV('testeC.csv') 
        tabelas = {
            'testeA':dadosA,
            'testeB':dadosB,
            'testeC':dadosC
        }
        '''
        dadosA = self.leitorCSV.lerCSV('employees.csv')
        tabelas = {
            'employees':dadosA
        }
        #t = tabelaOperacao(tabelas)
        '''
        >	Maior que
        >=	Maior ou igual
        <	Menor que
        <=	Menor ou igual
        <> ou !=	Diferente de
        =	Igual
        '''
            
        query = 'select birth_date as b,emp_no from employees where nome.emp_no >10051 order by emp_no asc'

        resultado = self.g.executarQuery(query,tabelas)
        pass

if __name__ == '__main__':  
    app = Aplicacao()
    app.rodar()
