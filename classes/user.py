from classes.base_object import BaseObject
from typing import Optional

class User(BaseObject):
    storage_file: str = 'user.json'

    id: Optional[int]
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool = True

    def __init__(self, username: str, email: str, full_name: Optional[str] = None, is_active: bool = True, id: Optional[int] = None):
        super().__init__(
            id=id,
            username=username,
            email=email,
            full_name=full_name,
            is_active=is_active
        )
