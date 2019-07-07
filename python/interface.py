import web
urls = ('/','index')

render = web.template.render('templates/')

class index:
    keyword_list = []
    def log_io(self, kw):
        
        st_len = len(self.keyword_list) #current number of keywords
        
        #open pipeline config, find position of keyword field
        fo = open("pipeline/twitter_pipeline.conf", "r+")
        f = fo.read()
        pos = f.find("keywords => ")
        fo.seek(pos + 13)
        rest = fo.read()
        fo.seek(pos + 13)
        
        #format keywords for pipeline
        keyword = ""
        kw_split = kw.split()
        for word in kw_split:
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
    def GET(self):
        kwl = self.keyword_list
        return render.index(kwl)
    def POST(self):
        form = web.input(keywords='')
        kws = form.keywords
        self.log_io(kws)
        kwl = self.keyword_list
        return render.index(kwl)
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
    
