import win32api
import win32gui
import win32con
import win32clipboard
import time
import keyDict


class Control:
    def __init__(self):
        self.KEY = keyDict.getDict()
        print(self.KEY)
    #===================按键功能=================================
    def pressKey(self, keyName, interT, num):
        '''
            功能: 按键响应函数
            keyName:按键名,按键点击次数
            interT:按键每次按下的停顿时间
            num:按键响应次数
            返回值: 无
        '''
        keyName = keyName   # 按键名大写化
        keyId = int(self.KEY[keyName])        # 获取按键名的键码
        # 按键次数迭代
        for i in range(num):
            win32api.keybd_event(keyId, 0, 0, 0)    # 按下按键
            time.sleep(interT)                      # 停顿
            # 松开按键
            win32api.keybd_event(keyId, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    def keyisPress(self, keyName):
        if win32api.GetAsyncKeyState(int(self.KEY[keyName])) & 0x8000:
            return True
        return False
            
    def checkPressKey(self, flag):
        '''
            功能: 检测当前是否有一个按键按下
            返回值：按键名/空
        '''
        while flag[0]:
            for key in self.KEY.keys():
                if win32api.GetAsyncKeyState(int(self.KEY[key])) & 0x8000:
                    flag[0] = False
                    return key
    
    #====================鼠标功能=================================
    def getMousePoint(self):
        '''
            功能: 获取鼠标当前位置
            返回值: (x, y)
        '''
        pos = win32api.GetCursorPos()
        return int(pos[0]), int(pos[1])
    
    def moveMouse(self, pos):
        '''
            功能: 控制鼠标
            pos: 移动到某位置
            返回值：无
        '''
        # 设置活跃窗口，程序管理器窗口。以防窗口切换时，SetCursorPos方法出问题
        hwnd = win32gui.FindWindow('Program', 'Program Manager')
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        # 移动鼠标
        if pos[0] is not None and pos[1] is not None:
            win32api.SetCursorPos(pos)
    
    def controlMouse(self, pos, stopTime, clickName, clickTime, clickNum):
        '''
            功能: 控制鼠标
            pos: 移动到某位置
            stopTime: 鼠标停留时间
            clickName: 鼠标操作名：左键，右键，无
            clickTime: 点击停顿时间
            clickNum: 点击次数
            返回值: 无
        '''
        # 设置活跃窗口，程序管理器窗口。以防窗口切换时，SetCursorPos方法出问题
        hwnd = win32gui.FindWindow('Program', 'Program Manager')
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        
        # 移动鼠标
        if pos[0] is not None and pos[1] is not None:
            win32api.SetCursorPos(pos)
        
        clickName = clickName # 键名大写化
        # 判断是否点击 且 点击左右， 若点击，则迭代点击操作
        if clickName != '无':        # 如果要点击鼠标
            if clickName == '左键':
                clickDown = win32con.MOUSEEVENTF_LEFTDOWN
                clickUp = win32con.MOUSEEVENTF_LEFTUP
            else:
                clickDown = win32con.MOUSEEVENTF_RIGHTDOWN
                clickUp = win32con.MOUSEEVENTF_RIGHTUP
            
            # 迭代执行鼠标操作
            for i in range(clickNum):
                win32api.mouse_event(clickDown, 0, 0, 0)
                time.sleep(clickTime)
                win32api.mouse_event(clickUp, 0, 0, 0)
        
        time.sleep(stopTime)    # 停留一段时间
    
    #======================文本输入============================
    def printText(self, text):
        '''
            功能: 输出文本
            text: 文本内容
        '''
        # 保存到复制板中
        win32clipboard.OpenClipboard(None) # 打开剪切板
        win32clipboard.EmptyClipboard() # 清空剪切板
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT,text) #向剪贴板中写入信息
        win32clipboard.CloseClipboard() #关闭剪贴板
        # 模拟按键粘贴
        # Ctrl+V
        win32api.keybd_event(17, 0, 0, 0)   # 按下按键Ctrl
        win32api.keybd_event(86, 0, 0, 0)   # 按下按键V
        time.sleep(0.3)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放Ctrl
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放V
        
        time.sleep(0.3)
        
    #========================测试==============================
    def test(self):
        time.sleep(1)
        self.printText("成功")
    

if __name__ == '__main__':
    ctl = Control()
    ctl.test()
        