from web_api.dialogue_api import dialogue_api_handler
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from tools import draw
import os

app = Flask(__name__)
api = Api(app)
CORS(app)
file_path = r"../output/sessionlog.txt"
parser = reqparse.RequestParser()
parser.add_argument('user_input',type=str,location='json')
dialogue_api_hl = dialogue_api_handler()
draw.set_initialization(file_path)

class request_openai(Resource):
    AdditionalWord = "在你每次输出的时候,对小说中除了语言描写的内容,其他的内容都用”[]“框住。并单独一段生成在回复的最末尾。你不要输出你自己的状态。不多于50个单词，用英文回复"
    def post(self):
        # 设置 http_proxy 和 https_proxy 的值
        os.environ['http_proxy'] = 'http://127.0.0.1:7890'
        os.environ['https_proxy'] = 'http://127.0.0.1:7890'
        res_dict = {'code':0,'message':'success','res':''}
        args = parser.parse_args()
        user_request_input = args['user_input']

        try:
            res = dialogue_api_hl.generate_massage(user_request_input+request_openai.AdditionalWord)
            res_dict['res'] = res           
        except Exception as e:
            res_dict['code'] = 1
            res_dict['message'] = 'call failde'
            res_dict['res'] = '!!! The api call is abnormal, please check the backend log'
        return res_dict
@app.route("/")
def index():
    return render_template("index.html")


api.add_resource(request_openai, '/request_openai')

if __name__ == '__main__':    app.run(host='0.0.0.0',port=9200,debug=True)
