
import os
import fnmatch


def get_path(path=[]):
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def list_files(path=None, pattern='*'):
    assert path
    assert type(path) == str
    files = fnmatch.filter(os.listdir(path), pattern)
    return [get_path([path, f]) for f in files
            if os.path.isfile(get_path([path, f]))]


def find_files(path=None, pattern='*'):
    d = []
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            if os.path.isfile(os.path.join(directory, filename)):
                if os.path.islink(os.path.join(directory, filename)):
                    d.append(os.path.join(get_path([directory]), filename))
                else:
                    d.append(get_path([directory, filename]))
    return d


def find_dirs(path=None, pattern='*'):
    d = []
    import fnmatch
    assert path
    assert pattern
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for subdir in fnmatch.filter(subdirs, pattern):
            if os.path.isdir(os.path.join(directory, subdir)):
                if os.path.islink(os.path.join(directory, subdir)):
                    d.append(os.path.join(get_path([directory]), subdir))
                else:
                    d.append(get_path([directory, subdir]))
    return d+[path]


def is_subdir(subpath, path):
    commonpath = os.path.commonprefix([os.path.realpath(subpath),
                                       os.path.realpath(path)])
    return commonpath == path


def create_file_if_notfound(filename):
    dedir = os.path.dirname(filename)
    if not os.path.isdir(dedir):
        os.makedirs(dedir)
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            os.utime(filename, None)
    return filename
