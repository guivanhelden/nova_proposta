from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
from typing import Optional

class SixvoxLogin:
    def __init__(self):
        # Get credentials and data from environment variables
        self.login_email: str = os.environ.get('LOGIN', '')
        self.login_senha: str = os.environ.get('SENHA', '')
        self.nome: str = os.environ.get('NOME', '')
        self.telefone: str = os.environ.get('TELEFONE', '')
        self.email: str = os.environ.get('EMAIL', '')
        
        if not all([self.login_email, self.login_senha, self.nome, self.telefone, self.email]):
            raise ValueError("Required environment variables not found")
            
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
        """Preencher dados do cliente após o login"""
        try:
            # Clicar no menu
            menu_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="menu_corr"]'))
            )
            menu_btn.click()
            logging.info("Menu clicked successfully")
            
            # Preencher nome
            nome_field = self.driver.find_element(By.XPATH, '//*[@id="site"]')
            nome_field.clear()
            nome_field.send_keys(self.nome)
            
            # Preencher email
            email_field = self.driver.find_element(By.XPATH, '//*[@id="facebook"]')
            email_field.clear()
            email_field.send_keys(self.email)
            
            # Preencher telefone
            telefone_field = self.driver.find_element(By.XPATH, '//*[@id="fone"]')
            telefone_field.clear()
            telefone_field.send_keys(self.telefone)
            
            # Clicar em Salvar
            salvar_btn = self.driver.find_element(By.XPATH, '//*[@id="salvar01"]')
            salvar_btn.click()
            logging.info("Dados preenchidos e salvos com sucesso")
            
            # Fazer logout
            logout_link = self.driver.find_element(By.XPATH, "//a[@href='/sair.php']")
            logout_link.click()
            logging.info("Logout realizado com sucesso")
            
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
