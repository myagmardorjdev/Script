import time,datetime
import random,sys

class list_unique_counter():
    def __init__(self, listname,index):
        self.content = listname
        self.index = index
        self.checkvalues = []
        for i in range(len(self.content)):
            if self.content[i][self.index] in self.checkvalues:
                pass
            else:
                self.checkvalues.append(self.content[i][self.index])
    def returnc(self):
        return self.checkvalues

class writetextnew():                                                                               
    def __init__(self, content,path):
        self.path = path
        self.content =content
        with open(self.path, 'w') as f:
            string = self.content
            f.write(string)

class writetextappend():                                                                               
    def __init__(self, content,path):
        self.path = path
        self.content = "\n" + content
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                pass
        with open(self.path, 'a') as f:
            string = self.content
            f.writelines(string)

class generatepkid():
    def __init__(self):
        self.now = datetime.now()
        self.genid = random.randint(10000,99999)
        self.value = (str(self.now.year) + ("0" if self.now.month < 10 else "") + str(self.now.month)+("0" if self.now.day < 10 else "")+str(self.now.day)+("0" if self.now.hour < 10 else "")+str(self.now.hour)+("0" if self.now.minute < 10 else "")+str(self.now.minute)+("0" if self.now.second < 10 else "")+str(self.now.second)+ str(self.genid))
    
    def returnc(self):
        return self.value

class readtextfile_to_dict():                                                                              
    def __init__(self, value):
        self.filename = value
        self.contents = []
        self.configuredict = {}
        self.read_file_contents()

    def read_file_contents(self):
        with open(self.filename, 'r') as f:
            self.contents = f.readlines()

    def returnc(self):
        for i in range(len(self.contents)):
            ind = self.contents[i].strip().find('=') 
            if ind != -1:
                self.configuredict[(self.contents[i].strip()[:ind]).strip()]=(self.contents[i].strip()[ind+1:]).strip()
        return self.configuredict
    


