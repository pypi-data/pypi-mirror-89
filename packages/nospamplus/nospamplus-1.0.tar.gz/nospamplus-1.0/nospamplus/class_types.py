
class ClassTypes:
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.__dict__}>'

    def __repr__(self) -> str:
        return self.__str__()


class nospamplusclass(ClassTypes):
    token: str
    userid: int
    reason: str
    banned: str
    ban_code: str

    def __init__(self, banned: str, ban_code: str, reason: str, token: str, userid: int, **kwargs) -> None:
        self.token = token
        self.userid = userid
        self.reason = reason
        self.ban_code = ban_code
        self.banned = banned
