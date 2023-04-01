from django.core.exceptions import ValidationError

def file_size(value):
    filesize=value.size
    if filesize>25165824:
        raise ValidationError("maximum size is 24MB")

def image_size(value):
    imagesize=value.size
    if imagesize>15728640:
        raise ValidationError("maximum size is 15MB")