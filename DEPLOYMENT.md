# Guia de Implantação do ErgoEduca em Servidor Linux

Este documento descreve os passos para implantar a aplicação ErgoEduca em um servidor Linux (ex: Ubuntu/Debian) usando Gunicorn como servidor WSGI e Nginx como proxy reverso.

## Pré-requisitos do Servidor

*Um servidor Linux (Ubuntu 20.04/22.04 ou Debian 10/11 são boas escolhas).
*Acesso root ou um usuário com privilégios `sudo`.
*Python 3.8+ e `pip` instalados.
*PostgreSQL instalado e rodando.
*Nginx instalado.
*Git instalado.
*(Opcional, mas recomendado) Um nome de domínio apontando para o IP do seu servidor.

## Passos de Implantação

### 1. Preparação Inicial do Servidor

Conecte-se ao seu servidor via SSH.

**Atualize o Sistema:**
    ```bash
    sudo apt update
    sudo apt upgrade -y
    ```

**Instale Pacotes Essenciais (se ainda não instalados):**
    ```bash
    sudo apt install -y python3-pip python3-dev python3-venv build-essential libpq-dev nginx curl git
    ```
    *`python3-pip`: Para instalar pacotes Python.
    *`python3-dev`: Contém arquivos de cabeçalho para compilar extensões Python.
    *`python3-venv`: Para criar ambientes virtuais.
    *`build-essential`: Pacotes necessários para compilação.
    *`libpq-dev`: Arquivos de desenvolvimento para PostgreSQL (necessário para `psycopg2`).
    *`nginx`: O servidor web/proxy reverso.
    *`curl`: Ferramenta para testar conexões.
    *`git`: Para clonar o repositório.

### 2. Configuração do Banco de Dados PostgreSQL (no Servidor)

**Instale o PostgreSQL (se ainda não instalado):**
    ```bash
    sudo apt install -y postgresql postgresql-contrib
    ```
**Acesse o prompt do PostgreSQL:**
    ```bash
    sudo -u postgres psql
    ```

**Crie um usuário e um banco de dados para a aplicação:**
    Substitua `ergoeduca_prod_user` e `sua_senha_forte_de_producao` por seus próprios valores.
    ```sql
    CREATE DATABASE ergoeduca_prod_db;
    CREATE USER ergoeduca_prod_user WITH PASSWORD 'sua_senha_forte_de_producao';
    ALTER ROLE ergoeduca_prod_user SET client_encoding TO 'utf8';
    ALTER ROLE ergoeduca_prod_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ergoeduca_prod_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE ergoeduca_prod_db TO ergoeduca_prod_user;
    \q
    ```

### 3. Obtenção e Configuração do Código da Aplicação

**Crie um diretório para a aplicação:**
    É comum usar `/var/www/` para aplicações web.
    ```bash
    sudo mkdir -p /var/www/ergoeduca_prod
    # Defina as permissões apropriadas. Você pode criar um usuário dedicado
    # ou usar seu usuário sudo para gerenciar os arquivos inicialmente.
    # Exemplo: sudo chown $USER:$USER /var/www/ergoeduca_prod
    ```

**Clone o repositório no servidor:**
    Navegue para o diretório criado e clone o projeto.
    ```bash
    cd /var/www/ergoeduca_prod
    git clone https://github.com/ViniciusOliveiraOV/ergoeduca.git .
    # O "." no final clona para o diretório atual
    ```

**Crie e Ative um Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**Instale as Dependências:**
    ```bash
    pip install wheel # Necessário para algumas compilações
    pip install -r requirements.txt
    # Gunicorn já está no requirements.txt, mas se não estivesse: pip install gunicorn
    ```

**Configure as Variáveis de Ambiente para Produção:**
    Crie um arquivo `.env` no diretório `/var/www/ergoeduca_prod/`.
    ```bash
    sudo nano .env
    ```
    Adicione o seguinte conteúdo, ajustando conforme necessário:
    ```env
    FLASK_APP=app.py
    FLASK_ENV=production
    FLASK_DEBUG=0
    SECRET_KEY='GERAR_UMA_NOVA_CHAVE_SECRETA_FORTE_PARA_PRODUCAO'
    DATABASE_URL='postgresql://ergoeduca_prod_user:sua_senha_forte_de_producao@localhost:5432/ergoeduca_prod_db'
    # Adicione outras variáveis de ambiente de produção aqui
    ```
    **IMPORTANTE:** Use uma `SECRET_KEY` diferente e mais forte do que a usada em desenvolvimento.

**Execute as Migrações do Banco de Dados:**
    ```bash
    flask db upgrade
    ```

**Teste o Gunicorn Manualmente (Opcional):**
    Para garantir que o Gunicorn pode servir sua aplicação antes de configurar o serviço systemd.
    ```bash
    # Dentro do diretório /var/www/ergoeduca_prod e com o venv ativado
    gunicorn --workers 3 --bind unix:/tmp/ergoeduca.sock -m 007 app:app
    ```
    Pressione `Ctrl+C` para parar após o teste. O socket `/tmp/ergoeduca.sock` é temporário para este teste. Usaremos `/run/gunicorn/ergoeduca.sock` para o serviço.

### 4. Configuração do Gunicorn como Serviço Systemd

Isso garantirá que o Gunicorn inicie com o sistema e seja reiniciado em caso de falha.

**Crie um diretório para o socket do Gunicorn em `/run`:**
    ```bash
    sudo mkdir -p /run/gunicorn
    # Defina o proprietário para o usuário que executará o Gunicorn (ex: www-data ou seu usuário)
    # Se for usar www-data para Gunicorn e Nginx:
    sudo chown www-data:www-data /run/gunicorn
    sudo chmod 770 /run/gunicorn
    ```

