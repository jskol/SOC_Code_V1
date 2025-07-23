from time import time

def timing(f):
    def wraped_func(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r, took: %2.4f sec' % \
            (f.__name__, te-ts))
        return result
    return wraped_func
