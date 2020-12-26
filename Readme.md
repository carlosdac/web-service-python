<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Readme</title>
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__html"><ul>
<li>
<h2 id="setup">Setup</h2>
<ol>
<li>Tenha o python3 instalado na sua máquina</li>
<li>Através do pip instale o pacote virtualenv, com o seguinte comando: <code>pip3 install virtualenv</code></li>
<li>Para criar uma nova virtualenv digite o seguinte comando: <code>virtualenv noma_da_sua_env</code>. Será criada na pasta atual um diretório com o nome que você deu para a env.</li>
<li>Para ativar sua env, você deve digitar no terminal <code>sua_env\scripts\activate</code> se estiver no windows, ou <code>sua_env\bin\activate</code> se estiver no linux.</li>
<li>Para instalar os pacotes necessários para a execeução do projeto, navegue até as pastas backend e frontend e com a env ativada, digite o seguinte comando: <code>pip3 install -r requirements.txt</code></li>
<li>Pronto. Os pacotes foram instalados e você pode continuar para a execução nesse momento.</li>
</ol>
</li>
<li>
<h2 id="execução">Execução</h2>
<ol>
<li>Backend<br>
1. Com a env ativada, execute na pasta backend o seguinte comando: <code>python3 main.py</code><br>
2. O servidor está configurado para escutar a variável de ambiente PORT, mas caso o SO não possua essa variável, ele escutará na porta 8080.<br>
3. Pronto. O servidor está em execução.</li>
<li>Frontend
<ol>
<li>Com a env ativada, execute na pasta frontend o seguinte comando: <code>python3 manage.py runserver</code></li>
<li>Pronto. O servidor está em execução no seguinte endereço: 127.0.0.1:8000</li>
<li>Basta acessar a endereço acima para ter acesso ao projeto.</li>
<li>Ele inicialmente está configurado para receber requisições do WS hospedado no heroku através do seguinte endereço: <code>https://stark-scrubland-14642.herokuapp.com/</code></li>
<li>Caso você queira mudar o endereço do WS, vá ao arquivo <code>.env</code> na pasta frontend e mude para o endereço que você desejar. Não esqueça de informar a porta e colocar o “/” no final da URL.</li>
</ol>
</li>
</ol>
</li>
<li>
<h2 id="endpoints">Endpoints</h2>
<p><strong>GET</strong></p>
<ol>
<li>Lembrete: Todas as rotas que necessitam de autenticação, esperam um atributo: “User” no header da requisição, onde este atributo tem como valor, o id do usuário “autenticado”.</li>
<li>Como obtenho este id?
<ul>
<li>A rota <code>login/</code>, é responsável por informar o id do usuário que está se autenticando. Veja nos exemplos mais adiante.</li>
</ul>
</li>
</ol>
</li>
</ul>

<table>
<thead>
<tr>
<th>Rota</th>
<th>Requer login?</th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>messages/:id/</td>
<td>Sim</td>
<td>Detalha uma mensagem do usuário logado.</td>
</tr>
<tr>
<td>messages/</td>
<td>Sim</td>
<td>Retorna todas as mensagens do usuário logado, enviadas ou recebidas.</td>
</tr>
<tr>
<td>users/</td>
<td>Sim</td>
<td>Retorna a lista de usuários cadastrados no sistema.</td>
</tr>
</tbody>
</table><p><strong>POST</strong></p>

<table>
<thead>
<tr>
<th>Rota</th>
<th>Requer Login?</th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>login/</td>
<td>Não</td>
<td>Realiza o login de um usuário</td>
</tr>
<tr>
<td>messages/</td>
<td>Sim</td>
<td>Envia uma mensagem para um usuário</td>
</tr>
<tr>
<td>messages/:id/foward/</td>
<td>Sim</td>
<td>Encaminha uma mensagem para outro usuário</td>
</tr>
<tr>
<td>messages/:id/answer/</td>
<td>Sim</td>
<td>Responde uma mensagem enviada para o usuário logado</td>
</tr>
</tbody>
</table><ul>
<li>Exemplos de <em>request body</em> esperados para as rotas <strong>POST</strong>:
<ul>
<li>
<p>login/</p>
<ul>
<li>{<br>
“usuario”: “”<br>
}</li>
</ul>
</li>
<li>
<p>messages/</p>
<ul>
<li>{<br>
“assunto”: “Aula de ESS II”,<br>
“corpo”: “ieha”,<br>
“destinatario”: 2<br>
}</li>
</ul>
</li>
<li>
<p>messages/:id/foward/</p>
<ul>
<li>{<br>
“assunto”: “Teste encaminhamento 2”,<br>
“corpo”: “olhae”,<br>
“destinatario”: 1<br>
}</li>
</ul>
</li>
<li>
<p>messages/:id/answer/</p>
<ul>
<li>{<br>
“corpo”: “Hehehe. É verdade!”<br>
}</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>DELETE</strong></p>

<table>
<thead>
<tr>
<th>Rota</th>
<th>Requer Login?</th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>messages/:id/</td>
<td>Sim</td>
<td>Deleta uma mensagem enviada pelo usuário logado</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table></div>
</body>

</html>
