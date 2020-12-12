from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import sqlite3
import json
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args ,**kwargs):
        self.routes_GET  = {
            '^/messages/$': self.get_all_messages,
            '^/messages/[0-9]/$': self.get_one_message
            }
        self.routes_POST  = {
            '^/login/$': self.login,
            '^/messages/$': self.send_message,
            '^/messages/[0-9]/foward/$': self.foward_message,
            '^/messages/[0-9]/answer/$': self.answer_message,
        } 
        self.routes_DELETE = {
            '^/messages/[0-9]/$': self.delete_message
        }
        self.create_connection_db('db.sqlite3')
        self.create_tables()
        super().__init__(*args, **kwargs)
    def is_authorized(self):
        headers = dict(self.headers)
        try:
            user = headers['user']
            return user
        except:
            return None

    def get_body_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return eval(post_data.decode('utf-8'))

    def send_response_custom(self, status_code, data,headers={}):
        data = json.dumps(data)
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(b"" + str(data).encode())

    def do_GET(self):
        exists, route = self.in_routes(self.path, self.routes_GET)
        if not exists:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"{'message': 'Not Found'}  " + self.path.encode())
            return
        else:
            print(route)
            self.routes_GET[route]()

    def do_POST(self):
        exists, route = self.in_routes(self.path, self.routes_POST)
        if not exists:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"{'message': 'Not Found'}  " + self.path.encode())
            return
        else:
            print(route)
            self.routes_POST[route]()
    def do_DELETE(self):
        exists, route = self.in_routes(self.path, self.routes_DELETE)
        if not exists:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"{'message': 'Not Found'}  " + self.path.encode())
            return
        else:
            print(route)
            self.routes_DELETE[route]()
        

    def in_routes(self, path, routes):
        for route in routes:
            matched = re.match(route, path)
            
            if bool(matched):
                return True, route
            
        return False, None

    def extract_id(self):
        return self.path.split("/")[2]

    def get_all_messages(self):
        id_message = self.extract_id()
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return

        usuario = Usuario().get_usuario(id=user)
        if usuario == None:
            self.send_response_custom(404, {"error": "Usuário não encontrado"})
            return
        messages = Message().get_messages_by_user_id(id=user)
        self.send_response_custom(200, messages)

    def get_one_message(self):
        id_message = self.extract_id()
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return
        
        usuario = Usuario().get_usuario(id=user)
        if usuario == None:
            self.send_response_custom(404, {"error": "Usuário não encontrado"})
            return

        message = Message().get_message_by_id(id=id_message)
        if message == None:
            self.send_response_custom(404, {"error": "Mensagem não encontrada"})
            return

        if message.remetente.id != usuario.id and message.destinatario.id != usuario.id:
            self.send_response_custom(403, {"error": "Usuário não autorizado a acessar esta mensagem."})
            return


        self.send_response_custom(200, message.to_dict())


    def send_message(self, verify_body=True, message_foward=None, message_answer=None):
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return
            
        campos = ['assunto', 'corpo', 'destinatario']
        post_data = self.get_body_request()
        if verify_body:

            contador_campos = 0
            for chave in post_data:
                if chave not in campos:
                    self.send_response_custom(400, {"error": "Foi enviado um campo (" + chave + ") que não era esperado."})
                    return
                else:
                    if len(str(post_data[chave])) > 0:
                        contador_campos += 1
            if contador_campos < len(campos):
                self.send_response_custom(400, {"error": "Não foi enviado um ou mais campos que eram esperados."})
                return
            

        remetente = Usuario().get_usuario(id=user)
        if message_answer == None:
            assunto = post_data['assunto']
            destinatario = Usuario().get_usuario(id=post_data['destinatario'])
        else:
            destinatario = message_answer.remetente
            assunto = message_answer.assunto
        
        if remetente == None:
            self.send_response_custom(401, {"error": "Remetente não encontrado"})
            return
        
        if destinatario == None:
            self.send_response_custom(404, {"error": "Destinatário não encontrado"})
            return

        if remetente.id == destinatario.id:
            self.send_response_custom(403, {"error": "O remetente não pode enviar uma mensagem para si"})
            return
       

        corpo = post_data['corpo']
        
        mensagem = Message(remetente, destinatario, assunto=assunto, corpo=corpo, message_fowarded=message_foward, message_answered=message_answer)
        mensagem.save()

        self.send_response_custom(201, {"message": "ok"})
        

    def login(self):
        post_data = self.get_body_request()
        try:
            usuario = post_data['usuario']
        except KeyError as e:
            self.send_response_custom(400, {"error": "Bad Request"})
            return
        
        print(usuario)
        usuario_db = Usuario(nome=usuario)
        retorno = usuario_db.get_usuario(nome=usuario_db.nome)
        if retorno == None or retorno == 0:
            print(usuario_db.save())
        usuario_db= Usuario().get_usuario(nome=usuario_db.nome)
        self.send_response_custom(200, {"message": "ok", "user_id": usuario_db.id})

    def answer_message(self):
        id_message = self.extract_id()
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return
        
        usuario = Usuario().get_usuario(id=user)
        if usuario == None:
            self.send_response_custom(404, {"error": "Usuário não encontrado"})
            return

        message = Message().get_message_by_id(id_message)
        if (message.remetente.id != usuario.id and message.destinatario.id != usuario.id):# and (message.message != None and message.message.remetente.id != usuario.id and message.message.destinatario.id):
            self.send_response_custom(403, {"error": "Usuário não autorizado a acessar esta mensagem."})
            return
        
        self.send_message(False, message_answer=message)

    def delete_message(self):
        id_message = self.extract_id()
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return
        

        usuario = Usuario().get_usuario(id=user)
        if usuario == None:
            self.send_response_custom(404, {"error": "Usuário não encontrado"})
            return

        message = Message().get_message_by_id(id=id_message)
        if message == None:
            self.send_response_custom(404, {"error": "Mensagem não encontrada"})
            return

        if message.remetente.id != usuario.id:
            self.send_response_custom(403, {"error": "Usuário não autorizado a deletar esta mensagem."})
            return
        
        try:
            message.delete()
            self.send_response_custom(200, {"message": "Mensagem apagada com sucesso!"})
        except:
            self.send_response_custom(500, {"error": "Erro no servidor"})


    def foward_message(self):
        id_message = self.extract_id()
        user = self.is_authorized()
        if user == None:
            self.send_response_custom(401, {"error": "Unauthorized"})
            return
        
        usuario = Usuario().get_usuario(id=user)
        if usuario == None:
            self.send_response_custom(404, {"error": "Usuário não encontrado"})
            return

        message = Message().get_message_by_id(id_message)
        if (message.remetente.id != usuario.id and message.destinatario.id != usuario.id):# and (message.message != None and message.message.remetente.id != usuario.id and message.message.destinatario.id):
            self.send_response_custom(403, {"error": "Usuário não autorizado a acessar esta mensagem."})
            return
        
        self.send_message(False, message_foward=message)


    
    def create_connection_db(self, db_file='db.sqlite3'):
        self.conection = None
        try:
            self.conection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Exception as e:
            print(e)
    def create_tables(self):
        commands = [
        """
        CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );


        CREATE TABLE IF NOT EXISTS message ( 

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente_id INTEGER NOT NULL,
        destinatario_id INTEGER NOT NULL,
        assunto TEXT NOT NULL,
        corpo TEXT NOT NULL,
        message_id INTEGER  NULL,
        message_answer_id INTEGER  NULL,
        FOREIGN KEY(message_id) references message(id),
        FOREIGN KEY(message_answer_id) references message(id),
        FOREIGN KEY(remetente_id) references usuario(id),
        FOREIGN KEY(destinatario_id) references usuario(id)
        );"""]
        for command in commands:
            try:
                c = self.conection.cursor()
                return c.executescript(command)
            except Exception as e:
                print(e)


