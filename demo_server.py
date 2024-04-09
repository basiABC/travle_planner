from flask_cors import CORS
import json
from gevent import pywsgi
import os
import sys
import subprocess
import time
from flask import Flask, request, make_response, send_from_directory,g
import requests

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})

history = []
destination=''
app.config['param']=0

#返回json格式的结果给文心一言，由其润色后输出给用户
def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.context_processor
def get_question():
    global destination
    answer=g.get('answer', '')
    question ={
        1:f"根据用户输入'{answer}'给出相应回答，并询问是几个人出游",
        2:f"根据用户输入‘{answer}’给出相应回答，并询问计划呆多久",
        3:f"根据用户输入‘{answer}’给出相应回答，并询问用户想要什么风格的旅程",
        4:f"根据用户输入‘{answer}’给出相应回答，并询问{destination}有没有特别想去的地方",
        5:f"根据用户输入‘{answer}’给出相应回答，并询问用户的游玩预算",
        6:f"根据用户输入‘{answer}’给出相应回答，并询问用户打算在住宿上花费的预算",
        7:f"根据用户输入‘{answer}’给出相应回答，并告诉用户旅游计划马上生成"
    }
    return dict(prompt= question[app.config['param']])

@app.route("/get_info", methods=['POST'])
async def get_info():
    global destination
    global history
    g.answer = request.json.get('info', "")
    print(g.answer)
    history.append(g.answer)
    app.config['param'] = len(history)
    if(destination!=""):
        destination = request.json.get('destination', "")
    print(destination)
    print(history)
    return make_json_response( {"prompt":get_question()['prompt']})

def info_processing():
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_monet?access_token=" + "24.776588ead166875f54e62a0b839b4ddc.2592000.1714468642.282335-57393223"
    info = "".join(history)
    dict_info={
    "content_list":[
        {
            "content":f'{info}',
            "query_list":[
                {
                    "query":"出游人数"
                },
                {
                    "query":"行程持续时间"
                },
                {
                    "query": "旅游风格"
                },
                {
                    "query": "特别想游玩的景点"
                },
                {
                    "query": "游玩预算"
                },
                {
                    "query": "住宿预算"
                }
            ]
        }]
    }
    json_info = json.dumps(dict_info, ensure_ascii = False, indent = 4).encode('uft-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers = headers, data = json_info)

    print(response.text)


@app.route("/get_destination", methods=['POST'])
async def get_destination():
    global destination
    if destination != "":
        #加入获得目的地后的操作
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # 构造hotel_note项目的目录路径
        hotel_note_directory = os.path.join(current_directory, 'hotel_note')
        # 确保hotel_note目录存在
        if not os.path.exists(hotel_note_directory):
            print("hotel_note项目目录不存在")
            sys.exit(1)
        os.chdir(hotel_note_directory)
        print("当前工作目录:", os.getcwd())
        commands = [
            'scrapy crawl cityid',
            'scrapy crawl hotel_search -a tag={}'.format(destination),
            'scrapy crawl travel_note -a tag={}'.format(destination)
        ]
        for cmd in commands:
            process = subprocess.Popen(cmd.split(), cwd=hotel_note_directory)
            process.wait()  # 等待命令执行完成
            time.sleep(2)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_directory)  # 改变工作目录到包含 scrapy.cfg 的目录
        with open('./hotel_note/hotel.json', 'r',encoding='utf-8') as file:
                # 加载JSON内容
                result = json.load(file)
    else:
        result = "抱歉，无法找到这个地方。" 
    return make_json_response( {"result":result})


@app.route('/maps/<filename>')
def maps(filename):
    # 此处假设你的HTML文件位于服务器的/var/www/html/maps目录下
    # 你需要确保这个路径是正确的，并且服务器配置允许从此目录提供文件
    return send_from_directory('/var/www/html/maps', filename)

@app.route("/get_navigation_needs", methods=['POST'])
def get_navigation_needs():
    start_location = request.json.get('start_location', "")
    end_location = request.json.get('end_location', "")
    
    # tenxunMAP.html已经移动到目录
    url = "http://122.51.205.7/.connection/tenxunMAP.html"
    
    link = f'<a href="{url}" target="_blank">点击这里查看从 {start_location} 到 {end_location} 的路线</a>'
    
    result = f"请参考以下链接了解详细信息：{link}"
    #处理后输出的结果放在result中，prompt暂时可以不加
    return make_json_response( {"result":result})

@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """
        注册用的：返回插件的描述文件，描述了插件是什么等信息。
        注意：API路由是固定的，事先约定的。
    """
    host = request.host_url
    with open(".well-known/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "application/json"}


@app.route("/.well-known/openapi.yaml")
async def openapi_spec():
    """
        注册用的：返回插件所依赖的插件服务的API接口描述，参照openapi规范编写。
        注意：API路由是固定的，事先约定的。
    """
    with open(".well-known/openapi.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 8081), app)
    server.serve_forever()
