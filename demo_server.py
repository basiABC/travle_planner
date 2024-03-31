from flask_cors import CORS
import json
from gevent import pywsgi
import os
import sys
import subprocess
import time
from flask import Flask, request, make_response, send_from_directory

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})

#返回json格式的结果给文心一言，由其润色后输出给用户
def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/get_destination", methods=['POST'])
async def get_destination():
    destination = request.json.get('destination', "")
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
    
    # 假设tenxunMAP.html已经移动到/var/www/html/maps目录
    url = "http://<你的服务器的IP或域名>/maps/tenxunMAP.html"
    
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
