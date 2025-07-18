from db.models import session, PlayTime
from datetime import datetime


def create(name: str, is_running: bool, start_time: datetime, max_time: int) -> PlayTime:
    play_time = PlayTime(name, is_running, start_time, max_time)
    session.add(play_time)
    session.commit()
    return play_time


def edit(name: str, is_running: bool, start_time: datetime, max_time: int, new_name: str | None = None) -> PlayTime | None:
    play_time: PlayTime = session.query(PlayTime).filter(PlayTime.name == name).scalar()
    if not play_time:
        return None
    if new_name:
        play_time.name = new_name
    play_time.is_running = is_running
    play_time.start_time = start_time
    play_time.max_time = max_time
    session.commit()
    return play_time


def get_all() -> list[PlayTime]:
    return session.query(PlayTime)


def get_by_name(name: str) -> PlayTime | None:
    return session.query(PlayTime).filter(PlayTime.name == name).scalar()
