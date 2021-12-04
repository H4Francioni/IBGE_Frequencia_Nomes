# Bibliotecas
import pandas as pd
import requests
import json

class FrequenciaNomes:
    
    def __init__(self):
        self.contador_f = 0
        self.contador_m = 0
    
    def recebe_nome(self):
        self.nome = str( input('Digite apenas o seu primeiro nome: ') )
        while self.nome.isalpha() != True:
            print('ERRO: É esperado apenas letras para seu nome!')
            self.recebe_nome()

    def groupby_sexo(self):
        
        self.path_nome = ( 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{}'.format(self.nome) )
        self.path_sexo_f = ( 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{}/?sexo=F'.format(self.nome) )
        self.path_sexo_m = ( 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{}/?sexo=M'.format(self.nome) )
                
        self.get_info_name_f = requests.get(self.path_sexo_f)
        self.json_info_name_f = json.loads(self.get_info_name_f.text) 
        self.total_linhas_f = len( self.json_info_name_f[0]['res'] )
        #print(self.total_linhas_f)
    
        self.lista_ano_f = []
        self.lista_frequencia_f = []
    
        while self.contador_f < self.total_linhas_f:
            
            self.check = self.json_info_name_f[0]['res'][self.contador_f]
            self.periodo = self.check['periodo']
            self.lista_ano_f.append(self.periodo)
            self.frequencia_f = self.check['frequencia']
            self.lista_frequencia_f.append(self.frequencia_f)
            self.contador_f += 1
          
        self.j_dict_f = {
            'Periodo':self.lista_ano_f,
            'Frequência_F':self.lista_frequencia_f,
        }
        
        self.df_f = pd.DataFrame(self.j_dict_f)
        #print(self.df_f)
        
        # - - - - - - - - - - 
        
        self.get_info_name_m = requests.get(self.path_sexo_m)
        self.json_info_name_m = json.loads(self.get_info_name_m.text) 
        self.total_linhas_m = len( self.json_info_name_m[0]['res'] )
        #print(self.total_linhas_m)
        
        self.lista_ano_m = []
        self.lista_frequencia_m = []
        
        while self.contador_m < self.total_linhas_m:
            
            self.check = self.json_info_name_m[0]['res'][self.contador_m]
            self.periodo = self.check['periodo']
            self.lista_ano_m.append(self.periodo)
            self.frequencia_m = self.check['frequencia']
            self.lista_frequencia_m.append(self.frequencia_m) 
            self.contador_m += 1
        
        self.j_dict_m = {
            'Periodo':self.lista_ano_m,
            'Frequência_M':self.lista_frequencia_m,
        }
        self.df_m = pd.DataFrame(self.j_dict_m)
        #print(self.df_m)
        
        self.df_all = pd.merge(self.df_f, self.df_m, how='inner', on='Periodo')
        self.df_all['Frequência_Total'] = self.df_all['Frequência_F'] + self.df_all['Frequência_M']
        self.df_all['F_%'] = round( self.df_all['Frequência_F'] / sum(self.df_all['Frequência_Total']) * 100, 2 )
        self.df_all['M_%'] = round( self.df_all['Frequência_M'] / sum(self.df_all['Frequência_Total']) * 100, 2 )
        self.df_all['Década_%'] = round( self.df_all['Frequência_Total'] / sum(self.df_all['Frequência_Total']) * 100, 2 )
        print(self.df_all)
    
Run = FrequenciaNomes()
Run.recebe_nome()
Run.groupby_sexo()