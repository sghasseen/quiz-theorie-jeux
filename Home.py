"""
🎮 MIASHS - Quiz Théorie des Jeux
Application complète tout-en-un
"""

import streamlit as st
import random
from fractions import Fraction

st.set_page_config(
    page_title="MIASHS - Théorie des Jeux",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS GLOBAL
# ============================================
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    
    p, span, div, label, h1, h2, h3 { color: #000000 !important; }
    
    .stButton > button {
        background-color: #000000;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
    }
    .stButton > button:hover { background-color: #333; }
    
    .guide-section {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #000;
    }
    
    .situation-box {
        background: #f5f5f5;
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    
    .matrice-table {
        width: 100%;
        max-width: 320px;
        margin: 10px auto;
        border-collapse: collapse;
    }
    
    .matrice-table td {
        padding: 12px;
        text-align: center;
        border: 1px solid #000;
    }
    
    .matrice-table .header {
        font-weight: bold;
        background: #e0e0e0;
    }
    
    .matrice-table .cell {
        background: #ffffff;
        font-size: 15px;
    }
    
    .explication {
        background: #f9f9f9;
        border-left: 4px solid #000000;
        padding: 16px 20px;
        margin: 16px 0;
        border-radius: 0 12px 12px 0;
    }
    
    .step {
        background: #ffffff;
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    
    .concept-tag {
        background: #e0e0e0;
        color: #000 !important;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #000;
    }
    
    .bloc-card {
        background: #f5f5f5;
        border: 2px solid #000;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "guide_seen" not in st.session_state:
    st.session_state.guide_seen = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "menu"
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_idx" not in st.session_state:
    st.session_state.quiz_idx = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None

# ============================================
# CODES D'ACCÈS
# ============================================
VALID_CODES = {"TDJ2024", "NASH", "PARETO", "JEUX", "MIASHS"}

# ============================================
# HELPERS
# ============================================
def frac(x):
    if isinstance(x, Fraction):
        f = x
    else:
        f = Fraction(x).limit_denominator(100)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"

# ============================================
# PAGE LOGIN
# ============================================
def page_login():
    st.markdown('<div style="text-align:center;font-size:80px;margin-top:50px;">🎮</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center;margin-bottom:5px;">MIASHS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#666!important;font-size:18px;">Quiz Théorie des Jeux</p>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        code = st.text_input("🔐 Code d'accès", type="password", placeholder="Entre le code...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Entrer", use_container_width=True):
            if code.upper() in VALID_CODES:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Code incorrect")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#999!important;font-size:12px;">Demande le code à ton pote 😉</p>', unsafe_allow_html=True)

# ============================================
# PAGE GUIDE
# ============================================
def page_guide():
    st.markdown('<div style="text-align:center;font-size:48px;margin-top:20px;">🎮</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center;">Bienvenue !</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#666!important;">Ton guide pour réussir l\'exam de Théorie des Jeux</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="guide-section">
        <h3>📖 NIVEAU 1 — Découverte</h3>
        <p><b>T'es perdu ?</b> → Mode <b>"Étudier"</b></p>
        <p>⏱️ 1h-2h | 📊 Note : Tu survis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="guide-section">
        <h3>✏️ NIVEAU 2 — Absorption</h3>
        <p><b>Tu connais les concepts ?</b> → Mode <b>"QCM"</b> (52 questions)</p>
        <p>⏱️ 2h-3h | 📊 Note : 10-12/20 ✅</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="guide-section">
        <h3>🎯 NIVEAU 3 — Application</h3>
        <p><b>Tu veux te tester ?</b> → <b>Quiz Chronométré</b></p>
        <p>⏱️ 20 min | 📊 Note : 12-15/20 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="guide-section">
        <h3>🏆 NIVEAU 4 — Maîtrise</h3>
        <p><b>Tu veux 15+ ?</b> → <b>Exercices Rédaction</b> (bientôt)</p>
        <p style="font-size:12px;color:#888!important;">(sauf si t'es autiste, là c'est 20/20)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 C'est parti !", use_container_width=True):
            st.session_state.guide_seen = True
            st.rerun()

# ============================================
# PAGE MENU PRINCIPAL
# ============================================
def page_menu():
    st.markdown('<h1 style="text-align:center;">🎮 MIASHS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#666!important;margin-bottom:30px;">Choisis ton bloc de révision</p>', unsafe_allow_html=True)
    
    # Bloc A
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="bloc-card"><span style="font-size:40px;">🎯</span><br><b>Bloc A</b><br>Jeux Finis<br><small>18 questions</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 Étudier", key="etude_a", use_container_width=True):
                st.session_state.current_page = "etude_a"
                st.rerun()
        with c2:
            if st.button("✏️ QCM", key="qcm_a", use_container_width=True):
                st.session_state.current_page = "qcm_a"
                st.session_state.quiz_data = None
                st.rerun()
    
    with col2:
        st.markdown('<div class="bloc-card"><span style="font-size:40px;">📈</span><br><b>Bloc B</b><br>Jeux Continus<br><small>12 questions</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 Étudier", key="etude_b", use_container_width=True):
                st.session_state.current_page = "etude_b"
                st.rerun()
        with c2:
            if st.button("✏️ QCM", key="qcm_b", use_container_width=True):
                st.session_state.current_page = "qcm_b"
                st.session_state.quiz_data = None
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="bloc-card"><span style="font-size:40px;">🎲</span><br><b>Bloc C</b><br>Stratégies Mixtes<br><small>12 questions</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 Étudier", key="etude_c", use_container_width=True):
                st.session_state.current_page = "etude_c"
                st.rerun()
        with c2:
            if st.button("✏️ QCM", key="qcm_c", use_container_width=True):
                st.session_state.current_page = "qcm_c"
                st.session_state.quiz_data = None
                st.rerun()
    
    with col2:
        st.markdown('<div class="bloc-card"><span style="font-size:40px;">⚖️</span><br><b>Bloc D</b><br>Somme Nulle<br><small>10 questions</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 Étudier", key="etude_d", use_container_width=True):
                st.session_state.current_page = "etude_d"
                st.rerun()
        with c2:
            if st.button("✏️ QCM", key="qcm_d", use_container_width=True):
                st.session_state.current_page = "qcm_d"
                st.session_state.quiz_data = None
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📋 Guide", use_container_width=True):
            st.session_state.guide_seen = False
            st.rerun()
    with col3:
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.guide_seen = False
            st.session_state.current_page = "menu"
            st.rerun()

# ============================================
# PAGES ÉTUDIER
# ============================================
def page_etude_a():
    if st.button("← Retour au menu"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown("# 📖 Bloc A — Jeux Finis")
    
    st.markdown("""
    ## 1. Lire une matrice de gains
    Chaque case contient **(gain J1, gain J2)**.
    - **J1** = joueur ligne
    - **J2** = joueur colonne
    
    ---
    ## 2. Meilleure Réponse (BR)
    La BR de J1 = stratégie qui **maximise son gain** quand J2 joue une stratégie donnée.
    
    **Méthode du soulignement :**
    - Pour J1 : souligner le max de chaque **colonne**
    - Pour J2 : souligner le max de chaque **ligne**
    
    ---
    ## 3. Équilibre de Nash
    Profil où **personne ne veut dévier**.
    → Case avec **2 soulignements** = équilibre
    
    ---
    ## 4. Dominance
    - **Strictement dominée** : Toujours strictement moins bonne
    - **Faiblement dominée** : Toujours ≤ et parfois <
    - **EISD** : Éliminer les dominées une par une
    
    ---
    ## 5. Optimum de Pareto
    Issue où on ne peut améliorer un joueur **sans dégrader l'autre**.
    
    ⚠️ L'équilibre de Nash n'est pas toujours Pareto-optimal !
    """)

def page_etude_b():
    if st.button("← Retour au menu"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown("# 📖 Bloc B — Jeux Continus")
    
    st.markdown("""
    ## 1. Trouver la BR
    1. Écrire g₁(x, y)
    2. Dériver : ∂g₁/∂x
    3. Poser ∂g₁/∂x = 0 (CPO)
    4. Résoudre pour x → BR₁(y)
    
    ---
    ## 2. Équilibre de Nash
    Résoudre le système :
    - x = BR₁(y)
    - y = BR₂(x)
    
    **Graphiquement** = intersection des BR
    
    ---
    ## 3. Vérification
    - CSO : ∂²g₁/∂x² < 0 (max, pas min)
    - Bornes : si BR hors domaine → prendre le bord
    """)

def page_etude_c():
    if st.button("← Retour au menu"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown("# 📖 Bloc C — Stratégies Mixtes")
    
    st.markdown("""
    ## 1. Quand les utiliser ?
    Quand il n'y a **pas d'équilibre pur** (aucune case avec 2 soulignements)
    
    ---
    ## 2. Définition
    - J1 joue H avec proba **p**, B avec proba **(1-p)**
    - J2 joue G avec proba **q**, D avec proba **(1-q)**
    
    ---
    ## 3. Principe d'indifférence ⚠️
    **C'est le piège classique !**
    
    - Pour trouver **p*** : rendre **J2** indifférent
    - Pour trouver **q*** : rendre **J1** indifférent
    
    On rend l'**autre** indifférent, pas soi-même !
    
    ---
    ## 4. Calcul
    E[J2 | G] = E[J2 | D] → résoudre pour p*
    E[J1 | H] = E[J1 | B] → résoudre pour q*
    """)

def page_etude_d():
    if st.button("← Retour au menu"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown("# 📖 Bloc D — Somme Nulle")
    
    st.markdown("""
    ## 1. Définition
    g₁ + g₂ = 0 → Ce que J1 gagne, J2 le perd
    
    ---
    ## 2. Maximin (J1)
    1. Pour chaque ligne : calculer le **min**
    2. Choisir la ligne qui **maximise** ce min
    
    ---
    ## 3. Minimax (J2)
    1. Pour chaque colonne : calculer le **max**
    2. Choisir la colonne qui **minimise** ce max
    
    ---
    ## 4. Point-selle
    Si **maximin = minimax** → point-selle existe
    → Les stratégies prudentes = équilibre de Nash
    
    ---
    ## 5. Valeur du jeu
    = gain de J1 à l'équilibre = maximin = minimax
    """)

# ============================================
# GÉNÉRATEUR BLOC A
# ============================================
def generer_situation_a():
    while True:
        matrice = [[(random.randint(0, 9), random.randint(0, 9)) for _ in range(2)] for _ in range(2)]
        
        br1 = {}
        for j in range(2):
            gains = [matrice[i][j][0] for i in range(2)]
            max_g = max(gains)
            br1[j] = [i for i in range(2) if gains[i] == max_g]
        
        br2 = {}
        for i in range(2):
            gains = [matrice[i][j][1] for j in range(2)]
            max_g = max(gains)
            br2[i] = [j for j in range(2) if gains[j] == max_g]
        
        equilibres = []
        for i in range(2):
            for j in range(2):
                if i in br1[j] and j in br2[i]:
                    equilibres.append((i, j))
        
        if len(equilibres) == 1:
            break
    
    return {
        "matrice": matrice,
        "br1": br1,
        "br2": br2,
        "equilibres": equilibres
    }

def generer_questions_a(sit):
    m = sit["matrice"]
    br1 = sit["br1"]
    br2 = sit["br2"]
    eq = sit["equilibres"][0]
    L = ["H", "B"]
    C = ["G", "D"]
    
    questions = []
    
    # Q1: Lire gain J1
    i, j = random.randint(0, 1), random.randint(0, 1)
    questions.append({
        "concept": "Lecture matrice",
        "question": f"Quel est le gain de <b>J1</b> en ({L[i]}, {C[j]}) ?",
        "choix": {"A": str(m[i][j][0]), "B": str(m[i][j][1]), "C": str(m[1-i][j][0]), "D": str(m[i][1-j][0])},
        "reponse": "A",
        "explication": f"En ({L[i]}, {C[j]}), la case contient ({m[i][j][0]}, {m[i][j][1]}). Le premier nombre = gain J1 = <b>{m[i][j][0]}</b>"
    })
    
    # Q2: BR de J1
    j_test = random.randint(0, 1)
    br_correct = br1[j_test][0]
    questions.append({
        "concept": "Meilleure réponse",
        "question": f"Quelle est la BR de J1 si J2 joue <b>{C[j_test]}</b> ?",
        "choix": {"A": L[br_correct], "B": L[1-br_correct], "C": "Les deux", "D": "Aucune"},
        "reponse": "A",
        "explication": f"Colonne {C[j_test]} : J1 compare {m[0][j_test][0]} (H) vs {m[1][j_test][0]} (B). Max = {max(m[0][j_test][0], m[1][j_test][0])} → BR = <b>{L[br_correct]}</b>"
    })
    
    # Q3: Équilibre de Nash
    questions.append({
        "concept": "Équilibre de Nash",
        "question": "Quel est l'équilibre de Nash ?",
        "choix": {"A": f"({L[eq[0]]}, {C[eq[1]]})", "B": f"({L[1-eq[0]]}, {C[eq[1]]})", "C": f"({L[eq[0]]}, {C[1-eq[1]]})", "D": "Pas d'équilibre"},
        "reponse": "A",
        "explication": f"En utilisant le soulignement, seule la case ({L[eq[0]]}, {C[eq[1]]}) a 2 soulignements → <b>Équilibre de Nash</b>"
    })
    
    # Q4: Gains à l'équilibre
    questions.append({
        "concept": "Gains équilibre",
        "question": f"Quels sont les gains à l'équilibre ({L[eq[0]]}, {C[eq[1]]}) ?",
        "choix": {"A": f"({m[eq[0]][eq[1]][0]}, {m[eq[0]][eq[1]][1]})", "B": f"({m[eq[0]][eq[1]][1]}, {m[eq[0]][eq[1]][0]})", "C": f"({m[1-eq[0]][eq[1]][0]}, {m[1-eq[0]][eq[1]][1]})", "D": "(0, 0)"},
        "reponse": "A",
        "explication": f"À l'équilibre ({L[eq[0]]}, {C[eq[1]]}), les gains sont <b>({m[eq[0]][eq[1]][0]}, {m[eq[0]][eq[1]][1]})</b>"
    })
    
    return questions

# ============================================
# GÉNÉRATEUR BLOC C (Stratégies Mixtes)
# ============================================
def generer_situation_c():
    while True:
        a, b = random.randint(0, 4), random.randint(5, 9)
        c, d = random.randint(5, 9), random.randint(0, 4)
        a2, b2 = random.randint(5, 9), random.randint(0, 4)
        c2, d2 = random.randint(0, 4), random.randint(5, 9)
        
        matrice = [[(a, a2), (b, b2)], [(c, c2), (d, d2)]]
        
        # Vérifier pas d'équilibre pur
        br1_G = 0 if a >= c else 1
        br1_D = 0 if b >= d else 1
        br2_H = 0 if a2 >= b2 else 1
        br2_B = 0 if c2 >= d2 else 1
        
        eq_purs = []
        if br1_G == 0 and br2_H == 0: eq_purs.append((0, 0))
        if br1_D == 0 and br2_H == 1: eq_purs.append((0, 1))
        if br1_G == 1 and br2_B == 0: eq_purs.append((1, 0))
        if br1_D == 1 and br2_B == 1: eq_purs.append((1, 1))
        
        if len(eq_purs) == 0:
            break
    
    denom_p = a2 - c2 - b2 + d2
    p_star = Fraction(d2 - c2, denom_p) if denom_p != 0 else Fraction(1, 2)
    
    denom_q = a - b - c + d
    q_star = Fraction(d - b, denom_q) if denom_q != 0 else Fraction(1, 2)
    
    return {
        "matrice": matrice,
        "a": a, "b": b, "c": c, "d": d,
        "a2": a2, "b2": b2, "c2": c2, "d2": d2,
        "p_star": p_star.limit_denominator(100),
        "q_star": q_star.limit_denominator(100)
    }

def generer_questions_c(sit):
    m = sit["matrice"]
    p_star, q_star = sit["p_star"], sit["q_star"]
    
    questions = []
    
    questions.append({
        "concept": "Équilibre pur",
        "question": "Ce jeu a-t-il un équilibre en stratégies pures ?",
        "choix": {"A": "Non", "B": "Oui, en (H, G)", "C": "Oui, en (B, D)", "D": "Oui, plusieurs"},
        "reponse": "A",
        "explication": "Aucune case n'a 2 soulignements → pas d'équilibre pur → il faut chercher en <b>stratégies mixtes</b>"
    })
    
    questions.append({
        "concept": "Principe d'indifférence",
        "question": "Pour trouver p*, on rend quel joueur indifférent ?",
        "choix": {"A": "J2", "B": "J1", "C": "Les deux", "D": "Aucun"},
        "reponse": "A",
        "explication": "Pour trouver p* (proba de J1), on rend <b>J2</b> indifférent entre G et D. C'est contre-intuitif !"
    })
    
    questions.append({
        "concept": "Calcul p*",
        "question": f"p* = ?",
        "choix": {"A": frac(p_star), "B": frac(1 - p_star), "C": "1/2", "D": frac(q_star)},
        "reponse": "A",
        "explication": f"E[J2|G] = E[J2|D] donne <b>p* = {frac(p_star)}</b>"
    })
    
    questions.append({
        "concept": "Calcul q*",
        "question": f"q* = ?",
        "choix": {"A": frac(q_star), "B": frac(1 - q_star), "C": "1/2", "D": frac(p_star)},
        "reponse": "A",
        "explication": f"E[J1|H] = E[J1|B] donne <b>q* = {frac(q_star)}</b>"
    })
    
    return questions

# ============================================
# GÉNÉRATEUR BLOC D (Somme Nulle)
# ============================================
def generer_situation_d():
    while True:
        matrice = [[random.randint(-5, 5) for _ in range(3)] for _ in range(2)]
        
        mins_lignes = [min(row) for row in matrice]
        maximin = max(mins_lignes)
        
        maxs_colonnes = [max(matrice[i][j] for i in range(2)) for j in range(3)]
        minimax = min(maxs_colonnes)
        
        if maximin == minimax:
            break
    
    return {
        "matrice": matrice,
        "maximin": maximin,
        "minimax": minimax,
        "ligne_maximin": mins_lignes.index(maximin),
        "col_minimax": maxs_colonnes.index(minimax)
    }

def generer_questions_d(sit):
    m = sit["matrice"]
    maximin = sit["maximin"]
    minimax = sit["minimax"]
    L = ["H", "B"]
    C = ["G", "M", "D"]
    
    questions = []
    
    questions.append({
        "concept": "Somme nulle",
        "question": "Que signifie 'somme nulle' ?",
        "choix": {"A": "g₂ = -g₁", "B": "g₁ = g₂", "C": "g₁ + g₂ > 0", "D": "Pas d'équilibre"},
        "reponse": "A",
        "explication": "Somme nulle = ce que J1 gagne, J2 le perd → <b>g₂ = -g₁</b>"
    })
    
    questions.append({
        "concept": "Maximin",
        "question": f"La valeur maximin est ?",
        "choix": {"A": str(maximin), "B": str(minimax + 1), "C": str(max(max(row) for row in m)), "D": "0"},
        "reponse": "A",
        "explication": f"Maximin = max des min de chaque ligne = <b>{maximin}</b>"
    })
    
    questions.append({
        "concept": "Point-selle",
        "question": "Y a-t-il un point-selle ?",
        "choix": {"A": "Oui", "B": "Non", "C": "Impossible à dire", "D": "Seulement en mixte"},
        "reponse": "A",
        "explication": f"Maximin ({maximin}) = Minimax ({minimax}) → <b>Point-selle OUI</b>"
    })
    
    questions.append({
        "concept": "Valeur du jeu",
        "question": "Quelle est la valeur du jeu ?",
        "choix": {"A": str(maximin), "B": "0", "C": str(maximin + 1), "D": str(maximin - 1)},
        "reponse": "A",
        "explication": f"Valeur = maximin = minimax = <b>{maximin}</b>"
    })
    
    return questions

# ============================================
# PAGE QCM GÉNÉRIQUE
# ============================================
def page_qcm(bloc):
    if st.button("← Retour au menu"):
        st.session_state.current_page = "menu"
        st.session_state.quiz_data = None
        st.rerun()
    
    titres = {"a": "🎯 Bloc A — Jeux Finis", "b": "📈 Bloc B — Jeux Continus", "c": "🎲 Bloc C — Stratégies Mixtes", "d": "⚖️ Bloc D — Somme Nulle"}
    st.markdown(f"# {titres[bloc]}")
    
    # Générer les questions si nécessaire
    if st.session_state.quiz_data is None:
        if bloc == "a":
            sit = generer_situation_a()
            questions = generer_questions_a(sit)
            st.session_state.quiz_data = {"sit": sit, "questions": questions, "bloc": bloc}
        elif bloc == "c":
            sit = generer_situation_c()
            questions = generer_questions_c(sit)
            st.session_state.quiz_data = {"sit": sit, "questions": questions, "bloc": bloc}
        elif bloc == "d":
            sit = generer_situation_d()
            questions = generer_questions_d(sit)
            st.session_state.quiz_data = {"sit": sit, "questions": questions, "bloc": bloc}
        else:
            st.info("Ce bloc est en cours de développement. Reviens bientôt !")
            return
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.rerun()
    
    data = st.session_state.quiz_data
    questions = data["questions"]
    idx = st.session_state.quiz_idx
    
    if idx >= len(questions):
        # Résultats
        score = st.session_state.quiz_score
        pct = score / len(questions) * 100
        st.markdown(f"""
        <div style="text-align:center;padding:40px;">
            <div style="font-size:80px;">{"🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"}</div>
            <h2>{score}/{len(questions)} ({pct:.0f}%)</h2>
            <p>{"Excellent !" if pct >= 80 else "Bien joué !" if pct >= 60 else "Continue à réviser !"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Recommencer", use_container_width=True):
            st.session_state.quiz_data = None
            st.rerun()
        return
    
    # Afficher la situation
    sit = data["sit"]
    if bloc == "a" or bloc == "c":
        m = sit["matrice"]
        st.markdown(f"""
        <div class="situation-box">
            <table class="matrice-table">
                <tr><td class="header"></td><td class="header">G</td><td class="header">D</td></tr>
                <tr><td class="header">H</td><td class="cell">({m[0][0][0]}, {m[0][0][1]})</td><td class="cell">({m[0][1][0]}, {m[0][1][1]})</td></tr>
                <tr><td class="header">B</td><td class="cell">({m[1][0][0]}, {m[1][0][1]})</td><td class="cell">({m[1][1][0]}, {m[1][1][1]})</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    elif bloc == "d":
        m = sit["matrice"]
        st.markdown(f"""
        <div class="situation-box">
            <p><b>Jeu à somme nulle</b> (gains de J1)</p>
            <table class="matrice-table">
                <tr><td class="header"></td><td class="header">G</td><td class="header">M</td><td class="header">D</td></tr>
                <tr><td class="header">H</td><td class="cell">{m[0][0]}</td><td class="cell">{m[0][1]}</td><td class="cell">{m[0][2]}</td></tr>
                <tr><td class="header">B</td><td class="cell">{m[1][0]}</td><td class="cell">{m[1][1]}</td><td class="cell">{m[1][2]}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    # Question
    q = questions[idx]
    st.markdown(f"**Q{idx+1}/{len(questions)}** — Score: {st.session_state.quiz_score}")
    st.markdown(f"<span class='concept-tag'>{q['concept']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;margin-top:10px;'>{q['question']}</p>", unsafe_allow_html=True)
    
    if not st.session_state.quiz_answered:
        for lettre, texte in q["choix"].items():
            if st.button(f"{lettre}. {texte}", key=f"btn_{lettre}", use_container_width=True):
                st.session_state.quiz_selected = lettre
                st.session_state.quiz_answered = True
                if lettre == q["reponse"]:
                    st.session_state.quiz_score += 1
                st.rerun()
    else:
        for lettre, texte in q["choix"].items():
            if lettre == q["reponse"]:
                st.success(f"✓ {lettre}. {texte}")
            elif lettre == st.session_state.quiz_selected:
                st.error(f"✗ {lettre}. {texte}")
            else:
                st.markdown(f"<div style='opacity:0.5;padding:10px;'>{lettre}. {texte}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='explication'><b>💡 Explication</b><br>{q['explication']}</div>", unsafe_allow_html=True)
        
        if st.button("Suivant →", use_container_width=True):
            st.session_state.quiz_idx += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected = None
            st.rerun()

# ============================================
# MAIN ROUTER
# ============================================
if not st.session_state.authenticated:
    page_login()
elif not st.session_state.guide_seen:
    page_guide()
elif st.session_state.current_page == "menu":
    page_menu()
elif st.session_state.current_page == "etude_a":
    page_etude_a()
elif st.session_state.current_page == "etude_b":
    page_etude_b()
elif st.session_state.current_page == "etude_c":
    page_etude_c()
elif st.session_state.current_page == "etude_d":
    page_etude_d()
elif st.session_state.current_page == "qcm_a":
    page_qcm("a")
elif st.session_state.current_page == "qcm_b":
    page_qcm("b")
elif st.session_state.current_page == "qcm_c":
    page_qcm("c")
elif st.session_state.current_page == "qcm_d":
    page_qcm("d")
else:
    page_menu()