class ModelDB():
    def create_connection_db(self, db_file='db.sqlite3'):
        self.conection = None
        try:
            self.conection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Exception as e:
            print(e)
    def send_command_db(self, command, type=''):
        try:
            print(command)
            c = self.conection.cursor()
            c.execute(command)
            if type == 'insert':
                self.conection.commit()
            if type == 'select':
                rows = c.fetchall()
                return rows
        except Exception as e:
            print(e)

class Usuario(ModelDB):
    def __init__(self, nome='', id=None):
        self.nome = nome
        self.id = id
        self.create_connection_db()
    
    def save(self):
        command = """ INSERT INTO USUARIO(nome) values('{}') """.format(self.nome)
        print(command)
        self.send_command_db(command, type='insert')
    
    def get_usuario(self, id=-1, nome='',all=False):
        command = """SELECT * FROM usuario WHERE id={} or nome like '{}'
        """.format(id, nome)
        command_nome = """SELECT * FROM usuario"""
        if all:
            retorno =  self.send_command_db(command_nome, type='select')
        else:
            retorno =  self.send_command_db(command, type='select')
        print(retorno)
        if retorno == None or len(retorno) == 0:
            return None
        else:
            if len(retorno) > 1:
                lista = []
                for row in retorno:
                    lista.append(Usuario(nome=row[1], id=row[0]))
            else:
                return Usuario(nome=retorno[0][1], id=retorno[0][0])

    def to_dict(self):
        return {"nome": self.nome,"id": self.id}

