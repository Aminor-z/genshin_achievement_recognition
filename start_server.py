import subprocess

def run(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    ex.wait()

if __name__ == '__main__':
    run("python GenshinAchievementRecognitionServer.py")