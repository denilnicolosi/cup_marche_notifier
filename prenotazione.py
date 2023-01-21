import smtplib, ssl
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import argparse

parser = argparse.ArgumentParser(description='Script che invia una notifica mail quando si libera un posto per il cup marche')
parser.add_argument('--cf', type=str, help='Codice fiscale', required=True)
parser.add_argument('--ricetta', type=str, help='Ricetta', required=True)
parser.add_argument('--sender', type=str, help='Email mittente', required=True)
parser.add_argument('--password', type=str, help='Password email mittente', required=True)
parser.add_argument('--receiver', type=str, help='Email destinatario', required=True)
parser.add_argument('--timespan', default=10, type=int, help='Intervallo controllo (minuti)')
parser.add_argument('--port', default=465, type=int, help='Porta smtp')
parser.add_argument('--smtp', default="smtp.gmail.com", type=str, help='Smtp server')
parser.add_argument('--headless', default=argparse.SUPPRESS, nargs='?', help='Chrome headless')
args = parser.parse_args()

send_mail=False
timeout=10

try:
    while(send_mail==False):  
        #utilizzo chrome
        options = webdriver.ChromeOptions() 
        if(hasattr(args, 'headless')):
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(options=options)
        driver.get("https://mycupmarche.it/prenotazionecittadino/web/guest/searchCf")
        WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[3]/div[3]/p"), "Prenotazione Online tramite Codice Fiscale e NRE"))

        driver.find_element(By.ID,"matrice2").send_keys(args.ricetta)
        driver.find_element(By.ID,"cf").send_keys(args.cf) 

        driver.find_element(By.CLASS_NAME,"btn-primary").click()       
        WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[3]/div[4]/div[1]/h3"), "Prestazione trovata"))    
        
        element = driver.find_element(By.XPATH,"/html/body/div[3]/div[4]/div[1]/form/input[5]").click()
        time.sleep(3)
        WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[3]/div[3]/p[2]/span"), args.ricetta))  
        
        if(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[3]/div[4]/div[1]/h3"), "Nessun risultato trovato")):
            print("{} - Nessun risultato trovato".format( datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        else:
            print("{} - Trovata prenotazione disponibile!".format( datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            send_mail=True

        driver.quit() #chiusura chrome 

        if(send_mail):
            #creazione email
            msg = EmailMessage()
            msg.set_content("Trovata prenotazione cup per "+args.cf+" con ricetta "+args.ricetta+". Orario rilevamento: "+datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            msg['Subject'] = "Notifica prenotazione trovata per CUP marche"
            msg['From'] = args.sender
            msg['To'] = args.receiver

            #invio email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(args.smtp, args.port, context=context) as server:
                server.login(args.sender, args.password)
                server.send_message(msg, from_addr=msg['From'], to_addrs=msg['To'])
                print("Email inviata")
        
        time.sleep(args.timespan*60) #attesa intervallo controllo

except Exception as e:
    print(e)

    