# ==========================================================
# Desenvolvido por Marcos Vinicius - github.com/MarcosViniicius
# ==========================================================
#
# MODO PORTFÓLIO / VITRINE (sem backend ativo)
# -----------------------------------------------
# Este arquivo foi refatorado para funcionar sem banco de dados
# ou serviço de e-mail, mantendo toda a lógica de backend
# comentada para reativação futura.
#
# Para reativar o backend completo:
#   1. Descomente os blocos marcados com [BACKEND - REATIVAR]
#   2. Configure o arquivo .env com as credenciais corretas
#   3. Instale as dependências: pip install -r requirements.txt
#   4. Remova o parâmetro mock das rotas que usam dados estáticos
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import logging
import urllib.parse
from datetime import datetime

# ----------------------------------------------------------
# [BACKEND - REATIVAR] Imports necessários para integração completa
# ----------------------------------------------------------
# from dotenv import load_dotenv
# import psycopg2
# from psycopg2 import pool
# from flask_mail import Mail, Message
# from email.mime.image import MIMEImage
# from io import BytesIO
# ----------------------------------------------------------

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# [BACKEND - REATIVAR] Carrega variáveis de ambiente do .env
# ----------------------------------------------------------
# load_dotenv()
# ----------------------------------------------------------

# Configuração do Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_padrao")

# ----------------------------------------------------------
# [BACKEND - REATIVAR] Configuração do Flask-Mail (envio de e-mails)
# Para reativar: descomente este bloco e o bloco `mail = Mail(app)` abaixo
# ----------------------------------------------------------
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
# app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
# mail = Mail(app)
# ----------------------------------------------------------

# ----------------------------------------------------------
# [BACKEND - REATIVAR] Variáveis de ambiente para PostgreSQL
# ----------------------------------------------------------
# USER   = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST   = os.getenv("host")
# PORT   = os.getenv("port")
# DBNAME = os.getenv("dbname")
# ----------------------------------------------------------

# ----------------------------------------------------------
# [BACKEND - REATIVAR] Pool de conexões com PostgreSQL
# Para reativar: descomente este bloco
# ----------------------------------------------------------
# try:
#     connection_pool = psycopg2.pool.SimpleConnectionPool(
#         5,   # minconn
#         20,  # maxconn
#         user=USER,
#         password=PASSWORD,
#         host=HOST,
#         port=PORT,
#         dbname=DBNAME
#     )
#     logger.info("Pool de conexões inicializado com sucesso!")
# except Exception as e:
#     logger.error(f"Erro ao inicializar o pool de conexões: {e}")
#     connection_pool = None
connection_pool = None  # Desativado no modo portfólio
# ----------------------------------------------------------


def get_db_connection():
    """Obtém uma conexão do pool e retorna a conexão e o cursor.
    
    [BACKEND - REATIVAR] Para reativar, descomente o corpo desta função
    e ative o connection_pool acima.
    """
    # if connection_pool:
    #     try:
    #         conn = connection_pool.getconn()
    #         cursor = conn.cursor()
    #         return conn, cursor
    #     except Exception as e:
    #         logger.error(f"Erro ao obter conexão do pool: {e}")
    #         return None, None
    return None, None  # sem banco no modo portfólio


def release_db_connection(conn):
    """Devolve a conexão ao pool.
    
    [BACKEND - REATIVAR] Para reativar, descomente o corpo desta função.
    """
    # if connection_pool and conn:
    #     connection_pool.putconn(conn)
    pass  # sem banco no modo portfólio


def flash_with_logging(message, category="message"):
    """Função personalizada para registrar mensagens de flash no terminal."""
    logger.info(f"Flash message - Categoria: {category}, Mensagem: {message}")
    flash(message, category)


# ----------------------------------------------------------
# DADOS ESTÁTICOS (modo portfólio)
# [BACKEND - REATIVAR] Substituir pelas queries ao banco de dados
# nas respectivas rotas abaixo quando reativar o backend
# ----------------------------------------------------------

PRESENTES_DISPONIVEIS = [
    "Papete Branca TAM. 36",
    "Jansport Mini Mochila Misty Rose",
    "Zara Tênis Hello Kitty TAM. 36",
    "Cartão presente C&A",
    "Kit Skincare Neutrogena",
    "Colar Dourado Delicado",
    "Livro: O Diário de Bridget Jones",
    "Perfume La Vie Est Belle Lancôme 30ml",
    "Bolsa Pequena Retrô Rosa",
    "Mimo de 100 reais",
]

