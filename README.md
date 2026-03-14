# 🎀 Birthday 15 — Landing Page

> Landing page de convite digital para festa de 15 anos, desenvolvida com Flask (Python).  
> Atualmente configurada como **vitrine de portfólio** — funciona 100% sem backend ativo.

**Desenvolvido por** [Marcos Vinicius](https://github.com/MarcosViniicius)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tech Stack](#-tech-stack)
- [Modos de Operação](#-modos-de-operação)
- [Como Executar](#-como-executar)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Reativando o Backend](#-reativando-o-backend)
- [Segurança](#-segurança)
- [Deploy (Vercel)](#-deploy-vercel)

---

## 🌟 Visão Geral

Site de convite digital para festa de 15 anos com:
- Página principal com countdown, informações do evento e formulário de confirmação de presença
- Lista de presentes integrada diretamente no convite
- Página de participantes confirmados
- Página de pagamento via Pix
- Integração com Google Calendar
- Design responsivo com Bootstrap 5

---

## ✨ Funcionalidades

| Funcionalidade | Modo Portfólio | Modo Backend Ativo |
|---|:---:|:---:|
| Página principal e informações | ✅ | ✅ |
| Formulário de confirmação (UX) | ✅ | ✅ |
| Lista de presentes (dados estáticos) | ✅ | ✅ |
| Flash messages de sucesso/erro | ✅ | ✅ |
| Página de Pix | ✅ | ✅ |
| Link Google Calendar | ✅ | ✅ |
| Persistência no PostgreSQL | ❌ | ✅ |
| Envio de e-mail de confirmação | ❌ | ✅ |
| Lista de confirmados em tempo real | ❌ (mock) | ✅ |
| Ferramentas administrativas | ❌ | ✅ |

---

## 📁 Estrutura do Projeto

```
birthday15-landingpage-backend/
│
├── index.py                  # Aplicação Flask principal
├── test_index.py             # Testes automatizados (pytest)
├── requirements.txt          # Dependências Python
├── vercel.json               # Configuração de deploy no Vercel
├── .env.example              # Exemplo de variáveis de ambiente
│
├── templates/                # Templates Jinja2 (HTML)
│   ├── index.html            # Página principal do convite
│   ├── confirmados.html      # Lista de participantes confirmados
│   ├── pix.html              # Página de pagamento via Pix
│   └── 404.html              # Página de erro 404
│
└── static/                   # Arquivos estáticos
    ├── css/
    │   └── style.css         # Estilos personalizados
    └── js/
        ├── main.js           # Lógica do formulário e interações
        └── countdown.js      # Countdown até o evento
```

---

## 🛠 Tech Stack

**Backend**
- [Python 3.x](https://python.org)
- [Flask](https://flask.palletsprojects.com/) — framework web
- [psycopg2](https://pypi.org/project/psycopg2/) — driver PostgreSQL *(desativado no modo portfólio)*
- [Flask-Mail](https://flask-mail.readthedocs.io/) — envio de e-mails *(desativado no modo portfólio)*
- [python-dotenv](https://pypi.org/project/python-dotenv/) — gerenciamento de variáveis de ambiente

**Frontend**
- [Bootstrap 5.3](https://getbootstrap.com/)
- [Animate.css](https://animate.style/)
- [Google Fonts](https://fonts.google.com/) (Great Vibes + Open Sans)
- Vanilla JavaScript

**Infraestrutura**
- [Vercel](https://vercel.com/) — deploy serverless (Python)
- [PostgreSQL](https://www.postgresql.org/) — banco de dados *(reativável)*

---

## 🔄 Modos de Operação

### Modo Portfólio (padrão atual)

O projeto funciona **sem nenhuma dependência de backend ativo**. Todos os dados (presentes, participantes confirmados, chave Pix) são estáticos ou configurados via variáveis de ambiente.

- ✅ Nenhum banco de dados necessário
- ✅ Nenhum servidor de e-mail necessário
- ✅ Formulários funcionam visualmente (UX completo) mas sem persistência
- ✅ Seguro para deploy público

### Modo Backend Completo (para uso real em evento)

Quando reativado, o sistema:

- Persiste confirmações no PostgreSQL
- Envia e-mails de confirmação via SMTP (Gmail)
- Exibe lista de participantes em tempo real
- Permite ferramentas administrativas (excluir, reestabelecer índice, atualizar reservas)

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+
- pip

### Instalação

```powershell
# 1. Clone o repositório
git clone https://github.com/MarcosViniicius/birthday15-landingpage-backend.git
cd birthday15-landingpage-backend

# 2. Crie e ative um ambiente virtual
python -m venv venf
venf\Scripts\activate  # Windows
# source venf/bin/activate  # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# 5. Execute o servidor
python index.py
```

O site estará disponível em `http://localhost:4800`.

### Executar Testes

```powershell
pip install pytest pytest-mock
python -m pytest test_index.py -v
```

---

## 🔐 Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha as variáveis necessárias.

| Variável | Obrigatória | Descrição |
|---|:---:|---|
| `SECRET_KEY` | ✅ | Chave secreta do Flask (sessions/flash) |
| `CHAVE_PIX` | ⚠️ | Chave Pix do organizador (exibida na página /pix) |
| `WHATSAPP_ORGANIZADOR` | ⚠️ | Número WhatsApp com DDI (ex: `+5584999999999`) |
| `MAIL_USERNAME` | 🔴 Backend | E-mail remetente para confirmações |
| `MAIL_PASSWORD` | 🔴 Backend | Senha de app do e-mail remetente |
| `user` | 🔴 Backend | Usuário do PostgreSQL |
| `password` | 🔴 Backend | Senha do PostgreSQL |
| `host` | 🔴 Backend | Host do banco de dados |
| `port` | 🔴 Backend | Porta do PostgreSQL (padrão: 5432) |
| `dbname` | 🔴 Backend | Nome do banco de dados |

> **⚠️** = Opcional no modo portfólio, mas recomendado para exibir dados reais  
> **🔴 Backend** = Necessário apenas quando reativar o backend completo

---

## ♻️ Reativando o Backend

Todo o código de backend está preservado em comentários com a tag `[BACKEND - REATIVAR]`.

### Passo a passo

1. **Configure o `.env`** com todas as credenciais (PostgreSQL + SMTP)

2. **Em `index.py`**, descomente os blocos marcados:
   - Imports: `dotenv`, `psycopg2`, `flask_mail`
   - Configuração Flask-Mail
   - Variáveis de ambiente do banco
   - Pool de conexões PostgreSQL
   - Corpo de `get_db_connection()` e `release_db_connection()`
   - Corpo de `enviar_email_confirmacao()`
   - Blocos de query SQL nas rotas `/`, `POST /confirmar`, `/confirmados`
   - Rotas `/admin/*`

3. **Em `templates/confirmados.html`**, descomente os blocos `fetch()` nas funções admin JS

4. **Crie as tabelas no PostgreSQL:**

```sql
CREATE TABLE participante (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    confirmado BOOLEAN DEFAULT FALSE,
    quantidade_pessoas INTEGER,
    presente VARCHAR(255),
    data_confirmacao TIMESTAMP,
    pix BOOLEAN DEFAULT FALSE
);

CREATE TABLE presentes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    quantidade_maxima INTEGER DEFAULT 1,
    quantidade_reservada INTEGER DEFAULT 0,
    imagem_url TEXT,
    link_compra TEXT
);
```

5. **Para e-mail via Gmail:** gere uma [Senha de App](https://support.google.com/accounts/answer/185833) e use-a em `MAIL_PASSWORD`

---

## 🔒 Segurança

### Modo Portfólio (atual)

- ✅ Nenhuma credencial exposta no código-fonte
- ✅ Chave Pix e WhatsApp lidos de variáveis de ambiente (`.env` — fora do controle de versão)
- ✅ Formulários não transmitem dados para servidores externos
- ✅ Nenhum dado é persistido (local ou remotamente)
- ✅ Rotas `/admin/*` retornam erro sem executar nenhuma operação
- ✅ `.env` listado no `.gitignore`

### Ao reativar o backend

- ⚠️ Adicione autenticação às rotas `/admin/*` antes de usar em produção
- ⚠️ Use HTTPS em produção para proteger dados do formulário
- ⚠️ Valide e sanitize inputs no servidor
- ⚠️ Nunca commite o arquivo `.env` com credenciais reais

---

## ☁️ Deploy (Vercel)

O projeto já está configurado para deploy no Vercel como função serverless Python.

```json
// vercel.json
{
  "version": 2,
  "builds": [{ "src": "index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "index.py" }]
}
```

**Para fazer deploy:**

```bash
# Instale o Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Configure as variáveis de ambiente no painel do Vercel em  
**Project Settings → Environment Variables**.

---

## 📄 Licença

Projeto desenvolvido para uso pessoal/portfólio.  
© 2025 Marcos Vinicius — [github.com/MarcosViniicius](https://github.com/MarcosViniicius)
