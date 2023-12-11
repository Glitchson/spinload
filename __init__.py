""" 
Launches a load spinner in the console whilst a background process is running
It runs in a daemon thread to prevent the stopping of other background tasks
`Methods`
1. `start(delay_ms:int)` - Starts the spinner with a delay of `delay_ms` milliseconds
2. `stop(epilogue:str)` - Stops the spinner and prints `epilogue` at the end
3. `echo(_str:str)` - Prints some text whilst ensuring the animation remains unruined
`Demo`
>>> from spinload import Spinner
    spinner=Spinner(prefix="Downloading module ... ",cycles=["\\","-","|","-","/"])
    def some_process():
        ...
        # use this instead of the print statement
        spinner.echo("Almost there!")
        ...
    def some_other_process():
        ...
        # use this instead of the print statement
        spinner.echo("Almost there!")
        ...
    def main():
        spinner.start()
        try:
            someProcess()
            spinner.stop("Process done!")
            spinner.update(prefix="Running other process ... ")
            spinner.start()
            some_other_process()
            spinner.stop("Process 2 done!")
        except KeyboardInterrupt:
            spinner.stop("Process interrupted!")
        except Exception as e:
            spinner.stop(f"Error: {e}")
    if __name__=="__main__":
        main()
NOTE: The spin loader cannot be used in more than one threaded process.
"""
from threading import Thread
from time import sleep
def thread(f):
    def wrapper(*args,**kwargs):
        def main():
            return f(*args,**kwargs)
        t=Thread(target=main)
        t.daemon=True
        return t
    return wrapper
class _spinner:
    def __init__(self,prefix:str,cycles:list[str]) -> None:
        self.prefix=prefix or "Loading "
        cycles=cycles or [chr(0x2190),chr(0x2191),chr(0x2192),chr(0x2193)]
        self.cycles=[f"{self.prefix} {i}" for i in cycles]
        self.__load__=True
        self.__started__=False
        self.cycelen=max([len(i) for i in self.cycles])
    def start(self,delay_ms:int):
        self.delay_ms=delay_ms or 500
        @thread
        def load():
            cycles=self.cycles
            counter=0
            while self.__load__:
                counter+=1
                if counter==len(cycles):
                    counter=0
                print(f"\r{cycles[counter]} ",end="")
                sleep(self.delay_ms/1000)
            print(f"\r{" "*self.cycelen}",end="")
        self.t=load()
        self.__started__=True
        self.t.start()
    def stop(self,epilogue:str):
        epilogue=epilogue or "Process done !"
        self.__load__=False
        self.t.join()
        print(f"\r{epilogue}")
        self.__load__=True
        self.__started__=False
    def echo(self,_str:str):
        print(f"\r{" "*self.cycelen}",end="")
        _str= _str if _str.endswith("\n") else _str+"\n"
        print(f"\r{_str}",end="")
        self.start(self.delay_ms)
    def update(self,prefix:str=None,cycles:list[str]=None):
        self.prefix=prefix or self.prefix
        cycles=cycles or self.cycles
        self.cycles=[f"{self.prefix} {i}" for i in cycles]
        self.cycelen=max([len(i) for i in self.cycles])
class Spinner(_spinner):
    """
    This is a class that creates a loading animation for a process.
    It takes in :
        `prefix`
    The text before the loading animation,,, you can add syle using colorama.
    It is set to `loading` on default
        `cycles`
    This is a list that contains the strings that will give an illusion of progress.
    For example:
        ['.  ','.. ','...',' ..','  .','   ']
    The example above is set as the default
    The class contains methods such as :
        `start`
    Takes in the delay in miliseconds in which the animation occurs and initialises the loading animation
        `stop`
    Stops the loading animation
    """
    def __init__(self, prefix: str=None, cycles: list[str]=None) -> None:
        super().__init__(prefix, cycles)
    def start(self, delay_ms: int = None)->None:
        """
        Starts the loading animation in the background as your process runs
        The `delay_ms` is set to 500 default
        """
        return super().start(delay_ms)
    def stop(self,epilogue:str=None)->None:
        """
        Stops the loading animation
        """
        return super().stop(epilogue)
    def echo(self,_str):
        """
        Overwrites the Loader text while the loading continues hence preventing the animation from being ruined.
        """
        super().echo(_str)
    def update(self, prefix: str = None, cycles: list[str] = None):
        """
        Changes the spinner prefix or cycles if the same spinner is meant to be reused in another process.
        """	
        return super().update(prefix, cycles)
__all__=["Loader"]