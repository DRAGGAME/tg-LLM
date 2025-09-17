import aiosqlite

class DefaultDB:
    """
    Класс для работы с базой данных
    """
    def __init__(self):
        """Инициализация начальных переменных"""
        self.pool = None

    async def connect(self) -> None:
        try:
            self.pool = await aiosqlite.connect('project_LLM.db')
        except Exception as e:
            raise ValueError(f"Ошибка подключения к базе данных: {e}")

    async def close(self) -> None:
        try:
            if self.pool:
                await self.pool.close()
        except Exception as e:
            raise ValueError(f"Ошибка закрытия подключения к базе данных: {e}")

    async def execute_query(self, query: str, params=None) -> tuple:
        try:
            async with self.pool.cursor() as cursor:
                if params:
                    await cursor.execute(query, params)
                    await self.pool.commit()
                else:
                    await cursor.execute(query)
                rows = await cursor.fetchall()
                return rows
        except Exception as e:
            raise ValueError(f"Ошибка выполнения запроса: {e}")
