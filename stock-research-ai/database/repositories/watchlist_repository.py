from uuid import uuid4
from psycopg2.extensions import connection
from schemas.watchlist import WatchListAdd, WatchListOut

class WatchListRepository:
    def __init__(self, db: connection):
        self.db = db

    def add(self, item: WatchListAdd) -> WatchListOut:
        item_id = str(uuid4())

        with self.db.cursor() as cur:
            cur.execute(
                """
                insert into watchlist(
                    id,
                    user_id,
                    symbol,
                    notes
                )
                Values(%s, %s, %s,%s)
                on conflict(user_id , symbol)
                Do update set notes = excluded.notes
                Returning id , user_id , symbol , notes , created_at
                )
                """,
                (
                    item_id,
                    item.user_id,
                    item.symbol.upper(),
                    item.notes,
                ),
            )
            row = cur.fetchone()

        self.db.commit()
        return WatchListOut(**row)
    
    def list_by_user(self, user_id: str) -> list[WatchListOut]:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT id, user_id, symbol, notes, created_at
                FROM watchlist_items
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cur.fetchall()

        return [WatchListOut(**row) for row in rows]
    
    def remove(self, user_id: str , symbol:str) -> bool:
        with self.db.cursor() as cur:
            cur.execute(
                """
                DELETE FROM watchlist_items
                WHERE user_id = %s AND symbol = %s
                """,
                (user_id, symbol.upper()),
            )
            deleted = cur.rowcount > 0

        self.db.commit()
        return deleted