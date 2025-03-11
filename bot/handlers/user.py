from aiogram import Router, types, F
from aiogram.filters import Command
from bot.crud import crud
from bot.keyboard.user import get_user_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    if await crud.get_user_by_user_id(user_id = message.from_user.id):
        await crud.update_user(
            user_id = message.from_user.id,
            username = message.from_user.username
        )
    else:
        create = await crud.create_user(
            user_id = message.from_user.id,
            username = message.from_user.username
        )
        print(create)

    await message.answer(
        "Добро пожаловать!",
        reply_markup = get_user_keyboard()
    )


@router.message(F.text == "Показать профиль")
async def profile_handler(message: types.Message):
    try:
        user = await crud.get_user_by_user_id(user_id = message.from_user.id)
        await message.answer(
            f"Ваш профиль:\n"
            f"Имя пользователя: {user.username}\n"
            f"Дата регистрации: {user.created_at}"
        )
    except Exception as e:
        await message.answer(f"Ошибка при получении профиля: {e}")