# ERGOEDUCA – Conscientização Ergonômica e Gerenciamento de Tarefas

Este projeto é uma aplicação web sendo desenvolvida em Python com Flask, parte da iniciativa ERGOEDUCA. A ERGOEDUCA, um projeto de extensão da UNICSUL (Universidade Cruzeiro do Sul), visa conscientizar as pessoas sobre a importância da boa postura e das cadeiras ergonômicas, com o objetivo de reduzir a incidência de problemas de saúde relacionados à postura e ao uso de cadeiras de escritório. A aplicação web inclui anúncios (ad-banners com scroll horizontal em loop), bem como um formulário de cadastro (para recebimento de dicas ergonômicas e novidades do site, por email).


## Estrutura do Projeto

```
projeto/
├── app.py               # Backend Flask com rotas e lógica da API
├── requirements.txt     # Dependências do projeto
├── static/
│   ├── main.js          # Lógica frontend
│   └── style.css        # Estilos da interface
├── templates/
│   ├── index.html       # Página principal 
│   └── sobre.html       # Página "Sobre" o projeto ERGOEDUCA
└── venv/                # Ambiente virtual Python
```

### Backend (`app.py`)
- Utiliza Flask para servir as páginas HTML do website.
- Principais rotas:
  - `/` – Página principal (index.html), com informações sobre ergonomia, anúncios e formulário de cadastro.
  - `/sobre` – Página "Sobre" detalhando a ERGOEDUCA, sua missão de conscientização postural e ergonômica, e a parceria com a UNICSUL.
  - `/contato` - Página "Contato", caso queira falar com o desenvolvedor. 

### Frontend
- **`templates/index.html`**: Estrutura HTML da página principal. Inclui conteúdo informativo sobre ergonomia, anúncios (ad-banners com scroll horizontal), um formulário para cadastro de email (para recebimento de dicas e novidades), e a funcionalidade de leitura de texto em voz alta.
- **`templates/sobre.html`**: Página "Sobre" do projeto ERGOEDUCA. Apresenta os objetivos de conscientização sobre boa postura, cadeiras ergonômicas, e sua afiliação como projeto de extensão da UNICSUL. Contém banners e informações institucionais.
- **`templates/contato.html`**: Estrutura HTML da página de contato. Fornece informações ou um formulário para que os usuários possam entrar em contato com o desenvolvedor ou responsáveis pelo projeto.
- **`static/main.js`**: Lógica frontend. Responsável pela manipulação de eventos de formulário (como o de cadastro de email), interações da interface do usuário, e a funcionalidade de leitura de texto em voz alta (Text-to-Speech).
- **`static/style.css`**: Estiliza a aplicação. Define a aparência da navbar, banners, layout das páginas, botões, e garante a responsividade do site.
- **`templates/sobre.html`**: Página "Sobre" do projeto ERGOEDUCA, apresentando seus objetivos de conscientização sobre boa postura, cadeiras ergonômicas, e sua afiliação como projeto de extensão da UNICSUL. Contém banners e informações institucionais.

## Como Executar
1. Instale as dependências (recomenda-se uso de ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o servidor Flask:
   ```bash
   python app.py
   ```
3. Acesse a aplicação em [http://localhost:5000](http://localhost:5000)

## Licença
Este projeto é livre para uso educacional.
