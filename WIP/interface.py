import json
import uuid
from kafka import KafkaProducer
from kafka import KafkaConsumer
import web

urls = ('/','index')

render = web.template.render('templates/')

class index:
    message_list = []
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
        uid = int(uuid.uuid4())
        pack = {'id':uid, 'command':comm, 'keywords':kw}
        self.producer.send('twitter-crawler-command', value=pack)
        return uid
    def listen(self, uid):
        for old_message in self.message_list:
            if (old_message.get('id') == uid):
                return old_message
        message = self.consumer.next()
        if (message.get('id') == uid):
            return message
        else:
            self.message_list.append(message)
        
        res = {'response':'non'} 
        return res
    def GET(self):
        if self.initialized == False:
            uid = self.send_command('cur',[])
        res = self.listen(uid)
        return render.index(res)
    
    def POST(self):
        form_c = web.input(command='add')
        form_kw = web.input(keywords='')
        
        com = form_c.command
        kws = form_kw.keywords
        kw = kws.split()
        uid = self.send_command(com,kw)
        res = self.listen(uid)
        return render.index(res)
    
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
    