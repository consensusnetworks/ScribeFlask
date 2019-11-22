import functools
import time
import urllib.request
import urllib.error

def sleep(timeout, retry=5):
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            exponential = 1
            print(str(retries), str(exponential))
            while retries < retry:
                try:
                    value = function(*args, **kwargs)
                    if value is None:
                        return
                except:
                    timer = ( timeout ** exponential)
                    print(f'Chain Not Ready, sleeping for {timer} seconds')
                    time.sleep(timer)
                    retries += 1
                    exponential +=1
        return wrapper
    return the_real_decorator