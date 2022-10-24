from interpretador import Interpretador
from tabela import Tabela

class GerenciadorQuery:
    def executarQuery(self,query:str,tabelas):
        interpretador = Interpretador()
        interpretador.interpretar(query)

        tabelaCriada = self.executarFrom(interpretador,tabelas)
        if tabelaCriada == None:
            return None

        if interpretador.interpretacaoWhere:
            tabelaCriada = self.executarWhere(interpretador,tabelaCriada)
            if tabelaCriada is None:
                return None
        else:
            tabelaCriada = list(tabelaCriada.values())[0]

        if interpretador.interpretacaoOrderBy != None:
            tabelaCriada = self.executarOrderBy(interpretador,tabelaCriada)
    
        tabelaCriada = self.executarSelect(interpretador,tabelaCriada)
        if tabelaCriada == None:
            return None

        pass
        
    def executarOrderBy(self,interpretador:Interpretador,tabela:Tabela):
        tabelaCriada = tabela.orderBy(interpretador.interpretacaoOrderBy['nome'] ,
                                      interpretador.interpretacaoOrderBy['direcao'] )
        return tabelaCriada
    def executarSelect(self,interpretador:Interpretador,tabela:Tabela):
        if interpretador.interpretacaoSelect['nome'] == '*':
            return tabela
        colunas = []
        nomesColunas = []
        for campo in range(len(interpretador.interpretacaoSelect['nome'])):
            if interpretador.interpretacaoSelect['tabela'][campo] == '':
                nome = interpretador.interpretacaoSelect['nome'][campo]
                indice = tabela.nomesColunas.index(nome)
                colunas.append(tabela.colunas[indice].registros)
                nomesColunas.append(interpretador.interpretacaoSelect['alias'][campo])
            else:
                aliasTabela = interpretador.interpretacaoSelect['tabela'][campo]
                nomeTabela = ''
                if aliasTabela in interpretador.interpretacaoFrom['alias']: 
                    indiceTabela = interpretador.interpretacaoFrom['alias'].index(aliasTabela)
                    nomeTabela = interpretador.interpretacaoFrom['tabela'][indiceTabela]
                if nomeTabela == tabela.nomeTabela or aliasTabela in interpretador.interpretacaoFrom['tabela']:
                    nome = interpretador.interpretacaoSelect['nome'][campo]
                    indice = tabela.nomesColunas.index(nome)
                    colunas.append(tabela.colunas[indice].registros)
                    nomesColunas.append(interpretador.interpretacaoSelect['alias'][campo])
        return Tabela(nomesColunas,colunas,nomeTabela = tabela.nomeTabela)
        

         
    def executarFrom(self,interpretador:Interpretador,tabelas):
        tabelasFrom = {}
        for nomeTabela in interpretador.interpretacaoFrom['tabela']:
            try:
                tabelasFrom[nomeTabela] = tabelas[nomeTabela]
            except:
                return None
        return tabelasFrom

    def executarWhere(self,interpretador:Interpretador,tabelas):
    
        resultadoOperacao1 =self.executaOperacao(interpretador,tabelas,0)
        if resultadoOperacao1 is None:
            return None

        if 'and' in interpretador.interpretacaoWhere:
            resultadoOperacao2 = self.executaOperacao(interpretador,tabelas,2)
            selecao = (resultadoOperacao1) & (resultadoOperacao2)
        elif 'or' in interpretador.interpretacaoWhere:
            resultadoOperacao2 = self.executaOperacao(interpretador,tabelas,2)
            selecao = (resultadoOperacao1) | (resultadoOperacao2)
        else:
            selecao = resultadoOperacao1

        aliasTabela1 = interpretador.interpretacaoWhere[0]['tabela1']
        nomeTabela1 = ''
        campo1 = interpretador.interpretacaoWhere[0]['valor1']

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

        return tabelas[nomeTabela1][selecao]

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

    def operacao(self,campo1,nomeTabela1,campo2,nomeTabela2,operador,ehTabela,tabelas):
        selecao = None
        match operador:
            case '>':
                if(ehTabela):
                    return None
                else:
                    selecao = tabelas[nomeTabela1][campo1] > campo2
            case '>=':
                if(ehTabela):
                    return None
                else:
                    selecao = tabelas[nomeTabela1][campo1] >= campo2
            case '<':
                if(ehTabela):
                    return None
                else:
                    selecao = tabelas[nomeTabela1][campo1] < campo2
            case '<=':
                if(ehTabela):
                    return None
                else:
                    selecao = tabelas[nomeTabela1][campo1] <= campo2
            case '<>':
                if(ehTabela):
                    selecao = tabelas[nomeTabela1][campo1] != tabelas[nomeTabela2][campo2]
                else:
                    selecao = tabelas[nomeTabela1][campo1] != campo2
            case '!=':
                if(ehTabela):
                    selecao = tabelas[nomeTabela1][campo1] != tabelas[nomeTabela2][campo2]
                else:
                    selecao = tabelas[nomeTabela1][campo1] != campo2
                    pass
            case '=':
                if(ehTabela):
                    selecao = tabelas[nomeTabela1][campo1] == tabelas[nomeTabela2][campo2]
                else:
                    selecao = tabelas[nomeTabela1][campo1] == campo2
        return selecao
        
            
    

    '''
    >	Maior que
    >=	Maior ou igual
    <	Menor que
    <=	Menor ou igual
    <> ou !=	Diferente de
    =	Igual
    '''
        