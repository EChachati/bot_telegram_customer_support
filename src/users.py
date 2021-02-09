class User:
    def __init__(self, chat_id: int, username: str, first_name: str = 'None', last_name: str = 'None'):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'chat_id={self.chat_id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}'
