def writeKeyName(fileName='KeyName.txt'):
    with open(fileName, 'w') as f:
        # 写入鼠标键
        mouseName = ('左键', '右键', '中键')
        for i in mouseName:
            f.write(i+'\n')
        # 写入字符键
        for i in range(65, 91):
            ch = chr(i)
            f.write(ch+'\n')
        # 写入数字键
        for i in range(48, 58):
            ch = chr(i)
            f.write(ch+'\n')
    
        # 写入数字盘上的数字键
        for i in range(0, 10):
            ch = 'n_'+str(i)
            f.write(ch+'\n')
            
        for i in ('*', '+', 'Enter', '-', '.', '/'):
            ch = 'n_'+i
            f.write(ch+'\n')
            
        # 写入功能按键
        for i in range(1, 13):
            ch = 'F' + str(i)
            f.write(ch+'\n')
            
        # 写入控制按键的键码
        keyName = ('BackSpace', 'Tab', 'Clear', 'Enter', 'Shift', 
                   'Control', 'Alt', 'CapeLock', 'Esc', 'Spacebar', 
                   'Page Up', 'Page Down', 'End', 'Home', 'Left Arrow',
                   'Up Arrow', 'Right Arrow', 'Down Arrow', 'Insert', 'Delete',
                   'Num Lock', ';:', '=+', ',<', '-_', '.>', '/?', '`~', 
                   '[{', '\|', '}]', ''' '" ''', 'win')
        for i in keyName:
            f.write(i+'\n')
            
        # 写入多媒体按键
        keyName2 = ('加音量', '减音量', '静音')
        for i in keyName2:
            f.write(i+'\n')
            
def writeKeyId(fileName='KeyId.txt'):
    with open(fileName, 'w') as f:
        # 写入鼠标键
        mouseName = (1, 2, 4)
        for i in mouseName:
            f.write(str(i)+'\n')
       # 写入字符键
        for i in range(65, 91):
            ch = str(i)
            f.write(ch+'\n')
        # 写入数字键
        for i in range(48, 58):
            ch = str(i)
            f.write(ch+'\n')
    
        # 写入数字盘上的数字键写入功能按键
        for i in range(96, 124):
            ch = str(i)
            f.write(ch+'\n')
            
            
        # 写入控制按键的键码
        keyName = (8, 9, 12, 13, 16, 17, 18, 20, 27, 32, 33, 34, 35,
                   36, 37, 38, 39, 40, 45, 46, 144, 186, 187, 188, 189,
                   190, 191, 192, 219, 220, 221, 222, 91)
        
        for i in keyName:
            f.write(str(i)+'\n')
            
        # 写入多媒体按键
        keyName2 = (175, 174, 173)
        for i in keyName2:
            f.write(str(i)+'\n')
        
writeKeyName()
writeKeyId()
