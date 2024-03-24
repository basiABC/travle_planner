import json


file_path='hotel.json'
with open(file_path,'r',encoding='utf-8') as f:
    file_con=f.read()


#data=json.loads(file_con)


"""
for i,value in data.items():
    print(f"酒店编号: {i}")
    print(f"名称: {value['name']}")
    print(f"类型: {value['type']}")
    print(f"评分: {value['score']}")
    print(f"预览: {value['preview']}")
    print(f"价格: {value['price']}")
    print()
"""

def chooseby_price(json_str,max_price):

    data=json.loads(json_str)
    choosenhotels=[]

    for key,value in data.items():
        price_string = value['price']
        price=float(price_string[1:-1])
        if price <max_price:
            choosenhotels.append((key,value, price))


    choosenhotels.sort(key=lambda x:float(x[2]))

    print("合适的酒店：")
    for hotel in choosenhotels:
        print(f"酒店编号: {hotel[0]}")
        print(f"名称: {hotel[1]['name']}")
        print(f"类型: {hotel[1]['type']}")
        print(f"评分: {hotel[1]['score']}")
        print(f"预览: {hotel[1]['preview']}")
        print(f"价格: {hotel[1]['price']}")
        print()


#max_price=float(input("请告诉我您的预算（元）："))
max_price=300.0
chooseby_price(file_con,max_price)









