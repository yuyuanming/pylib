#!/usr/bin/env python

import string
from time import time
from itertools import chain
from random import sample, choice, seed

def mkpasswd(length=8, digits=2, upper=2, lower=2):
    ''' Create a random password, with specified length
    
    :param length: the totoal length of the password
    
    :param digits: minimum length of digits in password
    
    :param upper: minimum length of uppercase 
    
    :param lower: minimum length of lowercase

    :returns: A random password with the above constrains
    :rtype: str
    '''
    seed(time())
    lowercase = string.lowercase
    uppercase = string.uppercase
    rest = "{0}{1}{2}".format(lowercase, uppercase, string.digits)

    password = list(
            chain(
                (choice(lowercase) for _ in range(lower)),
                (choice(uppercase) for _ in range(upper)),
                (choice(string.digits) for _ in range(digits)),
                (choice(rest) for _ in range(length - lower - upper - digits))
            )
    )

    return ''.join(sample(password, len(password)))

if __name__ == "__main__":
    print mkpasswd()
    print mkpasswd(12)
    print mkpasswd(digits=6)
    print mkpasswd(12, upper=4)
