from tabela import Tabela

class LeitorCSV:
    def __init__(self):
        pass
    def lerCSV(self,path:str,sep = ','):
        dados = open(path,'r')
        registros = []
        nomesColunas = []
        for indice,linha in enumerate(dados):
            campos = linha.replace('\n','').split(',')
            if indice==0:
                nomesColunas = campos
                for i in range(len(campos)):
                    registros.append([])
            else:
                for indice,campo in enumerate(campos):
                    registros[indice].append(campo)

        novaTabela = Tabela(nomesColunas,registros)

        return novaTabela
        