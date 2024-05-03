# general functions for all python activity
from datetime import datetime as dt
from time import sleep

def _get_datetime():
    return dt.now()
    
def _get_sdatetime(insteadofspace=None):
    return str(dt.now()).replace(' ','T' if insteadofspace == None else insteadofspace)


def wait(secs:int=None, message:str="\n\n<cr> to continue <ctrl-c> to interrupt"):    
    global wait_interrupt
    if wait_interrupt:
        if secs:
            sleep(secs)

            return
        input (message)
    return

def lprint(textToPrint):
    global auxMessagesPrint
    if auxMessagesPrint:
        print(textToPrint)
    return

