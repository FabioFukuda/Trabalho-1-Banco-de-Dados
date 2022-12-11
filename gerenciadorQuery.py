'''
AUTORES: FABIO SEITI FUKUDA
         PEDRO AUGUSTO TORTOLA PEREIRA
'''

from interpretador import Interpretador
from tabela import Tabela

class GerenciadorQuery:
    def executarQuery(self,query:str,tabelas):
        interpretador = Interpretador()
        interpretador.interpretar(query.lower())

        tabelaCriada = self.executarFrom(interpretador,tabelas)
        if tabelaCriada is None:
            return None

        if interpretador.interpretacaoWhere:
            tabelaCriada = self.executarWhere(interpretador,tabelaCriada)
            if tabelaCriada is None:
                return None

        if interpretador.interpretacaoOrderBy is not None:
            tabelaCriada = self.executarOrderBy(interpretador,tabelaCriada)
            if tabelaCriada is None:
                return 
        tabelaCriada = self.executarSelect(interpretador,tabelaCriada)
        
        return tabelaCriada
        
    def executarOrderBy(self,interpretador:Interpretador,tabela:Tabela):
        if interpretador.interpretacaoOrderBy['tabela'] != '' and interpretador.interpretacaoOrderBy['tabela'] != tabela.nomeTabela:
            return None
        tabelaCriada = tabela.orderBy(interpretador.interpretacaoOrderBy['nome'] ,
                                      interpretador.interpretacaoOrderBy['direcao'] )
        return tabelaCriada
    def executarSelect(self,interpretador:Interpretador,tabela:Tabela):
        if interpretador.interpretacaoSelect['nome'][0] == '*':
            return tabela
        colunas = []
        nomesColunas = []
        for campo in range(len(interpretador.interpretacaoSelect['nome'])):
            if interpretador.interpretacaoSelect['tabela'][campo] == '':
                try:
                    nome = interpretador.interpretacaoSelect['nome'][campo]
                    indice = tabela.nomesColunasLower.index(nome)
                    colunas.append(tabela.colunas[indice].registros)
                    nomesColunas.append(interpretador.interpretacaoSelect['alias'][campo])
                except:
                    return 
            else:
                aliasTabela = interpretador.interpretacaoSelect['tabela'][campo]
                nomeTabela = ''
                try:
                    if aliasTabela in interpretador.interpretacaoFrom['alias']: 
                        indiceTabela = interpretador.interpretacaoFrom['alias'].index(aliasTabela)
                        nomeTabela = interpretador.interpretacaoFrom['tabela'][indiceTabela]
                    if nomeTabela == tabela.nomeTabela or aliasTabela in interpretador.interpretacaoFrom['tabela']:
                        nome = interpretador.interpretacaoSelect['nome'][campo]
                        indice = tabela.nomesColunasLower.index(nome)
                        colunas.append(tabela.colunas[indice].registros)
                        nomesColunas.append(interpretador.interpretacaoSelect['alias'][campo])
                except:
                    return
        return Tabela(nomesColunas,colunas,nomeTabela = tabela.nomeTabela)
        

         
    def executarFrom(self,interpretador:Interpretador,tabelas):
        tabelaFrom = {}
        for nomeTabela in interpretador.interpretacaoFrom['tabela']:
            try:
                tabelaFrom[nomeTabela] = tabelas[nomeTabela]
            except:
                return None
        if interpretador.interpretacaoFrom['join']['enable']:
            try:
                coluna1 = tabelaFrom[interpretador.interpretacaoFrom['join']['tabela'][0]][interpretador.interpretacaoFrom['join']['att'][0]]
                coluna2 = tabelaFrom[interpretador.interpretacaoFrom['join']['tabela'][1]][interpretador.interpretacaoFrom['join']['att'][1]]
                tabela = (coluna1 == coluna2)
                tabela = tabelaFrom[interpretador.interpretacaoFrom['join']['tabela'][0]].join(tabelaFrom[interpretador.interpretacaoFrom['join']['tabela'][1]],tabela)
            except:
                return None
        else:
            tabela = Tabela.produtoCartesiano(tabelaFrom)
        return tabela

    def executarWhere(self,interpretador:Interpretador,tabela:Tabela):
    
        campo1,nomeTabela1,campo2,nomeTabela2,operacao = self.organizaInstrucoes(interpretador,tabela,0)

        if campo1 == None:
            return

        # if(nomeTabela1!=tabela.nomeTabela):
        #     return None
            
        resultadoOperacao1 = self.operacao(campo1,nomeTabela1,campo2,nomeTabela2,operacao,tabela)
        nomeTabela2 = ''
        if 'and' in interpretador.interpretacaoWhere:
            campo1,nomeTabela1,campo2,nomeTabela2,operacao = self.organizaInstrucoes(interpretador,tabela,2)
            resultadoOperacao2 = self.operacao(campo1,nomeTabela1,campo2,nomeTabela2,operacao,tabela)
            selecao = (resultadoOperacao1) & (resultadoOperacao2)
        elif 'or' in interpretador.interpretacaoWhere:
            campo1,nomeTabela1,campo2,nomeTabela2,operacao = self.organizaInstrucoes(interpretador,tabela,2)
            resultadoOperacao2 =  self.operacao(campo1,nomeTabela1,campo2,nomeTabela2,operacao,tabela)
            selecao = (resultadoOperacao1) | (resultadoOperacao2)
        else:
            selecao = resultadoOperacao1

        # if nomeTabela1!=nomeTabela2 and nomeTabela2 != '':
        #     return None

        return tabela[selecao]

    def organizaInstrucoes(self,interpretador:Interpretador,tabela:Tabela,indiceOp):
        aliasTabela1 = interpretador.interpretacaoWhere[indiceOp]['tabela1']
        nomeTabela1 = ''
        campo1 = interpretador.interpretacaoWhere[indiceOp]['valor1']
        campo1EhValor = False

        if aliasTabela1 != '':
            nomeTabela1 = interpretador.interpretacaoFrom['tabela'][interpretador.interpretacaoFrom['alias'].index(aliasTabela1)]
        #Então é um atributo da tabela, sem alias.
        else:
            aliasTabela1 = ''
            #nomeTabela1 = tabela.nomeTabela
            nomeTabela1 = tabela.procuraTabelaPorColuna(campo1)

        aliasTabela2 = interpretador.interpretacaoWhere[indiceOp]['tabela2']
        nomeTabela2 = ''
        campo2 = interpretador.interpretacaoWhere[indiceOp]['valor2']
        campo2EhValor = False

        if aliasTabela2 != '':
            if aliasTabela2!='STRING' and aliasTabela2!='NUMERO': 
                nomeTabela2 = interpretador.interpretacaoFrom['tabela'][interpretador.interpretacaoFrom['alias'].index(aliasTabela2)]
            else:
                campo2EhValor = True
        else:
            nomeTabela2 = tabela.procuraTabelaPorColuna(campo2)

        if not campo1EhValor and campo2EhValor:
            return campo1,nomeTabela1,campo2,nomeTabela2,interpretador.interpretacaoWhere[indiceOp]['operacao']
        elif not campo1EhValor and not campo2EhValor:
            return campo1,nomeTabela1,campo2,nomeTabela2,'join'
        else:
            return None,None,None,None
    
    def operacao(self,campo1,nomeTabela1,campo2,nomeTabela2,operador,tabela:Tabela):
        selecao = None
        match operador:
            case '>':
                selecao = tabela[campo1] >  campo2
            case '>=':
                selecao = tabela[campo1] >= campo2
            case '<':
                selecao = tabela[campo1] <  campo2
            case '<=':
                selecao = tabela[campo1] <= campo2
            case '<>':
                selecao = tabela[campo1] != campo2
            case '!=':
                selecao = tabela[campo1] != campo2
            case '=':
                selecao = tabela[campo1] == campo2
            case 'join':
                selecao = tabela.joinCartesiano(nomeTabela1,campo1,nomeTabela2,campo2)
        return selecao
        
            
    

    '''
    >	Maior que
    >=	Maior ou igual
    <	Menor que
    <=	Menor ou igual
    <> ou !=	Diferente de
    =	Igual
    '''
        