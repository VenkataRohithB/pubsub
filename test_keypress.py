#import keyboard
#import time

#
# Install PY package: https://pypi.org/project/pytimedinput/
#   def timedKey(prompt="", timeout=5, resetOnInput=True, allowCharacters="")
#   def timedInput(prompt="", timeout=5, resetOnInput=True, maxLength=0, allowCharacters="", endCharacters="\x1b\n\r")
#   def timedInteger(prompt="", timeout=5, resetOnInput=True, allowNegative=True)
#
from pytimedinput import timedInput, timedKey


# Example usage:
while True:
    #key_pressed, timeout = timedKey("Enter something: ", timeout=0.05, endCharacters=" ")
    key_pressed, timeout = timedKey(prompt = None, timeout=0.05, allowCharacters="")
    if key_pressed != "":
        break

    #choice, timedOut = timedInput(prompt="Input now:", timeout=2, resetOnInput=True, maxLength=2, allowCharacters=None, endCharacters=None)
    #print("Key pressed choice=:", choice)

    #choice, timedOut = timedKey(prompt=prompt, timeout=timeout, resetOnInput=resetOnInput, allowCharacters=allowCharacters)
    #print("Key pressed choice=:", choice)

    continue

print("key_pressed=:", key_pressed, " timeout=", timeout)

exit(0)