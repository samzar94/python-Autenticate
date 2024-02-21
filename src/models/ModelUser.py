from .entities.User import User
from mysql.connector.errors import IntegrityError
#___init__.py en este archivo se uso para que funcione como paquete

class ModelUser():

    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            password_hash=user.password_hash(user.password)
            sql = """INSERT INTO user (username, password, fullname) VALUES
            (%s, %s,%s)"""
            values= (user.username,password_hash, user.fullname)
            cursor.execute(sql,values)
            db.connection.commit()
            cursor.close()
            
        except IntegrityError as e:
            raise Exception(e)
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
