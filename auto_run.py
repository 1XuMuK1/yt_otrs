import time

import schedule
from config import URL, USERNAME, PASSWORD
from otrs2youtrack import run


def main():
    params = dict(
        url=URL, 
        username=USERNAME,
        password=PASSWORD
    )
    schedule.every(5).seconds.do(run, **params)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    print('info', 'start auto parsing otrs_youtrack', 'auto_parsing')
    main()
