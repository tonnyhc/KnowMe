from django.core.exceptions import ValidationError


def validate_file_size(image_object):
    if image_object.size > 15_728_640:
        raise ValidationError('The maximum file size that can be uploaded is 15MB!')