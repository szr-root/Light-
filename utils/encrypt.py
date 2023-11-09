import hashlib
from TB_test import settings


def md5_string(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


if __name__ == '__main__':
    res = md5_string("12345")
    print(res)