# ERGOEDUCA – Website de Conscientização Ergonômica

Este projeto é uma aplicação web desenvolvida em Python com Flask, parte da iniciativa ERGOEDUCA. A ERGOEDUCA, um projeto de extensão da UNICSUL (Universidade Cruzeiro do Sul), visa conscientizar as pessoas sobre a importância da boa postura e das cadeiras ergonômicas, com o objetivo de reduzir a incidência de problemas de saúde relacionados à postura e ao uso de cadeiras de escritório. A aplicação web inclui anúncios (ad-banners com scroll horizontal em loop), bem como um formulário de cadastro (para recebimento de dicas ergonômicas e novidades do site, por email).

## Tecnologias Utilizadas

* Python 3.x
* Flask (e extensões como Flask-SQLAlchemy, Flask-Migrate)
* PostgreSQL
* HTML, CSS, JavaScript

## Pré-requisitos

* Python 3.8+ e pip (instalados e adicionados ao PATH do sistema)
* PostgreSQL instalado e rodando
* Git

## Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar o projeto em sua máquina local.

1. **Clone o Repositório:**
    Abra seu terminal ou prompt de comando e execute:

    ```bash
    git clone https://github.com/ViniciusOliveiraOV/ergoeduca.git
    cd ergoeduca
    ```

2. **Crie e Ative um Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

    * **Linux e macOS:**
        No terminal:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

        *(Se `python3` não funcionar, tente `python` se ele apontar para Python 3.8+)*

    * **Windows:**
        No Prompt de Comando (cmd) ou PowerShell:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

        *(Se `python` não funcionar, certifique-se de que o Python foi adicionado ao PATH durante a instalação.)*

    Após a ativação, você deverá ver `(venv)` no início do seu prompt.

3. **Instale as Dependências:**
    Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o Banco de Dados PostgreSQL:**
    * **Instalação:**
        * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install postgresql postgresql-contrib`
        * **Linux (Fedora):** `sudo dnf install postgresql-server postgresql-contrib && sudo postgresql-setup --initdb`
        * **macOS (usando Homebrew):** `brew install postgresql && brew services start postgresql`
        * **Windows:** Baixe o instalador em [postgresql.org](https://www.postgresql.org/download/windows/) e siga as instruções. Durante a instalação, você definirá uma senha para o usuário `postgres`.
    * **Criação do Banco de Dados e Usuário:**
        Abra o `psql` (prompt do PostgreSQL).
        * **Linux/macOS:** Geralmente `sudo -u postgres psql` ou apenas `psql` se seu usuário tiver permissões.
        * **Windows:** Procure por "SQL Shell (psql)" no menu Iniciar. Você será solicitado a fornecer o servidor (localhost), banco de dados (postgres), porta (padrão 5432), nome de usuário (postgres) e a senha definida durante a instalação.

        Dentro do `psql`, execute os seguintes comandos SQL:

        ```sql
        CREATE DATABASE ergoeduca_db;
        CREATE USER ergoeduca_user WITH PASSWORD 'sua_senha_segura';
        ALTER DATABASE ergoeduca_db OWNER TO ergoeduca_user;
        GRANT ALL PRIVILEGES ON DATABASE ergoeduca_db TO ergoeduca_user;
        \q  -- Para sair do psql
        ```

        (Lembre-se de substituir `sua_senha_segura` por uma senha forte e memorizável).

5. **Configure as Variáveis de Ambiente:**
    * Copie o arquivo de exemplo `.env.example` para `.env`:
        * **Linux/macOS:**

            ```bash
            cp .env.example .env
            ```

        * **Windows:**

            ```bash
            copy .env.example .env
            ```

    * Abra o arquivo `.env` com um editor de texto e preencha com suas configurações:

        ```env
        FLASK_APP=app.py
        FLASK_ENV=development # Mude para 'production' em produção
        FLASK_DEBUG=1         # Mude para 0 em produção
        SECRET_KEY='uma_chave_secreta_muito_forte_e_aleatoria'
        DATABASE_URL='postgresql://ergoeduca_user:sua_senha_segura@localhost:5432/ergoeduca_db'
        # Adicione outras variáveis de ambiente necessárias aqui
        ```

        **Importante:** O arquivo `.env` contém segredos e **NÃO** deve ser versionado no Git (ele já está no `.gitignore`). Certifique-se de usar a senha que você definiu para `ergoeduca_user` no passo anterior.

6. **Execute as Migrações do Banco de Dados:**
    Com o ambiente virtual ativado e as variáveis de ambiente configuradas:

    ```bash
    flask db upgrade
    ```

    *Nota: Se este for o primeiro setup do projeto e as migrações ainda não foram criadas, o proprietário do repositório pode ter precisado executar `flask db init` e `flask db migrate -m "Initial migration"` anteriormente. Como um contribuidor/usuário, você geralmente só precisa executar `flask db upgrade`.*

7. **Execute a Aplicação:**

    ```bash
    flask run
    ```

    A aplicação estará disponível em seu navegador em `http://127.0.0.1:5000/` ou `http://localhost:5000/`.

