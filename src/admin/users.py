ADMIN_USERS = [
    581235655,  # Edkar J Chachati
]


def is_admin(chat_id: int):
    return (chat_id in ADMIN_USERS)