PRESENTES_INFO = {
    "Papete Branca TAM. 36": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://i.imgur.com/IxWjkp4.jpeg",
        "link_compra": ""
    },
    "Jansport Mini Mochila Misty Rose": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://i.imgur.com/PsDWkUA.png",
        "link_compra": ""
    },
    "Zara Tênis Hello Kitty TAM. 36": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://i.imgur.com/tenis_placeholder.jpeg",
        "link_compra": ""
    },
    "Cartão presente C&A": {
        "max": 2, "reservado": 0,
        "imagem_url": "https://cea.vtexassets.com/arquivos/ids/59283743/giftcard_01-1--1-.png?v=638957169206400000",
        "link_compra": "https://www.cea.com.br/cartao-presente---arcos-3001701-arcos/p"
    },
    "Kit Skincare Neutrogena": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://www.mercadolivre.com.br/kit-limpeza-facial-neutrogena-purified-hydro-boost-original/up/MLBU1719170910#polycard_client=search-desktop&search_layout=grid&position=5&type=product&tracking_id=15d09a64-064d-41ba-b464-fe2ab866cf0b&wid=MLB2015466592&sid=search",
        "link_compra": ""
    },
    "Colar Dourado Delicado": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://www.mercadolivre.com.br/colar-dourado-delicado-up/MLB2015466592#polycard_client=search-desktop&search_layout=grid&position=5&type=product&tracking_id=15d09a64-064d-41ba-b464-fe2ab866cf0b&wid=MLB2015466592&sid=search",
        "link_compra": ""
    },
    "Perfume La Vie Est Belle Lancôme 30ml": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://i.imgur.com/FUQgB2y.png",
        "link_compra": ""
    },
    "Bolsa Pequena Retrô Rosa": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://i.imgur.com/7Vxuol7.png",
        "link_compra": ""
    },
    "Mimo de 100 reais": {
        "max": 5, "reservado": 0,
        "imagem_url": "https://i.imgur.com/def3Vu5.png",
        "link_compra": ""
    },
    "Livro: O Diário de Bridget Jones": {
        "max": 1, "reservado": 0,
        "imagem_url": "https://www.google.com/aclk?sa=L&ai=DChsSEwijjbaLlZ6TAxWLVEgAHVeiH94YACICCAEQAxoCY2U&co=1&ase=2&gclid=EAIaIQobChMIo422i5WekwMVi1RIAB1Xoh_eEAQYASABEgJuAPD_BwE&cid=CAASuwHkaG9wasidHKN7etDIH0_UKJ3TJGOenoU0K1fjwgWcpr4frsGnumvCg8nO0rL6-iZVYwcOlK3UGN4NuDwKCnVzEoBrRPRqHG50bnS070m4D9wm3vu-creKK3muXZ2ubUKmCO5pcy9UUBfYQqExIe9fFCxrOUi93qJsqRw3Syzo2-GnWvDR8f2nx3jzbILOKeixXcqo0MBWhgdi8JMkfmvzFwcOKAr4HQ1RG89O6hcrpCWXNOIRK_GjzK_i&cce=2&category=acrcp_v1_32&sig=AOD64_3qbffGrzuEYxVbPcwoDAWERRUTlg&ctype=5&q=&nis=4&ved=2ahUKEwim6rCLlZ6TAxWwGLkGHbzdJbgQwg8oAXoECDEQDA&adurl=",
        "link_compra": ""
    },
}

# Participantes mockados para exibição na página /confirmados
# [BACKEND - REATIVAR] Substituir pela query: SELECT id, nome, confirmado, presente, data_confirmacao FROM participante
PARTICIPANTES_MOCK = [
    (1, "Maria Oliveira",   True, "Papete Branca TAM. 36",          "2025-05-10"),
    (2, "João Almeida",     True, None,                              "2025-05-11"),
    (3, "Fernanda Lima",    True, "Cartão presente C&A",             "2025-05-12"),
    (4, "Lucas Souza",      True, "Mimo de 100 reais",               "2025-05-13"),
    (5, "Carolina Mendes",  True, "Kit Skincare Neutrogena",         "2025-05-14"),
    (6, "Rafael Costa",     True, None,                              "2025-05-15"),
    (7, "Ana Paula Ramos",  True, "Colar Dourado Delicado",          "2025-05-16"),
    (8, "Thiago Barbosa",   True, "Livro: O Diário de Bridget Jones","2025-05-17"),
]

