
import os


class Eraser:

    def __init__(self, files = True, origin = True):

        self.files = files
        self.origin = origin
        
        '''PARAMETER DEFINITIONS'''
        cwd = os.getcwd()       # finds the current working directory

        '''FILE DELETION'''
        for ix in os.listdir(cwd + '/output'):      # if so, loops through all files in the directory corresponding to that parameter
            try:
                os.remove(cwd + '/output' + '/' + ix)       # and removes it
            except:
                raise       # raises an error just in case something gets in the way
        for iy in os.listdir(cwd + '/origin'):      # if so, loops through all files in the directory corresponding to that parameter
            try:
                os.remove(cwd + '/origin' + '/' + iy)       # and removes it
            except:
                raise       # raises an error just in case something gets in the way



"""
===================================================================================================
DELETING DATA FROM MAIN
===================================================================================================
"""

if __name__ == '__main__':

    Eraser()