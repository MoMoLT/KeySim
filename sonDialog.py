from tkinter import messagebox
from tkinter import *
from tools import *
import threading

# 弹窗类
class SonDialog:
    def __init__(self):
        self.root = None
        
        self.control = {}
        self.btnState = {'normal':'raised', 'set':'groove', 'run':'groove'} # 按钮外形
    #====================弹窗设计===============================================
    def createErrorDialog(self, title="错误", message="参数错误！！！"):
        '''
            功能: 警告弹窗
            返回值: 无
        '''
        # 创建警告弹窗
        messagebox.showerror(title, message)
        if self.root:
            self.root.destroy()
    def createInsertDialog(self, title, pList, insSet, instruction):
        '''
            功能: 插入按钮弹窗
            pList: 列表控件
            insSet:列表中所有的指令集合
            instruction:待插入指令
            insStr: 待插入指令字符串
            返回值: 无
        '''
        self.root = Toplevel()
        self.root['bg'] = color['bg']
        self.root.title(title)
        Label(self.root, text='你要将该指令插入到第几行？', bg=color['bg'], foreground=color['font']).pack(padx=10, pady=10)
        ind = StringVar()
        ind.set(str(pList.size() + 1))
        Entry(self.root, textvariable=ind).pack(padx=5, pady=10)

        Button(self.root, text='确认', foreground=color['font'], bg=color['btnNormal'], activebackground=color['btnClick'], width=10, command=lambda:self.insert(self.root,pList, insSet, instruction, ind)).pack(padx=5, pady=5)

    #========================按钮绑定函数=======================================
    def bindKey(self, btnName):
        '''
            功能: 按键设置按钮绑定函数
            btnName: self.control中的按钮名
            返回值: 无
        '''
        threading.Thread(target=self.checkKey, args=(btnName, )).start()
        
    def checkKey(self, btnName):
        '''
            功能: 获取当前按下的按键， 并根据状态改变按钮的外观
            返回值: 无
        '''
        keyButton = self.control[btnName]
        keyButton['relief'] = self.btnState['set']
        
        whileflag = [True]  # 循环flag，True则一直循环
        #threading.Thread(self.ctl.checkPressKey()).start()
        keyName = self.ctl.checkPressKey(whileflag)
        print(keyName)
        keyButton['text'] = keyName
        keyButton['relief'] = self.btnState['normal']
        
        
    def insert(self, root, pList, insSet, instruction, ind):
        '''
            功能: 插入指令
            pList: 列表控件
            insSet:列表中所有的指令集合
            instruction:待插入指令
            insStr: 待插入指令字符串
            ind: 要插入的位置
            返回值: 无
        '''
        # num数值安全检测
        cur = ind.get()
        if checkInt(cur) == False:
            self.createErrorDialog()
            return
        cur = int(cur) - 1
        if cur < 0:
            self.createErrorDialog()
            return
        
        length = len(insSet)
        if cur > length:
            cur = length
        
        # 把指令插入到集合中
        insSet.insert(cur, instruction)
        pList.see(cur)
        '''
        # 清空弹窗
        self.clearList(pList)
        
        # 开始迭代插入列表
        for ins in insSet:
            insStr = getInsStr(ins)
            insStr = "["+str(pList.size() + 1)+"] " + insStr
            pList.insert(END, insStr)
        '''
        showList(pList, insSet)
        
        # 弹窗关闭
        root.destroy()
        
        
        