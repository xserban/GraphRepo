from graph import GraphRepo
from constants import Constants

CT = Constants()


def main():
    neo = GraphRepo(CT.DB_URL, CT.DB_USER, CT.DB_PWD)


if __name__ == '__main__':
    main()
