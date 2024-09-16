from PySide6 import QtGui


def df_to_tableView(self, input_df, input_tableView):
    # df 정리
    df = input_df[['ID','label']].copy()
    df = df.drop_duplicates()
    columns = df.columns
    # tableView 정의
    tableView = input_tableView
    # 모델 초기화를 데터 추가 전에 수행
    qmodel_ = QtGui.QStandardItemModel()
    qmodel_.setColumnCount(len(columns))
    qmodel_.setHorizontalHeaderLabels(columns)
    for row in range(len(df)):
        value_objs = [QtGui.QStandardItem(str(value)) for value in df.iloc[row]]
        qmodel_.appendRow(value_objs)
    tableView.setModel(qmodel_)
    self.update()