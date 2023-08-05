import requests, time ,os, socket, hashlib, sys, datetime

def start():
    hostname = socket.gethostname()

    
    today = datetime.date.today()
    node_token = hashlib.md5('miaosla_token{}'.format(str(today.day)).encode('utf-8')).hexdigest()

    dataa = {
            'token': node_token,
            'nodename': "-----\rSystem Message",
            'log':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：Start BOT in {}\rLocal IP: {} | Request IP:".format(hostname,str(get_host_ip()))
        }
    get_node = requests.get('https://miao.mw-ai.cn/cloudlog/start.php',params=dataa)
    if get_node.text == 'ok':
        print('Central node connection: \033[0;32mSuccess\033[0m')
    elif get_node.text == 'error':
        print('Central node connection: \033[0;31mError\033[0m')
        sys.exit()
    else:
        print('Central node connection: {}'.format(get_node.text))
        sys.exit()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def sleep(time_d):
    for i in range(time_d, -1, -1):
        if i == 0:
            print("\r", "\b\b\b\b\b\b\b\b\b\b\b\b\b", end="", flush=True)
        else:
            print("\r", "\bSLA | Wait {}s".format(i), end="", flush=True)
            time.sleep(1)

def sla(url, status, node_name, bot_token, chat_id):

    def cloudlog(node_name_a, error_num_a, url_a):
        try:
            today = datetime.date.today()
            node_token = hashlib.md5('miaosla_token{}'.format(str(today.day)).encode('utf-8')).hexdigest()
            dataa = {
                'token': node_token,
                'nodename': node_name_a,
                'log':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num_a))
            }
            get_node = requests.get('https://miao.mw-ai.cn/cloudlog/log.php',params=dataa, timeout=10)
            if get_node.text == 'ok':
                pass
            elif get_node.text == 'error':
                print('Central node connection: \033[0;31mError\033[0m')
                bot_error('於中央節點的通訊失敗')
                sys.exit()
            else:
                print('Central node connection: {}'.format(get_node.text))
                bot_error('於中央節點的通訊失敗')
                sys.exit()
        except requests.exceptions.ConnectionError:
            print('Central node connection: \033[0;31mError\033[0m')
            bot_error("建立於中央節點的通訊失敗")
            sys.exit()
        except requests.exceptions.ReadTimeout:
            print('Central node connection: \033[0;31mError\033[0m')
            bot_error("於中央節點的通訊超時")
            sys.exit()
        except:
            print('Central node connection: \033[0;31mError\033[0m')
            bot_error("於中央節點的通訊失敗")
            sys.exit()

    def get_error(error_num, url_node):
                
        print("\033[31m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} | {}".format(str(error_num), node_name))
        data = {
            "chat_id":chat_id,
            "text":"{}：{}".format(node_name,str(error_num.replace(' ','%20'))),
            "reply_markup":'{"inline_keyboard": [[{"text": "訪問該節點", "url": "' + url_node + '"}, {"text": "忽略問題", "callback_data": "pass"}]]}'
        }
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), timeout=5, params=data)
        open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num)+"\n"))
        cloudlog(node_name, error_num.replace(' ','%20'), url_node)

    def bot_error(error_num): 
        print("\033[31m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} | {}".format(str(error_num), node_name))
        data = {
            "chat_id":chat_id,
            "text":"{} (BOT)：{}".format(node_name,str(error_num.replace(' ','%20'))),
            "reply_markup":'{"inline_keyboard": [[{"text": "忽略問題", "callback_data": "pass"}]]}'
        }
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), timeout=5, params=data)
        open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num)+"\n"))

    try:
        miao = requests.get(url,timeout=5)
        
        if str(miao) == "<Response [{}]>".format(status):
            print("\033[34m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} OK | {}".format(status, node_name))
            open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：400 OK" + "\n")
        elif str(miao) == "<Response [404]>":
            get_error("404 ERROR", url)
        elif str(miao) == "<Response [403]>":
            get_error("403 ERROR", url)
        elif str(miao) == "<Response [503]>":
            get_error("503 ERROR", url)
        elif str(miao) == "<Response [502]>":
            get_error("502 ERROR", url)
        else:
            get_error(miao, url)
    except:
        print("Error, repeat request")
        try:
            miao = requests.get(url,timeout=5)
        
            if str(miao) == "<Response [{}]>".format(status):
                print("\033[34m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} OK | {}".format(status, node_name))
                open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：400 OK" + "\n")
            elif str(miao) == "<Response [404]>":
                get_error("404 ERROR", url)
            elif str(miao) == "<Response [403]>":
                get_error("403 ERROR", url)
            elif str(miao) == "<Response [503]>":
                get_error("503 ERROR", url)
            elif str(miao) == "<Response [502]>":
                get_error("502 ERROR", url)
            else:
                get_error(miao, url)
        except requests.exceptions.ConnectionError:
            get_error("ConnectionError", url)
        except requests.exceptions.ReadTimeout:
            get_error("Timeout", url)
        except:
            get_error("未知錯誤", url)

if __name__ == "__main__":
    print('Please do not execute the module file directly')
    