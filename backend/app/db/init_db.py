from app.db.session import engine
from app.db.base import Base

from app.models import project, user, task

def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库表已初始化。")

if __name__ == "__main__":
    init_db()