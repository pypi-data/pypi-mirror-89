#!/usr/bin/env python
from weboa import *
from weboa import __VERSION__
import sys
import glob

def runcli():
    print("Welcome to Weboa!")
    commands = {
        "version": ("--version", "-v"),
        "init": ("--init","-i"),
        "start": ("--start", "-S"),
        "update": ("--update","-u"),

        "less": ("--less","-l"),
        "sass": ("--sass","--scss","-s"),

        "langs": ("--langs", "-L"),
        "css": ("--css")
    }

    args = sys.argv
    for i in range(len(args)):
        if args[i] in commands["version"]:
            print(f"Weboa version is {__VERSION__}")

        elif args[i] in commands["update"]:
            os.system("pip install weboa --upgrade")
            os.system("pip3 install weboa --upgrade")

        elif args[i] in commands["start"]:
            Processing.Save_Path(os.getcwd())
            Printer.info(f"Weboa is installed at {prepare.Package.stream}")

        elif args[i] in commands["less"]:
            _path = os.getcwd()
            _weboa = Processing.Weboa_Open()
            while True:
                for i in glob.glob(_path+"/*.less"):
                    if(not Processing.is_file_changed(_weboa, i, precss="less")):
                        continue
                    Processing.pre_css(_weboa, i, precss="less")

        elif args[i] in commands["sass"]:
            _path = os.getcwd()
            _weboa = Processing.Weboa_Open()
            while True:
                for i in glob.glob(_path + "/*.scss"):
                    if (not Processing.is_file_changed(_weboa, i, precss="scss")):
                        continue
                    Processing.pre_css(_weboa, i, precss="scss")
                for i in glob.glob(_path+"/*.sass"):
                    if(not Processing.is_file_changed(_weboa, i, precss="sass")):
                        continue
                    Processing.pre_css(_weboa, i, precss="sass")


        elif args[i] in commands["init"]:
            _path = os.getcwd()
            Processing.Save_Path(_path)
            try:
                if commands["langs"][0] in args:
                    lindex = args.index(commands["langs"][0])
                elif commands["langs"][1] in args:
                    lindex = args.index(commands["langs"][1])
                else:
                    lindex = False

                if(lindex):
                    Printer.info(f"Langs {args[lindex + 1]}")
            except IndexError:
                pass

            try:
                if commands["css"][0] in args:
                    cssindex = args.index(commands["css"][0])
                    Printer.info(f"Css {args[cssindex+1]}")
            except IndexError:
                pass

            php=PHP(path="")
            php.BUILDFOLDER = _path+"/"
            php.FS()
            php.index()
            php.language()
            php.project()
            php.libs()
            php.ico()
            php.css()
            php.robots()
            php.js()
            php.img()
            php.readme()
            php.gitignore()
            php.ico_langs()

if(__name__=="__main__"):
    runcli()