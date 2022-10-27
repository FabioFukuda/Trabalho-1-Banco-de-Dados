from interpretador import Interpretador
from tabela import Tabela

class GerenciadorQuery:
    def executarQuery(self,query:str,tabelas):
        interpretador = Interpretador()
        interpretador.interpretar(query)

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
                    indice = tabela.nomesColunas.index(nome)
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
                        indice = tabela.nomesColunas.index(nome)
                        colunas.append(tabela.colunas[indice].registros)
                        nomesColunas.append(interpretador.interpretacaoSelect['alias'][campo])
                except:
                    return
        return Tabela(nomesColunas,colunas,nomeTabela = tabela.nomeTabela)
        

         
    def executarFrom(self,interpretador:Interpretador,tabelas):
        tabelaFrom = None
        for nomeTabela in interpretador.interpretacaoFrom['tabela']:
            try:
                tabelaFrom = tabelas[nomeTabela]
                break
            except:
                return None
        return tabelaFrom

    def executarWhere(self,interpretador:Interpretador,tabela:Tabela):
    
        campo,nomeTabela1,valor,operacao = self.organizaInstrucoes(interpretador,tabela,0)

        if campo == None:
            return

        if(nomeTabela1!=tabela.nomeTabela):
            return None
            
        resultadoOperacao1 = self.operacao(campo,valor,operacao,tabela)
        nomeTabela2 = ''
        if 'and' in interpretador.interpretacaoWhere:
            campo,nomeTabela2,valor,operacao = self.organizaInstrucoes(interpretador,tabela,2)
            resultadoOperacao2 = self.operacao(campo,valor,operacao,tabela)
            selecao = (resultadoOperacao1) & (resultadoOperacao2)
        elif 'or' in interpretador.interpretacaoWhere:
            campo,nomeTabela2,valor,operacao = self.organizaInstrucoes(interpretador,tabela,2)
            resultadoOperacao2 =  self.operacao(campo,valor,operacao,tabela)
            selecao = (resultadoOperacao1) | (resultadoOperacao2)
        else:
            selecao = resultadoOperacao1

        if nomeTabela1!=nomeTabela2 and nomeTabela2 != '':
            return None

        return tabela[selecao]

    def organizaInstrucoes(self,interpretador:Interpretador,tabela:Tabela,indiceOp):
        aliasTabela1 = interpretador.interpretacaoWhere[indiceOp]['tabela1']
        nomeTabela1 = ''
        campo1 = interpretador.interpretacaoWhere[indiceOp]['valor1']
        campo1EhValor = False

        if aliasTabela1 != '':
            if aliasTabela1!='STRING' and aliasTabela1!='NUMERO': 
                #Campo é um atributo da tabela.
                nomeTabela1 = interpretador.interpretacaoFrom['tabela'][interpretador.interpretacaoFrom['alias'].index(aliasTabela1)]

            #campo ou é string, ou é valor.
            else:
                campo1EhValor = True
        #Então é um atributo da tabela, sem alias.
        else:
            contador = 0
            aliasTabela1 = ''
            nomeTabela1 = tabela.nomeTabela

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
            contador = 0
            nomeTabela2 = tabela.nomeTabela

        if not campo1EhValor and campo2EhValor:
            return campo1,nomeTabela1,campo2,interpretador.interpretacaoWhere[indiceOp]['operacao']
        elif not campo2EhValor and campo1EhValor:
            return campo2,nomeTabela2,campo1,interpretador.interpretacaoWhere[indiceOp]['operacao']
        else:
            return None,None,None,None
    ''' 
    def executaOperacao(self,interpretador:Interpretador,tabelas,indiceOp):

        aliasTabela1 = interpretador.interpretacaoWhere[indiceOp]['tabela1']
        nomeTabela1 = ''
        campo1 = interpretador.interpretacaoWhere[indiceOp]['valor1']

        
        if aliasTabela1 == '':
            contador = 0
            nomeTabela1 = ''
            for tabela in tabelas.values():
                if campo1 in tabela.nomesColunas:
                    contador+=1
                    nomeTabela1 = tabela.nomeTabela
            if contador!=1:
                return None
        else:
            nomeTabela1 = interpretador.interpretacaoFrom['tabela'][interpretador.interpretacaoFrom['alias'].index(aliasTabela1)]

        aliasTabela2 = interpretador.interpretacaoWhere[indiceOp]['tabela2']
        nomeTabela2 = ''
        campo2 = interpretador.interpretacaoWhere[indiceOp]['valor2']
        ehTabela = True

        if aliasTabela2 != '':
            if aliasTabela2!='STRING' and aliasTabela2!='NUMERO': 
                nomeTabela2 = interpretador.interpretacaoFrom['tabela'][interpretador.interpretacaoFrom['alias'].index(aliasTabela2)]
            else:
                ehTabela = False
        else:
            contador = 0
            nomeTabela2 = ''
            for tabela in tabelas.values():
                if campo2 in tabela.nomesColunas:
                    contador+=1
            if contador!=1:
                return None
                
        return self.operacao(campo1,nomeTabela1,campo2,nomeTabela2,interpretador.interpretacaoWhere[indiceOp]['operacao'],ehTabela,tabelas)
    '''
    
    def operacao(self,campo,valor,operador,tabela):
        selecao = None
        match operador:
            case '>':
                selecao = tabela[campo] > valor
            case '>=':
                selecao = tabela[campo] >= valor
            case '<':
                selecao = tabela[campo] < valor
            case '<=':
                selecao = tabela[campo] <= valor
            case '<>':
                selecao = tabela[campo] != valor
            case '!=':
                selecao = tabela[campo] != valor
            case '=':
                selecao = tabela[campo] == valor
        return selecao
        
            
    

    '''
    >	Maior que
    >=	Maior ou igual
    <	Menor que
    <=	Menor ou igual
    <> ou !=	Diferente de
    =	Igual
    '''
        