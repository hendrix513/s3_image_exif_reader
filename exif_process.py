import exifread

def exif_get_data(pathname):
    file = open(pathname)
    tags = exifread.process_file(file)
    file.close()
    return tags
