import multiprocessing

bind = "192.168.1.246:8000"
workers = multiprocessing.cpu_count() * 2 + 1
