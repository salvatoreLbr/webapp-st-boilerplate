from webapp_st_boilerplate.db.database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
