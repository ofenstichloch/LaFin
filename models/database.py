from models.db_schema import *
from app import db
import secrets
import datetime

def getWidgets(userid):
    return Dashboards.query.filter_by(user_id=userid).first().widgets


def checkLogin(username, password):
    user = Users.query.filter_by(name=username).first()
    if user is None:
        return False
    if user.password == password:
        return user.id
    else:
        return False


def startSession(userid):
    session_token = secrets.token_hex(64)
    csrf_token = secrets.token_hex(64)
    session = Sessions(session_token=session_token, csrf_token=csrf_token, user_id=userid)
    db.session.add(session)
    db.session.commit()
    return session_token


def clearSessions():
    sessions = Sessions.query.all()
    for session in sessions:
        expire = session.created + datetime.timedelta(minutes=30)
        if expire < datetime.datetime.now():
            db.session.delete(session)
    db.session.commit()