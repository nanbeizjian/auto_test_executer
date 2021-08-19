from configparser import ConfigParser
from basePage.common.public import *



filename = get_work_dir() +  '/config/config.ini'
encoding = 'utf8'
conf = ConfigParser()
conf.read(filename, encoding)

def conf_get_str(section, option):
    return conf.get(section, option)

def conf_get_int(section, option):
    return conf.getint(section, option)

def conf_get_float(section, option):
    return conf.getfloat(section, option)

def conf_get_bool(section, option):
    pass

def conf_write_data(section, option, value):
    conf.set(section, option, value)

