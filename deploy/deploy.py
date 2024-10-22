import os 
#############
# 옵션 설정 #
#############
onefile = False
console = True
# 제외할 파일과 폴더를 지정
excludes = ['영상자료', '__pycache__', '.vscode', 'build', 'dist', 'test_widget']
hidden_imports = [
    "torch.jit",
    "scipy.special",
]

#######################
# 생성된 exe 파일 삭제 #
#######################
def delete():
    wd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    deletes_dir = ['build', 'dist']
    deletes_dir = [ os.path.join(wd, item, 'main') for item in deletes_dir]

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


################
# 실행파일 생성 #
################
def build():
    import subprocess

    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))   
    os.chdir(path)   
    # 현재 디렉토리의 모든 파일과 폴더를 가져옴
    files_and_folders = os.listdir('.')
    # 각 파일과 폴더를 --add-data 옵션으로 추가 
    add_data_options = [f'--add-data "{item};{item}"' for item in files_and_folders if item not in excludes]
    # 기타 옵션 추가 y
    other_options = []
    if onefile:
        other_options.append('--onefile')
    else:
        other_options.append('--onedir')
    console_text = '--console' if console else '--noconsole'
    # ultralytics_module = 'rsc/ultralytics'  # ultralytics 모듈을 추가
    other_options.append(console_text)

    hidden_imports_text = ' '.join([f'--hidden-import {item}' for item in hidden_imports])
    text = f'pyinstaller {" ".join(add_data_options)} {" ".join(other_options)} {hidden_imports_text} --collect-all ultralytics --collect-all torch --collect-all torchvision main.py'
    print(text)
    subprocess.run(text, shell=True)




################
# 생성파일 실행 #
################
def exe():
    wd = os.path.abspath(os.path.dirname(__file__))
    try:
        python_path = r'C:/Users/prude/anaconda3/envs/pol/python.exe'
    except:
        python_path = r'C:/Users/prudent13/anaconda3/envs/pol_ai/python.exe'
    target = os.path.join(wd, 'dist', 'main','main.exe')
    comand = f'{target}'
    print(comand)
    os.system(comand) 



delete()
build()
# exe()