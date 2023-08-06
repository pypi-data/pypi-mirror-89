import os
import shutil
import filecmp


def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def reset_dir(out_dir):
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)


def diff(fn0, fn1):
    return not filecmp.cmp(fn0, fn1, shallow=False)


def cp(dst, src):
    shutil.copyfile(src, dst)


def file_to_string_list(fn, encoding='utf-8'):
    with open(fn, 'rt', encoding=encoding) as fin:
        ret = fin.readlines()
    ret = [i.strip('\n') for i in ret]
    return ret


def string_list_to_file(fn, txt_list, encoding='utf-8'):
    with open(fn, mode='wt', encoding=encoding) as fout:
        for txt in txt_list:
            fout.write('{}\n'.format(txt))


def file_to_bytes(fn):
    with open(fn, mode='rb') as fin:
        return fin.read()


def bytes_to_file(fn, bytes):
    dirname = os.path.dirname(fn)
    if not is_dir(dirname):
        makedirs(dirname)
    with open(fn, mode='wb') as fout:
        fout.write(bytes)

# TODO need testcase


def find_file(dir):
    file_list = []
    for root, _, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


is_dir = os.path.isdir

is_file = os.path.isfile


def is_exist(path):
    return is_dir(path) or is_file(path)


def rm_dir(path):
    if is_file(path):
        raise ValueError()
    shutil.rmtree(path, ignore_errors=True)


def rm_file(path):
    if is_dir(path):
        raise ValueError()
    if not is_exist(path):
        return
    os.remove(path)


def rm(path):
    if is_dir(path):
        rm_dir(path)
        return
    if is_file(path):
        rm_file(path)
        return
