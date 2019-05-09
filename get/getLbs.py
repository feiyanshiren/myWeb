# -*- coding: utf-8 -*-
import traceback

def post(self):
    try:
        config = self.settings['config']
        the_path = config.main_path + "/tasks/lbs"
        files = open(the_path, "r")
        str1 = files.read()
        files.close()
        return str1
    except:
        return traceback.format_exc()