class Message(ModelDB):
    def __init__(self, remetente=None, destinatario=None, assunto=None, corpo=None, id=None,message_answered=None, message_fowarded=None):
        self.remetente = remetente
        self.destinatario = destinatario
        self.assunto = assunto
        self.corpo = corpo
        self.id = id
        self.message_fowarded = message_fowarded
        self.message_answered = message_answered

        self.create_connection_db()
    def save(self):
        id_message_foward = None if self.message_fowarded == None else self.message_fowarded.id
        id_message_answer = None if self.message_answered == None else self.message_answered.id
        if id_message_foward == None and id_message_answer == None:
            command = "INSERT INTO message(remetente_id, destinatario_id, assunto, corpo) values({},{},'{}','{}')".format(self.remetente.id, self.destinatario.id, self.assunto, self.corpo)
        elif id_message_foward != None:
            command = "INSERT INTO message(remetente_id, destinatario_id, assunto, corpo, message_id) values({},{},'{}','{}', {})".format(self.remetente.id, self.destinatario.id, self.assunto, self.corpo, self.message_fowarded.id)
        else:
            command = "INSERT INTO message(remetente_id, destinatario_id, assunto, corpo, message_answer_id) values({},{},'{}','{}', {})".format(self.remetente.id, self.destinatario.id, self.assunto, self.corpo, self.message_answered.id)
        self.send_command_db(command,type='insert')
    
    def to_dict(self):
        return {"rementente": self.remetente.to_dict(),"destinatario": self.destinatario.to_dict(),"id":self.id,"assunto":self.assunto,"corpo":self.corpo, "message_fowarded": None if self.message_fowarded == None else self.message_fowarded.to_dict(), "message_answered": None if self.message_answered == None else self.message_answered.to_dict()}
    
    def delete(self):
        # command = " UPDATE message SET message_id=null WHERE message_id={}".format(self.id)
        # self.send_command_db(command, type="insert")
        command = "DELETE FROM message WHERE id={}".format(self.id)
        self.send_command_db(command, type="insert")

    def get_message_by_id(self, id):
        command = """SELECT * FROM message WHERE id = {}""".format(id if id != None else -1)
        messages = self.send_command_db(command, type='select')

        for message in messages:
            id=message[0]
            remetente=Usuario().get_usuario(id=message[1])
            destinatario=Usuario().get_usuario(id=message[2])
            assunto=message[3]
            corpo=message[4]
            message_fowarded = Message().get_message_by_id(id=message[5])
            message_answered = Message().get_message_by_id(id=message[6])
            message_serializer = Message(remetente=remetente, destinatario=destinatario, assunto=assunto, corpo=corpo, id=id, message_fowarded=message_fowarded, message_answered=message_answered)
            return message_serializer
        return None
    def get_messages_by_user_id(self, id):
        command = """SELECT * FROM message WHERE destinatario_id = {} or remetente_id = {}""".format(id, id)
        messages = self.send_command_db(command, type='select')
        return_list = []
        for message in messages:
            id=message[0]
            remetente=Usuario().get_usuario(id=message[1])
            destinatario=Usuario().get_usuario(id=message[2])
            assunto=message[3]
            corpo=message[4]
            message_fowarded = Message().get_message_by_id(id=message[5])
            message_answered = Message().get_message_by_id(id=message[6])
            message_serializer = Message(remetente=remetente, destinatario=destinatario, assunto=assunto, corpo=corpo, id=id, message_fowarded=message_fowarded, message_answered=message_answered).to_dict()
            print(message_serializer)
            return_list.append(message_serializer)
        return return_list

class Foward(ModelDB):
    def __init__(self, message=None, remetente=None, destinatario=None):
        self.message = message
        self.remetente = remetente
        self.destinatario = destinatario
        self.create_connection_db()
    def save(self):
        pass

    def get_foward_by_id(self):
        pass
httpd = HTTPServer(('localhost', os.environ.get('PORT', "8000")), SimpleHTTPRequestHandler)
httpd.serve_forever()