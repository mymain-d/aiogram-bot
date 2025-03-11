from tortoise import fields, models


class User(models.Model):
    """
    Класс User хранит данные о пользователях системы.
    """
    user_id: int = fields.IntField(pk=True)
    username: str = fields.CharField(
        max_length = 32,  # https://core.telegram.org/method/account.checkUsername
        null=True,
        index=True
    )
    created_at: fields.DatetimeField = fields.DatetimeField(
        auto_now_add=True,
        description = "Дата и время создания аккаунта"
    )
    updated_at: fields.DatetimeField = fields.DatetimeField(
        auto_now=True,
        description = "Дата и время последнего обновления записи"
    )

    def __str__(self) -> str:
        return f"User(ID={self.user_id}, username='{self.username}')"

    class Meta:
        table = "users"
        ordering = ["user_id"]