# ----------------------------------------------------------


@app.route('/')
def index():
    """Página principal — modo portfólio com dados estáticos.
    
    [BACKEND - REATIVAR] Para integração com banco de dados:
      1. Descomente os blocos de consulta abaixo
      2. Comente/remova os dados estáticos PRESENTES_DISPONIVEIS e PRESENTES_INFO
      3. Use conn, cursor = get_db_connection() para buscar os dados reais
    """
    # ----------------------------------------------------------
    # [BACKEND - REATIVAR] Consultas ao banco de dados PostgreSQL
    # ----------------------------------------------------------
    # conn, cursor = get_db_connection()
    # participantes = []
    # presentes_disponiveis = []
    # presentes_esgotados = []
    # presentes_info = {}
    # try:
    #     if cursor:
    #         cursor.execute("""
    #             SELECT nome, quantidade_maxima, quantidade_reservada, imagem_url, link_compra
    #               FROM presentes
    #              WHERE disponivel = TRUE
    #                AND (quantidade_reservada < quantidade_maxima)
    #         """)
    #         todos_presentes = cursor.fetchall()
    #         presentes_disponiveis = [row[0] for row in todos_presentes]
    #         presentes_info = {row[0]: {'max': row[1], 'reservado': row[2], 'imagem_url': row[3], 'link_compra': row[4]} for row in todos_presentes}
    #
    #         cursor.execute("""
    #             SELECT nome, quantidade_maxima, quantidade_reservada, imagem_url, link_compra
    #               FROM presentes
    #              WHERE disponivel = TRUE
    #                AND (quantidade_reservada >= quantidade_maxima)
    #         """)
    #         presentes_esgotados_dados = cursor.fetchall()
    #         presentes_esgotados = [row[0] for row in presentes_esgotados_dados]
    #         for row in presentes_esgotados_dados:
    #             presentes_info[row[0]] = {'max': row[1], 'reservado': row[2], 'imagem_url': row[3], 'link_compra': row[4]}
    #
    #         cursor.execute("SELECT id, nome, confirmado, presente, data_confirmacao FROM participante;")
    #         participantes = cursor.fetchall()
    #         presentes_disponiveis = sorted(presentes_disponiveis)
    #         presentes_esgotados = sorted(presentes_esgotados)
    #     else:
    #         flash("Não foi possível conectar ao banco de dados. Tente novamente mais tarde.", "error")
    # except Exception as e:
    #     logger.error(f"Erro ao consultar dados: {e}")
    #     flash("Ocorreu um erro ao carregar os dados. Por favor, tente novamente.", "error")
    # finally:
    #     if cursor: cursor.close()
    #     release_db_connection(conn)
    # ----------------------------------------------------------

    # Dados estáticos (modo portfólio)
    presentes_disponiveis = sorted(PRESENTES_DISPONIVEIS)
    presentes_esgotados = []   # nenhum esgotado no modo demonstração
    presentes_info = PRESENTES_INFO
    participante_id = None     # não utilizado no modo portfólio

    # Variáveis de ambiente para exibição (modo portfólio/vitrine)
    mail_remetente = os.getenv("MAIL_USERNAME", "confirmacaoanabeariz15@gmail.com")

    return render_template(
        'index.html',
        participantes=[],
        disponiveis=presentes_disponiveis,
        esgotados=presentes_esgotados,
        presentes_info=presentes_info,
        participante_id=participante_id,
        mail_remetente=mail_remetente
    )


# ----------------------------------------------------------
# [BACKEND - REATIVAR] Função de envio de e-mail de confirmação
# Para reativar: descomente todo este bloco e ative Flask-Mail acima
# ----------------------------------------------------------
def enviar_email_confirmacao(email, nome, confirmado, quantidade_pessoas, presente, forma_presente, mimo_100=False):
    """Envia e-mail de confirmação de presença.
    
    [BACKEND - REATIVAR] Função desativada no modo portfólio.
    Para reativar:
      1. Ative a configuração do Flask-Mail no topo deste arquivo
      2. Descomente o corpo desta função abaixo
    """
    logger.info(f"[PORTFÓLIO] Simulação de e-mail para {email} — envio real desativado.")
    # try:
    #     referencias_presentes = {}
    #     img_url = None
    #     link_compra = None
    #     if presente:
    #         conn, cursor = get_db_connection()
    #         if cursor:
    #             cursor.execute("SELECT imagem_url, link_compra FROM presentes WHERE nome = %s", (presente,))
    #             row = cursor.fetchone()
    #             if row:
    #                 img_url = row[0]
    #                 link_compra = row[1]
    #             cursor.close()
    #             release_db_connection(conn)
    #
    #     assunto = "Confirmação de Presença - 15 Anos da Ana"
    #     # [corpo do e-mail HTML omitido para brevidade — preservado no git]
    #     msg = Message(
    #         assunto,
    #         sender=app.config['MAIL_USERNAME'],
    #         recipients=[email],
    #         reply_to=app.config['MAIL_USERNAME']
    #     )
    #     # msg.body = corpo_texto
    #     # msg.html = corpo_html
    #     mail.send(msg)
    #     logger.info(f"E-mail enviado com sucesso para {email}")
    # except Exception as e:
    #     logger.error(f"Erro ao enviar e-mail para {email}: {e}")
