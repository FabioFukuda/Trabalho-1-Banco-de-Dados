'''
AUTORES: FABIO SEITI FUKUDA
         PEDRO AUGUSTO TORTOLA PEREIRA
'''

from coluna import Coluna

class Tabela:
    def __init__(self,nomesColunas:list,origemColunas:list,registros=None,nomeTabela=None,):
        self.nomeTabela = nomeTabela
        self.nomesColunas = []
        self.nomesColunasLower = []
        self.colunas = []
        self.origemColunas = origemColunas
        for index,coluna in enumerate(nomesColunas):
            self.nomesColunas.append(coluna)
            self.nomesColunasLower.append(coluna.lower())
            self.colunas.append(Coluna(coluna,registros[index]))


    def procuraTabelaPorColuna(self,coluna):
        for i in range(len(self.nomesColunas)):
            if self.nomesColunas[i] == coluna:
                return self.origemColunas[i]
        return -1

    def procuraIndiceColunaPorTabelaEColuna(self,tabela,coluna):
        for i in range(len(self.origemColunas)):
            if(self.origemColunas[i] == tabela and self.nomesColunas[i] == coluna):
                return i
        return -1

    def produtoCartesiano(tabelas):
        tabelasAux = []
        indice = 0
        nomesColunas = []
        origemColunas = []
        for nomeTabela,tabela in tabelas.items():
            tabelaAux = []
            indice+=1
            for coluna in tabela.colunas:
                tabelaAux.append(coluna.registros)
                nomesColunas.append(coluna.nome)
                origemColunas.append(tabela.nomeTabela)
            tabelasAux.append(tabelaAux)
        dictIndex = {0:0}
        tabela = Tabela.produtoCartesianoRecursivo(tabelasAux,dictIndex,1)
        # for indiceTabela,nomeTabela in enumerate(list(tabelas.keys())):
        #     novaTabela.dictTabelaIndiceInicio[nomeTabela]=dictIndex[indiceTabela]
        novaTabela = Tabela(nomesColunas,origemColunas,tabela[0])
        return novaTabela

    def produtoCartesianoRecursivo(tabelas:list,dictIndex,numeroTabela):
        if(len(tabelas)>1):
            tabela1 = tabelas.pop(0)
            tabela2 = tabelas.pop(0)
            dictIndex[numeroTabela] = len(tabela1)
            numeroTabela+=1
            registros = []

            for i in range(len(tabela1)):
                registros.append([])
            for i in range(len(tabela2)):
                registros.append([])
            inicioTabela2 = len(tabela1)

            for indiceGeralTabela1 in range(len(tabela1[0])):
                for indiceGeralTabela2 in range(len(tabela2[0])):
                    for indiceColuna,registroTabela1 in enumerate(tabela1):
                        registros[indiceColuna].append(registroTabela1[indiceGeralTabela1])
                    for indiceColuna,registroTabela2 in enumerate(tabela2):
                        registros[inicioTabela2+indiceColuna].append(registroTabela2[indiceGeralTabela2])
            tabelas.insert(0,registros) 

            return Tabela.produtoCartesianoRecursivo(tabelas,dictIndex,numeroTabela)
        else:
            return tabelas

    def getTamanho(self):
        return len(self.colunas[0])
    def getNumColunas(self):
        return len(self.nomesColunas)
    def getRegistro(self,index):
        registros = []
        for coluna in self.colunas:
            registros.append([coluna[index]])
        return [[coluna[index]] for coluna in self.colunas]
    
    def joinCartesiano(self,nomeTabela1,coluna1,nomeTabela2,coluna2):

        coluna1 = self.colunas[self.procuraIndiceColunaPorTabelaEColuna(nomeTabela1,coluna1)]
        coluna2 = self.colunas[self.procuraIndiceColunaPorTabelaEColuna(nomeTabela2,coluna2)]

        indices = []
        for i in range(self.getTamanho()):
            if(coluna1[i] == coluna2[i]):
                indices.append(True)
            else:
                indices.append(False)
        return Coluna('',indices)

    # def juntar(self,tabela,relacao):
    #     registros = []
    #     inicioRegistrosTabela2 = len(self.colunas)
    #     nomesColunas = []
    #     for coluna in self.colunas:
    #         nomesColunas.append(coluna.nome)
    #     for coluna in tabela.colunas:
    #         nomesColunas.append(coluna.nome)
    #     for i in range(len(self.colunas)+len(tabela.colunas)):
    #         registros.append([])
    #     for indiceTabela1,r in enumerate(relacao):
    #         if r:
    #             for reg2 in r:
    #                 for indiceColuna1,coluna1 in enumerate(self.colunas):
    #                     registros[indiceColuna1].append(coluna1[indiceTabela1])
    #                 for indiceColuna2,coluna2 in enumerate(tabela.colunas):
    #                     registros[inicioRegistrosTabela2+indiceColuna2].append(coluna2[reg2])
    #     return Tabela(nomesColunas,registros)

    def join(self,tabela,relacao):
        colunas = []
        colunasOrigem = []
        colunasNomes = []
        for i in range(self.getNumColunas()):
            colunas.append([])
            colunasOrigem.append(self.nomeTabela)
            colunasNomes.append(self.nomesColunas[i])
        for i in range(tabela.getNumColunas()):
            colunas.append([])
            colunasOrigem.append(tabela.nomeTabela)
            colunasNomes.append(tabela.nomesColunas[i])

        for match in relacao:
            for indice1 in match[0]:
                regs1 = self.getRegistro(indice1)
                for indice2 in match[1]:
                    regs2 = tabela.getRegistro(indice2)
                    reg = regs1+regs2
                    colunas = [reg[i] + colunas[i] for i in range(len(colunas))]

        return Tabela(colunasNomes,colunasOrigem,colunas,self.nomeTabela +' x '+ tabela.nomeTabela) 

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
            return Tabela(self.nomesColunas,self.nomeTabela,registros,nomeTabela=self.nomeTabela)
        elif type(key) == int:
            self.colunas[key]
        else:
            index = self.nomesColunasLower.index(key)
            return self.colunas[index]

