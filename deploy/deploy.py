import os
import subprocess


path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 현재 파일의 디렉토리 경로
os.chdir(path)  # 프로젝트 디렉토리로 이동


# 옵션 설정
onefile = False
console = True

# 제외할 파일과 폴더를 지정
excludes = ['영상자료', '__pycache__', '.vscode', 'build', 'dist', 'test_widget']


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
ultralytics_module = 'rsc/ultralytics'  # ultralytics 모듈을 추가
other_options.append(console_text)

text = f'pyinstaller {" ".join(add_data_options)} {" ".join(other_options)} --hidden-import torch.jit --collect-all ultralytics --collect-all torch --collect-all torchvision main.py'
print(text)
# pyinstaller 실행
subprocess.run(text, shell=True)


import os 

wd = os.path.abspath(os.path.dirname(__file__))
python_path = r'C:/Users/prude/anaconda3/envs/pol/python.exe'
target = os.path.join(wd, 'dist', 'main','main.exe')
comand = f'{target}'

# 파일이 존재하는지 확인
 
if not os.path.isfile(target):
    target = os.path.join(wd, 'dist', 'main','main.exe')

comand = f'{target}'
os.system(comand) 