## Estrutura do Projeto

```
   ergoeduca/
   ├── app.py           # Aplicação principal Flask
   ├── models.py        # Modelos de dados (SQLAlchemy)
   ├── routes.py        # Definições de rotas (se separadas de app.py)
   ├── static/          # Arquivos estáticos (CSS, JS, imagens)
   │   ├── style.css
   │   └── main.js
   ├── templates/       # Templates HTML (Jinja2)
   │   ├── index.html
   │   ├── sobre.html
   │   └── contato.html
   ├── migrations/      # Arquivos de migração do Flask-Migrate
   ├── venv/            # Ambiente virtual Python (ignorado pelo Git)
   ├── .env             # Variáveis de ambiente locais (ignorado pelo Git)
   ├── .env.example     # Exemplo de arquivo de variáveis de ambiente
   ├── .gitignore       # Arquivos e diretórios ignorados pelo Git
   ├── requirements.txt # Dependências do projeto
   └── README.md        # Este arquivo
```

### Backend (`app.py` e outros módulos Python)

--- Utiliza Flask para servir as páginas HTML do website.
*Principais rotas:
  *`/` – Página principal (index.html), com informações sobre ergonomia, anúncios e formulário de cadastro.
  *`/sobre` – Página "Sobre" detalhando a ERGOEDUCA, sua missão de conscientização postural e ergonômica, e a parceria com a UNICSUL.
  *`/contato` - Página "Contato", caso queira falar com o desenvolvedor.

### Frontend

**`templates/index.html`**: Estrutura HTML da página principal. Inclui conteúdo informativo sobre ergonomia, anúncios (ad-banners com scroll horizontal), um formulário para cadastro de email (para recebimento de dicas e novidades), e a funcionalidade de leitura de texto em voz alta.
**`templates/sobre.html`**: Página "Sobre" do projeto ERGOEDUCA. Apresenta os objetivos de conscientização sobre boa postura, cadeiras ergonômicas, e sua afiliação como projeto de extensão da UNICSUL. Contém banners e informações institucionais.
**`templates/contato.html`**: Estrutura HTML da página de contato. Fornece informações ou um formulário para que os usuários possam entrar em contato com o desenvolvedor ou responsáveis pelo projeto.
**`static/main.js`**: Lógica frontend. Responsável pela manipulação de eventos de formulário (como o de cadastro de email), interações da interface do usuário, e a funcionalidade de leitura de texto em voz alta (Text-to-Speech).
**`static/style.css`**: Estiliza a aplicação. Define a aparência da navbar, banners, layout das páginas, botões, e garante a responsividade do site.

## Licença

Este projeto é livre para uso educacional.
