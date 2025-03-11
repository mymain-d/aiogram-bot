from bot.crud.models import User
from tortoise.exceptions import DoesNotExist
import logging
from tortoise.exceptions import DoesNotExist, IntegrityError


async def create_user(user_id: int, username: str = None) -> 'User | None':
    """
    Создает нового пользователя в базе данных с указанным user_id.

    :param user_id: Идентификатор пользователя (например, Telegram user_id), который используется в качестве уникального ключа.
    :param username: Полное имя пользователя (необязательный параметр).
    :return: Объект созданного пользователя или None, если произошла ошибка.
    """
    try:
        user = await User.create(user_id=user_id, username=username)
        return user
    except IntegrityError as e:
        logging.error(f"Ошибка при создании пользователя user_id={user_id}: {e}")
        return None


async def get_user_by_user_id(user_id: int) -> 'User | None':
    """
    Получает пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя для поиска.
    :return: Объект пользователя или None, если пользователь не найден.
    """
    try:
        user = await User.get(user_id=user_id)
        return user
    except DoesNotExist:
        logging.warning(f"Пользователь с user_id={user_id} не найден.")
        return None


async def update_user(user_id: int, **kwargs) -> 'User | None':
    """
    Обновляет данные пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя, данные которого необходимо обновить.
    :param kwargs: Параметры для обновления (например, full_name).
    :return: Обновленный объект пользователя или None, если пользователь не найден.
    """
    try:
        user = await User.get(user_id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        await user.save()
        return user
    except DoesNotExist:
        logging.warning(f"Невозможно обновить данные - пользователь с user_id={user_id} не найден.")
        return None
    except IntegrityError as e:
        logging.error(f"Ошибка при обновлении пользователя user_id={user_id} с данными {kwargs}: {e}")
        return None


async def delete_user(user_id: int) -> bool:
    """
    Удаляет пользователя из базы данных по его идентификатору.

    :param user_id: Идентификатор пользователя, которого необходимо удалить.
    :return: True, если пользователь был удалён, False - если пользователь не найден.
    """
    try:
        user = await User.get(user_id=user_id)
        await user.delete()
        return True
    except DoesNotExist:
        logging.warning(f"Невозможно удалить - пользователь с user_id={user_id} не найден.")
        return False
    except IntegrityError as e:
        logging.error(f"Ошибка при удалении пользователя user_id={user_id}: {e}")
        return False
