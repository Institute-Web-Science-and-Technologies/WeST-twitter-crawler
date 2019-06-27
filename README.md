# WeST-twitter-crawler
A simple Twitter crawler powered by Logstash.

#Usage
1. Create '.env' based on '.env.example' with your own Twitter app keys.
2. Edit the 'keyword' field in 'twitter_pipeline.conf' with the keywords you want to crawl for.
3. Run 'docker-compose up --build'
4. Results shoud be in the 'output folder'.
