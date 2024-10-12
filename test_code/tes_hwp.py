import pandas as pd
import win32com.client as win32
import os, datetime


class Hwp:
    def __init__(self, file=None):  
        self.hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        # self.hwp.XHwpWindows.Active_XHwpWindow.Visible = True  # 한글 프로그램 보이는 상태에서 편집
        if file:
            self.hwp.Open(file, "HWP", "forceopen:true")
        if file == None:
            pass
 

    def display(self, bool):
        if bool:
            self.hwp.XHwpWindows.Active_XHwpWindow.Visible = True
        else:
            self.hwp.XHwpWindows.Active_XHwpWindow.Visible = False

    def dic_to_field(self, dict):
        for key, value in dict.items():
            self.hwp.PutFieldText(key, value)

    def create_table(self, rows, cols):
        self.hwp.HAction.GetDefault("TableCreate", self.hwp.HParameterSet.HTableCreation.HSet)
        self.hwp.HParameterSet.HTableCreation.Rows = rows  # 행
        self.hwp.HParameterSet.HTableCreation.Cols = cols  # 열
        self.hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1   # 표를 글자처럼 취급
        self.hwp.HAction.Execute("TableCreate", self.hwp.HParameterSet.HTableCreation.HSet)

    def insert_text(self, text):
        pset = self.hwp.HParameterSet.HInsertText
        self.hwp.HParameterSet.HInsertText.Text = text
        self.hwp.HAction.Execute("InsertText", self.hwp.HParameterSet.HInsertText.HSet)
        self.hwp.HAction.Execute("TableRightCell", pset.HSet)

    def insert_df(self, df):
        df = df.transpose()
        for col in df.columns:
            for row in df[col]:
                self.insert_text(str(row))

    def save(self, path, name):
        '''원본은 유지 하기 위해 다른이름으로 저장함'''
        path = r'C:\Users\prude\OneDrive\바탕 화면'
        name = 'test_out.hwp'
        save_path = os.path.join(path, name)
        self.hwp.SaveAs(save_path)
        self.hwp.Clear(option=1)   # 1: 문서의 내용을 버린다(계속 써야 하므로)

    def quit(self):
        self.hwp.Quit()



 
hwp = Hwp(file=r"C:\Users\prude\OneDrive\바탕 화면\src")
hwp.create_table(5, 5)
# hwp = Hwp()
weeks = ['월', '화', '수', '목', '금', '토', '일']
td = datetime.datetime.now().strftime('%y. %m. %d')
week = weeks[datetime.datetime.now().weekday()]
name = '김장희'
dic = {'date':td, 'week':week, 'name':name}
hwp.dic_to_field(dic)
hwp.save(0,0)
 

# df = pd.DataFrame({'a':['김밥','2','3','4','5'], 'b':[2,'라면',4,5,6], 'c':[3,3,3,3,3], 'd':[4,5,6,7,8], 'e':[5,6,7,8,9]})
# print(df)
# print(df.shape)
# print(df.transpose())

# hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  
# hwp.HParameterSet.HTableCreation.Rows = df.shape[0]  # 행
# hwp.HParameterSet.HTableCreation.Cols = df.shape[1]  # 열
# # hwp.HParameterSet.HTableCreation.WidthType = 2  # 폭 타입2: 절대값
# # hwp.HParameterSet.HTableCreation.HeightType = 1  # 높이 타입1: 절대값
# # hwp.HParameterSet.HTableCreation.CreateItemArray("RowHeight", 2)   # 높이 값 2개 생성
# # hwp.HParameterSet.HTableCreation.RowHeight.SetItem(0, hwp.MiliToHwpUnit(10))  # 첫번째 높이
# # hwp.HParameterSet.HTableCreation.RowHeight.SetItem(1, hwp.MiliToHwpUnit(20))  # 두 번째 높이
# # hwp.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 4)    # 폭 값 4개 생성
# # hwp.HParameterSet.HTableCreation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(10))   # 첫번째 폭
# # hwp.HParameterSet.HTableCreation.ColWidth.SetItem(1, hwp.MiliToHwpUnit(20))   # 두 번째 폭
# # hwp.HParameterSet.HTableCreation.ColWidth.SetItem(2, hwp.MiliToHwpUnit(30))   # 세 번째 폭
# # hwp.HParameterSet.HTableCreation.ColWidth.SetItem(3, hwp.MiliToHwpUnit(40))   # 네 번째 폭
# hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1   # 표를 글자처럼 취급
# hwp.HAction.Execute("TableCreate", hwp.HParameterSet.HTableCreation.HSet)


 



 