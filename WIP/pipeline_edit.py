import json
from kafka import KafkaConsumer

class pl:
    keyword_list = []
    initialized = False
    def read_existing(self):
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
    def add_keyword(self, kw):
        st_len = len(self.keyword_list) #current number of keywords
        #open pipeline config, find position of keyword field
        fo = open("twitter_pipeline.conf", "r+")
        f = fo.read()
        pos = f.find("keywords => ")
        fo.seek(pos + 13)
        rest = fo.read()
        fo.seek(pos + 13)
        #format keywords for pipeline
        keyword = ""
        kw_split = kw.split()
        for word in kw_split:
            if (self.check_kw(word) == False):
                print('Added',word)
                self.keyword_list.append(word)
                keyword += "'" + word + "', "
        keyword = keyword[0:-2]
        #If there are existing keywords, format so that new keywords do not break the old list of keywords
        if st_len > 0 :
            rest = ", " + rest
        
        fo.write(keyword)
        fo.write(rest)
        fo.close()
        return
    
    def delete_keyword(self, kw):
        #open pipeline config, find position of keyword field
        fo = open("twitter_pipeline.conf", "r+")
        f = fo.read()
        pos = f.find("keywords => ")
        fo.seek(pos + 13)
        rest = fo.read()
        fo.seek(pos + 13)
        
        kw_split = kw.split()
        for word in kw_split:
            if(self.check_kw(word) == True):
                #TODO: delete keyword
                print('Deleted',word) #placeholder
                
        return
    
    def check_kw(self, kw):
        if kw in self.keyword_list:
            return True
        else:
            return False
    
if __name__ == "__main__":
    pipeline = pl()
    pipeline.read_existing()
    consumer = KafkaConsumer(
        'twitter-crawler',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='twitter-crawler',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    #read message
    for message in consumer:
        content = message.value
        command = content.get('command')
        kw = content.get('keywords')
        if command == 'add':
            pipeline.add_keyword(kw)
        elif command == 'del':
            pipeline.delete_keyword(kw)
