
import sys
import os
# import schedule
# import time
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from be import serve

# def job():
#     print("I'm working...")
if __name__ == "__main__":
    serve.be_run()

    # schedule.every().second.do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
