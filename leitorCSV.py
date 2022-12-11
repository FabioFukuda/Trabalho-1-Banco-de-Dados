'''
AUTORES: FABIO SEITI FUKUDA
         PEDRO AUGUSTO TORTOLA PEREIRA
'''

from tabela import Tabela
import os

class LeitorCSV:
    def __init__(self):
        pass
    def lerCSV(self,path:str,sep = ','):
        dados = open(path,'r',encoding="utf8")
        registros = []
        nomesColunas = []
        for indice,linha in enumerate(dados):
            campos = linha.replace('\n','').split(sep)
            if indice==0:
                nomesColunas = campos
                for i in range(len(campos)):
                    registros.append([])
            else:
                for indice,campo in enumerate(campos):
                    registros[indice].append(campo)
        print(os.path.basename(path))
        novaTabela = Tabela(nomesColunas,[os.path.basename(path)[:-4] for i in range(len(nomesColunas))],registros,nomeTabela=os.path.basename(path)[:-4])

        return novaTabela
        