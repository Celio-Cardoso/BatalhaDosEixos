import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Batalha dos Eixos", layout="wide")

# --- CONSTANTES E LÓGICA (Mantidas do seu código original) ---
EIXO_MIN = -20
EIXO_MAX = 20

CONFIG_FASES = {
    1: {"titulo": "O DESPERTAR DO FEIXE", "grau": 1, "inimigos": 1, "tipo": "Reta", "eq": "y = ax + b", "dica": "Ajuste 'a' (inclinação) e 'b' (altura)."},
    2: {"titulo": "A CURVA DE INTERCEPTAÇÃO", "grau": 2, "inimigos": 2, "tipo": "Parábola", "eq": "y = ax² + bx + c", "dica": "3 pontos definem a parábola."},
    3: {"titulo": "O ESPELHO DA SINGULARIDADE", "grau": 2, "inimigos": 1, "tipo": "Parábola Simétrica", "eq": "y = ax² + bx + c", "dica": "Use a simetria a seu favor."},
    4: {"titulo": "A TORMENTA CÚBICA", "grau": 3, "inimigos": 3, "tipo": "Cúbica", "eq": "y = ax³ + ...", "dica": "Uma curva sinuosa para 3 alvos."},
    5: {"titulo": "O PROTOCOLO FANTASMA", "grau": 3, "inimigos": 2, "tipo": "Cúbica Estratégica", "eq": "y = ax³ + ...", "dica": "Crie um ponto de apoio imaginário."}
}


def _calcular_y(x, coefs, grau):
    a = coefs.get('a', 0.0)
    b = coefs.get('b', 0.0)
    c = coefs.get('c', 0.0)
    d = coefs.get('d', 0.0)
    if grau == 1:
        return a * x + b
    elif grau == 2:
        return a * (x**2) + b * x + c
    elif grau == 3:
        return a * (x**3) + b * (x**2) + c * x + d
    return 0


def gerar_fase(fase_id):
    config = CONFIG_FASES[fase_id]
    grau = config['grau']

    # Lógica simplificada de geração para garantir que funcione rápido na web
    while True:
        coefs = {}
        if grau == 1:
            coefs['a'] = random.choice([-2, -1, -0.5, 0.5, 1, 2])
            coefs['b'] = random.randint(-8, 8)
        elif grau == 2:
            coefs['a'] = random.choice([-1, -0.5, 0.5, 1])
            coefs['b'] = random.randint(-5, 5)
            coefs['c'] = random.randint(-5, 5)
        else:
            coefs['a'] = random.choice([-0.25, 0.25, 0.5, -0.5])
            coefs['b'] = random.randint(-2, 2)
            coefs['c'] = random.randint(-5, 5)
            coefs['d'] = random.randint(-5, 5)

        pontos_x = random.sample(
            range(EIXO_MIN + 2, EIXO_MAX - 2), config['inimigos'] + 1)
        x_jog = pontos_x.pop(0)
        y_jog = _calcular_y(x_jog, coefs, grau)

        if not (EIXO_MIN <= y_jog <= EIXO_MAX):
            continue

        inimigos = []
        valido = True
        for x_ini in pontos_x:
            y_ini = _calcular_y(x_ini, coefs, grau)
            if not (EIXO_MIN <= y_ini <= EIXO_MAX):
                valido = False
                break
            inimigos.append({'x': x_ini, 'y': int(round(y_ini))})

        if valido:
            return {'jogador': {'x': x_jog, 'y': int(round(y_jog))}, 'inimigos': inimigos, 'config': config}


# --- INICIALIZAÇÃO DE ESTADO (SESSION STATE) ---
if 'fase_atual' not in st.session_state:
    st.session_state.fase_atual = 1
if 'dados_jogo' not in st.session_state:
    st.session_state.dados_jogo = gerar_fase(1)
if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0
if 'historico_tentativas' not in st.session_state:
    st.session_state.historico_tentativas = []
if 'msg_resultado' not in st.session_state:
    st.session_state.msg_resultado = ""

# --- INTERFACE ---
st.title("🚀 BATALHA DOS EIXOS: OPERAÇÃO CARTESIANA")
st.markdown(
    f"**Comandante:** Aluno(a) | **Pontuação:** {st.session_state.pontuacao}")

col1, col2 = st.columns([1, 2])

