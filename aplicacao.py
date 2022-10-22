from leitorCSV import LeitorCSV

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
    def rodar(self):
        dados = self.leitorCSV.lerCSV('employees.csv') 
        registro = dados['emp_no'] != '10012'
        
