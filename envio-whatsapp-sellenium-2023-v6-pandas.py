# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:19:15 2023

@author: felipe.goes
"""

import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
from selenium.webdriver.common.by import By
import sys
import pandas as pd

## SET Recursion Limit ##
sys.setrecursionlimit(10 ** 9)

## Insere variaveis ##
id_mensagem =[]
mensagem = []
telefone = []

## Define driver ##
driver = webdriver.Chrome('C:\windows\chromedriver')
driver.get('https://web.whatsapp.com/')
driver.maximize_window()

contatos_df = pd.read_excel("C:/Users/felipe.goes/Desktop/teste-whatsapp.xlsx")
print(contatos_df)


def wpp():
    ## Loga no whatsapp ##
    while len(driver.find_elements(By.ID,"side"))  < 1:
        time.sleep(1)
        print('Tentativa de Login')

    ## login realizado, lendo API ###
    print('Leitura de API Realizada')
    request = requests.get('https://plataforma.ojo.com.br/api/whatsapp-python/v2')
    todos = json.loads(request.content)
    print(todos)
    
    for i, mensagem in enumerate(contatos_df['id_whatsapp_python_mensagem']):
            id_mensagem = contatos_df.loc[i, "id_whatsapp_python_mensagem"]
            telefone = contatos_df.loc[i, "destinatario"]
            mensagem = contatos_df.loc[i, "mensagem"]
            mensagem_replace = mensagem.replace('\r\n', '%0A')
            link =  f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem_replace}"
            print(link)
            driver.get(link)
        
            #### Espera a pagina do whatsapp carregar ####
            while len(driver.find_elements(By.ID,"side"))  < 1:
                time.sleep(1)
            
            print('Carregando pagina')
            time.sleep(5)
            
            #### Verifica numero invalido ####
            if len(driver.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
                time.sleep(1)
                driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div").send_keys(Keys.ENTER)
                print('mensagem enviada')
                time.sleep(5)
            else:
                link =  f"https://web.whatsapp.com/send?phone=41999298030&text=telefone invalido"
                print(link)
                driver.get(link)
                time.sleep(5)
                while len(driver.find_elements(By.ID,"side"))  < 1:
                    time.sleep(1)
                
                driver.find_element(By.XPATH,"//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div").send_keys(Keys.ENTER)    
                time.sleep(5)
    else:
                print("mensagens enviadas")
                time.sleep(30)
                wpp()
                
                
                


        
wpp()