**Crie o arquivo de serviço Systemd:**
    ```bash
    sudo nano /etc/systemd/system/ergoeduca.service
    ```
    Cole o seguinte conteúdo. Ajuste `User` e `Group` se necessário. `www-data` é um usuário comum para servidores web.
    ```ini
    [Unit]
    Description=Gunicorn instance to serve ErgoEduca
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/ergoeduca_prod
    Environment="PATH=/var/www/ergoeduca_prod/venv/bin"
    ExecStart=/var/www/ergoeduca_prod/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn/ergoeduca.sock -m 007 app:app
    # O -m 007 permite que o usuário e o grupo leiam/escrevam no socket.
    # Se Nginx rodar como www-data, ele poderá acessar o socket.

    Restart=always
    StandardOutput=append:/var/log/gunicorn/ergoeduca-access.log
    StandardError=append:/var/log/gunicorn/ergoeduca-error.log

    [Install]
    WantedBy=multi-user.target
    ```

**Crie os diretórios de log para o Gunicorn:**
    ```bash
    sudo mkdir -p /var/log/gunicorn
    sudo chown www-data:www-data /var/log/gunicorn
    ```

**Inicie e Habilite o Serviço Gunicorn:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start ergoeduca
    sudo systemctl enable ergoeduca
    ```

**Verifique o Status do Serviço:**
    ```bash
    sudo systemctl status ergoeduca
    # Verifique também os logs se houver problemas:
    # sudo journalctl -u ergoeduca
    # sudo cat /var/log/gunicorn/ergoeduca-error.log
    ```
    Você deve ver o socket `/run/gunicorn/ergoeduca.sock` criado se tudo estiver correto.
    ```bash
    ls -l /run/gunicorn/ergoeduca.sock
    ```

### 5. Configuração do Nginx como Proxy Reverso

O Nginx receberá as requisições da internet e as encaminhará para o Gunicorn.

**Crie um arquivo de configuração do Nginx para sua aplicação:**
    ```bash
    sudo nano /etc/nginx/sites-available/ergoeduca
    ```
    Cole a seguinte configuração. Substitua `seudominio.com` pelo seu nome de domínio ou pelo IP do servidor se não tiver um domínio.
    ```nginx
    server {
        listen 80;
        server_name seudominio.com www.seudominio.com seu_ip_do_servidor; # Adicione seu IP se não tiver domínio

        # Logs de acesso e erro específicos para este site
        access_log /var/log/nginx/ergoeduca.access.log;
        error_log /var/log/nginx/ergoeduca.error.log;

        location /static {
            alias /var/www/ergoeduca_prod/static;
            expires 30d; # Cache de arquivos estáticos
            add_header Cache-Control "public";
        }

        location / {
            proxy_pass http://unix:/run/gunicorn/ergoeduca.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            # Timeout settings (opcional, ajuste se necessário)
            # proxy_connect_timeout 75s;
            # proxy_read_timeout 300s;
        }
    }
    ```

**Crie um link simbólico para habilitar o site:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/ergoeduca /etc/nginx/sites-enabled/
    ```
    (Opcional: remova o site padrão se não for usá-lo: `sudo rm /etc/nginx/sites-enabled/default`)

**Teste a Configuração do Nginx:**
    ```bash
    sudo nginx -t
    ```
    Se mostrar "syntax is ok" e "test is successful", prossiga.

**Reinicie o Nginx:**
    ```bash
    sudo systemctl restart nginx
    ```

### 6. Configuração do Firewall (UFW)

Se você estiver usando UFW (Uncomplicated Firewall), permita o tráfego para Nginx:
```bash
sudo ufw allow 'Nginx Full' # Permite HTTP e HTTPS
# Ou apenas HTTP se não for usar HTTPS ainda:
# sudo ufw allow 'Nginx HTTP'
sudo ufw enable # Se ainda não estiver habilitado
sudo ufw status
```

### 7. Teste a Aplicação

Abra seu navegador e acesse seu nome de domínio ou o IP do servidor. Você deve ver sua aplicação ErgoEduca funcionando.

### 8. (Opcional, mas Altamente Recomendado) Configurar HTTPS com Certbot (Let's Encrypt)

Se você tem um nome de domínio, pode configurar HTTPS gratuitamente.

**Instale o Certbot e o plugin do Nginx:**
    ```bash
    sudo apt install -y certbot python3-certbot-nginx
    ```

**Obtenha e instale o certificado SSL:**
    Substitua `seudominio.com` e `www.seudominio.com` pelos seus.
    ```bash
    sudo certbot --nginx -d seudominio.com -d www.seudominio.com
    ```
    Siga as instruções na tela. O Certbot modificará sua configuração do Nginx para HTTPS e configurará a renovação automática.

**Verifique a Renovação Automática:**
    ```bash
    sudo systemctl status certbot.timer
    sudo certbot renew --dry-run
    ```

## Manutenção e Atualizações

**Para atualizar o código da aplicação:**
    1.  Navegue até `/var/www/ergoeduca_prod`.
    2.  `git pull origin main` (ou o branch que você usa).
    3.  Ative o ambiente virtual: `source venv/bin/activate`.
    4.  Instale novas dependências, se houver: `pip install -r requirements.txt`.
    5.  Execute migrações, se houver: `flask db upgrade`.
    6.  Reinicie o serviço Gunicorn: `sudo systemctl restart ergoeduca`.

**Monitorar Logs:**
    *Gunicorn: `/var/log/gunicorn/`
    *Nginx: `/var/log/nginx/`
    *Systemd: `sudo journalctl -u ergoeduca` e `sudo journalctl -u nginx`

Este guia fornece uma base sólida para implantar sua aplicação. Lembre-se de adaptar os nomes de usuário, senhas, caminhos e domínios conforme sua configuração específica.