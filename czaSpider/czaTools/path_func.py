import os


def get_current_path(__file__):
    return os.path.dirname(os.path.abspath(__file__))


def to_path(*args):
    return (os.sep).join(args)



if __name__ == "__main__":
    print(get_current_path(__file__))
    print(to_path("", "is", "sg"))
    print(get_database_path())
