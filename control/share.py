


class Args:
    '''
    공유 변수 클래스
    '''
    shared_args = {}

    def set(cls, key, value):
        cls.shared_args[key] = value

    def get(cls, key):
        return cls.shared_args[key]

    def all(cls):
        return cls.shared_args
