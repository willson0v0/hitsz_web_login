import argparse
import socket
import logging
import sys
from selenium import webdriver
import time

target_ip = "10.248.98.2"
logging.basicConfig(format="[%(asctime)15s] [%(levelname)8s] %(message)s", stream=sys.stdout, level=logging.INFO, )


def resolve_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target_ip, 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="input your username and password.")
    parser.add_argument('--username', type=str, required=True, help='Your user name to login into web auth system.')
    parser.add_argument('--password', type=str, required=True, help='Your password to login into web auth system.')
    parser.add_argument('--user_ip', type=str, required=False, help='Your IP address.')
    parser.add_argument('--phantomjs_path', type=str, required=False, help='Where is phantomjs?')
    args = parser.parse_args()
    if args.user_ip is None:
        args.user_ip = resolve_ip()
    args.domain = ""
    args.host = "http://" + target_ip + "/srun_portal_pc?ac_id=1&theme=basic2"
    logging.info("HITSZ Fake Web Login V0.1")
    logging.info("Trying to login with " + args.username + " for " + args.user_ip)

    if args.phantomjs_path is None:
        browser = webdriver.PhantomJS()
    else:
        browser = webdriver.PhantomJS(executable_path="./dependencies/phantomjs")
    
    browser.get(args.host)

    browser.execute_script(f'$(username).val("{args.username}")')
    browser.execute_script(f'$(password).val("{args.password}")')
    browser.execute_script('$(login).click()')
    time.sleep(5)
    browser.save_screenshot("result.png")
    logging.info("Login done, please check for result.")
