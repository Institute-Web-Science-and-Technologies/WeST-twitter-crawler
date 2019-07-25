import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
import web

urls = ('/','index')

render = web.template.render('templates/')

class index:
    keyword_list = []
    initialized = False
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], 
                value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    consumer = KafkaConsumer(
                'twitter-crawler-response',
                bootstrap_servers=['kafka:9092'],
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id='twitter-crawler',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                )
    def send_command(self, comm, kw):
        pack = {'command':comm, 'keywords':kw}
        self.producer.send('twitter-crawler-command', value=pack)
        return
    def listen(self):
        message = self.consumer.next()
        return message
    def GET(self):
        if self.initialized == False:
            self.send_command('cur',[])
        res = self.listen()
        return render.index(res)
    
    def POST(self):
        form = web.input(keywords='')
        kws = form.keywords
        kw = kws.split()
        self.send_command('add',kw)
        res = self.listen()
        return render.index(res)
    
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
    