with col1:
    fase_id = st.session_state.fase_atual
    if fase_id > 5:
        st.success("🎉 PARABÉNS! VOCÊ SALVOU A REALIDADE!")
        st.write("Todas as missões foram concluídas.")
        if st.button("Reiniciar Jogo"):
            st.session_state.fase_atual = 1
            st.session_state.pontuacao = 0
            st.session_state.dados_jogo = gerar_fase(1)
            st.session_state.historico_tentativas = []
            st.rerun()
    else:
        dados = st.session_state.dados_jogo
        config = dados['config']

        st.subheader(f"MISSÃO {fase_id}: {config['titulo']}")
        st.info(f"🎯 Objetivo: {config['dica']}")
        st.code(config['eq'])

        st.write("### 📡 RADAR")
        st.write(
            f"📍 **Sua Nave:** ({dados['jogador']['x']}, {dados['jogador']['y']})")
        for i, ini in enumerate(dados['inimigos']):
            st.write(f"👾 **Inimigo {i+1}:** ({ini['x']}, {ini['y']})")

        st.write("### 🎛️ SISTEMA DE MIRA")
        with st.form("form_disparo"):
            c_a = st.number_input(
                "Coeficiente 'a'", value=0.0, step=0.1, format="%.2f")
            c_b = st.number_input(
                "Coeficiente 'b'", value=0.0, step=1.0, format="%.2f")
            c_c = 0.0
            c_d = 0.0

            if config['grau'] >= 2:
                c_c = st.number_input(
                    "Coeficiente 'c'", value=0.0, step=1.0, format="%.2f")
            if config['grau'] == 3:
                c_d = st.number_input(
                    "Coeficiente 'd'", value=0.0, step=1.0, format="%.2f")

            disparar = st.form_submit_button("🔥 DISPARAR")

        if disparar:
            coefs_usuario = {'a': c_a, 'b': c_b, 'c': c_c, 'd': c_d}

            # Verificação
            acertou = True
            # Verifica nave
            y_nave = _calcular_y(
                dados['jogador']['x'], coefs_usuario, config['grau'])
            if abs(y_nave - dados['jogador']['y']) > 0.5:
                acertou = False
                msg = f"❌ O feixe não saiu da sua nave! (Passou em y={y_nave:.1f})"
            else:
                # Verifica inimigos
                for ini in dados['inimigos']:
                    y_tiro = _calcular_y(
                        ini['x'], coefs_usuario, config['grau'])
                    if abs(y_tiro - ini['y']) > 0.5:
                        acertou = False
                        msg = f"❌ Errou o alvo em x={ini['x']} (Passou em y={y_tiro:.1f})"
                        break

            st.session_state.historico_tentativas.append(
                {'coefs': coefs_usuario, 'sucesso': acertou})

            if acertou:
                st.session_state.msg_resultado = "✅ ALVO DESTRUÍDO! Avançando..."
                st.session_state.pontuacao += 1000
                st.session_state.fase_atual += 1
                if st.session_state.fase_atual <= 5:
                    st.session_state.dados_jogo = gerar_fase(
                        st.session_state.fase_atual)
                    st.session_state.historico_tentativas = []  # Limpa histórico na nova fase
                st.rerun()
            else:
                st.session_state.msg_resultado = msg

        if st.session_state.msg_resultado:
            if "❌" in st.session_state.msg_resultado:
                st.error(st.session_state.msg_resultado)
            else:
                st.success(st.session_state.msg_resultado)

with col2:
    # --- GRÁFICO MATPLOTLIB ---
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(EIXO_MIN, EIXO_MAX)
    ax.set_ylim(EIXO_MIN, EIXO_MAX)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Desenhar elementos se não terminou
    if st.session_state.fase_atual <= 5:
        d = st.session_state.dados_jogo
        # Nave
        ax.plot(d['jogador']['x'], d['jogador']['y'], '^',
                color='blue', markersize=12, label='Sua Nave')
        # Inimigos
        for ini in d['inimigos']:
            ax.plot(ini['x'], ini['y'], 'o', color='red',
                    markersize=10, label='Inimigo')

        # Histórico de tentativas
        x_vals = np.linspace(EIXO_MIN, EIXO_MAX, 400)
        for tent in st.session_state.historico_tentativas:
            y_vals = [_calcular_y(x, tent['coefs'], d['config']['grau'])
                      for x in x_vals]
            cor = 'green' if tent['sucesso'] else 'gray'
            estilo = '-' if tent['sucesso'] else '--'
            alpha = 1.0 if tent['sucesso'] else 0.5
            ax.plot(x_vals, y_vals, color=cor, linestyle=estilo, alpha=alpha)

    st.pyplot(fig)
