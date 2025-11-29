"""
BLOC B - JEUX CONTINUS
Exercice complet avec ~12 questions couvrant tous les concepts des TDs
"""

import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Bloc B - Jeux Continus", page_icon="📈", layout="centered")

# CSS avec couleurs corrigées
st.markdown("""
<style>
    .stApp { background-color: #fff; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Texte principal en noir */
    p, span, div, label { color: #1a1a1a !important; }
    
    .situation-box {
        background: #1e293b;
        color: #f8fafc !important;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    
    .situation-box p, .situation-box span {
        color: #f8fafc !important;
    }
    
    .situation-box .formula {
        background: #334155;
        color: #fbbf24 !important;
        padding: 8px 14px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        display: block;
        margin: 8px 0;
    }
    
    .correct-box {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .incorrect-box {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .explication {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        margin: 16px 0;
        border-radius: 0 12px 12px 0;
        color: #1e293b !important;
    }
    
    .explication b {
        color: #1e40af !important;
    }
    
    .step {
        background: #f1f5f9;
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 6px;
        border-left: 3px solid #64748b;
        color: #334155 !important;
    }
    
    .step b {
        color: #0f172a !important;
    }
    
    .warning {
        background: #fef3c7;
        border-left: 3px solid #f59e0b;
        padding: 10px 14px;
        margin: 10px 0;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
        color: #92400e !important;
    }
    
    .tip {
        background: #ecfdf5;
        border-left: 3px solid #10b981;
        padding: 10px 14px;
        margin: 10px 0;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
        color: #065f46 !important;
    }
    
    .stButton > button {
        background-color: #1a1a1a;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover { background-color: #333; }
    
    .concept-tag {
        background: #dbeafe;
        color: #1e40af !important;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
    }
    
    h1, h2, h3 { color: #0f172a !important; }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if "sit_b" not in st.session_state:
    st.session_state.sit_b = None
if "questions_b" not in st.session_state:
    st.session_state.questions_b = []
if "idx_b" not in st.session_state:
    st.session_state.idx_b = 0
if "score_b" not in st.session_state:
    st.session_state.score_b = 0
if "answered_b" not in st.session_state:
    st.session_state.answered_b = False
if "selected_b" not in st.session_state:
    st.session_state.selected_b = None
if "started_b" not in st.session_state:
    st.session_state.started_b = False


# ============================================
# HELPERS
# ============================================

def frac(x):
    """Convertit en fraction lisible"""
    if isinstance(x, Fraction):
        f = x
    else:
        f = Fraction(x).limit_denominator(100)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def frac_coef(c):
    """Affiche un coefficient proprement"""
    f = Fraction(c).limit_denominator(100)
    if f == 0:
        return ""
    if f == 1:
        return "+"
    if f == -1:
        return "-"
    if f > 0:
        return f"+{frac(f)}"
    return frac(f)


# ============================================
# GÉNÉRATION DE LA SITUATION
# ============================================

def generer_situation():
    """Génère un jeu continu avec fonctions de gain quadratiques"""
    
    while True:
        # g1(x,y) = a*x - b*x² + c*x*y
        # g2(x,y) = d*y - e*y² + f*x*y
        
        a = random.choice([2, 3, 4, 5, 6])
        b = random.choice([1, 2])
        c = Fraction(random.choice([-2, -1, 1, 2]), random.choice([1, 2]))
        
        d = random.choice([2, 3, 4, 5, 6])
        e = random.choice([1, 2])
        f = Fraction(random.choice([-2, -1, 1, 2]), random.choice([1, 2]))
        
        # BR1(y) : ∂g1/∂x = a - 2bx + cy = 0 → x = (a + cy) / (2b)
        # BR2(x) : ∂g2/∂y = d - 2ey + fx = 0 → y = (d + fx) / (2e)
        
        # Résoudre le système
        # x = (a + cy) / (2b)
        # y = (d + fx) / (2e)
        #
        # Substituer y dans x:
        # x = (a + c*(d + fx)/(2e)) / (2b)
        # x = (a + cd/(2e) + cfx/(2e)) / (2b)
        # x * 2b = a + cd/(2e) + cfx/(2e)
        # x * (2b - cf/(2e)) = a + cd/(2e)
        # x * (4be - cf) / (2e) = (2ae + cd) / (2e)
        # x = (2ae + cd) / (4be - cf)
        
        denom = 4*b*e - c*f
        if denom == 0:
            continue
        
        x_star = Fraction(2*a*e + c*d, denom)
        y_star = Fraction(d + f*x_star, 2*e)
        
        # Simplifier
        x_star = x_star.limit_denominator(100)
        y_star = y_star.limit_denominator(100)
        
        # Vérifier que c'est dans un domaine raisonnable
        if 0 < x_star < 5 and 0 < y_star < 5:
            break
    
    # Valeur test pour BR
    y_test = Fraction(1, 1)
    br1_at_test = Fraction(a + c*y_test, 2*b).limit_denominator(100)
    
    x_test = Fraction(1, 1)
    br2_at_test = Fraction(d + f*x_test, 2*e).limit_denominator(100)
    
    return {
        "a": a, "b": b, "c": c,
        "d": d, "e": e, "f": f,
        "x_star": x_star,
        "y_star": y_star,
        "y_test": y_test,
        "br1_at_test": br1_at_test,
        "x_test": x_test,
        "br2_at_test": br2_at_test
    }


# ============================================
# GÉNÉRATION DES QUESTIONS
# ============================================

def generer_questions(sit):
    """Génère toutes les questions pour le bloc B"""
    
    a, b, c = sit["a"], sit["b"], sit["c"]
    d, e, f = sit["d"], sit["e"], sit["f"]
    x_star, y_star = sit["x_star"], sit["y_star"]
    y_test, br1_test = sit["y_test"], sit["br1_at_test"]
    x_test, br2_test = sit["x_test"], sit["br2_at_test"]
    
    c_str = frac(c)
    f_str = frac(f)
    
    questions = []
    
    # ========== Q1: Identifier le type de jeu ==========
    questions.append({
        "concept": "Type de jeu",
        "question": "Quel <b>type de jeu</b> est-ce ?",
        "choix": {
            "A": "Jeu continu (stratégies dans ℝ ou un intervalle)",
            "B": "Jeu fini (matrice)",
            "C": "Jeu séquentiel",
            "D": "Jeu à somme nulle"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> Un jeu est <b>continu</b> quand les stratégies sont des nombres réels (ou un intervalle), pas un ensemble fini.</div>
<div class="step"><b>Ici :</b> x ∈ ℝ⁺ et y ∈ ℝ⁺ → ensemble <b>infini</b> de stratégies</div>
<div class="step"><b>Opposé :</b> Jeu fini = nombre fini de stratégies (ex: matrice 2×2)</div>
<div class="tip">💡 En jeu continu, on utilise le <b>calcul différentiel</b> pour trouver les BR.</div>
"""
    })
    
    # ========== Q2: Dérivée partielle de g1 ==========
    questions.append({
        "concept": "Dérivée partielle",
        "question": f"Quelle est la <b>dérivée partielle</b> ∂g₁/∂x ?",
        "choix": {
            "A": f"{a} - {2*b}x {frac_coef(c)}y",
            "B": f"{a} - {b}x² {frac_coef(c)}xy",
            "C": f"-{2*b}x {frac_coef(c)}y",
            "D": f"{a} {frac_coef(c)}y"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Rappel :</b> On dérive g₁ par rapport à x, en traitant y comme une <b>constante</b>.</div>
<div class="step"><b>g₁(x, y) = {a}x - {b}x² {frac_coef(c)}xy</b></div>
<div class="step"><b>Dérivation terme par terme :</b><br>
• d({a}x)/dx = {a}<br>
• d(-{b}x²)/dx = -{2*b}x<br>
• d({c_str}xy)/dx = {c_str}y</div>
<div class="step"><b>∂g₁/∂x = {a} - {2*b}x {frac_coef(c)}y</b></div>
"""
    })
    
    # ========== Q3: Condition du premier ordre ==========
    questions.append({
        "concept": "CPO (Condition Premier Ordre)",
        "question": "Pour trouver la BR de J1, on pose :",
        "choix": {
            "A": "∂g₁/∂x = 0",
            "B": "∂g₁/∂y = 0",
            "C": "g₁ = 0",
            "D": "∂g₁/∂x = ∂g₂/∂y"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> La meilleure réponse de J1 <b>maximise</b> son gain g₁.</div>
<div class="step"><b>Condition nécessaire :</b> Au maximum, la dérivée s'annule → <b>∂g₁/∂x = 0</b></div>
<div class="step"><b>Attention :</b> On dérive par rapport à la variable de <b>J1</b> (ici x).</div>
<div class="tip">💡 C'est la CPO (Condition du Premier Ordre). Il faut aussi vérifier que c'est un max (dérivée seconde < 0).</div>
"""
    })
    
    # ========== Q4: Trouver BR1(y) ==========
    questions.append({
        "concept": "Calcul de BR₁(y)",
        "question": f"Quelle est la <b>meilleure réponse</b> BR₁(y) de J1 ?",
        "choix": {
            "A": f"x = ({a} {frac_coef(c)}y) / {2*b}",
            "B": f"x = {a} {frac_coef(c)}y",
            "C": f"x = ({a} - {c_str}y) / {2*b}",
            "D": f"x = {2*b} / ({a} {frac_coef(c)}y)"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Résoudre ∂g₁/∂x = 0 pour x.</div>
<div class="step"><b>Équation :</b> {a} - {2*b}x {frac_coef(c)}y = 0</div>
<div class="step"><b>Isoler x :</b><br>
{2*b}x = {a} {frac_coef(c)}y<br>
x = ({a} {frac_coef(c)}y) / {2*b}</div>
<div class="step"><b>BR₁(y) = ({a} {frac_coef(c)}y) / {2*b}</b></div>
<div class="tip">💡 La BR de J1 dépend de y → c'est une <b>fonction</b> de la stratégie de J2.</div>
"""
    })
    
    # ========== Q5: Trouver BR2(x) ==========
    questions.append({
        "concept": "Calcul de BR₂(x)",
        "question": f"Quelle est la <b>meilleure réponse</b> BR₂(x) de J2 ?",
        "choix": {
            "A": f"y = ({d} {frac_coef(f)}x) / {2*e}",
            "B": f"y = {d} {frac_coef(f)}x",
            "C": f"y = ({d} - {f_str}x) / {2*e}",
            "D": f"y = {d} / {2*e}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Même méthode pour J2 :</b> ∂g₂/∂y = 0</div>
<div class="step"><b>g₂(x, y) = {d}y - {e}y² {frac_coef(f)}xy</b></div>
<div class="step"><b>∂g₂/∂y = {d} - {2*e}y {frac_coef(f)}x = 0</b></div>
<div class="step"><b>Résolution :</b><br>
{2*e}y = {d} {frac_coef(f)}x<br>
y = ({d} {frac_coef(f)}x) / {2*e}</div>
<div class="step"><b>BR₂(x) = ({d} {frac_coef(f)}x) / {2*e}</b></div>
"""
    })
    
    # ========== Q6: Évaluer BR1 en un point ==========
    questions.append({
        "concept": "Évaluer BR",
        "question": f"Si y = {frac(y_test)}, quelle est BR₁({frac(y_test)}) ?",
        "choix": {
            "A": frac(br1_test),
            "B": frac(br1_test + 1),
            "C": frac(br1_test - 1) if br1_test > 1 else "0",
            "D": frac(a / (2*b))
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Substituer y = {frac(y_test)} dans BR₁(y).</div>
<div class="step"><b>BR₁(y) = ({a} {frac_coef(c)}y) / {2*b}</b></div>
<div class="step"><b>BR₁({frac(y_test)}) = ({a} {frac_coef(c)}×{frac(y_test)}) / {2*b}</b></div>
<div class="step"><b>= ({a} {frac_coef(c*y_test)}) / {2*b} = {frac(a + c*y_test)} / {2*b} = {frac(br1_test)}</b></div>
"""
    })
    
    # ========== Q7: Système à résoudre ==========
    questions.append({
        "concept": "Système d'équilibre",
        "question": "Pour trouver l'équilibre de Nash, on résout :",
        "choix": {
            "A": "Le système BR₁(y) = x ET BR₂(x) = y",
            "B": "L'équation BR₁(y) = BR₂(x)",
            "C": "g₁(x,y) = g₂(x,y)",
            "D": "∂g₁/∂x = ∂g₂/∂y"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition équilibre :</b> (x*, y*) tel que chacun joue sa BR à l'autre.</div>
<div class="step"><b>Conditions :</b><br>
• x* = BR₁(y*) → J1 joue sa meilleure réponse à y*<br>
• y* = BR₂(x*) → J2 joue sa meilleure réponse à x*</div>
<div class="step"><b>C'est un système de 2 équations à 2 inconnues :</b><br>
x = ({a} {frac_coef(c)}y) / {2*b}<br>
y = ({d} {frac_coef(f)}x) / {2*e}</div>
<div class="tip">💡 Graphiquement : c'est l'<b>intersection</b> des courbes BR₁ et BR₂.</div>
"""
    })
    
    # ========== Q8: Résoudre le système ==========
    questions.append({
        "concept": "Résolution du système",
        "question": f"L'équilibre de Nash (x*, y*) est :",
        "choix": {
            "A": f"x* = {frac(x_star)}, y* = {frac(y_star)}",
            "B": f"x* = {frac(y_star)}, y* = {frac(x_star)}",
            "C": f"x* = {frac(x_star + 1)}, y* = {frac(y_star)}",
            "D": f"x* = {a}/{2*b}, y* = {d}/{2*e}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Substitution.</div>
<div class="step"><b>Système :</b><br>
x = ({a} {frac_coef(c)}y) / {2*b}  ... (1)<br>
y = ({d} {frac_coef(f)}x) / {2*e}  ... (2)</div>
<div class="step"><b>Substituer (2) dans (1) :</b><br>
x = ({a} {frac_coef(c)}·[({d} {frac_coef(f)}x)/{2*e}]) / {2*b}</div>
<div class="step"><b>Résoudre pour x, puis trouver y :</b><br>
x* = {frac(x_star)}<br>
y* = {frac(y_star)}</div>
<div class="tip">💡 Toujours <b>vérifier</b> en resubstituant dans les BR !</div>
"""
    })
    
    # ========== Q9: Vérification dérivée seconde ==========
    questions.append({
        "concept": "Condition du second ordre",
        "question": f"Pour confirmer que BR₁ donne un <b>maximum</b>, on vérifie :",
        "choix": {
            "A": f"∂²g₁/∂x² = -{2*b} < 0 ✓",
            "B": f"∂²g₁/∂x² = {2*b} > 0",
            "C": f"∂g₁/∂x > 0",
            "D": "g₁(x*, y*) > 0"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 CSO (Condition Second Ordre) :</b> Pour un maximum, ∂²g/∂x² < 0.</div>
<div class="step"><b>∂g₁/∂x = {a} - {2*b}x {frac_coef(c)}y</b></div>
<div class="step"><b>∂²g₁/∂x² = -{2*b}</b></div>
<div class="step"><b>-{2*b} < 0 ✓</b> → C'est bien un <b>maximum</b>.</div>
<div class="warning">⚠️ Si ∂²g/∂x² > 0, ce serait un minimum (pas ce qu'on cherche) !</div>
"""
    })
    
    # ========== Q10: Interprétation graphique ==========
    questions.append({
        "concept": "Interprétation graphique",
        "question": "Sur un graphe avec x en abscisse et y en ordonnée, l'équilibre est :",
        "choix": {
            "A": "L'intersection des courbes BR₁ et BR₂",
            "B": "Le point le plus haut de BR₁",
            "C": "L'origine (0, 0)",
            "D": "Le point où les gains sont égaux"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Graphiquement :</b><br>
• BR₁(y) : donne x en fonction de y<br>
• BR₂(x) : donne y en fonction de x</div>
<div class="step"><b>Équilibre :</b> Point (x*, y*) qui est sur <b>les deux courbes</b> simultanément.</div>
<div class="step"><b>= Intersection des BR</b></div>
<div class="tip">💡 Si les BR ne s'intersectent pas dans le domaine, il n'y a pas d'équilibre intérieur.</div>
"""
    })
    
    # ========== Q11: Équilibre aux bords ==========
    questions.append({
        "concept": "Équilibre aux bords",
        "question": "Si x ∈ [0, 1] et BR₁(y) = 1.5, que vaut la BR effective ?",
        "choix": {
            "A": "1 (bord supérieur)",
            "B": "1.5 (on garde la valeur)",
            "C": "0 (bord inférieur)",
            "D": "Pas de BR"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Contrainte :</b> Si x doit être dans [0, 1], la BR doit respecter ces bornes.</div>
<div class="step"><b>Cas BR(y) > 1 :</b> L'optimum intérieur est <b>hors domaine</b>.<br>
→ Le gain croît jusqu'à x = 1<br>
→ <b>BR effective = 1</b></div>
<div class="step"><b>Cas BR(y) < 0 :</b> Même logique → <b>BR effective = 0</b></div>
<div class="warning">⚠️ Toujours vérifier que la solution est dans l'ensemble des stratégies !</div>
"""
    })
    
    # ========== Q12: Théorème de Nash ==========
    questions.append({
        "concept": "Théorème de Nash",
        "question": "Le théorème de Nash garantit l'existence d'un équilibre si :",
        "choix": {
            "A": "Stratégies compactes convexes + gains continus quasi-concaves",
            "B": "Le jeu est à somme nulle",
            "C": "Il y a exactement 2 joueurs",
            "D": "Les gains sont positifs"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Théorème de Nash (version continue) :</b></div>
<div class="step"><b>Hypothèses :</b><br>
• Ensembles de stratégies <b>compacts</b> (fermés bornés) et <b>convexes</b><br>
• Fonctions de gain <b>continues</b><br>
• Gains <b>quasi-concaves</b> en sa propre stratégie</div>
<div class="step"><b>Conclusion :</b> Il existe au moins un équilibre de Nash.</div>
<div class="tip">💡 En TD2 Ex.2.4, on a vu des exemples où une hypothèse manque → pas d'équilibre !</div>
"""
    })
    
    return questions


# ============================================
# AFFICHAGE
# ============================================

def afficher_situation(sit):
    a, b, c = sit["a"], sit["b"], sit["c"]
    d, e, f = sit["d"], sit["e"], sit["f"]
    c_str = frac(c)
    f_str = frac(f)
    
    return f"""
    <div class="situation-box">
        <p style="margin-bottom: 16px; font-size: 13px; color: #94a3b8 !important;">Jeu continu à 2 joueurs</p>
        <p style="margin-bottom: 8px; color: #f8fafc !important;"><b>Joueur 1</b> choisit x ∈ ℝ⁺</p>
        <div class="formula">g₁(x, y) = {a}x - {b}x² {frac_coef(c)}xy</div>
        <p style="margin: 16px 0 8px 0; color: #f8fafc !important;"><b>Joueur 2</b> choisit y ∈ ℝ⁺</p>
        <div class="formula">g₂(x, y) = {d}y - {e}y² {frac_coef(f)}xy</div>
    </div>
    """


# ============================================
# PAGES
# ============================================

def page_menu():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("# 📈 Bloc B — Jeux Continus")
    st.markdown("*Exercice complet avec 12 questions*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    **Concepts couverts :**
    - Identifier un jeu continu
    - Dérivée partielle ∂g/∂x
    - Condition du premier ordre (CPO)
    - Calculer BR₁(y) et BR₂(x)
    - Évaluer BR en un point
    - Résoudre le système d'équilibre
    - Condition du second ordre (CSO)
    - Interprétation graphique
    - Équilibre aux bords
    - Théorème de Nash
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Commencer l'exercice", use_container_width=True):
        sit = generer_situation()
        st.session_state.sit_b = sit
        st.session_state.questions_b = generer_questions(sit)
        st.session_state.idx_b = 0
        st.session_state.score_b = 0
        st.session_state.answered_b = False
        st.session_state.selected_b = None
        st.session_state.started_b = True
        st.rerun()


def page_question():
    sit = st.session_state.sit_b
    questions = st.session_state.questions_b
    idx = st.session_state.idx_b
    
    if idx >= len(questions):
        page_results()
        return
    
    q = questions[idx]
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Menu"):
            st.session_state.started_b = False
            st.rerun()
    with col2:
        st.progress(idx / len(questions))
    with col3:
        st.markdown(f"**Q{idx + 1}/{len(questions)}** — {st.session_state.score_b} ✓")
    
    # Situation
    st.markdown(afficher_situation(sit), unsafe_allow_html=True)
    
    # Question
    st.markdown(f"<span class='concept-tag'>{q['concept']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;margin-top:10px;color:#1a1a1a;'>{q['question']}</p>", unsafe_allow_html=True)
    
    # Choix
    if not st.session_state.answered_b:
        for lettre, texte in q["choix"].items():
            if st.button(f"{lettre}. {texte}", key=f"btn_{lettre}", use_container_width=True):
                st.session_state.selected_b = lettre
                st.session_state.answered_b = True
                if lettre == q["reponse"]:
                    st.session_state.score_b += 1
                st.rerun()
    else:
        # Afficher résultat
        for lettre, texte in q["choix"].items():
            if lettre == q["reponse"]:
                st.markdown(f'<div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:8px;padding:10px;margin:4px 0;color:#166534;"><b>✓ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            elif lettre == st.session_state.selected_b:
                st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:10px;margin:4px 0;color:#991b1b;"><b>✗ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#f5f5f5;border-radius:8px;padding:10px;margin:4px 0;opacity:0.5;color:#666;">{lettre}. {texte}</div>', unsafe_allow_html=True)
        
        # Message
        if st.session_state.selected_b == q["reponse"]:
            st.markdown('<div class="correct-box"><b style="color:#22c55e;font-size:18px;">✓ Correct !</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="incorrect-box"><b style="color:#ef4444;font-size:18px;">✗ Incorrect</b><br><span style="color:#991b1b;">La bonne réponse était <b>{q["reponse"]}</b></span></div>', unsafe_allow_html=True)
        
        # Explication
        st.markdown(f'<div class="explication"><b style="color:#3b82f6;">💡 Explication détaillée</b>{q["explication"]}</div>', unsafe_allow_html=True)
        
        # Bouton suivant
        st.markdown("<br>", unsafe_allow_html=True)
        btn_txt = "Question suivante →" if idx < len(questions) - 1 else "Voir les résultats"
        if st.button(btn_txt, use_container_width=True, type="primary"):
            st.session_state.idx_b += 1
            st.session_state.answered_b = False
            st.session_state.selected_b = None
            st.rerun()


def page_results():
    score = st.session_state.score_b
    total = len(st.session_state.questions_b)
    pct = score / total * 100
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    color = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
    
    st.markdown(f"""
    <div style="text-align:center;">
        <div style="width:150px;height:150px;border-radius:50%;background:#fafafa;border:4px solid {color};display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto;">
            <span style="font-size:36px;font-weight:700;color:{color};">{score}/{total}</span>
            <span style="font-size:14px;color:#888;">{pct:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if pct >= 80:
        st.markdown("<p style='text-align:center;font-size:20px;color:#1a1a1a;'>🏆 Excellent ! Tu maîtrises le Bloc B.</p>", unsafe_allow_html=True)
    elif pct >= 60:
        st.markdown("<p style='text-align:center;font-size:20px;color:#1a1a1a;'>👍 Bien joué !</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;font-size:20px;color:#1a1a1a;'>📚 Continue à réviser.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Menu", use_container_width=True):
            st.session_state.started_b = False
            st.rerun()
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True, type="primary"):
            sit = generer_situation()
            st.session_state.sit_b = sit
            st.session_state.questions_b = generer_questions(sit)
            st.session_state.idx_b = 0
            st.session_state.score_b = 0
            st.session_state.answered_b = False
            st.session_state.selected_b = None
            st.rerun()


# ============================================
# MAIN
# ============================================

if st.session_state.started_b:
    if st.session_state.idx_b < len(st.session_state.questions_b):
        page_question()
    else:
        page_results()
else:
    page_menu()
