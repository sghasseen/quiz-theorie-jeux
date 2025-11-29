"""
BLOC D - JEUX À SOMME NULLE
Exercice complet avec ~10 questions couvrant tous les concepts des TDs
"""

import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Bloc D - Somme Nulle", page_icon="⚖️", layout="centered")

# CSS NOIR ET BLANC UNIQUEMENT
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Tout en noir sur blanc */
    p, span, div, label, h1, h2, h3 { color: #000000 !important; }
    
    .situation-box {
        background: #f5f5f5;
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    
    .matrice-table {
        width: 100%;
        max-width: 350px;
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
    
    .correct-box {
        background: #ffffff;
        border: 3px solid #000000;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .incorrect-box {
        background: #ffffff;
        border: 3px dashed #000000;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
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
    
    .warning {
        background: #fff;
        border-left: 4px solid #000;
        padding: 10px 14px;
        margin: 10px 0;
        font-size: 13px;
        font-style: italic;
    }
    
    .tip {
        background: #fff;
        border-left: 4px solid #000;
        padding: 10px 14px;
        margin: 10px 0;
        font-size: 13px;
    }
    
    .stButton > button {
        background-color: #000000;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover { background-color: #333; }
    
    .concept-tag {
        background: #e0e0e0;
        color: #000 !important;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #000;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if "sit_d" not in st.session_state:
    st.session_state.sit_d = None
if "questions_d" not in st.session_state:
    st.session_state.questions_d = []
if "idx_d" not in st.session_state:
    st.session_state.idx_d = 0
if "score_d" not in st.session_state:
    st.session_state.score_d = 0
if "answered_d" not in st.session_state:
    st.session_state.answered_d = False
if "selected_d" not in st.session_state:
    st.session_state.selected_d = None
if "started_d" not in st.session_state:
    st.session_state.started_d = False


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
# GÉNÉRATION DE LA SITUATION
# ============================================

def generer_situation():
    """Génère un jeu à somme nulle 2x3 ou 3x2"""
    
    # On fait 2x3 (J1 a 2 stratégies, J2 a 3)
    lignes = ["H", "B"]
    colonnes = ["G", "M", "D"]
    
    while True:
        # Matrice des gains de J1 (J2 gagne l'opposé)
        matrice = []
        for i in range(2):
            row = []
            for j in range(3):
                row.append(random.randint(-5, 5))
            matrice.append(row)
        
        # Calculer maximin (J1) et minimax (J2)
        # Maximin J1 : pour chaque ligne, min sur colonnes, puis max
        mins_lignes = [min(row) for row in matrice]
        maximin = max(mins_lignes)
        ligne_maximin = mins_lignes.index(maximin)
        
        # Minimax J2 : pour chaque colonne, max sur lignes, puis min
        maxs_colonnes = [max(matrice[i][j] for i in range(2)) for j in range(3)]
        minimax = min(maxs_colonnes)
        col_minimax = maxs_colonnes.index(minimax)
        
        # Point-selle existe si maximin == minimax
        point_selle = (maximin == minimax)
        
        # On veut parfois avec point-selle, parfois sans
        # Pour cet exercice, on va générer AVEC point-selle (plus simple)
        if point_selle:
            break
    
    return {
        "matrice": matrice,
        "lignes": lignes,
        "colonnes": colonnes,
        "mins_lignes": mins_lignes,
        "maxs_colonnes": maxs_colonnes,
        "maximin": maximin,
        "minimax": minimax,
        "ligne_maximin": ligne_maximin,
        "col_minimax": col_minimax,
        "point_selle": point_selle,
        "valeur": maximin if point_selle else None
    }


# ============================================
# GÉNÉRATION DES QUESTIONS
# ============================================

def generer_questions(sit):
    m = sit["matrice"]
    L = sit["lignes"]
    C = sit["colonnes"]
    mins_lignes = sit["mins_lignes"]
    maxs_colonnes = sit["maxs_colonnes"]
    maximin = sit["maximin"]
    minimax = sit["minimax"]
    ligne_maximin = sit["ligne_maximin"]
    col_minimax = sit["col_minimax"]
    
    questions = []
    
    # ========== Q1: Identifier somme nulle ==========
    questions.append({
        "concept": "Identification",
        "question": "Ce jeu est à <b>somme nulle</b>. Qu'est-ce que cela signifie ?",
        "choix": {
            "A": "Le gain de J2 = -gain de J1 (ce que J1 gagne, J2 le perd)",
            "B": "Les deux joueurs gagnent 0",
            "C": "La somme des stratégies est nulle",
            "D": "Il n'y a pas d'équilibre"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Définition :</b> Un jeu est à <b>somme nulle</b> si g₁ + g₂ = 0 pour toute issue.</div>
<div class="step"><b>Conséquence :</b> g₂ = -g₁<br>
Ce que J1 gagne, J2 le perd (et inversement).</div>
<div class="step"><b>Dans la matrice :</b> On n'affiche que les gains de J1.<br>
Les gains de J2 sont les opposés.</div>
<div class="tip">Exemples classiques : poker, échecs, pierre-feuille-ciseaux.</div>
"""
    })
    
    # ========== Q2: Gain garanti J1 pour une ligne ==========
    ligne_test = random.randint(0, 1)
    min_test = mins_lignes[ligne_test]
    questions.append({
        "concept": "Gain garanti",
        "question": f"Si J1 joue <b>{L[ligne_test]}</b>, quel est son <b>gain garanti</b> (pire cas) ?",
        "choix": {
            "A": f"{min_test}",
            "B": f"{max(m[ligne_test])}",
            "C": f"{sum(m[ligne_test]) / 3:.1f}",
            "D": f"{m[ligne_test][0]}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Gain garanti :</b> Le minimum que J1 obtient quoi que fasse J2.</div>
<div class="step"><b>Ligne {L[ligne_test]} :</b> gains = [{', '.join(str(x) for x in m[ligne_test])}]</div>
<div class="step"><b>Pire cas :</b> J2 choisit la colonne qui minimise le gain de J1.<br>
min({', '.join(str(x) for x in m[ligne_test])}) = <b>{min_test}</b></div>
<div class="tip">J1 raisonne : "Quel est le pire qui puisse m'arriver avec cette ligne ?"</div>
"""
    })
    
    # ========== Q3: Stratégie maximin J1 ==========
    questions.append({
        "concept": "Maximin",
        "question": f"Quelle est la <b>stratégie maximin</b> (prudente) de J1 ?",
        "choix": {
            "A": f"{L[ligne_maximin]}",
            "B": f"{L[1 - ligne_maximin]}",
            "C": "Jouer au hasard",
            "D": "Ça dépend de J2"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Méthode maximin :</b><br>
1) Pour chaque ligne, calculer le min (pire cas)<br>
2) Choisir la ligne qui maximise ce min</div>
<div class="step"><b>Calcul :</b><br>
• Ligne H : min = {mins_lignes[0]}<br>
• Ligne B : min = {mins_lignes[1]}</div>
<div class="step"><b>Maximin :</b> max({mins_lignes[0]}, {mins_lignes[1]}) = <b>{maximin}</b><br>
→ Stratégie prudente : <b>{L[ligne_maximin]}</b></div>
<div class="tip">La stratégie maximin garantit au moins {maximin}, quoi que fasse J2.</div>
"""
    })
    
    # ========== Q4: Valeur maximin ==========
    questions.append({
        "concept": "Valeur maximin",
        "question": f"Quelle est la <b>valeur maximin</b> de J1 ?",
        "choix": {
            "A": f"{maximin}",
            "B": f"{minimax}",
            "C": f"{max(max(row) for row in m)}",
            "D": f"{mins_lignes[1-ligne_maximin]}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Valeur maximin :</b> Le gain garanti par la stratégie prudente.</div>
<div class="step"><b>Formule :</b> max_i (min_j M[i,j])</div>
<div class="step"><b>Calcul :</b><br>
• min ligne H = {mins_lignes[0]}<br>
• min ligne B = {mins_lignes[1]}<br>
• maximin = max({mins_lignes[0]}, {mins_lignes[1]}) = <b>{maximin}</b></div>
"""
    })
    
    # ========== Q5: Minimax J2 ==========
    questions.append({
        "concept": "Minimax",
        "question": f"Quelle est la <b>stratégie minimax</b> (prudente) de J2 ?",
        "choix": {
            "A": f"{C[col_minimax]}",
            "B": f"{C[(col_minimax + 1) % 3]}",
            "C": f"{C[(col_minimax + 2) % 3]}",
            "D": "Jouer au hasard"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>J2 veut minimiser le gain de J1</b> (car somme nulle).</div>
<div class="step"><b>Méthode minimax :</b><br>
1) Pour chaque colonne, calculer le max (pire cas pour J2)<br>
2) Choisir la colonne qui minimise ce max</div>
<div class="step"><b>Calcul :</b><br>
• Colonne G : max = {maxs_colonnes[0]}<br>
• Colonne M : max = {maxs_colonnes[1]}<br>
• Colonne D : max = {maxs_colonnes[2]}</div>
<div class="step"><b>Minimax :</b> min({maxs_colonnes[0]}, {maxs_colonnes[1]}, {maxs_colonnes[2]}) = <b>{minimax}</b><br>
→ Stratégie prudente J2 : <b>{C[col_minimax]}</b></div>
"""
    })
    
    # ========== Q6: Valeur minimax ==========
    questions.append({
        "concept": "Valeur minimax",
        "question": f"Quelle est la <b>valeur minimax</b> ?",
        "choix": {
            "A": f"{minimax}",
            "B": f"{maximin}",
            "C": f"{min(min(row) for row in m)}",
            "D": f"{maxs_colonnes[(col_minimax + 1) % 3]}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Valeur minimax :</b> Le gain max que J2 peut empêcher J1 d'obtenir.</div>
<div class="step"><b>Formule :</b> min_j (max_i M[i,j])</div>
<div class="step"><b>Calcul :</b><br>
• max colonne G = {maxs_colonnes[0]}<br>
• max colonne M = {maxs_colonnes[1]}<br>
• max colonne D = {maxs_colonnes[2]}<br>
• minimax = min({maxs_colonnes[0]}, {maxs_colonnes[1]}, {maxs_colonnes[2]}) = <b>{minimax}</b></div>
"""
    })
    
    # ========== Q7: Point-selle ==========
    questions.append({
        "concept": "Point-selle",
        "question": f"Y a-t-il un <b>point-selle</b> dans ce jeu ?",
        "choix": {
            "A": "Oui" if sit["point_selle"] else "Non",
            "B": "Non" if sit["point_selle"] else "Oui",
            "C": "On ne peut pas savoir",
            "D": "Seulement en stratégie mixte"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Définition :</b> Un point-selle existe si <b>maximin = minimax</b>.</div>
<div class="step"><b>Ici :</b><br>
• maximin = {maximin}<br>
• minimax = {minimax}</div>
<div class="step">{maximin} {"=" if maximin == minimax else "≠"} {minimax} → <b>{"Point-selle OUI" if sit["point_selle"] else "Pas de point-selle"}</b></div>
<div class="tip">{"Au point-selle, les stratégies prudentes forment un équilibre de Nash." if sit["point_selle"] else "Sans point-selle, il faut chercher un équilibre en stratégies mixtes."}</div>
"""
    })
    
    # ========== Q8: Valeur du jeu ==========
    questions.append({
        "concept": "Valeur du jeu",
        "question": f"Quelle est la <b>valeur du jeu</b> ?",
        "choix": {
            "A": f"{maximin}" if sit["point_selle"] else "Il faut calculer en mixte",
            "B": f"{minimax}" if not sit["point_selle"] else f"{maximin + 1}",
            "C": "0",
            "D": f"({maximin} + {minimax}) / 2"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Valeur du jeu :</b> Le gain de J1 quand les deux jouent optimalement.</div>
<div class="step"><b>Théorème du minimax (von Neumann) :</b><br>
En somme nulle, maximin ≤ valeur ≤ minimax.</div>
<div class="step"><b>Si point-selle :</b> valeur = maximin = minimax = <b>{maximin}</b></div>
<div class="step"><b>Ici :</b> maximin = minimax = {maximin} → <b>Valeur = {maximin}</b></div>
"""
    })
    
    # ========== Q9: Équilibre de Nash ==========
    eq_i, eq_j = ligne_maximin, col_minimax
    questions.append({
        "concept": "Équilibre de Nash",
        "question": f"L'équilibre de Nash en stratégies pures est :",
        "choix": {
            "A": f"({L[eq_i]}, {C[eq_j]})" if sit["point_selle"] else "Pas d'équilibre pur",
            "B": f"({L[1-eq_i]}, {C[(eq_j+1)%3]})",
            "C": f"({L[eq_i]}, {C[(eq_j+1)%3]})",
            "D": f"({L[1-eq_i]}, {C[eq_j]})"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>En jeu à somme nulle avec point-selle :</b><br>
L'équilibre = (stratégie maximin J1, stratégie minimax J2)</div>
<div class="step"><b>Calcul :</b><br>
• Stratégie maximin J1 : {L[ligne_maximin]}<br>
• Stratégie minimax J2 : {C[col_minimax]}</div>
<div class="step"><b>Équilibre :</b> <b>({L[eq_i]}, {C[eq_j]})</b></div>
<div class="step"><b>Gain à l'équilibre :</b> M[{L[eq_i]},{C[eq_j]}] = {m[eq_i][eq_j]}</div>
"""
    })
    
    # ========== Q10: Vérification ==========
    questions.append({
        "concept": "Vérification",
        "question": f"À l'équilibre ({L[eq_i]}, {C[eq_j]}), J1 a-t-il intérêt à dévier ?",
        "choix": {
            "A": "Non, c'est bien un équilibre",
            "B": "Oui, vers l'autre ligne",
            "C": "Ça dépend de J2",
            "D": "On ne peut pas vérifier"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Vérification équilibre :</b> Aucun joueur ne veut dévier unilatéralement.</div>
<div class="step"><b>J1 dévie de {L[eq_i]} vers {L[1-eq_i]} ?</b><br>
• Gain actuel : M[{L[eq_i]},{C[eq_j]}] = {m[eq_i][eq_j]}<br>
• Gain si dévie : M[{L[1-eq_i]},{C[eq_j]}] = {m[1-eq_i][eq_j]}<br>
• {m[eq_i][eq_j]} {"≥" if m[eq_i][eq_j] >= m[1-eq_i][eq_j] else "<"} {m[1-eq_i][eq_j]} → {"Pas de déviation" if m[eq_i][eq_j] >= m[1-eq_i][eq_j] else "Déviation !"}</div>
<div class="step"><b>J2 dévie ?</b><br>
J2 veut minimiser → il compare les colonnes.<br>
{C[eq_j]} donne {m[eq_i][eq_j]} à J1 (donc -{m[eq_i][eq_j]} à J2).<br>
Pas mieux ailleurs → <b>Pas de déviation</b>.</div>
"""
    })
    
    return questions


# ============================================
# AFFICHAGE
# ============================================

def afficher_matrice(sit):
    m = sit["matrice"]
    L = sit["lignes"]
    C = sit["colonnes"]
    
    return f"""
    <div class="situation-box">
        <p style="margin-bottom: 16px; font-size: 13px;"><b>Jeu à somme nulle 2×3</b> (gains de J1 uniquement)</p>
        <table class="matrice-table">
            <tr>
                <td class="header"></td>
                <td class="header">{C[0]}</td>
                <td class="header">{C[1]}</td>
                <td class="header">{C[2]}</td>
            </tr>
            <tr>
                <td class="header">{L[0]}</td>
                <td class="cell">{m[0][0]}</td>
                <td class="cell">{m[0][1]}</td>
                <td class="cell">{m[0][2]}</td>
            </tr>
            <tr>
                <td class="header">{L[1]}</td>
                <td class="cell">{m[1][0]}</td>
                <td class="cell">{m[1][1]}</td>
                <td class="cell">{m[1][2]}</td>
            </tr>
        </table>
        <p style="font-size: 11px; margin-top: 12px; text-align: center;">J2 gagne l'opposé : g₂ = -g₁</p>
    </div>
    """


# ============================================
# PAGES
# ============================================

def page_menu():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("# ⚖️ Bloc D — Jeux à Somme Nulle")
    st.markdown("*Exercice complet avec 10 questions*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    **Concepts couverts :**
    - Identifier un jeu à somme nulle
    - Gain garanti (pire cas)
    - Stratégie maximin (J1)
    - Stratégie minimax (J2)
    - Point-selle
    - Valeur du jeu
    - Équilibre de Nash
    - Vérification de l'équilibre
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Commencer l'exercice", use_container_width=True):
        sit = generer_situation()
        st.session_state.sit_d = sit
        st.session_state.questions_d = generer_questions(sit)
        st.session_state.idx_d = 0
        st.session_state.score_d = 0
        st.session_state.answered_d = False
        st.session_state.selected_d = None
        st.session_state.started_d = True
        st.rerun()


def page_question():
    sit = st.session_state.sit_d
    questions = st.session_state.questions_d
    idx = st.session_state.idx_d
    
    if idx >= len(questions):
        page_results()
        return
    
    q = questions[idx]
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Menu"):
            st.session_state.started_d = False
            st.rerun()
    with col2:
        st.progress(idx / len(questions))
    with col3:
        st.markdown(f"**Q{idx + 1}/{len(questions)}** — {st.session_state.score_d} ✓")
    
    # Matrice
    st.markdown(afficher_matrice(sit), unsafe_allow_html=True)
    
    # Question
    st.markdown(f"<span class='concept-tag'>{q['concept']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;margin-top:10px;'>{q['question']}</p>", unsafe_allow_html=True)
    
    # Choix
    if not st.session_state.answered_d:
        for lettre, texte in q["choix"].items():
            if st.button(f"{lettre}. {texte}", key=f"btn_{lettre}", use_container_width=True):
                st.session_state.selected_d = lettre
                st.session_state.answered_d = True
                if lettre == q["reponse"]:
                    st.session_state.score_d += 1
                st.rerun()
    else:
        # Afficher résultat
        for lettre, texte in q["choix"].items():
            if lettre == q["reponse"]:
                st.markdown(f'<div style="background:#fff;border:3px solid #000;border-radius:8px;padding:10px;margin:4px 0;"><b>✓ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            elif lettre == st.session_state.selected_d:
                st.markdown(f'<div style="background:#fff;border:3px dashed #000;border-radius:8px;padding:10px;margin:4px 0;"><b>✗ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#eee;border-radius:8px;padding:10px;margin:4px 0;opacity:0.5;">{lettre}. {texte}</div>', unsafe_allow_html=True)
        
        # Message
        if st.session_state.selected_d == q["reponse"]:
            st.markdown('<div class="correct-box"><b style="font-size:18px;">✓ Correct !</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="incorrect-box"><b style="font-size:18px;">✗ Incorrect</b><br>La bonne réponse était <b>{q["reponse"]}</b></div>', unsafe_allow_html=True)
        
        # Explication
        st.markdown(f'<div class="explication"><b>💡 Explication détaillée</b>{q["explication"]}</div>', unsafe_allow_html=True)
        
        # Bouton suivant
        st.markdown("<br>", unsafe_allow_html=True)
        btn_txt = "Question suivante →" if idx < len(questions) - 1 else "Voir les résultats"
        if st.button(btn_txt, use_container_width=True, type="primary"):
            st.session_state.idx_d += 1
            st.session_state.answered_d = False
            st.session_state.selected_d = None
            st.rerun()


def page_results():
    score = st.session_state.score_d
    total = len(st.session_state.questions_d)
    pct = score / total * 100
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align:center;">
        <div style="width:150px;height:150px;border-radius:50%;background:#fff;border:4px solid #000;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto;">
            <span style="font-size:36px;font-weight:700;">{score}/{total}</span>
            <span style="font-size:14px;">{pct:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if pct >= 80:
        st.markdown("<p style='text-align:center;font-size:20px;'>🏆 Excellent !</p>", unsafe_allow_html=True)
    elif pct >= 60:
        st.markdown("<p style='text-align:center;font-size:20px;'>👍 Bien joué !</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;font-size:20px;'>📚 Continue à réviser.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Menu", use_container_width=True):
            st.session_state.started_d = False
            st.rerun()
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True, type="primary"):
            sit = generer_situation()
            st.session_state.sit_d = sit
            st.session_state.questions_d = generer_questions(sit)
            st.session_state.idx_d = 0
            st.session_state.score_d = 0
            st.session_state.answered_d = False
            st.session_state.selected_d = None
            st.rerun()


# ============================================
# MAIN
# ============================================

if st.session_state.started_d:
    if st.session_state.idx_d < len(st.session_state.questions_d):
        page_question()
    else:
        page_results()
else:
    page_menu()
