import random
import string


def make_activation_key():
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for i in range(40))
