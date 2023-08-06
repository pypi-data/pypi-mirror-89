import sys
import subprocess
import logging
from datetime import datetime


def send_result(arguments, start_time, end_time, return_code, text):
    title = 'Success' if return_code == 0 else "Error"
    command = ' '.join(arguments)


def notify(arguments):
    return_code = 0
    text = ""

    try:
        start_time = datetime.today()

        result = subprocess.check_output(arguments, stderr=subprocess.STDOUT)
        text = result.decode('utf-8')

        end_time = datetime.today()
        print(end_time - start_time)
        logging.info(f"Execution time is: {end_time - start_time}")

    except subprocess.CalledProcessError as error:
        return_code = error.returncode
        text = error.stdout.decode('utf-8')



def main():
    notify(sys.argv[1:])