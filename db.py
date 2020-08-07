from sqlalchemy import create_engine

engine = create_engine('sqlite:///saved/crypto_data.db', echo=True)
sqlite_conn = engine.connect()

sqlite_table = 'Crypto'

