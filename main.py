from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import sqlite3

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
        self.routes_DELETE = ['/messages/<id>/']
        self.create_connection_db('db.sqlite3')
        self.create_tables()
        super().__init__(*args, **kwargs)
    
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
        

    def in_routes(self, path, routes):
        for route in routes:
            matched = re.match(route, path)
            
            if bool(matched):
                return True, route
            
        return False, None

    def extract_id(self):
        return self.path.split("/")[2]

    def get_all_messages(self):
        pass

    def get_one_message(self):
        id_message = self.extract_id()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"{'message': 'GET one message'}  " + id_message.encode())

    def send_message(self):
        pass

    def login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = eval(post_data.decode('utf-8'))
        try:
            usuario = post_data['usuario']
        except KeyError as e:
            error = 400
            message = "Bad Request"
            response = {
                "error": message
            }
            self.send_response(error)
            self.end_headers()
            self.wfile.write(str(response).encode('utf-8'))    
            return
        
        

        response_code = 200
        response_data = {
            "message": "ok"
        }
        usuario_db = Usuario(nome=usuario)
        retorno = usuario_db.get_usuario(nome=usuario_db.nome)
        if retorno == None or retorno == 0:
            print(usuario_db.save())
        self.send_response(response_code)
        self.end_headers()
        self.wfile.write(str(response_data).encode('utf-8'))

    def answer_message(self):
        id_message = self.extract_id()
        pass

    def delete_message(self):
        id_message = self.extract_id()
        pass

    def foward_message(self):
        id_message = self.extract_id()
        pass
    
    def create_connection_db(self, db_file='db.sqlite3'):
        self.conection = None
        try:
            self.conection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
    def create_tables(self):
        commands = ["""CREATE TABLE IF NOT EXISTS usuario (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
   	    nome TEXT NOT NULL UNIQUE);""", """ CREATE TABLE IF NOT EXISTS message ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente INTEGER NOT NULL,
        destinatario INTEGER NOT NULL,
        FOREIGN KEY(remetente) references usuario(id),
        FOREIGN KEY(destinatario) references usuario(id)
        )"""]
        for command in commands:
            try:
                c = self.conection.cursor()
                return c.execute(command)
            except Exception as e:
                print(e)


class ModelDB():
    def create_connection_db(self, db_file='db.sqlite3'):
        self.conection = None
        try:
            self.conection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
    def send_command_db(self, command, type=''):
        try:
            print(command)
            c = self.conection.cursor()
            c.execute(command)
            if type == 'insert':
                self.conection.commit()
            # self.conection.close()
            if type == 'select':
                rows = c.fetchall()
                return rows
        except Exception as e:
            print(e)

class Usuario(ModelDB):
    def __init__(self, nome, id=None):
        self.nome = nome
        self.id = id
        self.create_connection_db()
    
    def save(self):
        command = """ INSERT INTO USUARIO(nome) values('{}') """.format(self.nome)
        print(command)
        self.send_command_db(command, type='insert')
    
    def get_usuario(self, id=None, nome=''):
        command = """SELECT * FROM usuario WHERE id={}
        """.format(id)
        command_nome = """SELECT * FROM usuario"""
        if nome != '':
            retorno =  self.send_command_db(command_nome, type='select')
        else:
            retorno =  self.send_command_db(command, type='select')
        print(retorno)
        if retorno == None or len(retorno) == 0:
            return retorno
        else:
            if len(retorno) > 1:
                lista = []
                for row in retorno:
                    lista.append(Usuario(nome=row[1], id=row[0]))
            else:
                return Usuario(nome=retorno[0][1], id=retorno[0][0])



class Message(ModelDB):
    def __init__(self, remetente, destinatario, assunto, corpo, id=None):
        self.remetente = remetente
        self.destinatario = destinatario
        self.assunto = assunto
        self.corpo = corpo
        self.id = id
    def save(self):
        command = ""
        try:
            c = self.conection.cursor()
            c.execute(command)
        except Exception as e:
            print(e)

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()