from aimlkernel import AIML
import rwutility

mybot = AIML()
rwutility.cls()
mybot.load("persona.aiml")

history = []
userinput = ""
exitwords = ["exit","bye","quit","stop"]


print("AIML %s online.\n" %mybot.label)
while True:
    print(">  ",end="",flush=True)
    userinput, history = rwutility.rawput(history)
    if userinput in exitwords : break
    response = mybot.process(userinput)
    print("\t\t"+response)
print("\t\tOK bye. Have a nice day. Take care.")
print("\nAIML %s offline" %mybot.label)
