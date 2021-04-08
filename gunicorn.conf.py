import config as cfg
import multiprocessing

bind = "%s:%s" % (cfg.SERVER.IP,cfg.SERVER.PORT)
workers = multiprocessing.cpu_count() * 2 + 1
