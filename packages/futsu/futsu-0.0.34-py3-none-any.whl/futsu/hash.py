import hashlib


def md5_str(s):
    m = hashlib.md5()
    m.update(s.encode('utf8'))
    return m.hexdigest()


def sha256_str(s):
    m = hashlib.sha256()
    m.update(s.encode('utf8'))
    return m.hexdigest()
