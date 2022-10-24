from leitorCSV import LeitorCSV
from gerenciadorQuery import GerenciadorQuery

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
        self.g = GerenciadorQuery()

    def rodar(self):
        dadosA = self.leitorCSV.lerCSV('employees.csv') 

        tabelas = {
            'employees':dadosA,
        }

        '''
        >	Maior que
        >=	Maior ou igual
        <	Menor que
        <=	Menor ou igual
        <> ou !=	Diferente de
        =	Igual
        '''
            
        query = 'select birth_date as b,emp_no from employees where emp_no >= 10051 order by emp_no asc'

        resultado = self.g.executarQuery(query,tabelas)
        pass

if __name__ == '__main__':  
    app = Aplicacao()
    app.rodar()
