from uuid import uuid4

from psycopg2.extensions import connection

class UserRepository:
    def __init__(self, db: connection):
        self.db = db

    def create(self, email: str , name: str | None = None) -> dict:
        user_id = str(uuid4())

        with self.db.cursor() as cur:
            cur.execute(
                """
                insert into users(
                    id,
                    email,
                    name
                )
                Values(%s, %s, %s)
                Returning id , email , name , created_at
                """,
                (
                    user_id,
                    email,
                    name,
                ),
            )
            row = cur.fetchone()

        self.db.commit()
        return row
    
    def get_by_id(self, user_id: str) -> dict | None:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, name, created_at
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()
        return dict(row) if row else None
    
    def get_by_email(self, email: str) -> dict | None:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, name, created_at
                FROM users
                WHERE email = %s
                """,
                (email,),
            )
            row = cur.fetchone()
        return dict(row) if row else None