# ----------------------------------------------------------


@app.route('/confirmar', methods=['POST'])
def confirmar():
    """Rota de confirmação de presença — modo portfólio (sem persistência).
    
    [BACKEND - REATIVAR] Para integração real:
      1. Descomente os blocos de INSERT/UPDATE no banco de dados abaixo
      2. Reative a chamada enviar_email_confirmacao()
      3. Remova o bloco de flash simulado
    """
    nome_submetido = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    confirmado_status = request.form.get('confirmado')
    quantidade_pessoas = request.form.get('quantidade_pessoas')
    presente_selecionado = request.form.get('presente')
    forma_presente = request.form.get('forma_presente')

    logger.info(
        f"[PORTFÓLIO] Confirmação simulada — Nome: '{nome_submetido}', "
        f"Status: '{confirmado_status}', Presente: '{presente_selecionado}', "
        f"Forma: '{forma_presente}'"
    )

    # Validações básicas de frontend
    if not nome_submetido or not email:
        flash("Por favor, informe seu nome completo e e-mail.", "error")
        return redirect((request.referrer or url_for('index')) + "#formConfirmacao")

    # ----------------------------------------------------------
    # [BACKEND - REATIVAR] Persistência no banco de dados e envio de e-mail
    # ----------------------------------------------------------
    # agora = datetime.now()
    # mimo_100 = presente_selecionado and presente_selecionado.strip().lower() == "mimo de 100 reais"
    # is_pix = (mimo_100 or forma_presente == "pix")
    # presente_db = None if is_pix else presente_selecionado
    #
    # conn, cursor = get_db_connection()
    # if not conn or not cursor:
    #     flash("Erro ao conectar ao banco de dados. Tente novamente.", "error")
    #     return redirect(url_for('index') + "#formConfirmacao")
    # try:
    #     if confirmado_status == 'sim':
    #         cursor.execute("""
    #             INSERT INTO participante (nome, email, confirmado, quantidade_pessoas, presente, data_confirmacao, pix)
    #             VALUES (%s, %s, TRUE, %s, %s, %s, %s);
    #         """, (nome_submetido, email, quantidade_pessoas, presente_db, agora, is_pix))
    #         conn.commit()
    #         if presente_db:
    #             cursor.execute(
    #                 "UPDATE presentes SET quantidade_reservada = quantidade_reservada + 1 WHERE nome = %s;",
    #                 (presente_db,)
    #             )
    #             conn.commit()
    #         enviar_email_confirmacao(email, nome_submetido, confirmado_status, quantidade_pessoas, presente_selecionado, forma_presente, mimo_100)
    #         if is_pix:
    #             flash("Presença confirmada! Não se esqueça de enviar o comprovante do Pix.", "success")
    #             return redirect(url_for('pix'))
    #         else:
    #             flash("Sua presença foi confirmada com sucesso!", "success")
    #     elif confirmado_status == 'nao':
    #         cursor.execute("""
    #             INSERT INTO participante (nome, email, confirmado, quantidade_pessoas, presente, data_confirmacao, pix)
    #             VALUES (%s, %s, FALSE, NULL, NULL, %s, FALSE);
    #         """, (nome_submetido, email, agora))
    #         conn.commit()
    #         flash("Resposta registrada. Que pena que não poderá comparecer!", "info")
    # except Exception as e:
    #     conn.rollback()
    #     logger.error(f"Erro ao processar confirmação: {e}")
    #     flash("Ocorreu um erro ao processar sua confirmação.", "error")
    # finally:
    #     release_db_connection(conn)
    # ----------------------------------------------------------

    # Simulação de resposta para o modo portfólio
    mimo_100 = presente_selecionado and presente_selecionado.strip().lower() == "mimo de 100 reais"
    is_pix = (mimo_100 or forma_presente == "pix")

    if confirmado_status == 'sim':
        if is_pix:
            flash("Presença confirmada! Não se esqueça de enviar o comprovante do Pix.", "success")
            return redirect(url_for('pix'))
        else:
            flash("Sua presença foi confirmada com sucesso!", "success")
    elif confirmado_status == 'nao':
        flash("Resposta registrada. Que pena que não poderá comparecer!", "info")
    else:
        flash("Por favor, informe se você vai comparecer.", "error")

    return redirect(url_for('index') + "#formConfirmacao")


