from coluna import Coluna

class Tabela:
    def __init__(self,nomesColunas:list,registros=None,nomeTabela=None):
        self.nomeTabela = nomeTabela
        self.nomesColunas = []
        self.colunas = []
        for index,coluna in enumerate(nomesColunas):
            self.nomesColunas.append(coluna)
            self.colunas.append(Coluna(coluna,registros[index]))
    def getTamanho(self):
        return len(self.colunas[0])
        
    def juntar(self,tabela,relacao):
        registros = []
        inicioRegistrosTabela2 = len(self.colunas)
        nomesColunas = []
        for coluna in self.colunas:
            nomesColunas.append(coluna.nome)
        for coluna in tabela.colunas:
            nomesColunas.append(coluna.nome)
        for i in range(len(self.colunas)+len(tabela.colunas)):
            registros.append([])
        for indiceTabela1,r in enumerate(relacao):
            if r:
                for reg2 in r:
                    for indiceColuna1,coluna1 in enumerate(self.colunas):
                        registros[indiceColuna1].append(coluna1[indiceTabela1])
                    for indiceColuna2,coluna2 in enumerate(tabela.colunas):
                        registros[inicioRegistrosTabela2+indiceColuna2].append(coluna2[reg2])
        return Tabela(nomesColunas,registros)

    def orderBy(self,nomeColuna,ordem):
        indiceColuna = self.nomesColunas.index(nomeColuna)
        indices = [i for i in range(len(self.colunas[indiceColuna]))]
        colunas = [registro.lower() for registro in self.colunas[indiceColuna]]
        dictAux = dict(zip(indices,colunas))
        reverse = False
        if ordem == 'desc':
            reverse = True
        dictOrdenado = {key: value for key, value in sorted(dictAux.items(), key=lambda item: item[1],reverse = reverse)}
        ordem = list(dictOrdenado.keys())

        registros = [[] for i in range(len(self.nomesColunas))]
        for indice in ordem:
            for indiceColuna in range(len(self.nomesColunas)):
                registros[indiceColuna].append(self.colunas[indiceColuna][indice])
        return Tabela(self.nomesColunas,registros,nomeTabela = self.nomeTabela)

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
            
        elif type(key) == Coluna:
            indices = [indice for indice,boleano in enumerate(key) if boleano]
            registros = [[] for i in range(len(self.colunas))]
            for indice in indices:
                for numColuna,coluna in enumerate(self.colunas):
                    registros[numColuna].append(coluna[indice])    
            return Tabela(self.nomesColunas,registros,nomeTabela=self.nomeTabela)
        else:
            index = self.nomesColunas.index(key)
            return self.colunas[index]
        

