import logging
import time


class Cache:

    def __init__(self, invalidate_timeout, update_func):
        self.timeout = invalidate_timeout
        self.update_func = update_func

        self.value = None
        self.last_fetch = -1

    def get(self):
        if self.value is None or (time.time() - self.last_fetch > self.timeout):
            logging.debug("[+] Fetch new dates from karlsruhe.de")
            self.value = self.update_func()
            self.last_fetch = time.time()

        return self.value
