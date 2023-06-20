import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import path
import hashlib
import logging
from multiprocessing import Pool
from selenium.common.exceptions import NoAlertPresentException

from functools import partial
from tqdm import tqdm


banner1 = """
   _____                 ______      _  
  / ____|               |  ____|    | |  
 | (___   ___ __ _ _ __ | |__  __  _| |_ 
  \___ \ / __/ _` | '_ \|  __| \ \/ / __|
  ____) | (_| (_| | | | | |____ >  <| |_ 
 |_____/ \___\__,_|_| |_|______/_/\_\\__|
 
 """

banner2 = """
  .-')                ('-.         .-') _   ('-.  ) (`-.      .-') _    
 ( OO ).             ( OO ).-.    ( OO ) )_(  OO)  ( OO ).   (  OO) )   
(_)---\_)   .-----.  / . --. /,--./ ,--,'(,------.(_/.  \_)-./     '._  
/    _ |   '  .--./  | \-.  \ |   \ |  |\ |  .---' \  `.'  / |'--...__) 
\  :` `.   |  |('-..-'-'  |  ||    \|  | )|  |      \     /\ '--.  .--' 
 '..`''.) /_) |OO  )\| |_.'  ||  .     |/(|  '--.    \   \ |    |  |    
.-._)   \ ||  |`-'|  |  .-.  ||  |\    |  |  .--'   .'    \_)   |  |    
\       /(_'  '--'\  |  | |  ||  | \   |  |  `---. /  .'.  \    |  |    
 `-----'    `-----'  `--' `--'`--'  `--'  `------''--'   '--'   `--'   
"""

banner3 = """
   SSSSSSSSSSSSSSS                                                    EEEEEEEEEEEEEEEEEEEEEE                           tttt          
 SS:::::::::::::::S                                                   E::::::::::::::::::::E                        ttt:::t          
S:::::SSSSSS::::::S                                                   E::::::::::::::::::::E                        t:::::t          
S:::::S     SSSSSSS                                                   EE::::::EEEEEEEEE::::E                        t:::::t          
S:::::S               cccccccccccccccc aaaaaaaaaaaaa nnnn  nnnnnnnn     E:::::E       EEEEExxxxxxx      xxxxxxttttttt:::::ttttttt    
S:::::S             cc:::::::::::::::c a::::::::::::an:::nn::::::::nn   E:::::E             x:::::x    x:::::xt:::::::::::::::::t    
 S::::SSSS         c:::::::::::::::::c aaaaaaaaa:::::n::::::::::::::nn  E::::::EEEEEEEEEE    x:::::x  x:::::x t:::::::::::::::::t    
  SS::::::SSSSS   c:::::::cccccc:::::c          a::::nn:::::::::::::::n E:::::::::::::::E     x:::::xx:::::x  tttttt:::::::tttttt    
    SSS::::::::SS c::::::c     ccccccc   aaaaaaa:::::a n:::::nnnn:::::n E:::::::::::::::E      x::::::::::x         t:::::t          
       SSSSSS::::Sc:::::c              aa::::::::::::a n::::n    n::::n E::::::EEEEEEEEEE       x::::::::x          t:::::t          
            S:::::c:::::c             a::::aaaa::::::a n::::n    n::::n E:::::E                 x::::::::x          t:::::t          
            S:::::c::::::c     cccccca::::a    a:::::a n::::n    n::::n E:::::E       EEEEEE   x::::::::::x         t:::::t    tttttt
SSSSSSS     S:::::c:::::::cccccc:::::a::::a    a:::::a n::::n    n::::EE::::::EEEEEEEE:::::E  x:::::xx:::::x        t::::::tttt:::::t
S::::::SSSSSS:::::Sc:::::::::::::::::a:::::aaaa::::::a n::::n    n::::E::::::::::::::::::::E x:::::x  x:::::x       tt::::::::::::::t
S:::::::::::::::SS  cc:::::::::::::::ca::::::::::aa:::an::::n    n::::E::::::::::::::::::::Ex:::::x    x:::::x        tt:::::::::::tt
 SSSSSSSSSSSSSSS      cccccccccccccccc aaaaaaaaaa  aaaannnnnn    nnnnnEEEEEEEEEEEEEEEEEEEEExxxxxxx      xxxxxxx         ttttttttttt  """



def logs(driver, alert, result, extension_name, payload):
    # !! [Selenium cant take screenshot of alerts as it occurs outside the DOM] !!
    # driver.save_screenshot("alert_screenshot.png")
    try:
        # Log the info (both success and fail)
        if result == 'Success':
            alert_text = alert.text
            alert.accept()  # Accept the alert window
            logging.critical(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.CRITICAL)}, {extension_name}, {alert_text}, {payload}")
        else:
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.info)}, {extension_name}, 'NIL', {payload}")
    except NoAlertPresentException:
        logging.warning("No alert present")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

# def process_payload(items, payloads,url_path, abs_path):

def process_payload(args,url_path, abs_path):
    
    items, payloads = args

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)

    driver.get(url_path)
    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new = driver.current_window_handle

    driver.get('https://www.example.com')
    driver.switch_to.window(original)
    
    for payload in payloads:
        a = driver.find_element(By.ID, 'replacementInput')
        a.clear()
        a.send_keys(payload)
        button = driver.find_element(By.ID, 'replaceButton')
        button.click()

        driver.switch_to.window(new)

        try:
            # wait 3 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            logs(driver, alert, 'Success', url_path, payload)
            # print('+ Alert Detected +')
        except TimeoutException:
            logs(driver, 'NIL', 'Fail', url_path, payload)
            # print('= No alerts detected =')
        
        # change back to popup.html to try another payload
        driver.switch_to.window(original)

        # update progress bar
        progress_bars[items - 1].update(1)  # Subtract 1 to match the index

    
    # close driver after  loop gaodim
    # driver.quit()

def gui(extension_path):
    # Getting id of extension [start]
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id(extension_path)

    def subset_payloads(file_path):
        payloads1 = []
        payloads2 = []
        payloads3 = []

        with open(file_path, 'r') as file:
            for line in file:
                payload = line.strip()  # Remove leading/trailing whitespace
                # Assign the payload to one of the subsets
                if len(payloads1) < len(payloads2) and len(payloads1) < len(payloads3):
                    payloads1.append(payload)
                elif len(payloads2) < len(payloads3):
                    payloads2.append(payload)
                else:
                    payloads3.append(payload)

        return payloads1, payloads2, payloads3

    payloads1, payloads2, payloads3 = subset_payloads('payloads/small_payload.txt')


    # list of payloads to process
    global items
    items = [1, 2, 3]

    global progress_bars 
    # progress_bars = [tqdm(total=len(payloads1), desc=f'Instance {item}') for item in items]
    progress_bars = [tqdm(total=len(payloads1), desc=f'Instance {item}', bar_format='{desc}: {bar} {percentage:3.0f}%|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]') for item in items]


    num_processes = 3  # Define the number of concurrent processes
    with Pool(num_processes) as pool:
        partial_process_payload = partial(process_payload, url_path=url_path, abs_path=abs_path)
        for _ in pool.imap(partial_process_payload, zip(items,[payloads1, payloads2, payloads3])):
            pass

def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/penetration_log_gui.txt',
        level=logging.ERROR,
        format='%(asctime)s, %(message)s'
    )
    #display Banner
    print(banner2)

    # Run program
    gui('Extensions/h1-replacer/h1-replacer_P')
    

if __name__ == '__main__':
    main()








