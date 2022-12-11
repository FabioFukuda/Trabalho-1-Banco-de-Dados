'''
AUTORES: FABIO SEITI FUKUDA
         PEDRO AUGUSTO TORTOLA PEREIRA
'''

from leitorCSV import LeitorCSV
from gerenciadorQuery import GerenciadorQuery
from tabela import Tabela

class Aplicacao:
    def __init__(self):
        self.leitorCSV = LeitorCSV()
        self.gerenciadorQuery = GerenciadorQuery()
        self.tabelas = {}
    def rodar(self):
        
        #APAGARRR
        
        tabela = self.leitorCSV.lerCSV('course.csv',sep=',')
        self.tabelas[tabela.nomeTabela] = tabela

        tabela = self.leitorCSV.lerCSV('student.csv',sep=',')
        self.tabelas[tabela.nomeTabela] = tabela
        

        self.fazerQueries()
        #APAGARR

        entrada = self.lerInput()
        while entrada!='3':
            match entrada:
                case '1':
                    self.importarArquivo()
                case '2':
                    self.fazerQueries()

            entrada = self.lerInput()
        
    def importarArquivo(self):
        entrada = input('Digite o caminho do csv (ex:C:\\Users\\Usuario\\Documents\\tabela.csv)\n')
        try:
            tabela = self.leitorCSV.lerCSV(entrada,sep=',')
            self.tabelas[tabela.nomeTabela] = tabela
        except:
            print('Falha na leitura.')
        
    def fazerQueries(self):
        entrada = ''
        while entrada!='2':
            entrada = input('Digite a query:')
            try:
                tabela = self.gerenciadorQuery.executarQuery(entrada,self.tabelas)
                self.imprimirTabela(tabela)
            except:
                print('Falha na query.')
            entrada = input('Deseja fazer mais uma query?\n[1]Sim\n[2]Não\n')

    def lerInput(self):
        entrada =  input('###Menu Princial###\n[1] Importar arquivo:\n[2] Fazer Queries \n[3] Sair\n')
        while entrada not in ['1','2','3']:
            entrada =  input('### Menu Principal ###\n[1] Importar arquivo:\n[2] Fazer Queries\n[3] Sair\n')
        return entrada

    def imprimirTabela(self,tabela:Tabela):
        if tabela!=None:
            tamanhoStringsColunas = [len(nomeColuna) for nomeColuna in tabela.nomesColunas]
            for i,coluna in enumerate(tabela.colunas):
                for dado in coluna:
                    if len(dado) > tamanhoStringsColunas[i]:
                        tamanhoStringsColunas[i] = len(dado)
            for tamanhoString in tamanhoStringsColunas:
                print('+',end='')
                print((tamanhoString+2)*'-',end='')
            print('+')

            for i,nomeColuna in enumerate(tabela.nomesColunas):
                print('| ' + nomeColuna + (tamanhoStringsColunas[i]-len(nomeColuna)+1)*' ',end='')
            print('|')

            for tamanhoString in tamanhoStringsColunas:
                print('+',end='')
                print((tamanhoString+2)*'-',end='')
            print('+')

            for i in range(tabela.getTamanho()):
                for j,coluna in enumerate(tabela.colunas):
                    print('| ' + coluna[i] + (tamanhoStringsColunas[j]-len(coluna[i])+1)*' ',end='')
                print('|')
            for tamanhoString in tamanhoStringsColunas:
                print('+',end='')
                print((tamanhoString+2)*'-',end='')
            print('+')
