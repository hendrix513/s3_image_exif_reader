import redis

def add_to_redis(key_name, exif_data):
    try:
        r = redis.Redis()
        #insert placeholder if exif_data is empty 
        if (exif_data):
            r.hmset(key_name, exif_data)
        else:
            r.set(key_name, "NONE")
    except:
        raise
