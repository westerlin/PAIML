import xml.etree.ElementTree as ET
import random
import re

def safeRetriveDefault(dictionary,label, default):
    leaf = dictionary.get(label)
    if leaf == None:
        return default
    else: 
        return leaf

class Category:
    
    def __init__(self):
        self.patterns = []
        self.templates = []

    def addPattern(self,pattern):
        pattern = re.sub(r'[\*]',r'(.*)',pattern)
        #print(pattern)
        self.patterns.append(pattern)
        
    def addTemplate(self,template):
        #print(template)
        template = template.replace("<star />","{params[1]}")
        template = template.replace("<star index=\"1\" />","{params[2]}")
        template = template.replace("<star index=\"2\" />","{params[3]}")
        #print(template)
        self.templates.append(template)
        
    def matchPattern(self,userinput):
        for pattern in self.patterns:
            self.res = re.match(pattern,userinput,flags=re.IGNORECASE)
            if self.res != None:
                #print(self.res.groups())
                return True
        return False    
        
    def process(self,userinput):
        if self.matchPattern(userinput):
            response = random.choice(self.templates).format(params=self.res)
            return response, True
        return "", False
    
    def normalization(self,text):
        #Remove punctuation
        #Expand contractions
        #Correct a few common spelling mistakes
        #Ensure one space between words
        return text
    

def getInnerXML(node):
    #output = ET.tostring(node).decode()
    #output = output.replace("<"+node.tag+">\n","**")
    #output = output.replace("\n</"+node.tag+">","**")
    #return output
    output = node.text
    for item in node:
        output += ET.tostring(item).decode()
    return output

class AIML:
    
    def __init__(self):
        self.defaultresponse = "I don't understand. Sorry."
        self.label = "nameless"
        self.tree = None
        self.root = None
        self.aimlfile = ""
        self.categories = []

    def load(self,aimlfile):
        self.tree = ET.parse(aimlfile)
        self.root = self.tree.getroot()
        self.source = aimlfile
        if self.root.tag.lower() == "aiml":
            version = safeRetriveDefault(self.root.attrib,"version","1.0")
            for category in self.root.findall("category"):
                cat = Category()
                for pattern in category.findall("pattern"):
                    cat.addPattern(pattern.text)
                for template in category.findall("template"):
                    cat.addTemplate(getInnerXML(template))
                self.categories.append(cat)
        else:
            raise Exception('Error loading {}. Missing AIML tag.'.format(aimlfile))

    def process(self,sentence):
        response = self.__processSentence(sentence)
        if response == None : return self.defaultresponse
        return response
        
    def __processSentence(self,sentence):
        for category in self.categories:
            response, matched = category.process(sentence)
            if matched : return response
        return None