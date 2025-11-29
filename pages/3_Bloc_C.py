"""
BLOC C - STRATÉGIES MIXTES
Exercice complet avec ~12 questions couvrant tous les concepts des TDs
"""

import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Bloc C - Stratégies Mixtes", page_icon="🎲", layout="centered")

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
    
    .formula {
        background: #f0f0f0;
        padding: 8px 14px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 14px;
        border: 1px solid #000;
        display: inline-block;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if "sit_c" not in st.session_state:
    st.session_state.sit_c = None
if "questions_c" not in st.session_state:
    st.session_state.questions_c = []
if "idx_c" not in st.session_state:
    st.session_state.idx_c = 0
if "score_c" not in st.session_state:
    st.session_state.score_c = 0
if "answered_c" not in st.session_state:
    st.session_state.answered_c = False
if "selected_c" not in st.session_state:
    st.session_state.selected_c = None
if "started_c" not in st.session_state:
    st.session_state.started_c = False


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
    """Génère un jeu 2x2 SANS équilibre pur (pour forcer les stratégies mixtes)"""
    
    while True:
        # Matrice de gains (g1, g2)
        # On veut un jeu sans équilibre pur
        
        # Gains J1
        a = random.randint(0, 4)   # (H, G)
        b = random.randint(5, 9)   # (H, D)
        c = random.randint(5, 9)   # (B, G)
        d = random.randint(0, 4)   # (B, D)
        
        # Gains J2 (on fait un jeu générique, pas forcément somme nulle)
        a2 = random.randint(5, 9)  # (H, G)
        b2 = random.randint(0, 4)  # (H, D)
        c2 = random.randint(0, 4)  # (B, G)
        d2 = random.randint(5, 9)  # (B, D)
        
        matrice = [
            [(a, a2), (b, b2)],
            [(c, c2), (d, d2)]
        ]
        
        # Vérifier pas d'équilibre pur
        # BR J1 pour chaque colonne
        br1_G = 0 if a >= c else 1  # si J2 joue G
        br1_D = 0 if b >= d else 1  # si J2 joue D
        
        # BR J2 pour chaque ligne
        br2_H = 0 if a2 >= b2 else 1  # si J1 joue H
        br2_B = 0 if c2 >= d2 else 1  # si J1 joue B
        
        # Équilibres purs
        eq_purs = []
        if br1_G == 0 and br2_H == 0:
            eq_purs.append((0, 0))
        if br1_D == 0 and br2_H == 1:
            eq_purs.append((0, 1))
        if br1_G == 1 and br2_B == 0:
            eq_purs.append((1, 0))
        if br1_D == 1 and br2_B == 1:
            eq_purs.append((1, 1))
        
        # On veut 0 équilibre pur
        if len(eq_purs) == 0:
            break
    
    # Calculer équilibre mixte
    # p = proba que J1 joue H
    # q = proba que J2 joue G
    
    # J1 rend J2 indifférent entre G et D:
    # E[G] = p*a2 + (1-p)*c2
    # E[D] = p*b2 + (1-p)*d2
    # E[G] = E[D] => p(a2 - c2) + c2 = p(b2 - d2) + d2
    # p(a2 - c2 - b2 + d2) = d2 - c2
    # p = (d2 - c2) / (a2 - c2 - b2 + d2)
    
    denom_p = a2 - c2 - b2 + d2
    if denom_p != 0:
        p_star = Fraction(d2 - c2, denom_p)
    else:
        p_star = Fraction(1, 2)
    
    # J2 rend J1 indifférent entre H et B:
    # E[H] = q*a + (1-q)*b
    # E[B] = q*c + (1-q)*d
    # E[H] = E[B] => q(a - b) + b = q(c - d) + d
    # q(a - b - c + d) = d - b
    # q = (d - b) / (a - b - c + d)
    
    denom_q = a - b - c + d
    if denom_q != 0:
        q_star = Fraction(d - b, denom_q)
    else:
        q_star = Fraction(1, 2)
    
    p_star = p_star.limit_denominator(100)
    q_star = q_star.limit_denominator(100)
    
    # Espérance de gain à l'équilibre pour J1
    # E[J1] = q*a + (1-q)*b quand J1 joue H (et c'est pareil pour B à l'équilibre)
    gain_eq_j1 = q_star * a + (1 - q_star) * b
    gain_eq_j1 = Fraction(gain_eq_j1).limit_denominator(100)
    
    return {
        "matrice": matrice,
        "a": a, "b": b, "c": c, "d": d,
        "a2": a2, "b2": b2, "c2": c2, "d2": d2,
        "p_star": p_star,
        "q_star": q_star,
        "gain_eq_j1": gain_eq_j1,
        "br1_G": br1_G, "br1_D": br1_D,
        "br2_H": br2_H, "br2_B": br2_B
    }


# ============================================
# GÉNÉRATION DES QUESTIONS
# ============================================

def generer_questions(sit):
    m = sit["matrice"]
    a, b, c, d = sit["a"], sit["b"], sit["c"], sit["d"]
    a2, b2, c2, d2 = sit["a2"], sit["b2"], sit["c2"], sit["d2"]
    p_star, q_star = sit["p_star"], sit["q_star"]
    L = ["H", "B"]
    C = ["G", "D"]
    
    questions = []
    
    # ========== Q1: Vérifier absence équilibre pur ==========
    questions.append({
        "concept": "Équilibre pur",
        "question": "Ce jeu admet-il un <b>équilibre de Nash en stratégies pures</b> ?",
        "choix": {
            "A": "Non, pas d'équilibre pur",
            "B": "Oui, en (H, G)",
            "C": "Oui, en (B, D)",
            "D": "Oui, plusieurs équilibres"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Méthode du soulignement :</b></div>
<div class="step"><b>BR de J1 :</b><br>
• Si J2 joue G : max({a}, {c}) → <b>{L[0 if a >= c else 1]}</b><br>
• Si J2 joue D : max({b}, {d}) → <b>{L[0 if b >= d else 1]}</b></div>
<div class="step"><b>BR de J2 :</b><br>
• Si J1 joue H : max({a2}, {b2}) → <b>{C[0 if a2 >= b2 else 1]}</b><br>
• Si J1 joue B : max({c2}, {d2}) → <b>{C[0 if c2 >= d2 else 1]}</b></div>
<div class="step"><b>Aucune case n'a 2 soulignements</b> → Pas d'équilibre pur !</div>
<div class="tip">→ Il faut chercher un équilibre en <b>stratégies mixtes</b>.</div>
"""
    })
    
    # ========== Q2: Définition stratégie mixte ==========
    questions.append({
        "concept": "Définition",
        "question": "Une <b>stratégie mixte</b> pour J1, c'est :",
        "choix": {
            "A": "Jouer H avec probabilité p et B avec probabilité (1-p)",
            "B": "Choisir H ou B au hasard avec proba 1/2",
            "C": "Alterner entre H et B",
            "D": "Laisser J2 décider"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Définition :</b> Une stratégie mixte est une <b>distribution de probabilité</b> sur les stratégies pures.</div>
<div class="step"><b>Pour J1 :</b> Jouer H avec proba p, B avec proba (1-p), où p ∈ [0,1]</div>
<div class="step"><b>Pour J2 :</b> Jouer G avec proba q, D avec proba (1-q), où q ∈ [0,1]</div>
<div class="step"><b>Cas particuliers :</b><br>
• p = 1 → stratégie pure H<br>
• p = 0 → stratégie pure B<br>
• p = 0.5 → équiprobable</div>
"""
    })
    
    # ========== Q3: Espérance si J2 joue G ==========
    questions.append({
        "concept": "Espérance de gain",
        "question": f"Si J1 joue H avec proba p et J2 joue <b>G</b>, l'espérance de gain de J1 est :",
        "choix": {
            "A": f"E = p×{a} + (1-p)×{c} = {c} + p×{a-c}",
            "B": f"E = p×{a} + p×{c}",
            "C": f"E = {a} + {c}",
            "D": f"E = p×{a}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>J2 joue G (colonne G) :</b></div>
<div class="step"><b>Gains possibles pour J1 :</b><br>
• Si J1 joue H (proba p) → gain = {a}<br>
• Si J1 joue B (proba 1-p) → gain = {c}</div>
<div class="step"><b>Espérance :</b><br>
E[J1 | J2 joue G] = p×{a} + (1-p)×{c}<br>
= {a}p + {c} - {c}p<br>
= {c} + ({a}-{c})p<br>
= <b>{c} + {a-c}p</b></div>
"""
    })
    
    # ========== Q4: Espérance si J2 joue D ==========
    questions.append({
        "concept": "Espérance de gain",
        "question": f"Si J1 joue H avec proba p et J2 joue <b>D</b>, l'espérance de gain de J1 est :",
        "choix": {
            "A": f"E = {d} + p×{b-d}",
            "B": f"E = {b} + p×{d-b}",
            "C": f"E = p×{b} × (1-p)×{d}",
            "D": f"E = ({b} + {d})/2"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>J2 joue D (colonne D) :</b></div>
<div class="step"><b>Gains possibles pour J1 :</b><br>
• Si J1 joue H (proba p) → gain = {b}<br>
• Si J1 joue B (proba 1-p) → gain = {d}</div>
<div class="step"><b>Espérance :</b><br>
E[J1 | J2 joue D] = p×{b} + (1-p)×{d}<br>
= {b}p + {d} - {d}p<br>
= <b>{d} + {b-d}p</b></div>
"""
    })
    
    # ========== Q5: Principe d'indifférence ==========
    questions.append({
        "concept": "Principe d'indifférence",
        "question": "Pour trouver p*, on utilise le fait que :",
        "choix": {
            "A": "J2 doit être indifférent entre G et D",
            "B": "J1 doit être indifférent entre H et B",
            "C": "Les gains doivent être égaux",
            "D": "p doit maximiser le gain de J1"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Principe d'indifférence :</b> À l'équilibre mixte, chaque joueur rend l'<b>autre</b> indifférent.</div>
<div class="step"><b>Pour trouver p* :</b><br>
J1 choisit p pour que J2 soit indifférent entre G et D.<br>
→ E[J2 | G] = E[J2 | D]</div>
<div class="step"><b>Pour trouver q* :</b><br>
J2 choisit q pour que J1 soit indifférent entre H et B.<br>
→ E[J1 | H] = E[J1 | B]</div>
<div class="warning">Attention : C'est contre-intuitif ! J1 choisit p pour rendre J2 indifférent, pas lui-même.</div>
"""
    })
    
    # ========== Q6: Calcul de p* ==========
    questions.append({
        "concept": "Calcul de p*",
        "question": f"Quelle est la valeur de <b>p*</b> (proba que J1 joue H) ?",
        "choix": {
            "A": f"p* = {frac(p_star)}",
            "B": f"p* = {frac(1 - p_star)}",
            "C": f"p* = 1/2",
            "D": f"p* = {frac(q_star)}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Condition :</b> J2 indifférent entre G et D</div>
<div class="step"><b>E[J2 | G] = E[J2 | D]</b><br>
p×{a2} + (1-p)×{c2} = p×{b2} + (1-p)×{d2}</div>
<div class="step"><b>Développer :</b><br>
{a2}p + {c2} - {c2}p = {b2}p + {d2} - {d2}p<br>
{c2} + ({a2}-{c2})p = {d2} + ({b2}-{d2})p<br>
{c2} + {a2-c2}p = {d2} + {b2-d2}p</div>
<div class="step"><b>Résoudre :</b><br>
{a2-c2}p - {b2-d2}p = {d2} - {c2}<br>
{a2-c2-b2+d2}p = {d2-c2}<br>
<b>p* = {frac(p_star)}</b></div>
"""
    })
    
    # ========== Q7: Calcul de q* ==========
    questions.append({
        "concept": "Calcul de q*",
        "question": f"Quelle est la valeur de <b>q*</b> (proba que J2 joue G) ?",
        "choix": {
            "A": f"q* = {frac(q_star)}",
            "B": f"q* = {frac(1 - q_star)}",
            "C": f"q* = 1/2",
            "D": f"q* = {frac(p_star)}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Condition :</b> J1 indifférent entre H et B</div>
<div class="step"><b>E[J1 | H] = E[J1 | B]</b><br>
q×{a} + (1-q)×{b} = q×{c} + (1-q)×{d}</div>
<div class="step"><b>Développer :</b><br>
{a}q + {b} - {b}q = {c}q + {d} - {d}q<br>
{b} + ({a}-{b})q = {d} + ({c}-{d})q<br>
{b} + {a-b}q = {d} + {c-d}q</div>
<div class="step"><b>Résoudre :</b><br>
{a-b}q - {c-d}q = {d} - {b}<br>
{a-b-c+d}q = {d-b}<br>
<b>q* = {frac(q_star)}</b></div>
"""
    })
    
    # ========== Q8: Équilibre mixte ==========
    questions.append({
        "concept": "Équilibre mixte",
        "question": f"L'équilibre de Nash en stratégies mixtes est :",
        "choix": {
            "A": f"(p* = {frac(p_star)}, q* = {frac(q_star)})",
            "B": f"(p* = {frac(q_star)}, q* = {frac(p_star)})",
            "C": f"(p* = 1/2, q* = 1/2)",
            "D": f"(p* = {frac(1-p_star)}, q* = {frac(1-q_star)})"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Équilibre de Nash mixte :</b></div>
<div class="step">J1 joue H avec proba <b>p* = {frac(p_star)}</b><br>
J1 joue B avec proba 1 - p* = {frac(1-p_star)}</div>
<div class="step">J2 joue G avec proba <b>q* = {frac(q_star)}</b><br>
J2 joue D avec proba 1 - q* = {frac(1-q_star)}</div>
<div class="step"><b>Vérification :</b> À cet équilibre, chaque joueur est indifférent entre ses stratégies pures.</div>
"""
    })
    
    # ========== Q9: Gain espéré à l'équilibre ==========
    gain_eq = sit["gain_eq_j1"]
    questions.append({
        "concept": "Gain à l'équilibre",
        "question": f"Quel est le <b>gain espéré de J1</b> à l'équilibre mixte ?",
        "choix": {
            "A": f"E[J1] = {frac(gain_eq)}",
            "B": f"E[J1] = {a}",
            "C": f"E[J1] = ({a}+{b}+{c}+{d})/4",
            "D": f"E[J1] = {frac(p_star)} × {frac(q_star)}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>À l'équilibre, J1 est indifférent</b> → on peut calculer E[J1] avec n'importe quelle stratégie pure.</div>
<div class="step"><b>Avec H :</b><br>
E[J1 | H] = q*×{a} + (1-q*)×{b}<br>
= {frac(q_star)}×{a} + {frac(1-q_star)}×{b}<br>
= {frac(gain_eq)}</div>
<div class="step"><b>Vérification avec B :</b><br>
E[J1 | B] = q*×{c} + (1-q*)×{d} = {frac(gain_eq)} ✓</div>
"""
    })
    
    # ========== Q10: Interprétation ==========
    questions.append({
        "concept": "Interprétation",
        "question": "Pourquoi J1 accepte-t-il de jouer aléatoirement ?",
        "choix": {
            "A": "Car s'il jouait pur, J2 l'exploiterait",
            "B": "Car le hasard maximise son gain",
            "C": "Car il ne connaît pas la matrice",
            "D": "Car c'est obligatoire"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Raisonnement :</b></div>
<div class="step">Si J1 joue H à coup sûr → J2 joue sa BR à H → J1 n'est pas content</div>
<div class="step">Si J1 joue B à coup sûr → J2 joue sa BR à B → J1 n'est pas content</div>
<div class="step"><b>Solution :</b> J1 "cache" son choix en jouant aléatoirement. J2 ne peut pas l'exploiter.</div>
<div class="step"><b>À l'équilibre :</b> Aucun joueur ne peut améliorer son gain en changeant de stratégie.</div>
"""
    })
    
    # ========== Q11: Vérifier un équilibre ==========
    p_faux = Fraction(1, 2)
    questions.append({
        "concept": "Vérification",
        "question": f"Si on propose (p = 1/2, q = 1/2), est-ce un équilibre ?",
        "choix": {
            "A": "Non" if p_star != Fraction(1,2) or q_star != Fraction(1,2) else "Oui",
            "B": "Oui" if p_star != Fraction(1,2) or q_star != Fraction(1,2) else "Non",
            "C": "Ça dépend",
            "D": "On ne peut pas vérifier"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Pour vérifier :</b> Est-ce que J2 est indifférent quand p = 1/2 ?</div>
<div class="step"><b>E[J2 | G] avec p=1/2 :</b> 0.5×{a2} + 0.5×{c2} = {(a2+c2)/2}</div>
<div class="step"><b>E[J2 | D] avec p=1/2 :</b> 0.5×{b2} + 0.5×{d2} = {(b2+d2)/2}</div>
<div class="step">{(a2+c2)/2} {"=" if (a2+c2)/2 == (b2+d2)/2 else "≠"} {(b2+d2)/2} → {"Indifférent ✓" if (a2+c2)/2 == (b2+d2)/2 else "Pas indifférent ✗"}</div>
<div class="step"><b>L'équilibre correct est (p* = {frac(p_star)}, q* = {frac(q_star)})</b></div>
"""
    })
    
    # ========== Q12: Unicité ==========
    questions.append({
        "concept": "Unicité",
        "question": "Combien d'équilibres de Nash ce jeu admet-il ?",
        "choix": {
            "A": "Un seul (l'équilibre mixte)",
            "B": "Zéro",
            "C": "Deux (un pur et un mixte)",
            "D": "Infini"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Équilibres purs :</b> 0 (on a vérifié au début)</div>
<div class="step"><b>Équilibre mixte :</b> 1, c'est (p* = {frac(p_star)}, q* = {frac(q_star)})</div>
<div class="step"><b>Total : 1 équilibre</b></div>
<div class="tip">En général, un jeu 2×2 sans équilibre pur a exactement 1 équilibre mixte.</div>
"""
    })
    
    return questions


# ============================================
# AFFICHAGE
# ============================================

def afficher_matrice(m):
    return f"""
    <div class="situation-box">
        <p style="margin-bottom: 16px; font-size: 13px;"><b>Jeu bimatriciel 2×2</b> (pas d'équilibre pur)</p>
        <table class="matrice-table">
            <tr>
                <td class="header"></td>
                <td class="header">G</td>
                <td class="header">D</td>
            </tr>
            <tr>
                <td class="header">H</td>
                <td class="cell">({m[0][0][0]}, {m[0][0][1]})</td>
                <td class="cell">({m[0][1][0]}, {m[0][1][1]})</td>
            </tr>
            <tr>
                <td class="header">B</td>
                <td class="cell">({m[1][0][0]}, {m[1][0][1]})</td>
                <td class="cell">({m[1][1][0]}, {m[1][1][1]})</td>
            </tr>
        </table>
        <p style="font-size: 11px; margin-top: 12px; text-align: center;">J1 = ligne (joue H avec proba p), J2 = colonne (joue G avec proba q)</p>
    </div>
    """


# ============================================
# PAGES
# ============================================

def page_menu():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("# 🎲 Bloc C — Stratégies Mixtes")
    st.markdown("*Exercice complet avec 12 questions*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    **Concepts couverts :**
    - Vérifier absence d'équilibre pur
    - Définition stratégie mixte
    - Calcul d'espérance de gain
    - Principe d'indifférence
    - Calcul de p* et q*
    - Équilibre de Nash mixte
    - Gain espéré à l'équilibre
    - Vérification d'un équilibre
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Commencer l'exercice", use_container_width=True):
        sit = generer_situation()
        st.session_state.sit_c = sit
        st.session_state.questions_c = generer_questions(sit)
        st.session_state.idx_c = 0
        st.session_state.score_c = 0
        st.session_state.answered_c = False
        st.session_state.selected_c = None
        st.session_state.started_c = True
        st.rerun()


def page_question():
    sit = st.session_state.sit_c
    questions = st.session_state.questions_c
    idx = st.session_state.idx_c
    
    if idx >= len(questions):
        page_results()
        return
    
    q = questions[idx]
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Menu"):
            st.session_state.started_c = False
            st.rerun()
    with col2:
        st.progress(idx / len(questions))
    with col3:
        st.markdown(f"**Q{idx + 1}/{len(questions)}** — {st.session_state.score_c} ✓")
    
    # Matrice
    st.markdown(afficher_matrice(sit["matrice"]), unsafe_allow_html=True)
    
    # Question
    st.markdown(f"<span class='concept-tag'>{q['concept']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;margin-top:10px;'>{q['question']}</p>", unsafe_allow_html=True)
    
    # Choix
    if not st.session_state.answered_c:
        for lettre, texte in q["choix"].items():
            if st.button(f"{lettre}. {texte}", key=f"btn_{lettre}", use_container_width=True):
                st.session_state.selected_c = lettre
                st.session_state.answered_c = True
                if lettre == q["reponse"]:
                    st.session_state.score_c += 1
                st.rerun()
    else:
        # Afficher résultat
        for lettre, texte in q["choix"].items():
            if lettre == q["reponse"]:
                st.markdown(f'<div style="background:#fff;border:3px solid #000;border-radius:8px;padding:10px;margin:4px 0;"><b>✓ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            elif lettre == st.session_state.selected_c:
                st.markdown(f'<div style="background:#fff;border:3px dashed #000;border-radius:8px;padding:10px;margin:4px 0;"><b>✗ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#eee;border-radius:8px;padding:10px;margin:4px 0;opacity:0.5;">{lettre}. {texte}</div>', unsafe_allow_html=True)
        
        # Message
        if st.session_state.selected_c == q["reponse"]:
            st.markdown('<div class="correct-box"><b style="font-size:18px;">✓ Correct !</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="incorrect-box"><b style="font-size:18px;">✗ Incorrect</b><br>La bonne réponse était <b>{q["reponse"]}</b></div>', unsafe_allow_html=True)
        
        # Explication
        st.markdown(f'<div class="explication"><b>💡 Explication détaillée</b>{q["explication"]}</div>', unsafe_allow_html=True)
        
        # Bouton suivant
        st.markdown("<br>", unsafe_allow_html=True)
        btn_txt = "Question suivante →" if idx < len(questions) - 1 else "Voir les résultats"
        if st.button(btn_txt, use_container_width=True, type="primary"):
            st.session_state.idx_c += 1
            st.session_state.answered_c = False
            st.session_state.selected_c = None
            st.rerun()


def page_results():
    score = st.session_state.score_c
    total = len(st.session_state.questions_c)
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
            st.session_state.started_c = False
            st.rerun()
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True, type="primary"):
            sit = generer_situation()
            st.session_state.sit_c = sit
            st.session_state.questions_c = generer_questions(sit)
            st.session_state.idx_c = 0
            st.session_state.score_c = 0
            st.session_state.answered_c = False
            st.session_state.selected_c = None
            st.rerun()


# ============================================
# MAIN
# ============================================

if st.session_state.started_c:
    if st.session_state.idx_c < len(st.session_state.questions_c):
        page_question()
    else:
        page_results()
else:
    page_menu()
