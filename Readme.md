 - Setup
	 - 
	 1. Tenha o python3 instalado na sua máquina
	 2. Através do pip instale o pacote virtualenv, com o seguinte comando: `pip3 install virtualenv`
	 3. Para criar uma nova virtualenv digite o seguinte comando: `virtualenv noma_da_sua_env`. Será criada na pasta atual um diretório com o nome que você deu para a env.
	 4. Para ativar sua env, você deve digitar no terminal `sua_env\scripts\activate` se estiver no windows, ou `sua_env\bin\activate` se estiver no linux.
	 5. Para instalar os pacotes necessários para a execeução do projeto, navegue até as pastas backend e frontend e com a env ativada, digite o seguinte comando: `pip3 install -r requirements.txt`
	 6. Pronto. Os pacotes foram instalados e você pode continuar para a execução nesse momento.
- Execução
	- 
	1. Backend
			1. Com a env ativada, execute na pasta backend o seguinte comando: `python3 main.py`
			2. O servidor está configurado para escutar a variável de ambiente PORT, mas caso o SO não possua essa variável, ele escutará na porta 8080.
			3. Pronto. O servidor está em execução.
	3. Frontend
		1. Com a env ativada, execute na pasta frontend o seguinte comando: `python3 manage.py runserver`
		2. Pronto. O servidor está em execução no seguinte endereço: 127.0.0.1:8000
		3. Basta acessar a endereço acima para ter acesso ao projeto.
		4. Ele inicialmente está configurado para receber requisições do WS hospedado no heroku através do seguinte endereço: `https://stark-scrubland-14642.herokuapp.com/`
		5. Caso você queira mudar o endereço do WS, vá ao arquivo `.env` na pasta frontend e mude para o endereço que você desejar. Não esqueça de informar a porta e colocar o "/" no final da URL.

- Endpoints
	-
	**GET**
	1. Lembrete: Todas as rotas que necessitam de autenticação, esperam um atributo: "User" no header da requisição, onde este atributo tem como valor, o id do usuário "autenticado".
	2. Como obtenho este id?
		- A rota `login/`, é responsável por informar o id do usuário que está se autenticando. Veja nos exemplos mais adiante.
	
| Rota          | Requer login?   |Descrição |
|-------------  |-----------------|-----------|
| messages/:id/ | Sim             |Detalha uma mensagem do usuário logado. |
| messages/     |Sim              |Retorna todas as mensagens do usuário logado, enviadas ou recebidas. |
|users/         | Sim             |Retorna a lista de usuários cadastrados no sistema. |


**POST** 

|Rota                 | Requer Login?  | Descrição |
|---------------------|----------------|-----------|
| login/              |  Não           | Realiza o login de um usuário |
| messages/           |  Sim           | Envia uma mensagem para um usuário |
| messages/:id/foward/| Sim            | Encaminha uma mensagem para outro usuário |
| messages/:id/answer/| Sim            | Responde uma mensagem enviada para o usuário logado |
- Exemplos de *request body* esperados para as rotas **POST**:
   -  login/
		 - {
				"usuario": ""
			} 
	- messages/
		- {
					"assunto": "Aula de ESS II",
					"corpo": "ieha",
					"destinatario": 2
			}


	- messages/:id/foward/
		- {
					"assunto": "Teste encaminhamento 2",
					"corpo": "olhae",
					"destinatario": 1
			}

	- messages/:id/answer/
		-  {
					"corpo": "Hehehe. É verdade!"
			   }
		
**DELETE**
|Rota          | Requer Login? |Descrição |
|--------------|---------------|-----------|
| messages/:id/| Sim           | Deleta uma mensagem enviada pelo usuário logado
 |
