from tkinter import filedialog
from tkinter import *
from control import *
import threading
import re
from sonDialog import *
from tools import *
import json

# 主窗口
class KZGUI:
    def __init__(self, titleName):
                         
        self.ctl = Control()
        self.root = Tk()                        # 创建根窗口
        #self.root.overrideredirect(True)       # 移除窗口栏
        self.root.iconbitmap('icon2.ico')
        self.root.title(titleName)              # 窗口标题
        self.btnState = {'normal':'raised', 'set':'groove', 'run':'groove'} # 按钮外形
        self.control = {}                       # 控件集合
        self.parameters = {}                    # 控件参数变量集合，临时参数存储，用于add方法取出
        self.insSet = []                        # 指令集合
        
        

        self.switch_pos = False                  # 位置更新开关
        self.clickStart = False                 # 是否点击开始按钮
        self.switch_start = False               # 程序启动开关
        self.switch_shortcut = True             # 热键开启
        self.lock = False                      # 计算
        
        try:
            with open('defaultKey.json', 'r') as f:
                key = f.read()
                self.defaultKey = json.loads(key)
        except:
            self.defaultKey = {'start':'F5',        # 默认的快捷键
                           'exit': 'F6',
                           'stopPos':'F2',
                           'savePos': 'F3'} 
        
    #======================GUI设计部分==========================================================================
    def setKeyLayout(self, group):
        '''
            功能: 按键布局
            group: 容器变量
            返回值: 无
        '''
        # 设置按键名输入
        Label(group, text="按键名: ", bg=color['bg'], foreground=color['font']).grid(row=0, column=0)
        keyButton = Button(group, text="按键", foreground=color['keyFont'], height=2, width=10, relief = self.btnState['normal'], command=lambda:self.bindKey('keyButton'), bg=color['btnNormal'], activebackground=color['btnClick'], font=fonts['keyBtn'])
        keyButton.grid(row=0, column=1)
        
        
        # 设置停顿时间输入
        Label(group, text='停顿时间/s: ', foreground=color['font'], bg=color['bg']).grid(row=1, column=0, padx=5, pady=5)
        interT = StringVar()
        self.parameters['interT'] = interT
        keyEntry1 = Entry(group, textvariable=interT, width=10, bg=color['entryBg']).grid(row=1, column=1, padx=5, pady=5)
        
        # 设置响应次数输入
        Label(group, text='响应次数: ', foreground=color['font'], bg=color['bg']).grid(row=2, column=0, padx=5, pady=5)
        num = StringVar()
        self.parameters['num'] = num
        keyEntry2 = Entry(group, textvariable=num, width=10, bg=color['entryBg']).grid(row=2, column=1, padx=5, pady=5)
        
        # 添加按钮控件
        Button(group, text="添加", foreground=color['font'], width=10, command=lambda:self.addIns('KEY'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=3, column=0, padx=5, pady=5)
        # 插入按钮控件
        Button(group, text="插入", foreground=color['font'], width=10, command=lambda:self.insertIns('KEY'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=3, column=1, padx=5, pady=5)
        
        self.control['keyButton'] = keyButton
        self.control['keyEntry1'] = keyEntry1
        self.control['keyEntry2'] = keyEntry2
        
    def setMoveLayout(self, group):
        '''
            功能: 鼠标移动布局
            group: 容器变量
            返回值: 无
        '''
        # 当前鼠标位置
        getPos = StringVar()
        self.parameters['getPos'] = getPos
        Label(group, textvariable=self.parameters['getPos'], foreground=color['font'], relief='groove', width=20, bg=color['showPosBg']).grid(row=0, column=0, columnspan=2)
        Button(group, text='获取位置', foreground=color['font'], width=19, command=lambda:threading.Thread(target=self.updatePos).start(), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=1, column=0, columnspan=2,pady=10)
        
        # 设置鼠标位置
        posX = StringVar()
        posY = StringVar()
        self.parameters['posX'] = posX
        self.parameters['posY'] = posY
        
        Label(group, text='鼠标移动位置: ', foreground=color['font'], bg=color['bg']).grid(row=2, column=0, columnspan=2, sticky='w')
        Label(group, text='X: ', foreground=color['font'], bg=color['bg']).grid(row=3, column=0, sticky='w')
        Entry(group, textvariable=posX, width=10, bg=color['entryBg']).grid(row=3, column=1)
        Label(group, text='Y: ', foreground=color['font'], bg=color['bg']).grid(row=4, column=0, sticky='w')
        Entry(group, textvariable=posY, width=10, bg=color['entryBg']).grid(row=4, column=1)
        
        # 添加按钮控件
        Button(group, text="添加", foreground=color['font'], width=10, command=lambda:self.addIns('MOVE'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=5, column=0, padx=5, pady=5, sticky='w')
        # 插入按钮控件
        Button(group, text="插入", foreground=color['font'], width=10, command=lambda:self.insertIns('MOVE'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=5, column=1, padx=5, pady=5, sticky='e')
    
    def setPrintLayout(self, group):
        '''
            功能: 内容输出
            group: 容器变量
            返回值: 无
        '''
        # 设置文本内容
        Label(group, text='要输出的内容: ', foreground=color['font'], bg=color['bg']).grid(row=0, column=0, columnspan=2, sticky='w')
        printText = Text(group, width=20, height = 9, bg=color['textBg'])
        printText.grid(row=1, column=0, columnspan = 2, sticky='we')
        self.control['printText'] = printText
        
        # 添加按钮控件
        Button(group, text="添加", foreground=color['font'], width=10, command=lambda:self.addIns('PRINT'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        # 插入按钮控件
        Button(group, text="插入", foreground=color['font'], width=10, command=lambda:self.insertIns('PRINT'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=2, column=1, padx=5, pady=5, sticky='e')
    
    def setWhileLayout(self, group):
        '''
            功能: 循环设置
            group: 容器变量
            返回值: 无
        '''
        
        # 设置循环次数
        Label(group, text="循环次数: ", foreground=color['font'], bg=color['bg']).grid(row=0, column=0, padx = 10, pady=10)
        whileNum = StringVar()
        self.parameters['whileNum'] = whileNum
        Entry(group, textvariable=whileNum, width=10, bg=color['entryBg']).grid(row=0, column=1)
        
        # 设置插入开始按钮
        Button(group, text="开始", foreground=color['font'], width=10, command=lambda:self.insertIns('WHILE'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=1, column=0, padx=5, pady=15, sticky='s')
        # 设置插入结束按钮
        Button(group, text="结束", foreground=color['font'], width=10, command=lambda:self.insertIns('END'), bg=color['btnNormal'], activebackground=color['btnClick']).grid(row=1, column=1, padx=5, pady=15, sticky='s')
    
    def setInsListLayout(self, group):
        '''
            功能: 指令列表布局
            group: 容器变量
            返回值: 无
        '''
        # 上下分割总体布局
        frame1 = Frame(group, bg=color['bg'])
        frame1.pack(side='top', fill='both')
        frame2 = Frame(group, bg=color['bg'])
        frame2.pack(side='top', fill='both')
        frame3 = Frame(group, bg=color['bg'])
        frame3.pack(side='bottom', fill='both')
        # 添加竖和横滑块
        sbx = Scrollbar(frame1, orient=HORIZONTAL)
        sbx.pack(side='bottom', fill='x')
        
        sby = Scrollbar(frame1)
        sby.pack(side='right', fill='y')
        
        # 指令列表控件
        insList = Listbox(frame1, height=30, width=30, yscrollcommand=sby.set, xscrollcommand=sbx.set, bg=color['listBg'])
        insList.pack(side='left', fill='both')

        sby.config(command=insList.yview)
        sbx.config(command=insList.xview)
        self.control['insList'] = insList
        
        # 删除按钮控件
        Button(frame2, text='删除', foreground=color['font'], width=10, command=self.deleteIns, bg=color['btnNormal'], activebackground=color['btnClick']).pack(side='left', anchor='e', padx=5, pady=5)
        # 清空按钮控件
        Button(frame2, text='清空', foreground=color['font'], width=10, command=self.clearIns, bg=color['btnNormal'], activebackground=color['btnClick']).pack(side='right', anchor='w', padx=5, pady=5)
        # 保存按钮控件
        Button(frame3, text='保存', foreground=color['font'], width=10, command=self.saveFile, bg=color['btnNormal'], activebackground=color['btnClick']).pack(side='left', anchor='e', padx=5, pady=5)
        # 导入按钮控件
        Button(frame3, text='导入', foreground=color['font'], width=10, command=self.reloadFile, bg=color['btnNormal'], activebackground=color['btnClick']).pack(side='right', anchor='w', padx=5, pady=5)
        
    def setPosListLayout(self, group):
        '''
            功能: 位置列表布局
            group: 容器变量
            返回值: 无
        '''
        # 上下分割总体布局
        frame1 = Frame(group, bg=color['bg'])
        frame1.pack(side='left', fill='both')
        frame2 = Frame(group, bg=color['bg'])
        frame2.pack(side='right')
        # 添加竖滑块
        sby = Scrollbar(frame1)
        sby.pack(side='right', fill='y')
        
        # 指令列表控件
        posList = Listbox(frame1, height=10, width=50, yscrollcommand=sby.set, bg=color['listBg'])
        posList.pack(side='left', fill='both')

        sby.config(command=posList.yview)
        #sbx.config(command=pList.xview)
        self.control['posList'] = posList
        
        # 移动按钮控件
        Button(frame2, text='移动', foreground=color['font'], width=10, command=self.move, bg=color['btnNormal'], activebackground=color['btnClick']).pack(padx=5, pady=10, ipady=6)
        # 添加按钮控件
        Button(frame2, text='添加', foreground=color['font'], width=10, command=lambda:self.addIns('MOVE2'), bg=color['btnNormal'], activebackground=color['btnClick']).pack(padx=5, pady=10, ipady=6)
        # 清空按钮控件
        Button(frame2, text='清空', foreground=color['font'], width=10, command=self.deletePos, bg=color['btnNormal'], activebackground=color['btnClick']).pack(padx=5, pady=10, ipady=6)
        
    #====================按钮绑定函数==================================================================
    def bindKey(self, btnName):
        '''
            功能: 按键设置按钮绑定函数
            btnName: self.control中的按钮名
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        threading.Thread(target=self.checkKey, args=(btnName, 0)).start()
    
    def addIns(self, insType):
        '''
            功能: 添加指令
            insType:指令类型(KEY, MOVE, PRINT, WHILE, END)
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        insList = self.control['insList']
        
        try:
            # 获取界面输入参数
            instruction = self.getParameters(insType)
            
            if instruction:
                # 获取指令字符串
                insStr = getInsStr(instruction)
                # 把指令放入指令集合中
                self.insSet.append(instruction)
                # 往指令列表中插入信息
                insStr = "["+str(insList.size() + 1)+"] " + insStr
                insList.insert(END, insStr)
                insList.see(END)
                
        except:
            self.error("有不明问题")
            
            
    def insertIns(self, insType):
        '''
            功能: 插入指令
            insType:指令类型(KEY, MOVE, PRINT, WHILE, END)
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        insList = self.control['insList']
        
        try:
            instruction = self.getParameters(insType)
            
            if instruction:
                son = SonDialog()
                son.createInsertDialog("插入", insList, self.insSet, instruction)
        except:
            self.error("有不明问题")
        
    def deleteIns(self):
        '''
            功能: 删除指令列表中指定的指令
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        insList = self.control['insList']
        ind = insList.curselection()
        if ind:
            del self.insSet[ind[0]]
        
        showList(insList, self.insSet)
        
    
    def clearIns(self):
        '''
            功能: 删除指令列表中所有指令
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        insList = self.control['insList']
        insList.delete(0, END)
        self.insSet = []
    
    def updatePos(self):
        '''
            功能: 更新鼠标位置
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        try:
            self.switch_pos = True
            while self.switch_pos:
                if self.switch_pos:
                    x, y = self.ctl.getMousePoint()
                    self.parameters['getPos'].set('(%d,%d)'%(x,y))
                    self.control['groupMove'].update()
        except:
            self.switch_pos = False
            print("一些问题")

            
    def move(self):
        '''
            功能: 移动鼠标
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        
        posList = self.control['posList']
        cur = posList.curselection()
        if cur:
            posStr = posList.get(cur)
            pos = list(map(int, re.findall('\d+', posStr)))
            instruction = {'insType': 'MOVE', 'parameters':pos}
            self.excuteKMPIns(instruction)
        
    
    def deletePos(self):
        '''
            功能: 清空位置
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        posList = self.control['posList']
        posList.delete(0, END)
    
    def startMain(self):
        '''
            功能: 程序启动
            返回值: 无
        '''
        # 让焦点不再在Entry中
        self.setFocus()
        print("==============test==================")
        print(self.insSet)
        print("==============test==================")
        W, E = dealWhile(self.insSet)

        if W and W[0] == -1:
            self.error("循环指令错误!!!")
            return
        
        # 开始按键按下了
        self.clickStart = True
        
        # 如果点击了开始键那么
        startButton = self.control['startButton']
        startButton['relief'] = self.btnState['run']
        startButton['state'] = 'disable'
        
        # 如果点击了开始按钮
        while self.clickStart:
            # 如果检测到强制退出快捷键因热键绑定事件按下
            if self.clickStart == False:
                break
            
            # 如果检测到开始快捷键按下
            if self.switch_start == True:
                self.excuteIns(self.insSet, W, E, 1, 0)
                # 指令执行完毕, 开关关闭
                self.switch_start = False
                self.clickStart = False
        
        # 按钮状态恢复
        startButton['relief'] = self.btnState['normal']
        startButton['state'] = 'normal'
        
    def saveFile(self):
        '''
            功能: 保存指令数据
            返回值:无
        '''
        fileName = filedialog.asksaveasfilename()
        jsobj = json.dumps(self.insSet)
        with open(fileName, 'w') as f:
            f.write(jsobj)
    
    def reloadFile(self):
        '''
            功能: 读取指令数据
            返回值:无
        '''
        try:
            fileName = filedialog.askopenfilename()
            if fileName:
                with open(fileName, 'r') as f:
                    ins = f.read()
                    self.insSet = json.loads(ins)
                print(self.insSet)
                showList(self.control['insList'], self.insSet)
        except:
            self.error("文件数据有问题")
    def mySet(self):
        '''
            功能: 全局设置
            返回值:无
        '''
        self.createSettingDialog()
    
    
        
    #====================功能函数=====================================================
    def setFocus(self):
        '''
            功能: 让焦点移到窗口
            返回值: 无
        '''
        self.root.focus_set()
    
    def createSettingDialog(self):
        '''
            功能: 设置面板按键
        '''
        root = Toplevel()
        root['bg'] = color['bg']
        root.title("设置")
        #root.attributes("-toolwindow", 1)
        root.wm_attributes("-topmost", 1)
        
        frame = Frame(root, bg=color['bg'])
        frame.grid(row=0, column=0, padx = 30, pady = 10)
        
        Label(frame, text='启动键: ', foreground=color['font'], bg=color['bg']).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        startSetButton = Button(frame, text=self.defaultKey['start'], foreground=color['font'], width=10, relief = self.btnState['normal'], command=lambda:self.bindKey('start'), bg=color['btnNormal'], activebackground=color['btnClick'])
        startSetButton.grid(row=0, column=1)
        
        Label(frame, text='停止键: ', foreground=color['font'], bg=color['bg']).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        exitSetButton = Button(frame, text=self.defaultKey['exit'], foreground=color['font'], width=10, relief = self.btnState['normal'], command=lambda:self.bindKey('exit'), bg=color['btnNormal'], activebackground=color['btnClick'])
        exitSetButton.grid(row=1, column=1)
        
        Label(frame, text='捕获位置键: ', foreground=color['font'], bg=color['bg']).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        stopSetButton = Button(frame, text=self.defaultKey['stopPos'], foreground=color['font'], width=10, relief = self.btnState['normal'], command=lambda:self.bindKey('stopPos'), bg=color['btnNormal'], activebackground=color['btnClick'])
        stopSetButton.grid(row=2, column=1)
        
        Label(frame, text='保存位置键: ', foreground=color['font'], bg=color['bg']).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        saveSetButton = Button(frame, text=self.defaultKey['savePos'], foreground=color['font'], width=10, relief = self.btnState['normal'], command=lambda:self.bindKey('savePos'), bg=color['btnNormal'], activebackground=color['btnClick'])
        saveSetButton.grid(row=3, column=1)
        
        self.control['start'] = startSetButton
        self.control['exit'] = exitSetButton
        self.control['stopPos'] = stopSetButton
        self.control['savePos'] = saveSetButton
        
        
        try:
            key = json.dumps(self.defaultKey)
            with open('defaultKey.json', 'w') as f:
                f.write(key)
        except:
            self.error("保存热键有问题")
        
    def checkKey(self, btnName, none):
        '''
            功能: 获取当前按下的按键， 并根据状态改变按钮的外观
            返回值: 无
        '''
        keyButton = self.control[btnName]
        keyButton['relief'] = self.btnState['set']
        
        whileflag = [True]  # 循环flag，True则一直循环
        #threading.Thread(self.ctl.checkPressKey()).start()
        keyName = self.ctl.checkPressKey(whileflag)
        
        keyButton['text'] = keyName
        keyButton['relief'] = self.btnState['normal']
        
        if btnName != 'keyButton':
            self.defaultKey[btnName] = keyName
    
    def bindShortcutKeys(self):
        '''
            功能: 快捷键绑定事件
            返回值: 无
        '''
        try:
            while self.switch_shortcut:
                
                # 程序启动快捷键
                if self.ctl.keyisPress(self.defaultKey["start"]):
                    if self.clickStart == True:
                        # 如果开始键被点了，那么把程序开关打开
                        self.switch_start = True
                        
                # 程序强制退出快捷键     
                if self.ctl.keyisPress(self.defaultKey["exit"]):
                    
                    self.switch_start = False
                    self.clickStart = False
                
                # 位置更新停止快捷键
                if self.ctl.keyisPress(self.defaultKey["stopPos"]):
                    self.switch_pos = False
                    
                # 保存位置
                if self.ctl.keyisPress(self.defaultKey['savePos']):
                    self.savePosToList()
                    time.sleep(0.5)
        except:
            print("线程有问题")
            
            
                
    def excuteKMPIns(self, instruction):
        '''
            功能: 执行一条普通命令(KEY, PRINT, MOVE)
            返回值: 无
        '''
        
        if instruction['insType'] == 'KEY':
            self.ctl.pressKey(*instruction['parameters'])
        elif instruction['insType'] == 'MOVE':
            self.ctl.moveMouse(instruction['parameters'])
        elif instruction['insType'] == 'PRINT':
            self.ctl.printText(instruction['parameters'])
            #time.sleep(1)
        else:
            print("开在开发之中")
    def excuteIns(self, insSet, W, E, num, currentID):
        length = len(insSet)
        for i in range(num):
            cur = 0      
            while cur < length:
                # 如果检测到强制退出快捷键因热键绑定事件按下, 结束
                if self.clickStart == False:
                    return 
                
                instruction = insSet[cur]
                ch = instruction['insType'][0]
                if ch == 'K' or ch == 'M' or ch=='P':
                    # 如果不在嵌套循环内
                    print("当前底下指令", instruction['parameters'][0])
                    self.excuteKMPIns(instruction)
                elif ch == 'W':
                    print("进入嵌套循环", ch)
                    # 如果遇到嵌套循环, 进入递归
                    print('currentID:', currentID)
                    print("cur=", cur)
                    wip = currentID + cur            # while指令在总指令的位置
                    wid = W.index(wip)
                    eip = E[wid]                # 与之对应的End在总指令的位置
                    
                    whileNum = instruction['parameters']
                    subInsSet = self.insSet[wip+1:eip]
                    self.excuteIns(subInsSet, W, E, whileNum, currentID+cur+1)
                    cur = cur + len(subInsSet) + 1
                else:
                    print("是个END")
                    
                cur += 1
        
        print("跳出了循环", length)
    
    def error(self, message="参数错误!!!"):
        '''
            功能：错误提示
            返回值: 无
        '''
        son = SonDialog()
        son.createErrorDialog(message=message)
        print(message)
    
    def getParameters(self, insType):
        '''
            功能: 获取界面上输入的参数
            返回: 指令/ None
        '''
        instruction = None
        try:
            if insType == 'KEY':
                # 如果是按键类型
                num = self.parameters['num'].get()
                interT = self.parameters['interT'].get()
                keyName = self.control['keyButton']['text']
                
                if keyName !='点击输入按键':
                    # 没有问题
                    instruction = {'insType': insType, 'parameters':[keyName, float(interT), int(num)]}
                else:
                    # 参数出现问题
                    sonDialog = SonDialog()
                    sonDialog.createErrorDialog()
            
            elif insType == 'MOVE':
                # 如果是鼠标移动类型
                x = int(self.parameters['posX'].get())
                y = int(self.parameters['posY'].get())
                
                instruction = {'insType':insType, 'parameters':(x, y)}
            elif insType == 'MOVE2':
                posList = self.control['posList']
                cur = posList.curselection()
                posStr = posList.get(cur)
                pos = list(map(int, re.findall('\d+', posStr)))
                instruction = {'insType': 'MOVE', 'parameters':pos}
            elif insType == 'PRINT':
                content = str(self.control['printText'].get("0.0", "end"))
                
                instruction = {'insType':insType, 'parameters':content}
            elif insType == 'WHILE':
                
                whileNum = int(self.parameters['whileNum'].get())
                instruction = {'insType':insType, 'parameters':whileNum}
            else:
                instruction = {'insType':'END', 'parameters':None}
            
            return instruction
        except:
            self.error()
            return None
    
    def savePosToList(self):
        '''
            功能: 通过热键，把当前鼠标的位置存入位置列表中
        '''
        try:
            
            #print(self.defaultKey)
            self.control['posList'].insert(END, self.parameters['getPos'].get())
            self.control['posList'].see(END)
        except:
            print("有点小问题")
            
    #=====================测试====================================
    def run(self):
        '''
            功能: 整体布局，启动界面
            返回值: 无
        '''
        
        threading.Thread(target=self.bindShortcutKeys).start()
        
        # 窗口大小定型
        self.root.resizable(width=False, height=False)
        self.root['bg'] = color['bg']
        #canvas = Canvas(self.root, height=300, width = 300 , bg=color['bg'])
        #image = Image.open('bg.jpg')
        #im = ImageTk.PhotoImage(image)
        
        #canvas.create_image(300,500,image = im)
        #canvas.grid(row=0, column=0)
        # 定义按键管理容器
        groupKey = LabelFrame(self.root, text="按键设置", foreground=color['font'], bg=color['bg'], padx=5, pady=5, font = fonts['labelFrame'])
        groupKey.grid(row=0, column=0, padx=10, pady=10, sticky='ns')
        self.setKeyLayout(groupKey)
        
        # 定义循环管理容器
        groupWhile = LabelFrame(self.root, text="循环设置", foreground=color['font'], bg=color['bg'], padx=5, pady=5, font = fonts['labelFrame'])
        groupWhile.grid(row=0, column=1, padx=10, pady=10, sticky='ns')
        self.setWhileLayout(groupWhile)
        
        
        # 定义鼠标移动管理容器
        groupMove = LabelFrame(self.root, text="移动设置", foreground=color['font'], bg=color['bg'],padx=5, pady=5, font = fonts['labelFrame'])
        groupMove.grid(row=1, column=1, padx=10, pady=10, sticky='ns')
        self.setMoveLayout(groupMove)
        
        # 定义内容输出管理容器
        groupPrint = LabelFrame(self.root, text="输出设置", foreground=color['font'], bg=color['bg'],padx=5, pady=5, font = fonts['labelFrame'])
        groupPrint.grid(row=1, column=0, padx=10, pady=10, sticky='ns')
        self.setPrintLayout(groupPrint)
        
        # 定义位置列表管理容器
        groupPosList = LabelFrame(self.root, text="位置列表", foreground=color['font'],  bg=color['bg'],padx=5, pady=5, font = fonts['labelFrame'])
        groupPosList.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.setPosListLayout(groupPosList)
        
        
        # 定义指令列表管理容器
        groupInsList = LabelFrame(self.root, text="指令列表", foreground=color['font'],  bg=color['bg'],padx=5, pady=5, font = fonts['labelFrame'])
        groupInsList.grid(row=0, column=2, padx=10, pady=10, rowspan=3, sticky='ns')
        self.setInsListLayout(groupInsList)
        
        # 开始按钮
        startButton = Button(self.root, text="开始", foreground=color['font'], height= 3, width=30, command=lambda:threading.Thread(target=self.startMain).start(), bg=color['btnNormal'], activebackground=color['btnClick'], font = fonts['rootBtn'])
        startButton.grid(row=3, column=0, padx=25, pady=10)
        # 设置按钮
        Button(self.root, text="设置", foreground=color['font'], height=3, width=30, command=self.mySet, bg=color['btnNormal'], activebackground=color['btnClick'], font = fonts['rootBtn']).grid(row=3, column=2, padx=25, pady=10)
        
        self.control['startButton'] = startButton
        self.control['groupMove'] = groupMove

        self.root.mainloop()
        
if __name__ == '__main__':
    kzgui = KZGUI('老梦的控3.0版本')
    kzgui.run()
        
        
        
