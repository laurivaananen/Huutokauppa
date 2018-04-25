import os

broker_url = os.environ.get("REDIS_URL")
result_backend = os.environ.get("REDIS_URL")

# broker_url = "redis://flaskredis.jspvaj.0001.usw2.cache.amazonaws.com:6379/0"
# result_backend = "redis://flaskredis.jspvaj.0001.usw2.cache.amazonaws.com:6379/0"