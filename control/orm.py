from apps.model_setting.models import ConfigModel, TubeModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
from django.core import serializers

__all__ = ['df_to_qmodel','df_to_tableview','get_selected_rows']
'''
df_to_qmodel(df)
df_to_tableview(df, self.tableView)
get_selected_rows(self.tableView)
'''
##################################################
## 테이블 관련
##################################################
def get_selected_row(self):
    row = self.tableView.selectionModel().selectedRows()[0]
    return row

def get_selected_pk(tableView):
    '''
    table.get_selected_rows(self.tableView) -> 선택된 행의 0열 값(pk==id)을 가지고 옴
    '''
    selected_indexes = tableView.selectedIndexes()
    selected_rows = set(index.row() for index in selected_indexes)
    pk = []
    for row in selected_rows:
      name = tableView.model().data(tableView.model().index(row, 0)) # 선택된 행의 0열 값을 가지고 옴
      pk.append(name)
    return pk

def reset_tableview(tableview):
    queryset = TubeModel.objects.all()
    queryset_to_tableview(queryset, tableview)
    
def queryset_to_df(queryset) -> pd.DataFrame:
    df = pd.DataFrame(list(queryset.values()))
    return df

def queryset_to_tableview(queryset, tableView) -> pd.DataFrame:
    df = pd.DataFrame(list(queryset.values()))
    model = df_to_qmodel(df)
    tableView.setModel(model)

def df_to_tableview(df, tableView):
    '''
    데이터 프레임과 df를 넣어줄 테이블을 인자로 입력
    table.df_to_tableview(df, self.tableView)
    '''
    model = df_to_qmodel(df)
    tableView.setModel(model)



def df_to_qmodel(df):
    '''
    df을 인자로 받고 QStandardItemModel 객체로 반환함
    '''
    if df is not None:
        model = QStandardItemModel()
        # 컬럼 헤더 생성
        model.setHorizontalHeaderLabels(df.columns)
        # 데이터를 모델로 치환
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, column]))
                model.setItem(row, column, item)
    else:
        model = QStandardItemModel()
    return model



################################################################
##  유튜브 관련
################################################################
def get_video_title(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
    return video_title


# 데이터 입력
def create_tube(url, tableview):
    '''
    유튜브 서버와 통신해서 제목을 가지고 옴
    '''
    try:
        title = get_video_title(url)
        data = TubeModel(title=title, url=url)
        data.save()
        text = f'{title}, {url} 저장완료'
    except:
        text = 'views.orm.inputdata 오류 발생'
    finally:
        reset_tableview(tableview)
        return text


################################################################
##  모델 컨트롤
################################################################
def getAll():
    return TubeModel.objects.all()
    
# 전체 데이터 삭제
def delete_all(tableview):
    TubeModel.objects.all().delete()
    reset_tableview(tableview)
    
def delete_rows(rows, tableview):
    '''
    list[id] -> 삭제 -> tableview갱신
    '''
    try:
        del_nums = rows
        TubeModel.objects.filter(id__in= del_nums).delete()
    except TubeModel.DoesNotExist:
        print("없는 데이터 삭제를 요청하여 아무런 작업을 하지 않았음")
    finally:
        reset_tableview(tableview)
        
