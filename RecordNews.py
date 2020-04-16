import numpy as np
import queue
import time
import soundfile as sf
import sounddevice as sd

sd.default.device = 0
_FS = 16000
_CHANNELS = 1

q = queue.Queue()
link = ''
records = []

def createRecord(filename, data, text):
    records.append([filename, data, text])
    
def saveRecord(nameRec):
    fname = 'record_data_' + nameRec
    f = open(fname, 'w', encoding='utf-8')
    resultData = []
    resultData.append(link)
    
    for rec in records:
        sf.write(rec[0],rec[1],_FS) # rec[0]: tên file , rec[1]: dữ liệu
        resultData.append(str(rec[0])) # rec[0]: tên file
        resultData.append(str(rec[2])) # rec[2]: đoạn báo
    f.write('\n'.join(resultData))
    f.close()
    print('Lưu dữ liệu thành công!')
    
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())

def recordstream(text):
    try:
        data = []
        with sd.InputStream(samplerate=_FS,
                       channels=_CHANNELS,
                       callback=audio_callback) as stream:
            print('Đang ghi âm . . .')
            print('Nhấn Ctr + C để dừng ghi âm')
            while True:                    
                data = np.append(data, q.get())
            
    except KeyboardInterrupt:
       print('Dừng ghi âm!')
       filename = input('Đặt tên cho bản ghi: ')
       createRecord(filename + '.wav',data, text)
       #sf.write(filename + '.wav', data, _FS)
       print('Lưu thành công!')

def readDataFile(file):
    #   >>>>>>> file format <<<<<<<
    #   line 1: link bài báo
    #   line 2, .. : các dữ liệu bài báo
    f = open(file,'r', encoding='utf-8')
    link = f.readline()[:-1]
    contents = f.read().split('\n')
    
    return link, contents

def showText(text):
    print('\t' + text)
  
def main(filename):
    globals()['link'], contents = readDataFile(filename)
    print('Đọc dữ liệu thành công!\n')
    cin = input('Bắt đầu ghi âm? [Y/N]: ')
    if (cin.lower()=='y'):
        globals()['record'] = []
        globals()['q'].queue.clear()
        for text in contents:
            print('-- ' + str(contents.index(text)) + ' --')
            showText(text)
            if (input('Ghi âm câu này?[Y/N]: ').lower()=='y'):
                recordstream(text)
            if (input('Ghi âm câu tiếp theo?[Y/N]:').lower()=='n'):
                break;
        print('Kết thúc!!!!!!!!!')
        saveRecord(filename)
    else: 
        return
    
def program(filename):
    globals()['record'] = []
    globals()['q'].queue.clear()
    while True:
      main(filename)
      off = input('Bạn muốn tắt chương trình? [Y/N]: ')
      if (off.lower()=='y'):
          break