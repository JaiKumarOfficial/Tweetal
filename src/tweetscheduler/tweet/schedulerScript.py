from datetime import datetime, timezone
import pytz
import time
import os
import twitter
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REFRESH_INTERVAL = 2  # seconds
utc = pytz.UTC
MEDIA_SOURCE = os.path.join(BASE_DIR, "media") # to the folder where documents is situated.


def users_list():
    try:
        server = '127.0.0.1'
        port = '3306'
        database = 'tweetscheduler'
        username = 'root'
        password = 'root'
        con = mysql.connector.connect(
                    host=server,
                    port=port,
                    user=username,
                    password=password,
                    db=database,
                    charset='utf8mb4',
                )
        print('user connection made')
        cursor = con.cursor()
        cursor.execute('select * from tweet_users')
        data = cursor.fetchall()
        col = cursor.column_names
        users = []
        for elem in data:
            users.append(dict(zip(col, elem)))
        con.commit()
        con.close()
        print('user connection closed')
        return users
    except Exception as e:
        print(e)


def postSchduleTweet():
    try:
        print('execution start')
        users = users_list()

        server = '127.0.0.1'
        port = '3306'
        database = 'tweetscheduler'
        username = 'root'
        password = 'root'
        con = mysql.connector.connect(
                    host=server,
                    port=port,
                    user=username,
                    password=password,
                    db=database,
                    charset='utf8mb4',
                )

        cursor = con.cursor()
        print('connection made')
        query = "select id, user, tweet, document, created_date, is_posted, schedule_post"\
                " from tweetscheduler.tweet_scheduledtweet where is_posted = false;"
        cursor.execute(query)
        print('query executed')

        data = cursor.fetchall()
        col = cursor.column_names
        dataset = []
        for elem in data:
            dataset.append(dict(zip(col, elem)))
        con.commit()
        print('query commit')

        if dataset is None or len(dataset) == 0:
            print('-- No scheduled tweet --')
        else:
            for row in dataset:
                if row['schedule_post'] is not None:
                    scheduled_time = utc.localize(row['schedule_post'])

                    if (scheduled_time - datetime.now(timezone.utc)).total_seconds() < 0:
                        Api = twitter.Api(consumer_key=users[0]['consumer_key'],
                                          consumer_secret=users[0]['consumer_secret_key'],
                                          access_token_key=users[0]['access_token'],
                                          access_token_secret=users[0]['access_secret_token'])
                        try:
                            media_url = MEDIA_SOURCE + '\\' + row['document']
                            print(media_url)
                            Api.PostUpdate(row['tweet'], media=media_url)
                            print('** tweet posted with media **')
                        except BaseException as e:
                            print(e)
                            Api.PostUpdate(row['tweet'])
                            print('** tweet posted w/o media **')
                        finally:
                            sql = "UPDATE tweetscheduler.tweet_scheduledtweet SET is_posted = true WHERE id =%s;"
                            tweet_id = row['id']
                            cursor.execute(sql, (tweet_id,))
                            print('update query executed')
                            con.commit()
                            print('update query commit')
                    else:
                        print('waiting . . . ')
                        pass
    except Exception as e:
        print('e1', e)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    print('scheduler started')
    scheduler.add_job(postSchduleTweet, 'interval', seconds=REFRESH_INTERVAL)
    while True:
        time.sleep(4)