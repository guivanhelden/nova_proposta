from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import time
from typing import Optional

class SixvoxLogin:
    def __init__(self):
        # Get credentials and data from environment variables
        self.login_email: str = os.environ.get('LOGIN', '')
        self.login_senha: str = os.environ.get('SENHA', '')
        
        # Dados Pessoais
        self.nome_corretor: str = os.environ.get('NOME_CORRETOR', '')
        self.nome_socio: str = os.environ.get('NOME_SOCIO', '')
        self.grade: str = os.environ.get('GRADE', '')
        self.telefone: str = os.environ.get('TELEFONE', '')
        self.email: str = os.environ.get('EMAIL', '')
        
        # Dados Profissionais
        self.unidade: str = os.environ.get('UNIDADE', '')
        self.equipe: str = os.environ.get('EQUIPE', '')
        self.data_entrada: str = os.environ.get('DATA_ENTRADA', '')
        
        # Endereço
        self.endereco: str = os.environ.get('ENDERECO', '')
        self.bairro: str = os.environ.get('BAIRRO', '')
        self.cidade: str = os.environ.get('CIDADE', '')
        self.cep: str = os.environ.get('CEP', '')
        self.estado: str = os.environ.get('ESTADO', '')
        
        # Documentos
        self.data_nascimento: str = os.environ.get('DATA_NASCIMENTO', '')
        self.cpf: str = os.environ.get('CPF', '')
        self.cnpj: str = os.environ.get('CNPJ', '')
        self.rg: str = os.environ.get('RG', '')
        
        # Dados Bancários
        self.banco: str = os.environ.get('BANCO', '')
        self.codigo_banco: str = os.environ.get('CODIGO_BANCO', '')
        self.agencia: str = os.environ.get('AGENCIA', '')
        self.conta: str = os.environ.get('CONTA', '')
        self.tipo_conta: str = os.environ.get('TIPO_CONTA', '')
        
        # Dados do Titular
        self.titular_conta: str = os.environ.get('TITULAR_CONTA', '')
        self.titular_cpf: str = os.environ.get('TITULAR_CPF', '')
        
        # Dados PIX
        self.chave_pix: str = os.environ.get('CHAVE_PIX', '')
        self.tipo_pix: str = os.environ.get('TIPO_PIX', '')
        
        required_fields = [
            'login_email', 'login_senha', 'nome_corretor', 'telefone', 
            'email', 'cpf'
        ]
        
        missing_fields = [field for field in required_fields 
                         if not getattr(self, field)]
        
        if missing_fields:
            raise ValueError(f"Required fields missing: {', '.join(missing_fields)}")
            
        self.driver: Optional[webdriver.Chrome] = None
        
        # Logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def setup_driver(self):
        """Initialize Chrome driver with headless options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Chrome driver initialized successfully")
    
    def login(self) -> bool:
        """Perform login to the Sixvox platform"""
        try:
            self.setup_driver()
            self.driver.get("http://vhseguro.sixvox.com.br/")
            
            # Wait for email field to be available
            email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
            )
            email.send_keys(self.login_email)
            
            # Fill password
            password = self.driver.find_element(By.XPATH, '//*[@id="xenha"]')
            password.send_keys(self.login_senha)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, '//*[@id="enviar"]')
            login_button.click()
            
            logging.info("Login successful!")
            return True
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return False
            
    def preencher_dados(self) -> bool:
        """Preencher dados do corretor"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Navegação inicial
            logging.info("Iniciando navegação no menu")
            menu_equipe = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="menu_equipe"]/i')))
            menu_equipe.click()
            time.sleep(1)
            
            com_manual = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="com_manual"]')))
            com_manual.click()
            time.sleep(1)
            
            sub_manual = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="sub_manual"]/a[1]')))
            sub_manual.click()
            time.sleep(1)
            
            # Novo corretor
            logging.info("Iniciando cadastro de novo corretor")
            novo_corretor = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabs-1"]/button[4]')))
            novo_corretor.click()
            
            # Preenchimento dos dados básicos
            logging.info("Preenchendo dados básicos")
            self.driver.find_element(By.XPATH, '//*[@id="corretor"]').send_keys(self.nome_corretor)
            self.driver.find_element(By.XPATH, '//*[@id="nome_alternativo"]').send_keys(self.nome_socio)
            
            # Selecionar grade
            grade_select = Select(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="cod_corretor_tipo"]'))))
            grade_select.select_by_value(self.grade)
            
            # Contato
            self.driver.find_element(By.XPATH, '//*[@id="fone"]').send_keys(self.telefone)
            self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.email)
            
            # Unidade e equipe
            unidade_select = Select(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="cod_loja"]'))))
            unidade_select.select_by_value(self.unidade)
            
            equipe_select = Select(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="cod_equipe"]'))))
            equipe_select.select_by_value(self.equipe)
            
            # Dados pessoais
            logging.info("Preenchendo dados pessoais e endereço")
            self.driver.find_element(By.XPATH, '//*[@id="entrada"]').send_keys(self.data_entrada)
            self.driver.find_element(By.XPATH, '//*[@id="endereco"]').send_keys(self.endereco)
            self.driver.find_element(By.XPATH, '//*[@id="bairro"]').send_keys(self.bairro)
            self.driver.find_element(By.XPATH, '//*[@id="cidade"]').send_keys(self.cidade)
            self.driver.find_element(By.XPATH, '//*[@id="cep"]').send_keys(self.cep)
            self.driver.find_element(By.XPATH, '//*[@id="uf"]').send_keys(self.estado)
            
            # Mudança para aba de documentos e banco
            logging.info("Mudando para aba de documentos e banco")
            aba_docs = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ui-id-2"]')))
            aba_docs.click()
            time.sleep(2)
            
            # Documentos
            logging.info("Preenchendo documentos")
            self.driver.find_element(By.XPATH, '//*[@id="nascimento"]').send_keys(self.data_nascimento)
            self.driver.find_element(By.XPATH, '//*[@id="cpf"]').send_keys(self.cpf)
            self.driver.find_element(By.XPATH, '//*[@id="cnpj"]').send_keys(self.cnpj)
            self.driver.find_element(By.XPATH, '//*[@id="rg"]').send_keys(self.rg)
            
            # Dados bancários
            logging.info("Preenchendo dados bancários")
            self.driver.find_element(By.XPATH, '//*[@id="banco"]').send_keys(self.banco)
            self.driver.find_element(By.XPATH, '//*[@id="codigo_banco"]').send_keys(self.codigo_banco)
            self.driver.find_element(By.XPATH, '//*[@id="agencia"]').send_keys(self.agencia)
            self.driver.find_element(By.XPATH, '//*[@id="conta"]').send_keys(self.conta)
            
            # Tipo de conta
            conta_select = Select(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tipo_conta"]'))))
            conta_select.select_by_value(self.tipo_conta)
            time.sleep(2)
            
            # Dados do titular
            logging.info("Preenchendo dados do titular")
            self.driver.find_element(By.XPATH, '//*[@id="titular_conta"]').send_keys(self.titular_conta)
            self.driver.find_element(By.XPATH, '//*[@id="titular_cpf"]').send_keys(self.titular_cpf)
            
            # Configuração PIX
            logging.info("Configurando PIX")
            self.driver.find_element(By.XPATH, '//*[@id="pix"]').send_keys(self.chave_pix)
            pix_select = Select(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tipo_pix"]'))))
            pix_select.select_by_value(self.tipo_pix)
            time.sleep(2)
            
            # Salvar
            logging.info("Salvando dados")
            botao_salvar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="salvar01"]')))
            botao_salvar.click()
            time.sleep(3)
            
            logging.info("Dados salvos com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao preencher dados: {str(e)}")
            return False
            
    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            logging.info("Chrome driver closed")

if __name__ == "__main__":
    try:
        sixvox = SixvoxLogin()
        if sixvox.login():
            success = sixvox.preencher_dados()
            if not success:
                raise Exception("Falha ao preencher dados")
        else:
            raise Exception("Login failed")
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        exit(1)
    finally:
        sixvox.close_driver()
