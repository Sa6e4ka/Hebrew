from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Competition
from .user_queries import orm_get_user_id
from .get_queries import orm_get_user_compete_information


'''
Функция для обновления данных в таблице Competition 
''' 
async def orm_update_points(session: AsyncSession, data: dict) -> None:
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])
    point_info  = await orm_get_user_compete_information(session=session, id=id)

    query = update(Competition).where(Competition.user_id == id).values(
        global_points = point_info["points"] + data["points"],
        global_attempts = point_info["attempts"] + data["attempts"],
        global_percentage = round(((point_info["points"] + data["points"]) / (point_info["attempts"] + data["attempts"])), 2)
    )

    await session.execute(query)
    await session.commit()