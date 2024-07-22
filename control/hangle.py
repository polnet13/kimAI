import win32com.client as win32
import os
print('한글 모듈 임포트')
class HWP:
    '''
    get_fields() -> list of 누름틀 반환(누름틀 이름이 같으면 중복값이 입력됨)
    write_fields(field_name, input_text) -> 누름틀에 입력함
    to_hwp() -> output 파일 생성
    quit() -> 자원해제를 해줘야 함
    '''
    def __init__(self, file_path):

        # 한글 파일 열기
        self.hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    
        # 보안모듈은 보안성 확인후 도입예정, 그 전까지는 이미지 인식으로 자동 입력으로 해결할 예정임
        # hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")

        # 소스 문서 오픈
        self._file = os.path.abspath(file_path)
        self._c_dir = os.path.dirname(self._file)
        self.src_file = os.path.join(self._c_dir, 'rsc', '예제.hwp')
        self.out_path = os.path.join(self._c_dir, 'out', '예제_out.hwp')

        # 한글파일 오픈
        self.hwp.Open(self.src_file,"HWP","forceopen:true")
        
    # 누름틀 찾기
    def get_fields(self):
        '''
        Number=0 기본값으로 되어 있고,
        '\x02' 문자열을 기준으로 스플릿하여 리스트로 반환함
        '''
        self.__fields = self.hwp.GetFieldList(Number=0).split('\x02')
        print(self.__fields)
        return self.__fields

    # 누름틀에 입력
    def write_fields(self, DataFrame_row):
        '''
        DataFrame_row: df의 한 행
        field_names -> df의 한 행에 대한 인덱스 값이(df의 컬럼값) 담겨 있음
        '''
        field_names = DataFrame_row.index
        for field_name in field_names:
            input_text = DataFrame_row[field_name]
            self.hwp.PutFieldText(field_name, input_text)
        return self

    # 파일 다른 이름으로 저장
    def to_hwp(self, add_str='out'):
        '''
        var add_str
          아웃풋 파일의 어두에 붙일 str
          입력하지 않을 경우 out이 붙음
        '''
        out_dir = os.path.join(self._c_dir, 'out')
        out_path = os.path.join(self._c_dir, 'out', f'{add_str}_예제.hwp')
        if not os.path.exists(out_dir):
            print('out 폴더가 없어서 생성함')
            os.makedirs(out_dir)
        self.hwp.SaveAs(out_path)

    # 파일 닫기
    def quit(self):
        self.hwp.Quit()
        print('자원 반환: ')

 
