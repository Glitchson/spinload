from argparse import ArgumentParser
from . import Spinner,__doc__
from time import sleep
spinner= Spinner(prefix="Cloning repo ... ")
parser=ArgumentParser()
parser.add_argument("-d","--doc",action="store_true",help="Displays the documentation for the module")
parser.add_argument("-r","--rundemo",action="store_true",help="Shows a demo for how the spinner class works")
class Args:
    doc:bool
    rundemo:bool
def log(t:str):
    for i in t:
        if i=="\n":
            print(i,end="")
            sleep(0.02)
        elif i==" ":
            print(i,end="")
            sleep(0)
        else:
            print(i,end="",flush=True)
            sleep(0.01)
def doc():
    log(__doc__)
def cloningmock():
    sleep(2)
    spinner.echo("Cloned file src/main.py")
    sleep(2)
    spinner.echo("Cloned file src/other.py")
    sleep(2)
def demo():
    try:
        spinner.start()
        cloningmock()
        spinner.stop("Cloning done!")
    except KeyboardInterrupt:
        spinner.stop("Cloning interrupted!")
    except Exception as e:
        spinner.stop(f"Error: {e}")
def main():
    args:Args=parser.parse_args()
    if args.doc:
        doc()
        return
    if args.rundemo:
        demo()
        return
    parser.print_help()
if __name__=="__main__":
    main()