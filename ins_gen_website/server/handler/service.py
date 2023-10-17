import requests
import json
import fastBPE
import subword_nmt.apply_bpe as apply_bpe
from tornado.web import RequestHandler      #导入handler模块

bpe = fastBPE.fastBPE('/home/ysp2018/keywords_generation_web/server/bpe_600w.code')   

class TestHandler(RequestHandler):      #测试类
    def get(self):
        self.write("测试成功!")

class SenGen_cn_Handler(RequestHandler):     #继承RequestHandler类，
    def post(self):
        keys_list = self.get_body_arguments('keywords')     #从请求体中返回指定参数keywords的值，以列表形式返回
        print(keys_list)
        keys_list = bpe.apply(keys_list)
        
        start_span = '[pred]'
        for key in keys_list:
            start_span += ' ' + key + ' [blank]'
       
        for i in range(len(keys_list)+1):
            
            sents_json = json.dumps([start_span])
            res = requests.post(f"http://202.112.194.65:10811/",
                    json={"span_sent":sents_json})
            pred_span = res.json()[0]
            
            pred_span = pred_span.replace('[bos]', '') # remove [bos] [eos]
            pred_span = pred_span.replace('[eos]', '')
            
            start_span = start_span.replace('[pred]', pred_span, 1)
            start_span = start_span.replace('[blank]', '[pred]', 1)
            # 多个空格变成一个空格
            start_span = ' '.join(start_span.split())
        tmp = start_span.split('@@ ')
        start_span = ''.join(tmp)

        result = start_span.replace(" ","")             #删去空格
        self.write(result)

class SenGen_en_Handler(RequestHandler):
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

class SenGen_lyric_Handler(RequestHandler):     #继承RequestHandler类，
    def post(self):
        keys_list = self.get_body_arguments('keywords')     #从请求体中返回指定参数keywords的值，以列表形式返回
        print(keys_list)
        keys_list = bpe.apply(keys_list)
        
        start_span = '[pred]'
        for key in keys_list:
            start_span += ' ' + key + ' [blank]'
       
        for i in range(len(keys_list)+1):
            
            sents_json = json.dumps([start_span])
            res = requests.post(f"http://202.112.194.65:10808/",
                    json={"span_sent":sents_json})
            pred_span = res.json()[0]
            
            pred_span = pred_span.replace('[bos]', '') # remove [bos] [eos]
            pred_span = pred_span.replace('[eos]', '')
            
            start_span = start_span.replace('[pred]', pred_span, 1)
            start_span = start_span.replace('[blank]', '[pred]', 1)
            # 多个空格变成一个空格
            start_span = ' '.join(start_span.split())
        tmp = start_span.split('@@ ')
        start_span = ''.join(tmp)

        result = start_span.replace(" ","")             #删去空格
        self.write(result)

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