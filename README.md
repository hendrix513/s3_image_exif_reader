# s3_image_exif_reader
Tool to process EXIF data from images stored on Amazon S3

Requires Python Redis and exifreader libraries

To run tool on 'waldo-recruiting' bucket, run "python waldo_example.py" with Redis running. Images will be stored "images" folder. After tool finishes you can look up EXIF data by filename in Redis
