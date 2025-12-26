import streamlit as st
import json
import os
import random
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Batalha dos Eixos",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (PARA MANTER A VIBE SCI-FI) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .success-text { color: #00ff00; }
    .danger-text { color: #ff4b4b; }
    .gold-text { color: #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- CONSTANTES E TEXTOS ---
ARQUIVO_DADOS = "batalha_eixos_dados.json"
EIXO_MIN = -20
EIXO_MAX = 20

CORES_FROTA = {
    "Azul Aliança": "#0099ff",
    "Verde Vida": "#00ff00",
    "Vermelho Marte": "#ff3333",
    "Roxo Nebulosa": "#bf00ff",
    "Laranja Solar": "#ff9900",
    "Preto Furtivo": "#505050"
}

TEXTO_PROLOGO = """
### ANO DE 2437 - OPERAÇÃO HORIZONTE CARTESIANO

No início do século XXIV, a humanidade cruzou o limiar das estrelas. 
Tudo mudou quando encontramos **A Desordem**. Seus agentes, Naves de Instabilidade, são manifestações físicas de equações desfeitas.

**SUA MISSÃO**
Você é o operador do **Canhão de Singularidade**. 
Esta arma dispara **Feixes de Funções**: projeções de energia moldadas em trajetórias matemáticas puras (Lineares, Quadráticas, Cúbicas).

Cada acerto desfaz uma manifestação da Desordem. 
O destino dos eixos está em suas mãos.
"""

TEXTO_VITORIA_FINAL = """
### PARABÉNS! MISSÃO CUMPRIDA.

Você neutralizou a ameaça. Os Pilares de Estabilidade brilham novamente.
Você provou que a Matemática é a linguagem universal da ordem.

**PRÓXIMO PASSO:**
O infinito é sua próxima coordenada.
"""

CONFIG_FASES = {
    1: {"titulo": "O DESPERTAR DO FEIXE", "inimigos": 1, "grau": 1, "alvo": "Batedores da Desordem", "relatorio": "Naves batedoras em linha reta.", "dica": "y = ax + b. 'a' é a inclinação, 'b' é onde corta o Y.", "armamento": "y = ax + b"},
    2: {"titulo": "A CURVA DE INTERCEPTAÇÃO", "inimigos": 2, "grau": 2, "alvo": "Fragatas de Ataque", "relatorio": "Inimigo usa escudos curvos. Use uma parábola.", "dica": "3 pontos definem uma parábola única.", "armamento": "y = ax² + bx + c"},
    3: {"titulo": "O ESPELHO DA SINGULARIDADE", "inimigos": 1, "grau": 2, "alvo": "Nave-Mãe Furtiva", "relatorio": "Trajetória parabólica simétrica.", "dica": "Use a simetria do vértice.", "armamento": "y = ax² + bx + c"},
    4: {"titulo": "A TORMENTA CÚBICA", "inimigos": 3, "grau": 3, "alvo": "Esquadrão Triplo", "relatorio": "Comboio em formação complexa.", "dica": "Curva cúbica para 4 pontos.", "armamento": "y = ax³ + bx² + cx + d"},
    5: {"titulo": "O PROTOCOLO FANTASMA", "inimigos": 2, "grau": 3, "alvo": "Comandantes Supremos", "relatorio": "Invente um ponto de suporte.", "dica": "Escolha um ponto livre para fechar o sistema.", "armamento": "y = ax³ + bx² + cx + d"},
}

# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {}
    try:
        with open(ARQUIVO_DADOS, 'r') as f:
            return json.load(f)
    except:
        return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(dados, f, indent=4)

# --- LÓGICA MATEMÁTICA ---
def calcular_y(x, coefs, grau):
    a = float(coefs.get('a', 0))
    b = float(coefs.get('b', 0))
    c = float(coefs.get('c', 0))
    d = float(coefs.get('d', 0))
    if grau == 1: return a * x + b
    elif grau == 2: return a * (x**2) + b * x + c
    elif grau == 3: return a * (x**3) + b * (x**2) + c * x + d
    return 0

def gerar_fase(config_fase):
    grau = config_fase['grau']
    # Loop de segurança para garantir coordenadas válidas na tela
    for _ in range(100): 
        coefs = {}
        if grau == 1:
            coefs['a'] = random.choice([-2, -1, -0.5, 0.5, 1, 2])
            coefs['b'] = random.randint(-8, 8)
        elif grau == 2:
            coefs['a'] = random.choice([-1, -0.5, 0.5, 1])
            coefs['b'] = random.randint(-5, 5)
            coefs['c'] = random.randint(-5, 5)
        else:
            coefs['a'] = random.choice([-0.5, 0.5, 0.25, -0.25])
            coefs['b'] = random.randint(-2, 2)
            coefs['c'] = random.randint(-5, 5)
            coefs['d'] = random.randint(-5, 5)

        qtd_pontos = config_fase['inimigos'] + 1
        pontos_x = random.sample(range(EIXO_MIN + 2, EIXO_MAX - 2), qtd_pontos)
        x_jog = pontos_x.pop(0)
        y_jog = calcular_y(x_jog, coefs, grau)

        if not (EIXO_MIN <= y_jog <= EIXO_MAX): continue

        inimigos = []
        valido = True
        for x_ini in pontos_x:
            y_ini = calcular_y(x_ini, coefs, grau)
            if not (EIXO_MIN <= y_ini <= EIXO_MAX) or abs(y_ini - round(y_ini)) > 0.001:
                valido = False; break
            inimigos.append({'x': x_ini, 'y': int(round(y_ini))})

        if valido:
            return {'jogador': {'x': x_jog, 'y': int(round(y_jog))}, 'inimigos': inimigos, 'solucao_gerada': coefs, 'config': config_fase}
    return None # Fallback

# --- GRÁFICOS ---
def plotar_grafico(fase_atual, historico_tentativas, user_cor):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(EIXO_MIN, EIXO_MAX)
    ax.set_ylim(EIXO_MIN, EIXO_MAX)
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Plotar Elementos
    jog = fase_atual['jogador']
    ax.plot(jog['x'], jog['y'], marker='^', color=user_cor, markersize=12, label="Sua Nave")
    
    for i, ini in enumerate(fase_atual['inimigos']):
        ax.plot(ini['x'], ini['y'], 'ro', markersize=10, label=f"Alvo {i+1}")

    # Plotar Histórico
    x_vals = np.linspace(EIXO_MIN, EIXO_MAX, 200)
    grau = fase_atual['config']['grau']

    for tent in historico_tentativas:
        y_vals = [calcular_y(x, tent['coefs'], grau) for x in x_vals]
        cor = '#00cc00' if tent['sucesso'] else '#ffcccc'
        alpha = 1.0 if tent['sucesso'] else 0.5
        estilo = '-' if tent['sucesso'] else '--'
        ax.plot(x_vals, y_vals, color=cor, linestyle=estilo, alpha=alpha, linewidth=2)

    ax.legend()
    return fig

# --- INICIALIZAÇÃO DE ESTADO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'dados_jogo' not in st.session_state: st.session_state.dados_jogo = None
if 'tentativas' not in st.session_state: st.session_state.tentativas = 0
if 'historico_local' not in st.session_state: st.session_state.historico_local = []
if 'feedback_msg' not in st.session_state: st.session_state.feedback_msg = None

# --- PÁGINAS DO APLICATIVO ---

def tela_login():
    st.title("Batalha dos Eixos 🌌")
    st.subheader("Sistema de Defesa Cartesiano")
    
    dados = carregar_dados()
    
    tab1, tab2 = st.tabs(["Login", "Novo Recruta"])
    
    with tab1:
        with st.form("login_form"):
            user_input = st.selectbox("Selecione o Piloto", [""] + list(dados.keys()))
            pass_input = st.text_input("Código de Acesso", type="password")
            submitted = st.form_submit_button("Iniciar Sistema")
            
            if submitted:
                if user_input and dados[user_input]['matricula'] == pass_input:
                    st.session_state.usuario = user_input
                    st.session_state.pagina = 'menu'
                    st.success("Acesso Autorizado!")
                    st.rerun()
                else:
                    st.error("Acesso Negado.")

        # Opção de Deletar
        with st.expander("Zona de Perigo (Deletar Piloto)"):
             del_user = st.selectbox("Piloto a deletar", [""] + list(dados.keys()), key="del_sel")
             del_pass = st.text_input("Confirme a Senha", type="password", key="del_pass")
             if st.button("🗑️ DELETAR REGISTRO"):
                 if del_user and dados[del_user]['matricula'] == del_pass:
                     del dados[del_user]
                     salvar_dados(dados)
                     st.success("Registro apagado.")
                     st.rerun()
                 else:
                     st.error("Senha incorreta.")

    with tab2:
        with st.form("cadastro_form"):
            novo_nome = st.text_input("Nome de Guerra")
            nova_senha = st.text_input("Crie uma Senha", type="password")
            cor_frota = st.selectbox("Cor da Frota", list(CORES_FROTA.keys()))
            btn_cad = st.form_submit_button("Alistar-se")
            
            if btn_cad:
                if novo_nome and nova_senha:
                    if novo_nome in dados:
                        st.error("Piloto já existe.")
                    else:
                        dados[novo_nome] = {
                            "matricula": nova_senha, "fase_atual": 1, 
                            "pontuacao": 0, "medalhas": [], 
                            "historico_fases": {}, "cor_frota": CORES_FROTA[cor_frota]
                        }
                        salvar_dados(dados)
                        st.success("Recruta registrado! Faça login.")
                else:
                    st.warning("Preencha todos os dados.")

def tela_menu():
    st.title(f"Comandante {st.session_state.usuario} 🫡")
    dados = carregar_dados()
    user_data = dados[st.session_state.usuario]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pontuação", user_data.get('pontuacao', 0))
    col1.caption("Medalhas: " + ", ".join(user_data.get('medalhas', [])))
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Seletor de Missão")
        fase_atual = user_data.get('fase_atual', 1)
        
        for i in range(1, 6):
            conf = CONFIG_FASES[i]
            if i < fase_atual:
                st.button(f"✅ Missão {i}: {conf['titulo']}", disabled=True)
            elif i == fase_atual:
                if st.button(f"▶️ INICIAR Missão {i}: {conf['titulo']}", type="primary"):
                    st.session_state.dados_jogo = gerar_fase(conf)
                    st.session_state.tentativas = 0
                    st.session_state.historico_local = []
                    st.session_state.feedback_msg = None
                    st.session_state.pagina = 'jogo'
                    st.rerun()
            else:
                st.button(f"🔒 Missão {i}: Bloqueada", disabled=True)
                
    with c2:
        st.subheader("Base de Dados")
        if st.button("🏆 Hall da Fama"):
            st.session_state.pagina = 'ranking'
            st.rerun()
        if st.button("📜 Arquivos da Saga"):
            st.session_state.pagina = 'historia'
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.usuario = None
            st.session_state.pagina = 'login'
            st.rerun()

def tela_jogo():
    if not st.session_state.dados_jogo:
        st.session_state.pagina = 'menu'
        st.rerun()
        
    fase = st.session_state.dados_jogo
    config = fase['config']
    dados_user = carregar_dados()
    cor_user = dados_user[st.session_state.usuario].get('cor_frota', '#0099ff')
    
    st.sidebar.title(f"Missão {config['titulo']}")
    st.sidebar.info(config['relatorio'])
    st.sidebar.warning(f"Alvo: {config['alvo']}")
    
    with st.sidebar.expander("💡 Dica Tática"):
        st.markdown(config['dica'])
        st.latex(config['armamento'])
    
    if st.sidebar.button("Abortar Missão"):
        st.session_state.pagina = 'menu'
        st.rerun()

    # Layout Principal
    col_grafico, col_controles = st.columns([2, 1])
    
    with col_grafico:
        fig = plotar_grafico(fase, st.session_state.historico_local, cor_user)
        st.pyplot(fig)
        
        if st.session_state.feedback_msg:
            tipo, msg = st.session_state.feedback_msg
            if tipo == 'sucesso':
                st.success(msg)
                if st.button("Retornar à Base"):
                    st.session_state.pagina = 'menu'
                    st.rerun()
            else:
                st.error(msg)
    
    with col_controles:
        st.subheader("Painel de Controle de Disparo")
        st.markdown("Insira os coeficientes da função:")
        
        grau = config['grau']
        with st.form("disparo_form"):
            c1, c2 = st.columns(2)
            a = c1.number_input("a (x³ / x² / inclinação)", value=0.0, step=0.1, format="%.2f")
            b = c2.number_input("b (x² / x / intercepto)", value=0.0, step=0.1, format="%.2f")
            c = 0.0
            d = 0.0
            
            if grau >= 2:
                c = c1.number_input("c (x / constante)", value=0.0, step=0.1, format="%.2f")
            if grau >= 3:
                d = c2.number_input("d (constante)", value=0.0, step=0.1, format="%.2f")
                
            disparar = st.form_submit_button("🔥 DISPARAR FEIXE")
            
            if disparar:
                processar_disparo(a, b, c, d, fase, dados_user)

def processar_disparo(a, b, c, d, fase, dados_user):
    st.session_state.tentativas += 1
    coefs = {'a': a, 'b': b, 'c': c, 'd': d}
    grau = fase['config']['grau']
    
    # Verificação
    acertou = True
    msg_erro = ""
    
    # Checar nave (origem)
    y_nave = calcular_y(fase['jogador']['x'], coefs, grau)
    if abs(y_nave - fase['jogador']['y']) > 0.5: # Tolerância levemente maior para float
        acertou = False
        msg_erro = f"O feixe não saiu da sua nave! (Calculado y={y_nave:.2f})"
        
    # Checar inimigos
    if acertou:
        for i, ini in enumerate(fase['inimigos']):
            y_tiro = calcular_y(ini['x'], coefs, grau)
            if abs(y_tiro - ini['y']) > 0.5:
                acertou = False
                msg_erro = f"Errou o Inimigo {i+1}! (Calculado y={y_tiro:.2f})"
                break
    
    # Atualizar Histórico Local
    st.session_state.historico_local.append({'coefs': coefs, 'sucesso': acertou})
    
    if acertou:
        pontos = 1000 if st.session_state.tentativas == 1 else (500 if st.session_state.tentativas == 2 else 250)
        nome = st.session_state.usuario
        
        # Atualizar Save
        dados_user[nome]['pontuacao'] += pontos
        
        # Medalhas
        novas_medalhas = []
        if st.session_state.tentativas == 1 and "🎯 Sniper" not in dados_user[nome]['medalhas']:
            dados_user[nome]['medalhas'].append("🎯 Sniper")
            novas_medalhas.append("SNIPER MATEMÁTICO")
            
        fase_num = 1 # Descobrir numero da fase
        for k,v in CONFIG_FASES.items():
            if v['titulo'] == fase['config']['titulo']: fase_num = k
            
        if fase_num == 3 and "🔥 Mestre Parábola" not in dados_user[nome]['medalhas']:
            dados_user[nome]['medalhas'].append("🔥 Mestre Parábola")
            
        # Avançar Fase
        if fase_num == dados_user[nome]['fase_atual']:
            dados_user[nome]['fase_atual'] += 1
            
        salvar_dados(dados_user)
        
        msg_final = f"ALVO DESTRUÍDO! +{pontos} PONTOS."
        if novas_medalhas: msg_final += f" MEDALHAS: {', '.join(novas_medalhas)}"
        
        st.session_state.feedback_msg = ('sucesso', msg_final)
        
        if fase_num == 5:
            st.session_state.pagina = 'vitoria_final'
            st.rerun()
            
    else:
        st.session_state.feedback_msg = ('erro', f"FALHA: {msg_erro}")
        if st.session_state.tentativas == 5:
             nome = st.session_state.usuario
             if "🧠 Persistente" not in dados_user[nome]['medalhas']:
                 dados_user[nome]['medalhas'].append("🧠 Persistente")
                 salvar_dados(dados_user)
                 st.toast("Medalha ganha: 🧠 Persistente")
    
    st.rerun()

def tela_ranking():
    st.title("🏆 Hall da Fama")
    dados = carregar_dados()
    
    lista = []
    for nome, info in dados.items():
        lista.append({
            "Piloto": nome,
            "Fase": info.get('fase_atual', 1),
            "Pontos": info.get('pontuacao', 0),
            "Medalhas": len(info.get('medalhas', []))
        })
    
    # Ordenar
    lista = sorted(lista, key=lambda x: x['Pontos'], reverse=True)
    
    st.dataframe(lista, use_container_width=True)
    
    if st.button("Voltar ao Menu"):
        st.session_state.pagina = 'menu'
        st.rerun()

def tela_historia():
    st.title("Arquivos da Academia")
    st.markdown(TEXTO_PROLOGO)
    if st.button("Fechar Arquivo"):
        st.session_state.pagina = 'menu'
        st.rerun()

def tela_vitoria():
    st.title("🎉 VITÓRIA TOTAL 🎉")
    st.balloons()
    st.markdown(TEXTO_VITORIA_FINAL)
    if st.button("Voltar ao Menu Principal"):
        st.session_state.pagina = 'menu'
        st.rerun()

# --- ROTEADOR PRINCIPAL ---
if st.session_state.pagina == 'login':
    tela_login()
elif st.session_state.pagina == 'menu':
    tela_menu()
elif st.session_state.pagina == 'jogo':
    tela_jogo()
elif st.session_state.pagina == 'ranking':
    tela_ranking()
elif st.session_state.pagina == 'historia':
    tela_historia()
elif st.session_state.pagina == 'vitoria_final':
    tela_vitoria()
