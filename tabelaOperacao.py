from coluna import Coluna
from tabela import Tabela

class tabelaOperacao:
    def __init__(self,tabelas:dict):
        # {n:m} tabela de nome n inicia no indice m
        self.dictTabelaIndiceInicio = {}
        self.nomesColunas = []
        self.tabela = self.produtoCartesiano(tabelas)
        self.tabelasBoleanas = self.criaTabelasBoleanas()
        self.tabelaBoleanaFinal  = None
        self.tamanhoTabela = 0
        self.indicesTabelas = []

    def aplicaBoleanoTabela(self,nomeTabela,selecao:Coluna,numeroOperacao:int):
        if selecao.nome == 'relacao':
            tabela1 = selecao.tabelasRelacao[0]
            tabela2 = selecao.tabelasRelacao[1]
            for i in range(len(self.tabelasBolenas[tabela2][numeroOperacao-1])):
                self.tabelasBoleanas[tabela2][numeroOperacao-1][i] = False
            for indiceSelecao,relacao in enumerate(selecao):
                if relacao:
                    indiceColunaTabela2 = self.dictTabelaIndiceInicio[tabela2]
                    for indice,registro in enumerate(self.tabela[indiceColunaTabela2]):
                        if registro in relacao:
                            self.tabelasBoleanas[tabela2][numeroOperacao-1][indice] = True
                else:
                    indiceColunaTabela1 = self.dictTabelaIndiceInicio[tabela1]
                    for indice,registro in enumerate(self.tabela[indiceColunaTabela1]):
                        if self.tabela[indiceColunaTabela1][indice] == indiceSelecao:
                            self.tabelasBoleanas[tabela2][numeroOperacao-1][indice] = False
        else:
            tabela1 = selecao.tabelasRelacao[0]
            for indiceSelecao,relacao in enumerate(selecao):
                indiceColunaTabela1 = self.dictTabelaIndiceInicio[tabela1]
                for indice,registro in enumerate(self.tabela[indiceColunaTabela1]):
                    if self.tabela[indiceColunaTabela1][indice] == indiceSelecao:
                        self.tabelasBoleanas[tabela2][numeroOperacao-1][indice] = relacao

    def executaAnd(self):
        tabelaFinal = {}
        for nome,tabelaBoleana in self.tabelasBoleanas.items():
            tabela = []
            for indice in range(tabelaBoleana[0]):
                if tabelaBoleana[0][indice] and tabelaBoleana[0][indice]:         
                    tabela.append(True)
                else:
                    tabela.append(False)
            tabelaFinal[nome] = tabela
        self.tabelaBoleanaFinal = tabelaFinal

    def executaOr(self):
        tabelaFinal = {}
        for nome,tabelaBoleana in self.tabelasBoleanas.items():
            tabela = []
            for indice in range(tabelaBoleana[0]):
                if tabelaBoleana[0][indice] or tabelaBoleana[0][indice]:         
                    tabela.append(True)
                else:
                    tabela.append(False)
            tabelaFinal[nome] = tabela
        self.tabelaBoleanaFinal = tabelaFinal

    def criaTabelaFinal(self):
        dictColunasTabelas = {} 
        if self.tabelaBoleanaFinal == None:
            self.executaAnd()
        indicesFinais = []
        for indiceRegistro in range(self.tamanhoTabela):
            for nomeTabela in self.dictTabelaIndiceInicio.keys():
                flag = True
                if self.tabelaBoleanaFinal[nomeTabela][indiceRegistro]:
                    continue
                else:
                    flag = False
                    break
            if flag:
                indicesFinais.append(indiceRegistro)
        registros = [[] for i in range(len(self.nomesColunas))]
        
        for indice in indicesFinais:
            for indiceColuna,coluna in enumerate(self.tabela):
                registros.append(coluna[indice])
        nomesColunasFinais = []
        registrosFinais = []
    
        for indiceColuna,colunas in enumerate(registrosFinais):
            if indiceColuna not in self.dictTabelaIndiceInicio.values():
                nomesColunasFinais.append(self.nomesColunas[indiceColuna])
                registrosFinais.append(registros[indiceColuna])
        return Tabela(nomesColunasFinais,registros)
            

    def criaTabelasBoleanas(self):
        numeroDeRegistros = len(self.tabela[0])
        tabelasBoleanas = {}
        for nomeTabela in self.dictTabelaIndiceInicio.keys():
            tabelasBoleanas[nomeTabela] = [[True for i in range(numeroDeRegistros)],[True for i in range(numeroDeRegistros)]]
        return tabelasBoleanas

    def produtoCartesiano(self,tabelas):

        self.nomesColunas = []
        self.registros = []
        tabelasAux = []
        indice = 0
        for nomeTabela,tabela in tabelas.items():
            tabelaAux = []
            tabelaAux.append([i for i in range(tabela.getTamanho())])
            self.nomesColunas.append('indice')
            indice+=1
            for coluna in tabela.colunas:
                self.nomesColunas.append(coluna.nome)
                tabelaAux.append(coluna.registros)
                indice+=1
            tabelasAux.append(tabelaAux)
        dictIndex = {0:0}
        tabela = self.produtoCartesianoRecursivo(tabelasAux,dictIndex,1)
        for indiceTabela,nomeTabela in enumerate(list(tabelas.keys())):
            self.dictTabelaIndiceInicio[nomeTabela]=dictIndex[indiceTabela]
        return tabela

    def produtoCartesianoRecursivo(self,tabelas:list,dictIndex,numeroTabela):
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

            return self.produtoCartesianoRecursivo(tabelas,dictIndex,numeroTabela)
        else:
            self.tamanhoTabela = len(tabelas[0])
            return tabelas