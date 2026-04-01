"""
Автоматическая установка виртуальной среды и библиотек необходимых для работы программы.
"""
import os
import subprocess
import sys

dir_list = os.listdir()
process_flag = None

if not '.venv' in dir_list:
    if sys.platform == 'win32':
        process_flag = subprocess.run('py -m venv ./.venv',check=True,shell=True)
        if process_flag.returncode == 0:
            print(f'Успешно установлен .venv. код ошибки {process_flag.returncode}')

    else:
        process_flag = subprocess.run('python3 -m venv ./.venv', check=True, shell=True)
        if process_flag.returncode == 0:
            print(f'Успешно установлен .venv. код ошибки {process_flag.returncode}')

while process_flag:
    if process_flag.returncode != 0:
        sys.exit()
    if process_flag.returncode == 0:
        break
    pass

with open('requirements.txt','w') as file:
    file.write('pygame\nmutagen\npillow\nlibrosa\nsoundfile')

dir_list = os.listdir()

if '.venv' in dir_list:
    if 'requirements.txt' in dir_list:
        if sys.platform == 'win32':
            try:
                process_flag_pip = subprocess.run('.venv\\Scripts\\pip install -r requirements.txt', check=True, shell=True,capture_output=True)
                print(process_flag_pip.stdout)
                if process_flag_pip.returncode == 0:
                    print(f'Успешно установлены библиотеки. код ошибки {process_flag_pip.returncode}')
            except subprocess.CalledProcessError as e:
                print(f"Ошибка: {e}")
                print(f"Вывод: {e.stdout}")
                print(f"Ошибки: {e.stderr}")
        else:
            try:
                process_flag_pip = subprocess.run('.venv/bin/pip install -r requirements.txt', check=True, shell=True,capture_output=True)
                print(process_flag_pip.stdout)
                if process_flag_pip.returncode == 0:
                    print(f'Успешно установлены библиотеки. код ошибки {process_flag_pip.returncode}')
            except subprocess.CalledProcessError as e:
                print(f"Ошибка: {e}")
                print(f"Вывод: {e.stdout}")
                print(f"Ошибки: {e.stderr}")