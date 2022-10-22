from coluna import Coluna

class Tabela:
    def __init__(self,nomesColunas:list,registros=None):
        self.nomesColunas = []
        self.colunas = []
        for index,coluna in enumerate(nomesColunas):
            self.nomesColunas.append(coluna)
            self.colunas.append(Coluna(coluna,registros[index]))
        
    def __getitem__(self, key):
        if type(key) == list:
            indices = []
            registros = []
            for nomeColuna in key:
                indice = self.nomesColunas.index(nomeColuna)
                indices.append(indice)
            for indice in indices:
                registros.append(self.colunas[indice].toList())
            return Tabela(key,registros)
        else:
            index = self.nomesColunas.index(key)
            return self.colunas[index]
        

