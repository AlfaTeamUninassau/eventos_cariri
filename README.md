# Eventos Cariri - Back-end e Front-end

Este é o repositório oficial do projeto **Eventos Cariri**, uma plataforma web para divulgação de eventos na região do Cariri, feita com **Django**.

## 💻 Instalação do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o ambiente de desenvolvimento do projeto em sua máquina.

### 1. Clonar o Repositório

Primeiro, clone o repositório para sua máquina local:

`git clone https://github.com/AlfaTeamUninassau/eventos_cariri.git`

Acesse o diretório criado:
`cd eventos_cariri`

### 2. Instalar Python e Criar Ambiente Virtual

No Linux/Ubuntu: Instale o ambiente virtual Python:

`sudo apt install python3.10-venv -y`

No Windows: Se você estiver no Windows, garanta que o Python está instalado e use o seguinte comando para criar o ambiente virtual:

`python -m venv venv`

### 3. Criar o Ambiente Virtual

Com Python instalado, crie o ambiente virtual:

`python3 -m venv venv`

Habilitar execução de scripts no terminal:

`Set-ExecutionPolicy -Scope Process -Executi Bypass`

### 4. Ativar o Ambiente Virtual

Ative o ambiente virtual para que todas as dependências do projeto sejam instaladas no ambiente isolado.

No Linux/Mac:

`source venv/bin/activate`

### 5. Instalar Dependências

Agora, com o ambiente virtual ativo, instale as dependências do projeto. As dependências estão listadas no arquivo **`requirements.txt`** (por exemplo, Django, Pillow e outras bibliotecas necessárias).

`pip install -r requirements.txt`

Copie e renomeie o arquivo `.env.example` para `.env`:
    ```bash
    copy .env.example.txt .env
    ```
e coloque sua apikey do opencage, caso não tenha, basta criar uma nesse site:

`https://opencagedata.com/api#quickstart`


### 6. Realizar Migrações do Banco de Dados

O Django utiliza um sistema de migrações para criar e manter a estrutura do banco de dados. Execute os comandos abaixo para criar as tabelas necessárias:

`python manage.py makemigrations`

`python manage.py migrate`

### 7. Criar um Superusuário (Opcional, para Acesso ao Admin)

Crie um superusuário para poder acessar a área de administração do Django:

`python manage.py createsuperuser`

Siga as instruções na linha de comando para definir nome de usuário, senha e e-mail.

### 8. Rodar o Servidor Local

Com tudo configurado, agora você pode iniciar o servidor de desenvolvimento do Django para ver o projeto rodando em **`localhost:8000`**.

`python manage.py runserver`

Acesse o projeto no navegador em http://127.0.0.1:8000/.

## 📦 Organização do Projeto

O projeto está dividido da seguinte forma:

- **`events/`**: Contém a lógica para gerenciamento de eventos (criação, edição, moderação, etc.).
- **`comments/`**: Gerenciamento de comentários nos eventos.
- **`reviews/`**: Sistema de avaliação com estrelas dos eventos.
- **`users/`**: Lógica relacionada aos usuários e autenticação.
- **`static/`**: Arquivos estáticos, como CSS e JavaScript do front-end.
- **`templates/`**: Templates HTML usados no front-end.

## 🔧 Dependências

As principais dependências do projeto são:

- **Django**: Framework web usado para o back-end.
- **Django rest api**: Usado para a api.
- **Pillow**: Biblioteca de manipulação de imagens (necessária para upload de fotos nos eventos).

## 🚀 Testes

Para garantir que tudo está funcionando corretamente, você pode rodar os testes da aplicação com o Django:

`python manage.py test`

<br/>


## 👥 Contribuidores

<div> 
    <a href="https://github.com/Azinth">
        <img  src="https://avatars.githubusercontent.com/u/75175601?v=4" style="border-radius: 50%" width="70" height="70" border="5" alt="@Azinth">
    </a>
    <a href=“https://github.com/PedroGleidson”> 
        <img  src="https://avatars.githubusercontent.com/u/100448815?v=4" style="border-radius: 50%" width="70" height="70" border="5" alt="@PedroGleidson"> 
    </a> 
    <a href="https://github.com/alancglima"> 
        <img src="https://avatars.githubusercontent.com/u/100448739?v=4" style="border-radius: 50%" width="70" height="70" border="5" alt="@alancglima"> 
    </a> 
</div>
