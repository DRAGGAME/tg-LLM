from database.default_db import DefaultDB


class StartDB(DefaultDB):
    """
    Класс во время старта
    """
    async def start_db(self):

        await self.connect()

        await self.execute_query(
            """
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            user_id TEXT UNIQUE NOT NULL,
            last_model TEXT DEFAULT 'short_description'
            )
            """
        )
        await self.close()

    async def select_table(self):
        test = await self.execute_query("""SELECT * FROM users""")
        return test