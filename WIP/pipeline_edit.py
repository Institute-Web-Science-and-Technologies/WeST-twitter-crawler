import json
from kafka import KafkaConsumer
from kafka import KafkaProducer

class pipeline:
    keyword_list = []
    initialized = False
    def read_existing(self):#checks conf file for existing keywords
        if self.initialized == False:
            #open pipeline file, find position of keyword field
            fo = open("twitter_pipeline.conf", "r+")
            f = fo.read()
            pos = f.find("keywords => ")
            fo.seek(pos + 13)
            rest = fo.read()
            #reads existing keywords in pipeline file, add them to keyword_list
            curr_keyword = ""
            start_flag = False
            
            for char in rest:
                if char == "]":
                    break
                elif ((char == '"')|(char == "'")):
                    if start_flag == False:
                        start_flag = True
                    else:
                        self.keyword_list.append(curr_keyword)
                        curr_keyword = ""
                        start_flag = False
                elif ((char != " ")&(char != ",")):
                    curr_keyword = curr_keyword + char
            self.initialized = True
        return 
    def add_keyword(self, kw):#add new keyword to conf file
        st_len = len(self.keyword_list) #current number of keywords
        res = {'response':'Added', 'keywords':[]}
        #open pipeline config, find position of keyword field
        fo = open("twitter_pipeline.conf", "r+")
        f = fo.read()
        pos = f.find("keywords => ")
        fo.seek(pos + 13)
        rest = fo.read()
        fo.seek(pos + 13)
        #format keywords for pipeline
        keyword = ""
        for word in kw:
            if (self.check_kw(word) == False):
                print('Added', word)
                res.get('keywords').append(word)
                self.keyword_list.append(word)
                keyword += "'" + word + "', "
        #If there are no existing keywords, format ending of keyword string
        if st_len == 0 :
            keyword = keyword[0:-2]
        
        fo.write(keyword)
        fo.write(rest)
        fo.close()
        return res
    def delete_keyword(self, kw):#delete keyword from conf file
        res = {'response':'Deleted', 'keywords':[]}
        #open pipeline config, find position of keyword field
        fo = open("twitter_pipeline.conf", "r+")
        f = fo.read()
        pos = f.find("keywords => ")
        fo.seek(pos + 13)
        next_char = fo.read(1)
        char_count = 0
        while next_char !=']':
            next_char = fo.read(1)
            char_count += 1
        fo.seek(pos + (13+char_count))
        rest = fo.read()
        #delete keyword
        for word in kw:
            if(self.check_kw(word) == True):
                print('Deleted', word)
                res.get('keywords').append(word)
                self.keyword_list.remove(word)
        #rebuild conf file
        fo.seek(pos + 13)
        keyword = ""
        for word in self.keyword_list:
            keyword += "'" + word + "', "
        keyword = keyword[0:-2]
        fo.write(keyword)
        fo.write(rest)
        fo.truncate()
        fo.close()
        return res
    def check_kw(self, kw):#check if a keyword exists
        if kw in self.keyword_list:
            return True
        else:
            return False
    def check_keyword(self, kw):#check a list of keywords
        res = {'response':'Exists', 'keywords':[]}
        for word in kw:
            if self.check_kw(word) == True:
                res.get('keywords').append(word)
        return res
    def get_current(self):#return current list of keywords
        res = {'response':'Current', 'keywords':[]}
        res.get('keywords') = self.keyword_list
        return res
    
if __name__ == "__main__":
    pl = pipeline()
    pl.read_existing()
    
    #Create Kafka consumer
    consumer = KafkaConsumer(
        'twitter-crawler-command',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='twitter-crawler',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    #Create Kafka producer
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], 
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    #read message and response
    for message in consumer:
        content = message.value
        command = content.get('command')
        kw = content.get('keywords')
        if command == 'add':
            response = pl.add_keyword(kw)
        elif command == 'del':
            response = pl.delete_keyword(kw)
        elif command == 'chk':
            response = pl.check_keyword(kw)
        elif command == 'cur':
            response = pl.get_current()
        producer.send('twitter-crawler-response', value=response)
