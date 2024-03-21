#获得目标旅游地
destination = request.json.get('destination', "")

#返回json格式的结果给文心一言，由其润色后输出给用户
def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/get_destination", methods=['POST'])
async def get_destination():
    destination = request.json.get('destination', "")
    prompt = ""
    if response.status_code == 200:
        #加入获得目的地后的操作
        result=''
    else:
        result = "抱歉，无法找到这个地方。" 
    #处理后输出的结果放在result中，prompt暂时可以不加
    return make_json_response( {"result":result,"prompt": prompt})

@app.route("/get_navigation_needs", methods=['POST'])
async def get_navigation_needs():
    start_location = request.json.get('start_location', "")
    end_location = request.json.get('end_location', "")
    prompt = ""
    if response.status_code == 200:
        #加入获得导航需求后的操作
        result=''
    else:
        result = "抱歉，无法找到这个地方。" 
    #处理后输出的结果放在result中，prompt暂时可以不加
    return make_json_response( {"result":result,"prompt": prompt})