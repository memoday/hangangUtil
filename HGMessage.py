from openpyxl import Workbook, load_workbook
import time
import os
import openpyxl
import sys

today = time.strftime('%Y.%m.%d.') 
hours = int(time.strftime('%H'))
read_xlsx = load_workbook(r'source.xlsx')
sheet = read_xlsx.get_sheet_by_name("internet")
sheet2 = read_xlsx.get_sheet_by_name("paper")
settings = read_xlsx.get_sheet_by_name("settings")
settings_time = settings.cell(row=1, column=2) #시간(시) 설정 column

news_number = 1

#보도시간 자동설정, 오전 11시이전 실행시 09시
if hours <= 11:
   settings_time.value = "09"
else :
   settings_time.value = '17' 
report_time = str(settings['B1'].value)

#신문/방송 뉴스 정리
def sortPaper ():
    paper = sheet2['A']
    paperName = sheet2
    sorting(paper, paperName)
    
#인터넷 뉴스 정리
def sortInternet ():
    internet = sheet['A']
    internetName = sheet
    sorting(internet, internetName)

def sorting(sheetCol, sheetName):
    global news_number
    names1 = []
    names = []
    internet = []
    for cell in sheetCol:
      if cell.value != None: #NoneType값은 append에서 제외됨
        names.append(cell.value) 
    i = 1
    for i in range(len(names)):
        i = i+1
        row = sheetName[i]
        for cell in row:
            if cell.value != None: #NoneType값은 append에서 제외됨
                names1.append(cell.value) #행 데이터 names1에 저장
        internet.append(str(names1[2]+'('+names1[1]+'_'+names1[3]+')\n'+names1[4]+'\n'))
        names1 = []
        print(str(news_number)+'.'+internet[i-1])
        news_number = news_number + 1
        
if __name__ == "__main__":
    sys.stdout = open('temp.txt','w') #결과값 txt파일로 내보내기
    print("금일("+today+") "+report_time+"시까지 한강관련주요 보도사항입니다.")
    print("\n[신문/방송]")
    sortPaper()
    print("[인터넷]")
    sortInternet()
    print("\n-문화홍보과-")
    os.startfile('temp.txt')
