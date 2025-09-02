from database.default_db import DefaultDB


class UserQueries(DefaultDB):

    async def insert_user(self, username: str, user_id: str):
        await self.execute_query("""INSERT INTO users (username, user_id) VALUES ($1, $2)""", (username, user_id))

    async def update_model(self, user_id: str, model: str):
        await self.execute_query("""UPDATE users SET model = %s WHERE user_id = $1""", (model, user_id))

    async def get_user_model(self, user_id: str):
        model = await self.execute_query("""SELECT last_model FROM users WHERE user_id = $1""", (user_id, ))
        print(model)
        return model


