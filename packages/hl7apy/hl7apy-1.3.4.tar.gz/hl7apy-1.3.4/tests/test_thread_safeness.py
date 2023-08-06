import logging
import threading
import time
import random
from hl7apy.core import *
import traceback

def thread_function(version):
    try:
        m = Message("ADT_A01", version="2.4")
    except Exception as e:
        logging.error("thread failed %s", version)
        # logging.error(traceback.format_exc())
        pass
    else:
        logging.info("Thread %s success", version)
        pass
    s = random.randint(1, 5)
    # logging.info("Thread %s sleeping %s seconds", version, s)
    time.sleep(s)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    threads = []
    # for i in range(10):
    #     thread_function(i)
    for i in range(10):
        t = threading.Thread(target=thread_function, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


