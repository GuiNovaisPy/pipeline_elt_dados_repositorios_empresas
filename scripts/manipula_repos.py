import requests
import base64
import os
from dotenv import load_dotenv


load_dotenv()
class ManipulaRepositorios:
    def __init__(self,username):
        self.username = username
        self.url_base = 'https://api.github.com'
        acess_token = os.getenv('acess_token')
        self.headers = {
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization' :'Bearer '+ acess_token
        }
        
    def cria_repo(self,nome):
        data = {
            'name': nome,
            'description' : 'Dados dos repositorios de algumas empresas',
            'private' : False 
        }
        url = self.url_base +'/user/repos'
        response = requests.post(url,headers=self.headers,json=data)
        print('status de criacao do repositorio: ' +str(response.status_code))
        return response.status_code
    
    def upload_no_repositorio(self,caminho_arquivo,nome_repo,nome_arquivo_no_repo):
        with open(caminho_arquivo,'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)
        
        url = f'{self.url_base}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo_no_repo}'
        data = {
            'message' : 'adicionando um novo arquivo',
            'content' : encoded_content.decode('utf-8'),#indicando com decode que a sequencia binaria base64 é uma sequencia textual
        }
        response = requests.put(url,headers=self.headers,json=data)
        print('status de importacão do arquivo: ' +str(response.status_code))
        
 
novo_repo = ManipulaRepositorios(os.getenv('owner_git'))

nome_repo = 'linguagens_repositorios_empresas'
novo_repo.cria_repo(nome_repo)     
novo_repo.upload_no_repositorio('data_processed/linguagens_amazon.csv',nome_repo,'linguagens_amazon.csv')
novo_repo.upload_no_repositorio('data_processed/linguagens_netflix.csv',nome_repo,'linguagens_netlix.csv')
novo_repo.upload_no_repositorio('data_processed/linguagens_spotify.csv',nome_repo,'linguagens_spotify.csv')
   
