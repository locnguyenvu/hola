import json, psycopg2, asyncio

from .di import get_db

db = get_db()

def broadcast(channel:str, payload: dict):
    conn = db.engine.raw_connection()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("NOTIFY {channel}, '{payload}';".format(channel=channel, payload=json.dumps(payload)))
    return 

def consume(channel: str, callback):
    conn = db.engine.raw_connection()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("LISTEN {channel};".format(channel=channel))

    def handle():
        conn.poll()
        for mess in conn.notifies:
            args = json.loads(mess.payload)
            callback(args)
        conn.notifies.clear()

    loop = asyncio.get_event_loop()
    loop.add_reader(conn, handle)
    loop.run_forever()