import os, sys
import pandas as pd
#from ui_mainwindow import UI_MainWindow
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from mainwindow import Ui_Form


import time, datetime, timedelta
import pyautogui
import keyboard

from resources_rc import qt_resource_data


class Window(QWidget):
    
    
    ## 초기화
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.df1 = None     # 사건검색리스트 파일 -> df
        self.df2 = None     # 출동수당 파일 -> df
        self.result = None

    
    ## 사건검색리스트 엑셀 파일 등록
    def file_up_112(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '사건검색리스트 엑셀파일', os.getcwd(), 'All files (*)')
        if file_path:
            try:
                df = pd.read_excel(
                    file_path,
                    sheet_name='List', 
                    usecols='A:AJ',
                    header=0,
                    )
                file_name = os.path.basename(file_path)
                self.ui.textBrowser.append(f'엑셀파일(사건검색리스트) <br>=>{file_name}<br><br>')
                self.df1 = df
            except Exception as e:
                self.ui.textBrowser.append(f'오류 <br>=>{e}<br>')
                QMessageBox.critical(self, "Error", str(e))
                return


    ## 엑셀등록(이미 등록된 리스트) => df2 생성
    def file_up_enrolled(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '출동수당 등록 엑셀파일', os.getcwd(), 'All files (*)')
        if file_path: 
            try:
                df = pd.read_excel(
                    file_path, 
                    sheet_name='sheet_1', 
                    usecols='A:J',
                    header=1,
                    )
                file_name = os.path.basename(file_path)
                self.ui.textBrowser.append(f'엑셀파일(등록된 출동수당) <br>=>{file_name}<br><br>')
                self.df2 = df
            except Exception as e:
                self.ui.textBrowser.append(f'오류 <br>=>{e}<br>')
                QMessageBox.critical(self, "Error", str(e))
                return

    
    ## 엑셀 파일 정리
    def execute(self):
        try:
            name = self.ui.lineEdit_name.text()  # 라인에딧으로 입력 받은 이름을 name 변수에 저장
            df1 = self.df1   
            df2 = self.df2
            
            # df1: 112접수시간 datetime 형식으로 변경하여 '신고time' 변수에 저장
            print('df1: 112접수시간 datetime 형식으로 변경')
            df1['접수시간'] = pd.to_datetime(df1['접수시간'], format='%H:%M:%S')
            df1['신고time'] = df1['접수시간'].dt.time
            
            
            # df1에서 남길 열 정리
            print('df1에서 남길 열 정리')
            df1 = df1[['접수번호','신고내용','종결내용','종결보고자','사건번호','지령시간','신고time','코드','종결']]  # 지령시간은 외부코드에서 +5분하기 위해 사용
            
            # 종결 코드 동일건 제외
            print('동일건 제외')
            if self.ui.checkBox_1.isChecked():
                df1 = df1[ df1['종결']!='동일']
                
                
            # FTX 제외 
            print('FTX 제외 구현')
            if self.ui.checkBox_2.isChecked():
                df1 = df1[ df1['종결']!='FTX']


            # 신고내용에 '동일건' 제외 
            print('신고내용에 동일건 있는 경우 제외')
            if self.ui.checkBox_3.isChecked():
                df1 = df1[df1['종결보고자'].str.contains(name) == False]
                
            
            #조건1: 코드0,1 이름 필터링 
            print('조건1: 코드0,1 이름 필터링 ')
            df1_1 = df1[df1['코드'].isin(['C0','C1']) & df1['종결보고자'].str.contains(name)]
            df1_1.reset_index(inplace=True, drop=True)
            
            #조건2: 코드2 중에서 21:50 - 06:00
            print('조건2: 코드2 중에서 21:50 - 06:00 ')
            df1_2 = df1[ (df1['코드']=='C2') & (df1['종결보고자'].str.contains(name))]
            print('조건2: 코드2 중에서 21:50 - 06:00 중에서 종결보고자 포함된 것 필터링')
            df1_2 = df1_2[ (df1_2['신고time'] >= pd.to_datetime('21:50', format='%H:%M').time())|(df1_2['신고time'] <= pd.to_datetime('06:00', format='%H:%M').time())]
            print('조건2: 코드2 중에서 21:50 - 06:00 : 접수시간(신고time)이 21:50보다 크거나 같음 or 접수시간(신고time)이 06:00보다 작은것')
            df1_2.reset_index(drop=True, inplace=True)
            
            #조건1, 조건2 결합
            print('조건1, 조건2 결합')
            result = pd.concat([df1_1, df1_2])
            
            # df2: 이미 등록된 출동수당 리스트로 만들기
            print('df2: 이미 등록된 출동수당 리스트로 만들기')
            df2_list = df2['접수 번호'].tolist()
            
            # 출동수당 정리한거에서 이미 등록된 출동수당
            print('출동수당 정리한거에서 이미 등록된 출동수당')
            result = result.drop(result[result['접수번호'].isin(df2_list)].index)
            self.make_table_view(result)
            self.result = result 
     
        except Exception as e:
            self.ui.textBrowser.append(f'오류: {e}')
            QMessageBox.critical(self, "Error", str(e))
            return
    
    
    ## 외부 코드 실행
    def auto_register(self):
        try:
            print(self.result)
            print('-------auto_register 실행---------')
            print(f'작업 위치: {os.getcwd()}')
            txt = os.path.join(os.getcwd(), 'module', 'external_code.py')
            
            with open(txt, 'r', encoding='utf-8-sig') as f:
                external_code = f.read()

            exec(external_code, globals())

            # 외부 코드 실행
            print('외부코드 실행 시작')
            if self.result is None:
                print(f'self.result 값이 없음')
                self.ui.textBrowser.append(f'self.result 값이 없음')
            else:
                ex_code(self.result)
                print('외부코드 실행 끝')
                
        except Exception as e:
            print(e)
            self.ui.textBrowser.append(f'오류 <br>=>{e}<br>')
 

    ## tableView 생성
    def make_table_view(self, df):
        table_view = self.ui.tableView
        # standard item model 생성
        model = QStandardItemModel()
        # 컬럼 헤더 생성
        model.setHorizontalHeaderLabels(df.columns)
        # 데이터를 모델로 치환
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, column]))
                model.setItem(row, column, item)
        # tableView 에 모델 집어 넣기
        table_view.setModel(model)


    ## 선택된 행을 삭제합니다.
    def delete_row(self):
        selected_row = self.ui.tableView.currentIndex()
        index = selected_row.row()
        self.ui.tableView.model().removeRow(index)
        self.ui.textBrowser.append(f'{index+1}행 삭제')
        # 테이블뷰에 보이는 테이블을 데이터 프레임으로 만듭니다.
        self.result = pd.DataFrame([[self.ui.tableView.model().index(row, col).data() for col in range(self.ui.tableView.model().columnCount())] for row in range(self.ui.tableView.model().rowCount())])

        self.result.columns = ['접수번호','신고내용','종결내용','종결보고자','사건번호','지령시간','신고time','코드','종결']

        


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec()) 