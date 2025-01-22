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
        # Get credentials from environment variables
        self.login_email: str = os.environ.get('LOGIN', '')
        self.login_senha: str = os.environ.get('SENHA', '')
        
        if not all([self.login_email, self.login_senha]):
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
    
    def login(self):
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
        
    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            logging.info("Chrome driver closed")

if __name__ == "__main__":
    try:
        sixvox = SixvoxLogin()
        success = sixvox.login()
        if not success:
            raise Exception("Login failed")
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        exit(1)
    finally:
        sixvox.close_driver()
