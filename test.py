import json
from tkinter import *

root = Tk()

def callback():
    fileName = filedialog.askopenfilename()
    print(fileName)
    
Button(root, text="打开文件夹", command=callback)
a = {'start':123,
     'exit': 'F2'}

b = {'start':123, 'exit':['a', 'b']}

ins = [a, b]
jsobj = json.dumps(ins)
with open('test.json', 'w') as f:
    f.write(jsobj)
    

with open('test.json', 'r') as f:
   b = f.read()
   b = json.loads(b)
print(b[0])

root.title('你好')
root['font'] = ("黑体", 30, "bold")
root.mainloop()