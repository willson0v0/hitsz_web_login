import argparse
import socket
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import getpass
import os

target_ip = "10.248.98.2"
logging.basicConfig(format="[%(asctime)15s] [%(levelname)8s] %(message)s", stream=sys.stdout, level=logging.INFO, )

WINDOW_SIZE = "1920,1080"

def script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def resolve_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target_ip, 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main():
    parser = argparse.ArgumentParser(description="input your username and password.")
    parser.add_argument('--username', type=str, required=False, help='Your user name to login into web auth system.')
    parser.add_argument('--password', type=str, required=False, help='Your password to login into web auth system.')
    parser.add_argument('--user-ip', type=str, required=False, help='Your IP address.')
    parser.add_argument('--driver-path', type=str, required=False, help='Where is chromedriver?')

    args = parser.parse_args()
    if args.user_ip is None:
        args.user_ip = resolve_ip()
    args.domain = ""
    args.host = "http://" + target_ip + "/srun_portal_pc?ac_id=1&theme=basic2"
    logging.info("HITSZ Fake Web Login V0.1")
    
    if args.username is None:
        args.username = input("Username: ")
    
    if args.password is None:
        args.password = getpass.getpass("Password (no echo): ")

    logging.info("Trying to login with " + args.username + " for " + args.user_ip)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    
    if args.driver_path is None:
        browser = webdriver.Chrome(service=Service("dependencies\chromedriver.exe"), options=chrome_options)
    else:
        browser = webdriver.Chrome(service=Service(args.driver_path), options=chrome_options)
    
    browser.get(args.host)
    browser.execute_script(f'$(username).val("{args.username}")')
    browser.execute_script(f'$(password).val("{args.password}")')
    browser.execute_script('$(login).click()')
    time.sleep(5)

    # create result folder if not there
    os.makedirs(os.path.join(script_path(), "result"), exist_ok=True)

    time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    browser.save_screenshot(os.path.join(script_path(), "result", f"result_{time_str}.png"))
    
    list_of_files = os.listdir(os.path.join(script_path(), "result"))
    full_path = [os.path.join(script_path(), "result", x) for x in list_of_files]

    if len(list_of_files) > 5:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

    logging.info("Login done, please check for result.")

if __name__ == "__main__":
    main()
