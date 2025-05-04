from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}  # Replace 'models' with the actual path to your models if different
    )
    # await Tortoise.init(
    #     db_url='postgres://postgres:postgres@localhost:5432/postgres',
    #     modules={'models': ['models']}  # Ensure 'models' matches your models.py location
    # )
    # Generate schemas only if you want to auto-create tables (optional in production)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
