from periodicos import Periodicos
from config import DB
import warnings

warnings.filterwarnings("ignore")
conf = DB()
p = Periodicos(db_con=conf)


def main():
    '''
    Buscamos todas las noticias de todos los periodicos y las añadimos a la base de datos
    '''
    noticias = p.search()
    conf.save(noticias)


if __name__ == '__main__':
    main()