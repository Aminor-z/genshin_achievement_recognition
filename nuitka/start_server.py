import os
import subprocess
import traceback

if __name__ == '__main__':
    try:
        ex = subprocess.Popen("python GenshinAchievementRecognitionServer.py", stdout=subprocess.PIPE, shell=True)
        ex.wait()
    except:
        print(traceback.format_exc())
    os.system("pause")
