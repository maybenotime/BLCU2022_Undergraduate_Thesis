from flask import Flask, jsonify, request
from gevent import pywsgi
from transformers import MT5Tokenizer, MT5ForConditionalGeneration
import json
import re

print('ready to predict')
app = Flask(__name__)
model = MT5ForConditionalGeneration.from_pretrained('/home/ysp2018/keywords_generation_web/checkpoint-774501').to('cuda')
tokenizer = MT5Tokenizer.from_pretrained('/home/ysp2018/keywords_generation_web/checkpoint-774501')


@app.route(f"/", methods=['get', 'post'])
def api():
    input_json = request.json.get('input')
    complete_input = json.loads(input_json)
    print(complete_input)
    mode = r'[^a-z<>0123456789_▁]+'                 #删掉特殊token
    output = generate_sentence(complete_input[0],model,tokenizer)
    print(output)
    mask_group = re.findall(mode,output)
    word_group = re.findall(mode,complete_input[0])
    print(word_group)
    complete_str = ''
    temp_i = 0
    try:
        for i in range(len(word_group)):
            complete_str = complete_str +mask_group[i] + word_group[i]
            temp_i = i + 1
        complete_str = complete_str + mask_group[temp_i]
        print(complete_str)
        result = complete_str.replace(" ","")
    except Exception as e:
        print(str(e))

    return jsonify(result)

def generate_sentence(input, model, tokenizer):
    model.eval()                 
    input_ids = tokenizer.encode(input, return_tensors="pt").to('cuda')  
    outputs = model.generate(input_ids=input_ids,num_beams=20, max_length=128, repetition_penalty=10.0)
    output_str = tokenizer.decode(outputs.reshape(-1), skip_special_tokens=True)
    return output_str
    
server = pywsgi.WSGIServer(('0.0.0.0', 10000), app)
server.serve_forever()