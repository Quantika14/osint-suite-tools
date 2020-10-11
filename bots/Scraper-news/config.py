from pymongo import MongoClient
import datetime

class DB():
    def __init__(self, user='DG_noticias',password='123456@@', direction='127.0.0.1', port=27017 ):
        self.user = user
        self.password = password
        self.direction = direction
        self.port = port
        self.client = MongoClient(username=user, password=password, host=direction, port=port)

    def save(self,noticias):

        # Creamos la conexion a la base de datos y la coleccion que utilizaremos e insertamos
        db = self.client.Noticias
        noticia = db.noticia
        if not noticias:
            print('No hay ninguna noticia a guardar')
        else:
            post_ids = noticia.insert_many([{"url": noticia.url,
                                             "title": noticia.title,
                                             "text": noticia.text,
                                             "date": datetime.datetime.utcnow().replace(second=0,microsecond=0)} for noticia in noticias]).inserted_ids
            print(f'Insertadas noticias con ids {",".join([str(post_id) for post_id in post_ids])}')

    def get_all(self):
        db = self.client.Noticias
        noticia = db.noticia
        all_news = noticia.find()
        return [new for new in all_news]


