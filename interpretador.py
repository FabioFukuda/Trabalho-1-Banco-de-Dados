from copy import deepcopy
from tabela import Tabela

class Interpretador:
    def __init__(self):
        self.interpretacaoSelect = None
        self.interpretacaoFrom = None
        self.interpretacaoWhere = None
        self.interpretacaoOrderBy = None

    def interpretar(self,comando:str):
        comandosSeparados = self.sanitizaComando(comando)
        select_,from_,where_,orderBy_ = self.classificaComandos(comandosSeparados)

        self.interpretacaoSelect = self.interpretarSelect(select_)
        self.interpretacaoFrom = self.interpretarFrom(from_)
        self.interpretacaoWhere = self.interpretarWhere(where_)
        self.interpretacaoOrderBy = self.interpretarOrderBy(orderBy_)

    def interpretarOrderBy(self,orderBy_):
        if len(orderBy_) == 0:
            return None
        nome = ''
        tabela = ''
        direcao = ''
        if '.' in orderBy_[0]:
            tabela,nome = orderBy_[0].split('.')
        else:
            nome = orderBy_[0]
        
        if len(orderBy_)>1:
            direcao = orderBy_[1]
        else:
            direcao = 'asc'

        interpretacaoOrderBy = {
            'nome': nome,
            'tabela': tabela,
            'direcao': direcao.lower()
        }
        return interpretacaoOrderBy
        
    def interpretarWhere(self,where_):
        if len(where_) == 0:
            return None
        '''
        where n.idade >= 3

        >	Maior que
        >=	Maior ou igual
        <	Menor que
        <=	Menor ou igual
        <> ou !=	Diferente de
        =	Igual

        LIKE	Busca um padrão parecido

        ''' 
        interpretacaoWhere = []
        for operacao in where_:
            if operacao == 'and' or operacao == 'or':
                interpretacaoWhere.append(operacao)
                continue

            valor1 = ''
            tabela1  = ''
            valor2 = ''
            tabela2  = ''
            op = ''

            if '.' in operacao[0]:
                tabela1,valor1 = operacao[0].split('.')
            else:
                valor1 = operacao[0]

            try:
                float(operacao[2])
                tabela2 = "NUMERO"
                valor2 = operacao[2]
            except: 
                if '.' in operacao[2]:
                    tabela2,valor2 = operacao[2].split('.')
                elif operacao[2].find("'")!=-1 or operacao[2].find('"')!=-1:
                    tabela2 = "STRING"
                    valor2 = operacao[2][1:-1]
                else:
                    tabela2 = ""
                    valor2 = operacao[2]  
            op = operacao[1]

            interpretacaoWhere.append({
                'valor1':valor1,
                'valor2':valor2,
                'tabela1':tabela1,
                'tabela2':tabela2,
                'operacao':op
            })

        return interpretacaoWhere

    def interpretarSelect(self,select_):
        interpretacaoSelect = {'nome':[],
                        'alias':[],
                        'tabela':[]}
        
        camposSeparados = []
        campo = []
        for comando in select_:
            if comando == ',':
                camposSeparados.append(campo)
                campo = []
            else:
                campo.append(comando)
        camposSeparados.append(campo)

        for campo in camposSeparados:
            proximoCampo = 'nome'
            nome = ''
            alias = ''
            tabela = ''
            for comando in campo:
                if proximoCampo == 'nome':
                    if '.' in comando:
                        tabela,nome = comando.split('.')
                    else:
                        nome = comando
                    proximoCampo = 'alias'
                    continue
                if comando == 'as':
                    continue
                elif proximoCampo == 'alias':
                    alias = comando
            if alias == '':
                alias = nome
            interpretacaoSelect['alias'].append(alias)     
            interpretacaoSelect['nome'].append(nome)
            interpretacaoSelect['tabela'].append(tabela)
        return interpretacaoSelect

    def interpretarFrom(self,from_):
        interpretacaoFrom = {'tabela':[],
                        'alias':[]}
        
        camposSeparados = []
        campo = []
        for comando in from_:
            if comando == ',':
                camposSeparados.append(campo)
                campo = []
            else:
                campo.append(comando)
        camposSeparados.append(campo)

        for campo in camposSeparados:

            proximoCampo = 'tabela'
            tabela = ''
            alias = ''

            for comando in campo:
                if proximoCampo == 'tabela':
                    tabela = comando
                    proximoCampo = 'alias'
                    continue
                if comando == 'as':
                    continue
                elif proximoCampo == 'alias':
                    alias = comando
            if alias == '':
                alias = tabela
            interpretacaoFrom['tabela'].append(tabela)
            interpretacaoFrom['alias'].append(alias)     

        return interpretacaoFrom

    def sanitizaComando(self,comando):
        while ',' in comando:
            index = comando.find(',')
            comando = comando[:index] + ';' + comando[index+1:]
            if comando[index-1] == ' ':
                comando = comando[:index-1:] + comando[index:]
                index -=1
            if comando[index+1] == ' ':
                comando = comando[:index+1] + comando[index+2:]
        print(comando) 
        comandoSeparados = comando.split(' ')
        comandosMaisSeparados = []
        
        for comando in comandoSeparados:
            if ';' in comando:
                for c in comando.split(';'):
                    comandosMaisSeparados.append(c)
                    comandosMaisSeparados.append(',')
                comandosMaisSeparados.pop()
            else:
                comandosMaisSeparados.append(comando)
                    
                    
        return comandosMaisSeparados

    def classificaComandos(self,comandosSeparados):
        _select = comandosSeparados[1:comandosSeparados.index('from')]
        _from = []
        _where = []
        _order = []

        #from vai do from até o where
        if 'where' in comandosSeparados:
            _from = comandosSeparados[comandosSeparados.index('from')+1:comandosSeparados.index('where')]
            if 'order' in comandosSeparados:
                _where = comandosSeparados[comandosSeparados.index('where')+1:comandosSeparados.index('order')]
                _order = comandosSeparados[comandosSeparados.index('order')+2:]     
            else:
                _where = comandosSeparados[comandosSeparados.index('where')+1:]
        elif 'order' in comandosSeparados:
            #from vai do from até o order
            _from = comandosSeparados[comandosSeparados.index('from')+1:comandosSeparados.index('order')]
            _order = comandosSeparados[comandosSeparados.index('order')+2:]
        else:
            #from vai do from até o final
            _from = comandosSeparados[comandosSeparados.index('from')+1:]
        '''
        where n.idade >= 3

        >	Maior que
        >=	Maior ou igual
        <	Menor que
        <=	Menor ou igual
        <> ou !=	Diferente de
        =	Igual
        LIKE	Busca um padrão parecido

        IN	Incluindo (múltiplos valores)
        NOT IN	Excluindo (múltiplos valores)
        BETWEEN	Entre dois valores
        IS NULL	Traz todos os valores nulos
        IS NOT NULL	Traz todos os valores que não são nulos
        ''' 

        #Sanitizar o where
        if(len(_where)!=0):
            if 'and' in _where:
                indice = _where.index('and')
                where1 = _where[:indice]
                where2 = _where[indice+1:]
                _where = []
                _where.append(where1)
                _where.append('and')
                _where.append(where2)
            elif 'or' in _where:
                indice = _where.index('or')
                where1 = _where[:indice]
                where2 = _where[indice+1:]
                _where = []
                _where.append(where1)
                _where.append('or')
                _where.append(where2)
            else:
                _where = [_where]
                   
        return _select,_from,_where,_order

#Com Tudo
#comando = "select s.name as nome,s.id as identificador, t.semester as semestre from student as s, takes as t where s.id = t.id and t.semester >= 'Spring' order by tabela.nome ASC"
#Sem Where
#comando = "select s.name as nome,s.id as identificador, t.semester as semestre from student as s, takes as t order by tabela.nome ASC"
#Sem Order by
#comando = "select s.name as nome,s.id as identificador, t.semester as semestre from student as s, takes as t where s.id > 4 and idade like '%oi'"
#Sem Nada
#comando = "select name ,semester as semestre from student , takes as t"

#i = Interpretador()
#i.interpretar(comando)

