import tornado.web
import tornado.ioloop
from handler.service import SenGen_cn_Handler
from handler.service import SenGen_en_Handler
from handler.service import SenGen_lyric_Handler
from handler.service import TestHandler
from handler.predict import mt5_prompt_transfer_Handler 


HANDLERS = [                            #路由表
    (r"/CNsengen",mt5_prompt_transfer_Handler),         #映射到中文例句生成类
    (r"/ENsengen",SenGen_en_Handler),         #映射到英文例句生成类
    (r"/CNlyric",SenGen_lyric_Handler),       #映射到锦句类  
    (r"/test",TestHandler)                    #映射到测试类
]

settings = {                            #参数配置
    #"login_url": "/login",
    "debug": True,                      #debug模式，代码有更改时自动重启，方便开发
}


def make_app():                         #根据所提供的路由表和配置生成app实例
    return tornado.web.Application(HANDLERS, **settings)        


if __name__ == "__main__":
    port = 9999                       #使用的端口
    app = make_app()                    #创建应用对象
    app.listen(port)                    #监听服务所挂接的端口
    print('server start on port: {}'.format(port))
    tornado.ioloop.IOLoop.current().start()    #启动Ioloop轮循监听


