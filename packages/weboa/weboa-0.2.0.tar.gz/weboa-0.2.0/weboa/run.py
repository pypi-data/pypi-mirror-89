#!/usr/bin/env python
from weboa import *
from weboa import __VERSION__
import sys
import glob
import lesscpy
from six import StringIO

def runcli():
    print("Welcome to Weboa!")
    commands = {
        "version": ("--version", "-v"),
        "init": ("--init","-i"),
        "start": ("--start", "-s"),
        "update": ("--update","-u"),
        "less": ("--less","-l"),

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
                    if "less" not in _weboa.keys():
                        _weboa["less"] = dict()
                    if i not in _weboa["less"].keys():
                        _weboa["less"][i] = 0

                    ts0 = _weboa["less"][i]
                    ts1 = os.stat(i).st_mtime

                    if(ts0==ts1):
                        continue

                    with open(i,"r") as f:
                        less = f.read()
                        css = lesscpy.compile(StringIO(less), minify=True)
                    with open(i[:-4]+"css","w") as f:
                        f.write(css)
                    _weboa["less"][i] = os.stat(i).st_mtime
                    Processing.Weboa_Save(_weboa)

        elif args[i] in commands["init"]:
            _path = os.getcwd()
            Processing.Save_Path(_path)
            try:
                if commands["langs"][0] in args:
                    lindex = args.index(commands["langs"][0])
                elif commands["langs"][1] in args:
                    lindex = args.index(commands["langs"][1])

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