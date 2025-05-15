import pandas as pd
import requests
import math
import os
from dotenv import load_dotenv

class DadosRepositorios:
    def __init__(self,owner:str):
        load_dotenv()
        self.owner = owner
        self.url_base_git = 'https://api.github.com'
        acess_token = os.getenv('acess_token')
        self.headers = {
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization' :'Bearer '+ acess_token
        }
        
    def _calcula_o_numero_de_paginas(self,):
        MAX_REPOSITORIOS_POR_PAGINA = 30
        url  = f'https://api.github.com/users/{self.owner}'
        response = requests.get(url,headers=self.headers)
        data_json = response.json()
        qtd_repositorios = int(data_json['public_repos'])
        numero_de_paginas = math.ceil(
            qtd_repositorios / MAX_REPOSITORIOS_POR_PAGINA
        )
        return numero_de_paginas
        
    def _listar_repositorios(self,numero_total:int):
        repos_list = []
        for page_num in range(1,numero_total+1):
            try:
                url_page = f'{self.url_base_git}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url_page,self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)
        return repos_list
                
    def _resgatar_nome_e_linguagem_utilizada(self,repos_list:list):
        nome_repositorios = []
        linguagem_repositorios = []
        for page in repos_list:
            for repo in page:
                nome_repositorios.append(repo['name'])
                linguagem_repositorios.append(repo['language'])
        return nome_repositorios,linguagem_repositorios
    
    def criar_df_linguagens(self,):
        numero_de_paginas = self._calcula_o_numero_de_paginas()
        repositorios = self._listar_repositorios(numero_de_paginas)
        nomes,linguagens = self._resgatar_nome_e_linguagem_utilizada(
            repositorios
        )
        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['repository_language'] = linguagens
        return dados
                
  
dados_amazon = DadosRepositorios('amzn') 
ling_mais_usadas_amzn = dados_amazon.criar_df_linguagens()    
print(ling_mais_usadas_amzn)   

dados_netflix = DadosRepositorios('netflix') 
ling_mais_usadas_netflix = dados_netflix.criar_df_linguagens()    
print(ling_mais_usadas_netflix)   

dados_spotify = DadosRepositorios('spotify') 
ling_mais_usadas_spotify = dados_spotify.criar_df_linguagens()    
print(ling_mais_usadas_spotify)

#Salvando os dados
path_base = 'data_processed/'
ling_mais_usadas_amzn.to_csv(path_base+'linguagens_amazon.csv')
ling_mais_usadas_netflix.to_csv(path_base+'linguagens_netflix.csv')
ling_mais_usadas_spotify.to_csv(path_base+'linguagens_spotify.csv')
                
    