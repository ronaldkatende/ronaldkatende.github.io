"""Transactional local outbox and idempotent receiving, SQLite-only demonstration.
Not a production application; no authentication, encryption or network transport.
"""
import sqlite3
from tempfile import TemporaryDirectory
from pathlib import Path

def prepare(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS readings (id TEXT PRIMARY KEY, site TEXT, value REAL)')
    conn.execute('CREATE TABLE IF NOT EXISTS outbox (id TEXT PRIMARY KEY, acknowledged INTEGER DEFAULT 0)')
    conn.commit()

def save_local(conn,key,site,val):
    with conn:  # a single atomic transaction
        conn.execute('INSERT OR IGNORE INTO readings VALUES (?,?,?)',(key,site,val))
        conn.execute('INSERT OR IGNORE INTO outbox (id) VALUES (?)',(key,))

def receive_idempotently(remote,key,site,val):
    with remote:
        remote.execute('INSERT OR IGNORE INTO readings VALUES (?,?,?)',(key,site,val))

with TemporaryDirectory() as folder:
    base=Path(folder)
    with sqlite3.connect(base/'local.sqlite') as local,sqlite3.connect(base/'server.sqlite') as remote:
        prepare(local); prepare(remote)
        for key,site,val in [('r001','A',10.0),('r002','A',11.0),('r003','B',8.0)]:
            save_local(local,key,site,val)
        local_n=local.execute('SELECT count(*) FROM readings').fetchone()[0]
        outbox_n=local.execute('SELECT count(*) FROM outbox').fetchone()[0]
        assert local_n==outbox_n==3
        for attempt in (1,2): # simulate missing first acknowledgement
            receive_idempotently(remote,'r001','A',10.0)
        assert remote.execute('SELECT count(*) FROM readings').fetchone()[0]==1
        for row in local.execute('SELECT id,site,value FROM readings ORDER BY id'):
            receive_idempotently(remote,*row)
        assert remote.execute('SELECT count(*) FROM readings').fetchone()[0]==3
        # A deliberately raised exception exercises transaction rollback.
        try:
            with local:
                local.execute('INSERT INTO readings VALUES (?,?,?)',('fault','C',99.0))
                raise RuntimeError('injected pre-commit failure')
        except RuntimeError:
            pass
        assert local.execute("SELECT count(*) FROM readings WHERE id='fault'").fetchone()[0]==0
        assert local.execute("SELECT count(*) FROM outbox WHERE id='fault'").fetchone()[0]==0
        with sqlite3.connect(base/'local.sqlite') as reopened:
            assert reopened.execute('SELECT count(*) FROM readings').fetchone()[0]==3
            assert reopened.execute('SELECT count(*) FROM outbox').fetchone()[0]==3
        print('Atomic-outbox, duplicate-delivery, and injected rollback/reopen checks PASS.')