@app.route('/confirmados')
def confirmados():
    """Lista de participantes confirmados — modo portfólio com dados mockados.
    
    [BACKEND - REATIVAR] Para integração real:
      1. Descomente os blocos de consulta abaixo
      2. Remova o uso de PARTICIPANTES_MOCK
    """
    # ----------------------------------------------------------
    # [BACKEND - REATIVAR] Consulta ao banco de dados
    # ----------------------------------------------------------
    # conn, cursor = get_db_connection()
    # participantes_confirmados = []
    # presentes_disponiveis = []
    # try:
    #     if cursor:
    #         cursor.execute("SELECT id, nome, confirmado, presente, data_confirmacao FROM participante WHERE confirmado = TRUE ORDER BY data_confirmacao DESC LIMIT 50;")
    #         participantes_confirmados = cursor.fetchall()
    #         cursor.execute("SELECT nome FROM presentes WHERE disponivel = TRUE LIMIT 10;")
    #         presentes_disponiveis = [row[0] for row in cursor.fetchall()]
    # except Exception as e:
    #     logger.error(f"Erro ao consultar dados: {e}")
    #     flash(f"Ocorreu um erro ao carregar os dados. Por favor, tente novamente.", "error")
    # finally:
    #     if cursor: cursor.close()
    #     release_db_connection(conn)
    # ----------------------------------------------------------

    # Dados mockados para modo portfólio
    participantes_confirmados = PARTICIPANTES_MOCK
    presentes_disponiveis = sorted(PRESENTES_DISPONIVEIS)

    return render_template(
        'confirmados.html',
        participantes=participantes_confirmados,
        disponiveis=presentes_disponiveis
    )


@app.route('/calendar-link')
def calendar_link():
    """Gera link para adicionar o evento ao Google Calendar."""
    try:
        event_title = urllib.parse.quote("15 anos de Ana Beatriz🥳🎉")
        location = urllib.parse.quote("Av. Comandante Petit, 263 - Centro, Parnamirim - RN")
        details = urllib.parse.quote("Venha comemorar comigo!")
        start = '20250614T230000Z'
        end = '20250615T025900Z'
        link = (
            f"https://www.google.com/calendar/render?action=TEMPLATE"
            f"&text={event_title}&dates={start}/{end}"
            f"&details={details}&location={location}&sf=true&output=xml"
        )
        return redirect(link)
    except Exception as e:
        logger.error(f"Erro ao gerar link do calendário: {e}")
        flash("Não foi possível gerar o link para o calendário.", "error")
        return redirect(url_for('index'))


@app.route('/pix')
def pix():
    """Página de instruções para pagamento via Pix.
    
    [BACKEND - REATIVAR] Configure CHAVE_PIX, WHATSAPP_ORGANIZADOR, 
    NOME_TITULAR e BANCO_TITULAR no .env para exibir dados reais.
    """
    # Lidos de variáveis de ambiente para não expor dados em código-fonte público
    chave_pix = os.getenv("CHAVE_PIX", "[configurar no .env]")
    numero_whatsapp = os.getenv("WHATSAPP_ORGANIZADOR", "")
    nome_titular = os.getenv("NOME_TITULAR", "[Nome do Titular]")
    banco_titular = os.getenv("BANCO_TITULAR", "[Nome do Banco]")
    
    return render_template(
        'pix.html', 
        chave_pix=chave_pix, 
        numero_whatsapp=numero_whatsapp,
        nome_titular=nome_titular,
        banco_titular=banco_titular
    )


# ----------------------------------------------------------
# [BACKEND - REATIVAR] Rotas administrativas (requerem banco de dados ativo)
# Para reativar: descomente o corpo de cada função abaixo
# ATENÇÃO: estas rotas não possuem autenticação — adicione proteção antes de reativar
# ----------------------------------------------------------

