import os
import subprocess

# 현재 파일의 디렉토리 경로를 얻고 프로젝트 디렉토리로 이동
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
os.chdir(path)

# 옵션 설정 (예시)
onefile = False  # 하나의 실행 파일로 생성 여부
console = True   # 콘솔 창 표시 여부
excludes = ['영상자료', '__pycache__', '.vscode', 'build', 'dist', 'test_widget']  # 제외할 파일 및 폴더

# Nuitka 명령 생성
nuitka_command = f"nuitka --standalone --output-dir=dist "  # Python 버전은 필요에 따라 변경
nuitka_command += f"--include-data-dir={os.path.join(path, 'rsc')}=rsc "  # rsc 디렉토리 포함
nuitka_command += f"--include-data-dir={os.path.join(path, 'rsc', 'ultralytics')}=ultralytics "  # rsc 디렉토리 포함
nuitka_command += f"--windows-console-mode=disable "
nuitka_command += f"--include-module=ultralytics "
nuitka_command += f"--include-module=torch "
nuitka_command += f"--include-module=torchvision "
nuitka_command += f"--enable-plugin=pyside6 "
nuitka_command += "main.py"  # 실행할 파이썬 파일

print(nuitka_command)

# Nuitka 실행
subprocess.run(nuitka_command, shell=True) 

 