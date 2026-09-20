from flask import Flask, request, jsonify
# request: 是 Flask 提供的全局对象，包含了客户端发来的所有信息。
# jsonify: Flask 的工具函数，用于将 Python 字典或列表转换成标准的 JSON 格式发送给客户端。

from h6_bilstm_predict_fun import predict_fun



# 1. 创建App应用(对象)
app = Flask(__name__)

# 2. 创建预测接口(路由 + 预测函数)
# @app.route：这是一个装饰器，它将下面的函数与特定的网络地址关联起来。
# /predict：这是接口的 URL 路径。客户端需要访问 http://服务器IP:端口/predict才能触发这个函数。
# methods=['POST']：限制了访问方法只能是 POST。这意味着该接口用于接收客户端发送过来的数据，而不是像网页那样直接展示给用户看。

@app.route("/distill_predict", methods=['POST'])
def distill_predict():
    # 获取用户请求中的数据,
    # "request" 是 Flask 提供的全局对象，包含了客户端发来的所有信息。
    # get_json() 会把接收到的 JSON 数据自动转换成 Python 字典。
    request_data = request.get_json()
    print(request_data)
    # 调用预测函数
    response = predict_fun(request_data)
    print(response)

    # 返回结果,
    return response




# 3. 启动App应用
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)