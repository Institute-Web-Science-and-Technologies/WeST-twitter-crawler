FROM docker.elastic.co/logstash/logstash:7.1.1

RUN mkdir /usr/share/logstash/output

COPY twitter_pipeline.conf /usr/share/logstash/pipeline/twitter_pipeline.conf
