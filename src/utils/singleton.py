class Singleton(object):
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = cls()

        return cls._instance
