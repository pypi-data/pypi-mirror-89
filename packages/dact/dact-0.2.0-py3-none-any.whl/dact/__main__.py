import sys
import os
import json

from .classmodule import MyClass
from .funcmodule import startDjangoProject
from .createreact import getcurrent

def main():
    print('in main')
    args = sys.argv[1:]


    # print('count of args :: {}'.format(len(args)))
    # for arg in args:
    #     print('passed argument :: {}'.format(arg))
    
    
    
    if len(args) < 1: 
        print(
            
            """
            Congratulations! Dact is successfully installed in your system. 
            To learn more about dact, go to https://ayushmankumar7.github.io/dact/. 

            To get started with Dact, type dact newproject 

            Hurray! Your first Django + React Project is ready to be worked on.

            """
        )


    elif len(args) == 1:
        startDjangoProject(args[0])
        
    elif len(args) ==2:
        startDjangoProject(args[0], args[1])
    
    # my_object = MyClass('Your Django + reACT Project is ready to use.')
    # my_object.say_name()

def watch_react():
    with open("dact_config.json") as f:
        data = json.load(f)
    frontend_app = data['Frontend_AppName']
    os.chdir(f"{frontend_app}/static")
    os.system("npm run dev")


def testing():
    print("Testing function was called")

if __name__ == '__main__':
    main()