import Queue
import threading
import boto
from boto.exception import *
from ssl import SSLError
import exif_process
import redis_store_exif
import logging
import time
import os

subdir = '../images'

#Number of threads to use at a time for IO
num_threads = 8

# Function downloads image file from s3 bucket
def process_key(key_queue, file_queue, ind):
    while True:
        key = key_queue.get()
        while True:
            try:
                key.get_contents_to_filename(os.path.join(subdir, key.name))
                file_queue.put(key.name) 
                break
            except S3ResponseError as e:
                logging.error("%s: %s" % (key.name, e))
                break
            except SSLError as e:
                logging.error("%s: %s" % (key.name, e))
        
        key_queue.task_done()

# Function opens image file, reads exif data, and adds it to Redis
def process_file(file_queue, ind):
    while True:
        key_name = file_queue.get()

        try:
            exif_data = exif_process.exif_get_data(os.path.join(subdir, key_name))
            redis_store_exif.add_to_redis(key_name, exif_data)
        except Exception as e:
            logging.error("%s: %s" % (key_name, e))

        file_queue.task_done()

# Creates threads for downloading and processing images 
def process_images_from_s3(bucket_name):
    logging.basicConfig(filename='processing.log',level=logging.INFO)
  
    if (not os.path.isdir(subdir)):
        os.mkdir(subdir)
    
    conn = boto.connect_s3()    
    bucket = conn.get_bucket(bucket_name)

    key_queue = Queue.Queue()
    file_queue = Queue.Queue()

    for i in xrange(num_threads):
        key_process_thread = threading.Thread(target=process_key, args=(key_queue, file_queue, i,))
        file_process_thread = threading.Thread(target=process_file, args=(file_queue,i,))

        key_process_thread.daemon = True
        file_process_thread.daemon = True

        key_process_thread.start()
        file_process_thread.start()

    for key in bucket.list():
        key_queue.put(key)
   
    key_queue.join()
    file_queue.join()
