import sys
import os
import image_processor

def main():
    image_processor.process_images_from_s3('waldo-recruiting')
    
if __name__ == "__main__":
    main()
