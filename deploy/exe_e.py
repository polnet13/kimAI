import os 

wd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
python_path = r'C:/Users/prude/anaconda3/envs/pol/python.exe'
target = os.path.join(wd, 'dist', 'main','main.exe')
comand = f'{target}'

# 파일이 존재하는지 확인
 
if not os.path.isfile(target):
    target = os.path.join(wd, 'build', 'main','main.exe')

# C:\Users\prude\kimAI\build\main\main.exe

comand = f'{target}'
os.system(comand) 