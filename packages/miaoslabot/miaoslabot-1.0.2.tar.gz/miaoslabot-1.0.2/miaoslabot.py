import requests, time ,os, socket

def start():
    hostname = socket.gethostname()
    dataa = {
            'nodename': "-----\rSystem Message",
            'log':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：Start BOT in {}({})".format(hostname,str(get_host_ip()))
        }
    requests.get('https://miao.mw-ai.cn/cloudlog/log.php',params=dataa)

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

    def cloudlog(node_name_a, error_num_a):
        dataa = {
            'nodename': node_name_a,
            'log':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num_a))
        }
        requests.get('https://miao.mw-ai.cn/cloudlog/log.php',params=dataa)

    def get_error(error_num):
                
        print("\033[31m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} | {}".format(str(error_num), node_name))
        data = {
            "chat_id":chat_id,
            "text":"{}：{}".format(node_name,str(error_num.replace(' ','%20'))),
            "reply_markup":'{"inline_keyboard": [[{"text": "問題已解決", "callback_data": "ok"}, {"text": "忽略問題", "callback_data": "pass"}]]}'
        }
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), timeout=5, params=data)
        open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num)+"\n"))
        cloudlog(node_name, error_num.replace(' ','%20'))


    try:
        miao = requests.get(url,timeout=5)
        
        if str(miao) == "<Response [{}]>".format(status):
            print("\033[34m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} OK | {}".format(status, node_name))
            open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：400 OK" + "\n")
        elif str(miao) == "<Response [404]>":
            get_error("404 ERROR")
        elif str(miao) == "<Response [403]>":
            get_error("403 ERROR")
        elif str(miao) == "<Response [503]>":
            get_error("503 ERROR")
        elif str(miao) == "<Response [502]>":
            get_error("502 ERROR")
        else:
            get_error(miao)
    except:
        print("Error, repeat request")
        try:
            miao = requests.get(url,timeout=5)
        
            if str(miao) == "<Response [{}]>".format(status):
                print("\033[34m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{} OK | {}".format(status, node_name))
                open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：400 OK" + "\n")
            elif str(miao) == "<Response [404]>":
                get_error("404 ERROR")
            elif str(miao) == "<Response [403]>":
                get_error("403 ERROR")
            elif str(miao) == "<Response [503]>":
                get_error("503 ERROR")
            elif str(miao) == "<Response [502]>":
                get_error("502 ERROR")
            else:
                get_error(miao)
        except requests.exceptions.ConnectionError:
            get_error("ConnectionError")
        except requests.exceptions.ReadTimeout:
            get_error("Timeout")
        except:
            get_error("未知錯誤")