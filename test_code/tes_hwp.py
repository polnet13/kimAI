import pandas as pd
import win32com.client as win32


df = pd.DataFrame({'a':['김밥','2','3','4','5'], 'b':[2,'라면',4,5,6], 'c':[3,3,3,3,3], 'd':[4,5,6,7,8], 'e':[5,6,7,8,9]})


hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.XHwpWindows.Active_XHwpWindow.Visible = True  # 한글 프로그램 보이는 상태에서 편집

hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  
hwp.HParameterSet.HTableCreation.Rows = df.shape[0]  # 행
hwp.HParameterSet.HTableCreation.Cols = df.shape[1]  # 열
# hwp.HParameterSet.HTableCreation.WidthType = 2  # 폭 타입2: 절대값
# hwp.HParameterSet.HTableCreation.HeightType = 1  # 높이 타입1: 절대값
# hwp.HParameterSet.HTableCreation.CreateItemArray("RowHeight", 2)   # 높이 값 2개 생성
# hwp.HParameterSet.HTableCreation.RowHeight.SetItem(0, hwp.MiliToHwpUnit(10))  # 첫번째 높이
# hwp.HParameterSet.HTableCreation.RowHeight.SetItem(1, hwp.MiliToHwpUnit(20))  # 두 번째 높이
# hwp.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 4)    # 폭 값 4개 생성
# hwp.HParameterSet.HTableCreation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(10))   # 첫번째 폭
# hwp.HParameterSet.HTableCreation.ColWidth.SetItem(1, hwp.MiliToHwpUnit(20))   # 두 번째 폭
# hwp.HParameterSet.HTableCreation.ColWidth.SetItem(2, hwp.MiliToHwpUnit(30))   # 세 번째 폭
# hwp.HParameterSet.HTableCreation.ColWidth.SetItem(3, hwp.MiliToHwpUnit(40))   # 네 번째 폭
hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1   # 표를 글자처럼 취급
hwp.HAction.Execute("TableCreate", hwp.HParameterSet.HTableCreation.HSet)

pset = hwp.HParameterSet.HInsertText

def insert_text(text):
    '''
    text 입력 후 다음 셀로 이동
    '''
    hwp.HParameterSet.HInsertText.Text = text
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HAction.Execute("TableRightCell", pset.HSet)

print(df)
print(df.shape)
print(df.transpose())

df = df.transpose()
for col in df.columns:
    for row in df[col]:
        insert_text(str(row))


# 데이터 프레임을 트랜스 포즈 하면 행과 열이 바뀜
# 열을 순서대로 표에 입력하면 됨
