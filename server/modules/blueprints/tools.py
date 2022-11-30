class BlueprintInit:
    def __init__(self, bcrypt_ref):
        self._bcrypt = bcrypt_ref

    @property
    def bcrypt(self):
        return self._bcrypt
