'''
Created on 12.08.2013

@author: Clemens
'''
import os

def convert_ui_files(folder='\ui_files'):
    old_path=os.getcwd()
    new_path=os.getcwd()+folder
    os.chdir(new_path)
    for file in os.listdir('.'):
        if file.endswith(".ui"):
            file_name=str(file).split('.')[0]
            cmd='pyuic4 '+file +' > '+file_name+'.py'
            print cmd
            os.system(cmd)
    os.chdir(old_path)

if __name__=="__main__":
    convert_ui_files()