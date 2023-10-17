from transformers import MT5Tokenizer, MT5ForConditionalGeneration
from tornado.web import RequestHandler      #导入handler模块
import re
import json
import requests

class mt5_prompt_transfer_Handler(RequestHandler):     #继承RequestHandler类，
    def post(self):
        keys_list = self.get_body_arguments('keywords')     #从请求体中返回指定参数keywords的值，以列表形式返回
        prompt = self.get_body_argument('prompt')

        if prompt == 'easy':
            prefix_prompt = '<easy>'
        elif prompt == 'normal':
            prefix_prompt = '<normal>'
        elif prompt == 'hard':
            prefix_prompt = '<hard>'
        input = cat_input(keys_list)
        complete_input = prefix_prompt + input
        print(complete_input)
    
        input_json = json.dumps([complete_input])
        result = requests.post(f"http://202.112.194.62:10000/",
                json={"input":input_json})
        res = result.json()
        print(res)
        self.write(res)


def cat_input(word_list):
    num = len(word_list)
    if num == 1:
        return "<extra_id_0>{}▁<extra_id_1>".format(word_list[0])
    elif num == 2:
        return "<extra_id_0>{}▁<extra_id_1>{}▁<extra_id_2>".format(word_list[0],word_list[1])
    elif num == 3:
        return "<extra_id_0>{}▁<extra_id_1>{}▁<extra_id_2>{}▁<extra_id_3>".format(word_list[0],word_list[1],word_list[2])
    elif num ==4:
        return "<extra_id_0>{}▁<extra_id_1>{}▁<extra_id_2>{}▁<extra_id_3>{}▁<extra_id_4>".format(word_list[0],word_list[1],word_list[2],word_list[3])