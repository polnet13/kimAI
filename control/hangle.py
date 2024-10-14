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

    def make_table(self, rows, cols):
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