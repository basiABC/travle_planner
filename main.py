import numpy as np
import requests
import json


def get_embeddings(inputs):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=24.3fccde337b61f285871c8c59332f4244.2592000.1713771111.282335-56909350"
    payload = json.dumps({"input": inputs})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)
    return [data["embedding"] for data in json.loads(response.text)["data"]]

def calculate_similarity(embedding_vector1, embedding_vector2):
    embedding_vector1 = np.array(embedding_vector1)
    embedding_vector2 = np.array(embedding_vector2)
    cosine_similarity = np.dot(embedding_vector1, embedding_vector2.T) / (
        np.linalg.norm(embedding_vector1) * np.linalg.norm(embedding_vector2)
    )
    return cosine_similarity

if __name__ == "__main__":
    needs="想舒适地在古色古香地古镇踏青"
    #当作一个函数的参数传进来
    description="海滨海岛，游轮，踏春，摄影，徒步"
    texts = [
        needs,description
    ]
    print(texts)
    embeddings = get_embeddings(texts)
    similarity = calculate_similarity(embeddings[0], embeddings[1])
    print(f"文本相似度：{similarity}")