@app.route('/admin/excluir_participantes', methods=['POST'])
def excluir_participantes():
    """[BACKEND - REATIVAR] Exclui participantes do banco de dados.
    Desativado no modo portfólio.
    """
    # ids = request.json.get('ids', [])
    # if not ids:
    #     return jsonify(sucesso=False)
    # ids = [int(i) for i in ids]
    # conn, cursor = get_db_connection()
    # try:
    #     cursor.execute("SELECT presente FROM participante WHERE id = ANY(%s)", (ids,))
    #     presentes = [row[0] for row in cursor.fetchall() if row[0]]
    #     for presente in presentes:
    #         cursor.execute("UPDATE presentes SET quantidade_reservada = GREATEST(quantidade_reservada - 1, 0) WHERE nome = %s", (presente,))
    #     cursor.execute("DELETE FROM participante WHERE id = ANY(%s)", (ids,))
    #     conn.commit()
    #     return jsonify(sucesso=True)
    # except Exception as e:
    #     conn.rollback()
    #     logger.error(f"Erro ao excluir participantes: {e}")
    #     return jsonify(sucesso=False)
    # finally:
    #     if cursor: cursor.close()
    #     release_db_connection(conn)
    logger.info("[PORTFÓLIO] Tentativa de excluir participante — backend desativado.")
    return jsonify(sucesso=False, mensagem="Backend desativado no modo portfólio.")


@app.route('/admin/reestabelecer_indice', methods=['POST'])
def reestabelecer_indice():
    """[BACKEND - REATIVAR] Reestabelece o índice de ID no banco de dados.
    Desativado no modo portfólio.
    """
    # conn, cursor = get_db_connection()
    # try:
    #     cursor.execute("SELECT setval('participante_id_seq', (SELECT COALESCE(MAX(id), 1) FROM participante) + 1, false);")
    #     conn.commit()
    #     return jsonify(sucesso=True)
    # except Exception as e:
    #     conn.rollback()
    #     return jsonify(sucesso=False)
    # finally:
    #     if cursor: cursor.close()
    #     release_db_connection(conn)
    logger.info("[PORTFÓLIO] Tentativa de reestabelecer índice — backend desativado.")
    return jsonify(sucesso=False, mensagem="Backend desativado no modo portfólio.")


@app.route('/admin/atualizar_reservas', methods=['POST'])
def atualizar_reservas():
    """[BACKEND - REATIVAR] Sincroniza reservas de presentes com o banco de dados.
    Desativado no modo portfólio.
    """
    # conn, cursor = get_db_connection()
    # try:
    #     cursor.execute("UPDATE presentes SET quantidade_reservada = 0;")
    #     cursor.execute("SELECT presente, COUNT(*) FROM participante WHERE presente IS NOT NULL GROUP BY presente;")
    #     for presente, count in cursor.fetchall():
    #         cursor.execute("UPDATE presentes SET quantidade_reservada = %s WHERE nome = %s;", (count, presente))
    #     conn.commit()
    #     return jsonify(sucesso=True)
    # except Exception as e:
    #     conn.rollback()
    #     return jsonify(sucesso=False)
    # finally:
    #     if cursor: cursor.close()
    #     release_db_connection(conn)
    logger.info("[PORTFÓLIO] Tentativa de atualizar reservas — backend desativado.")
    return jsonify(sucesso=False, mensagem="Backend desativado no modo portfólio.")


# ----------------------------------------------------------
# [BACKEND - REATIVAR] Gerenciamento do pool de conexões
# ----------------------------------------------------------

def close_pool():
    """Fecha o pool de conexões ao encerrar a aplicação.
    [BACKEND - REATIVAR] Descomente quando reativar o pool.
    """
    # try:
    #     if connection_pool:
    #         connection_pool.closeall()
    # except Exception as e:
    #     logger.error(f"Erro ao fechar o pool de conexões: {e}")
    pass


def reconnect_pool():
    """Reconecta ao banco de dados se o pool estiver fechado.
    [BACKEND - REATIVAR] Descomente quando reativar o pool.
    """
    # global connection_pool
    # if connection_pool is None or connection_pool.closed:
    #     connection_pool = psycopg2.pool.SimpleConnectionPool(
    #         minconn=1, maxconn=10,
    #         user=USER, password=PASSWORD, host=HOST, dbname=DBNAME
    #     )
    pass


# ----------------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Renomear para 'application' como esperado pelo Vercel
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4800)
