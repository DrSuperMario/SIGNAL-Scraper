from sqlalchemy import create_engine


def createDb(nameID):

    nameID = create_engine(f"sqlite:///saved/{nameID}_data.db", echo=False)
    sqlite_conn = nameID.connect()

    return sqlite_conn, f"Scraped {nameID} data"


