




import os 

wd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
deletes_dir = ['build', 'dist']
deletes_dir = [ os.path.join(wd, item, 'main') for item in deletes_dir]


# 디렉토리 삭제
os.chdir(wd)
try: 
    for item in deletes_dir:
        if os.path.isdir(item):
            os.system(f'rmdir /s /q {item}')
            print(f'{item} 삭제 완료')
        else:
            print(f'{item} 없음') 
except Exception as e:
    print(e)