#pylint: skip-file
import string
import random

def slug_generator(size=50, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
