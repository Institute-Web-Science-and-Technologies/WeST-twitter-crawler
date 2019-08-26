# Usage
1. Create '.env' with your own Twitter app keys.
2. Edit pipelines.yml to control which city keyword sets are crawled.
3. Run "docker build -t docker-crawler ."
4. Run 
docker run --env-file .env \
--mount type=bind,src=/home/$USERNAME/docker-crawler/pipeline,dst=/usr/share/logstash/pipeline \
--mount type=bind,src=/home/$USERNAME/docker-crawler/output,dst=/usr/share/logstash/output \
docker-crawler

Replace the paths in src= with the absolute path to /pipeline/ and /output/ folders
5. Results shoud be in the 'output folder'.
