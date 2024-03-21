import logging
import os
import json

class DebugLogger:
    def __init__(self, file, seperator="---------------------------------------------"):
        self.abs_path = os.path.abspath(file)
        self.seperator = seperator

    def generate_log_str(self, msg: str="", fname: str = "", kwargs={}):
        print_str = self.abs_path + "  --  " + fname + "  " + msg + "\n"
        for key in kwargs.keys():
            print_str += "  " + key + ":  " + str(kwargs[key]) + "\n"
        return print_str

    def log(self, msg: str, fname: str = "", kwargs={}):
        print(self.seperator)
        print(self.generate_log_str(msg=msg,fname=fname,kwargs=kwargs),"\n")
        print(self.seperator)

    def error(self, msg: str, fname: str = "", kwargs={}):
        print(self.seperator)
        print("ERROR  " + self.generate_log_str(msg=msg,fname=fname,kwargs=kwargs),"\n")
        raise("ERROR  ")
    



def usage_ex():
    _logger = DebugLogger(__file__)
    _logger.log(msg="Loogging", fname="Test.Test()",kwargs={"a":3, "b": True})
    _logger.error(msg="Throwing Error", fname="Test.Test()",kwargs={"a":3, "b": True})