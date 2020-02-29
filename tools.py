import re
from tkinter import END


color = {'bg':'#424242',
         'showPosBg':'#4F4F4F',
         'showFont':'#FFFFFF',
         'btnNormal':'#3C3C3C',
         'btnClick':'#282828',
         'font':'#FFFFFF',
         'entryBg':'#FAFAFA',
         'textBg':'#FAFAFA',
         'listBg':'#FAFAFA',
         'keyFont':'#ffff00'}
         
fonts = {'labelFrame':("隶书", 15, "bold"),
         'rootBtn':("黑体", 10, "bold"),
         'keyBtn':("Verdana", 9, 'bold')}

def checkInt(*strings):
    '''
        功能: 检测字符串是否为整数
        返回: True(为整数) / False(不为整数)
    '''
    for string in strings:
        if string.isdigit() == False:
            return False
    return True

def checkNum(*strings):
    '''
        功能: 检测字符串是否为小数
        返回: True(为整数) / False(不为整数)
    '''
    for string in strings:
        #print(string in re.findall('\d+\.\d+', string))
        #print(string.isdigit())
        if string.isdigit() == False:
            # 非整数
            if (string in re.findall('\d+\.\d+', string)) == False:
                return False
        
    return True

def getInsStr(instruction):
    '''
        功能: 将字典指令转化为字符串指令格式
        返回: 字符串 / None
    '''
    insType = instruction['insType']
    parameters = instruction['parameters']
    if insType == 'KEY':
        keyName, interT, num = parameters
        return "按键 ==> <" + keyName + ">  " + str(interT) + "s    " + str(num) + "次"
    elif insType == 'MOVE':
        pos = parameters
        return "移至 ==> ("+ str(pos[0]) + ", " + str(pos[1]) + ")"
    elif insType == 'PRINT':
        content = parameters
        return "打印 ==> " + content
    elif insType == 'WHILE':
        whileNum = parameters
        return "WHILE   " + str(whileNum) + "次"
    else:
        return "END"
    return None

def clearList(pList):
    '''
        功能: 清空列表
        返回值:无
    '''
    pList.delete(0, END)
    
def showList(pList, insSet):
    '''
        功能: 重新将指令集合显示在指令列表中
        返回值: 无
    '''
    # 清空弹窗
    clearList(pList)
    
    # 开始迭代插入列表
    for ins in insSet:
        insStr = getInsStr(ins)
        insStr = "["+str(pList.size() + 1)+"] " + insStr
        pList.insert(END, insStr)
        

def dealWhile(insSet):
    '''
        功能: 处理循环，获取while与之对应的End
        返回值: while地址列表和end地址列表 / 或者[-1][-1]代表错误 
    '''
    stack = []
    W = []                      # 由于W插入数值是顺序的，而E插入数值是乱序的，所有初始化E就行
    E = [0 for x in insSet]
    cur = -1
    
    for i in range(len(insSet)):
        ch = insSet[i]['insType'][0]
        if ch == 'W':
            cur += 1
            stack.append(cur)
            W.append(i)
        if ch == 'E':
            if len(stack) > 0:
                E[stack.pop()] = i
    
    if len(stack) > 0:
        W = [-1]
        E = [-1]
    
    print('W:', W)
    print('E:', E)
    return (W, E)

            
    
    