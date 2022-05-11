import nfc
import time
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings
from dumper import NfcReader
from google_api import add_posted_event
from models import Base, User, Log

DB_URL = f"mysql://{settings.SQL_USER_NAME}:{settings.SQL_PASSWORD}@localhost/{settings.SQL_DB_NAME}?charset=utf8mb4"
engine = create_engine(DB_URL, echo=False, encoding="utf-8")


def update_user_status(engine, name, student_id):
    with Session(engine) as session:
        target_user = session.query(User).filter_by(student_id=student_id).first()
        if target_user is None:
            user = User(name=name, student_id=student_id, need_update_log=True)
            session.add(user)
        else:
            target_user.need_update_log = True
            target_user.update_at = datetime.now()
            session.add(target_user)
        session.commit()


def post_google_calender(user_name, enter_time, leave_time):
    try:
        add_posted_event(user_name.split(" ")[0], enter_time, leave_time)
        if enter_time > leave_time:
            return 0
        else:
            print("Post to Google Calender")
            print("    Name  : ", user_name.split(" ")[0])
            print("    Enter : ", enter_time)
            print("    Leave : ", leave_time)
            print("    Diff  : ", leave_time - enter_time)
    except Exception as e:
        print("Fail write data in Google Calender.")
        print("Error", e)


def post_slack(name, action, slack_th):
    # print("Post to Slack")
    print("Recorded.")
    print("    Name   : ", name)
    print("    Action : ", action)
    if (slack_th is not None) and (action == "Leave"):
        # Thread POST
        slack_res = "00000"
    else:
        # Normal POST
        slack_res = "12345"
    return slack_res


def update_user_log(engine):
    with Session(engine) as session:
        target_users = session.query(User).filter_by(need_update_log=True).all()
        for target_user in target_users:
            latest_log = session.query(Log).filter_by(student_id=target_user.student_id).order_by(
                Log.create_at.desc()).first()
            if latest_log is None:
                print("First use")
                print("Record enter")
                log = Log(student_id=target_user.student_id, action="Enter")
                target_user.need_notification = True
                session.add(log)
            elif target_user.update_at - latest_log.create_at < timedelta(seconds=10):
                print("Warning : Touch intervals are too short.")
                target_user.need_update_log = False
            else:
                if latest_log.action == "Enter":
                    print("Record leave")
                    log = Log(student_id=target_user.student_id, action="Leave")
                    post_google_calender(target_user.name, latest_log.create_at, target_user.update_at)
                elif latest_log.action == "Leave":
                    print("Record enter")
                    log = Log(student_id=target_user.student_id, action="Enter")
                target_user.need_notification = True
                session.add(log)
            target_user.need_update_log = False
            session.add(target_user)
            session.commit()


def check_need_notification(engine):
    with Session(engine) as session:
        target_users = session.query(User).filter_by(need_notification=True).all()
        for target_user in target_users:
            latest_log = session.query(Log).filter_by(student_id=target_user.student_id).order_by(
                Log.create_at.desc()).first()
            latest_enter_log = session.query(Log).filter_by(student_id=target_user.student_id, action="Enter").order_by(
                Log.create_at.desc()).first()
            slack_th = latest_enter_log.slack_th if latest_enter_log is not None else None
            slack_res = post_slack(target_user.name, latest_log.action, slack_th)
            target_user.need_notification = False
            latest_log.slack_th = slack_res
            session.add(target_user)
            session.add(latest_log)
            session.commit()


def on_connect(tag):
    nfcReader = NfcReader(tag)
    name = nfcReader.read_name()
    student_id = nfcReader.read_student_number()
    del nfcReader
    update_user_status(engine, name, student_id)


def main():
    while True:
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                tmp = clf.connect(rdwr={'on-connect': on_connect})
            update_user_log(engine)
            check_need_notification(engine)
            print()
            time.sleep(2)
        except Exception as e:
            print("Retry.")
            # print(e)


if __name__ == '__main__':
    main()
