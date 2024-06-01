from django.apps import apps
from asgiref.sync import sync_to_async

@sync_to_async
def create_user(
        telegram_id: str,
        firstname: str,
        lastname: str,
        username: str,
        phone_number: str
) -> None:
    Users = apps.get_model('config', 'Users')
    Users.objects.get_or_create(
        telegram_id=telegram_id,
        firstname=firstname,
        lastname=lastname,
        username=username,
        phone_number=phone_number
    )

