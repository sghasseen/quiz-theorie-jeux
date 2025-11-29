"""
BLOC A - JEUX FINIS (MATRICES)
Exercice complet avec ~18 questions couvrant tous les concepts des TDs
"""

import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Bloc A - Jeux Finis", page_icon="🎯", layout="centered")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #fff; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .situation-box {
        background: #1a1a1a;
        color: white;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
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
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        margin: 16px 0;
        border-radius: 0 12px 12px 0;
    }
    
    .step {
        background: #f8fafc;
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 6px;
        border-left: 3px solid #94a3b8;
    }
    
    .warning {
        background: #fef3c7;
        border-left: 3px solid #f59e0b;
        padding: 10px 14px;
        margin: 10px 0;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
    }
    
    .tip {
        background: #ecfdf5;
        border-left: 3px solid #10b981;
        padding: 10px 14px;
        margin: 10px 0;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
    }
    
    .stButton > button {
        background-color: #1a1a1a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover { background-color: #333; }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if "sit" not in st.session_state:
    st.session_state.sit = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "started" not in st.session_state:
    st.session_state.started = False


# ============================================
# GÉNÉRATION DE LA SITUATION
# ============================================

def generer_situation():
    """Génère une matrice 2x2 avec propriétés intéressantes"""
    
    while True:
        # Générer matrice avec valeurs variées
        m = [
            [(random.randint(-2, 6), random.randint(-2, 6)), 
             (random.randint(-2, 6), random.randint(-2, 6))],
            [(random.randint(-2, 6), random.randint(-2, 6)), 
             (random.randint(-2, 6), random.randint(-2, 6))]
        ]
        
        # Extraire gains
        g1 = [[m[i][j][0] for j in range(2)] for i in range(2)]  # gains J1
        g2 = [[m[i][j][1] for j in range(2)] for i in range(2)]  # gains J2
        
        # BR de J1 (pour chaque colonne, quelle ligne maximise g1)
        br1 = {}
        for j in range(2):
            if g1[0][j] > g1[1][j]:
                br1[j] = [0]
            elif g1[0][j] < g1[1][j]:
                br1[j] = [1]
            else:
                br1[j] = [0, 1]
        
        # BR de J2 (pour chaque ligne, quelle colonne maximise g2)
        br2 = {}
        for i in range(2):
            if g2[i][0] > g2[i][1]:
                br2[i] = [0]
            elif g2[i][0] < g2[i][1]:
                br2[i] = [1]
            else:
                br2[i] = [0, 1]
        
        # Équilibres de Nash
        equilibres = []
        for i in range(2):
            for j in range(2):
                if i in br1[j] and j in br2[i]:
                    equilibres.append((i, j))
        
        # On veut exactement 1 équilibre pour simplicité
        if len(equilibres) != 1:
            continue
        
        # Vérifier dominance J1
        dom_j1 = None
        # H domine B ?
        if g1[0][0] >= g1[1][0] and g1[0][1] >= g1[1][1]:
            if g1[0][0] > g1[1][0] or g1[0][1] > g1[1][1]:
                strict = g1[0][0] > g1[1][0] and g1[0][1] > g1[1][1]
                dom_j1 = ("B", "H", "stricte" if strict else "faible")
        # B domine H ?
        elif g1[1][0] >= g1[0][0] and g1[1][1] >= g1[0][1]:
            if g1[1][0] > g1[0][0] or g1[1][1] > g1[0][1]:
                strict = g1[1][0] > g1[0][0] and g1[1][1] > g1[0][1]
                dom_j1 = ("H", "B", "stricte" if strict else "faible")
        
        # Vérifier dominance J2
        dom_j2 = None
        # G domine D ?
        if g2[0][0] >= g2[0][1] and g2[1][0] >= g2[1][1]:
            if g2[0][0] > g2[0][1] or g2[1][0] > g2[1][1]:
                strict = g2[0][0] > g2[0][1] and g2[1][0] > g2[1][1]
                dom_j2 = ("D", "G", "stricte" if strict else "faible")
        # D domine G ?
        elif g2[0][1] >= g2[0][0] and g2[1][1] >= g2[1][0]:
            if g2[0][1] > g2[0][0] or g2[1][1] > g2[1][0]:
                strict = g2[0][1] > g2[0][0] and g2[1][1] > g2[1][0]
                dom_j2 = ("G", "D", "stricte" if strict else "faible")
        
        # Issue préférée J1
        best_g1 = max(g1[i][j] for i in range(2) for j in range(2))
        pref_j1 = [(i, j) for i in range(2) for j in range(2) if g1[i][j] == best_g1][0]
        
        # Issue préférée J2
        best_g2 = max(g2[i][j] for i in range(2) for j in range(2))
        pref_j2 = [(i, j) for i in range(2) for j in range(2) if g2[i][j] == best_g2][0]
        
        # Pareto
        def domine_pareto(a, b):
            """a domine b si a >= b pour les deux et > pour au moins un"""
            return (a[0] >= b[0] and a[1] >= b[1]) and (a[0] > b[0] or a[1] > b[1])
        
        pareto = []
        for i in range(2):
            for j in range(2):
                gains = (g1[i][j], g2[i][j])
                dominated = False
                for ii in range(2):
                    for jj in range(2):
                        if (ii, jj) != (i, j):
                            other = (g1[ii][jj], g2[ii][jj])
                            if domine_pareto(other, gains):
                                dominated = True
                                break
                    if dominated:
                        break
                if not dominated:
                    pareto.append((i, j))
        
        # Jeu dans la stratégie pour J1 ?
        # J1 a du jeu dans la stratégie si sa BR dépend de ce que joue J2
        jeu_strategie_j1 = br1[0] != br1[1]
        
        # Jeu dans le paiement pour J1 ?
        # Le gain de J1 dépend de J2
        jeu_paiement_j1 = not (g1[0][0] == g1[0][1] and g1[1][0] == g1[1][1])
        
        # On accepte cette matrice
        break
    
    return {
        "matrice": m,
        "g1": g1,
        "g2": g2,
        "br1": br1,
        "br2": br2,
        "equilibres": equilibres,
        "dom_j1": dom_j1,
        "dom_j2": dom_j2,
        "pref_j1": pref_j1,
        "pref_j2": pref_j2,
        "pareto": pareto,
        "jeu_strategie_j1": jeu_strategie_j1,
        "jeu_paiement_j1": jeu_paiement_j1,
        "lignes": ["H", "B"],
        "colonnes": ["G", "D"]
    }


# ============================================
# GÉNÉRATION DES QUESTIONS
# ============================================

def generer_questions(sit):
    """Génère toutes les questions pour le bloc A"""
    
    m = sit["matrice"]
    g1, g2 = sit["g1"], sit["g2"]
    L, C = sit["lignes"], sit["colonnes"]
    eq = sit["equilibres"][0]
    
    questions = []
    
    # ========== Q1: Lire gain J1 ==========
    i, j = random.randint(0, 1), random.randint(0, 1)
    questions.append({
        "concept": "Lire une matrice",
        "question": f"Quel est le <b>gain de J1</b> si J1 joue <b>{L[i]}</b> et J2 joue <b>{C[j]}</b> ?",
        "choix": {
            "A": str(g1[i][j]),
            "B": str(g2[i][j]),
            "C": str(g1[i][j] + g2[i][j]),
            "D": str(abs(g1[i][j] - g2[i][j]))
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Rappel :</b> Chaque case contient <b>(gain J1, gain J2)</b></div>
<div class="step"><b>Étape 1 :</b> Localiser la case ({L[i]}, {C[j]})</div>
<div class="step"><b>Étape 2 :</b> Lire le couple : ({g1[i][j]}, {g2[i][j]})</div>
<div class="step"><b>Étape 3 :</b> Le gain de J1 est le <b>premier nombre</b> = <b>{g1[i][j]}</b></div>
<div class="warning">⚠️ <b>Piège :</b> Ne pas confondre gain J1 et gain J2 !</div>
"""
    })
    
    # ========== Q2: Lire gain J2 ==========
    i2, j2 = 1 - i, 1 - j  # autre case
    questions.append({
        "concept": "Lire une matrice",
        "question": f"Quel est le <b>gain de J2</b> si J1 joue <b>{L[i2]}</b> et J2 joue <b>{C[j2]}</b> ?",
        "choix": {
            "A": str(g2[i2][j2]),
            "B": str(g1[i2][j2]),
            "C": str(-g2[i2][j2]),
            "D": str(g1[i2][j2] + g2[i2][j2])
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Rappel :</b> Case = (gain J1, gain J2)</div>
<div class="step"><b>Case ({L[i2]}, {C[j2]}) :</b> ({g1[i2][j2]}, {g2[i2][j2]})</div>
<div class="step"><b>Gain de J2</b> = <b>deuxième nombre</b> = <b>{g2[i2][j2]}</b></div>
<div class="tip">💡 J1 choisit la ligne, J2 choisit la colonne.</div>
"""
    })
    
    # ========== Q3: Issue préférée J1 ==========
    pj1 = sit["pref_j1"]
    autres = [(ii, jj) for ii in range(2) for jj in range(2) if (ii, jj) != pj1]
    random.shuffle(autres)
    
    questions.append({
        "concept": "Issue préférée",
        "question": "Quelle est l'<b>issue préférée par J1</b> ?",
        "choix": {
            "A": f"({L[pj1[0]]}, {C[pj1[1]]}) avec gain {g1[pj1[0]][pj1[1]]}",
            "B": f"({L[autres[0][0]]}, {C[autres[0][1]]}) avec gain {g1[autres[0][0]][autres[0][1]]}",
            "C": f"({L[autres[1][0]]}, {C[autres[1][1]]}) avec gain {g1[autres[1][0]][autres[1][1]]}",
            "D": f"({L[autres[2][0]]}, {C[autres[2][1]]}) avec gain {g1[autres[2][0]][autres[2][1]]}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Regarder <b>uniquement les gains de J1</b> (1er nombre)</div>
<div class="step"><b>Gains de J1 dans chaque case :</b><br>
• ({L[0]}, {C[0]}) → {g1[0][0]}<br>
• ({L[0]}, {C[1]}) → {g1[0][1]}<br>
• ({L[1]}, {C[0]}) → {g1[1][0]}<br>
• ({L[1]}, {C[1]}) → {g1[1][1]}</div>
<div class="step"><b>Maximum :</b> {g1[pj1[0]][pj1[1]]} en case <b>({L[pj1[0]]}, {C[pj1[1]]})</b></div>
<div class="warning">⚠️ L'issue préférée n'est PAS forcément atteignable ni un équilibre !</div>
"""
    })
    
    # ========== Q4: Issue préférée J2 ==========
    pj2 = sit["pref_j2"]
    questions.append({
        "concept": "Issue préférée",
        "question": "Quelle est l'<b>issue préférée par J2</b> ?",
        "choix": {
            "A": f"({L[pj2[0]]}, {C[pj2[1]]}) avec gain {g2[pj2[0]][pj2[1]]}",
            "B": f"({L[1-pj2[0]]}, {C[pj2[1]]}) avec gain {g2[1-pj2[0]][pj2[1]]}",
            "C": f"({L[pj2[0]]}, {C[1-pj2[1]]}) avec gain {g2[pj2[0]][1-pj2[1]]}",
            "D": f"({L[1-pj2[0]]}, {C[1-pj2[1]]}) avec gain {g2[1-pj2[0]][1-pj2[1]]}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Regarder <b>uniquement les gains de J2</b> (2ème nombre)</div>
<div class="step"><b>Gains de J2 dans chaque case :</b><br>
• ({L[0]}, {C[0]}) → {g2[0][0]}<br>
• ({L[0]}, {C[1]}) → {g2[0][1]}<br>
• ({L[1]}, {C[0]}) → {g2[1][0]}<br>
• ({L[1]}, {C[1]}) → {g2[1][1]}</div>
<div class="step"><b>Maximum :</b> {g2[pj2[0]][pj2[1]]} en case <b>({L[pj2[0]]}, {C[pj2[1]]})</b></div>
"""
    })
    
    # ========== Q5: BR de J1 ==========
    col_test = random.randint(0, 1)
    br_j1 = sit["br1"][col_test][0]  # prendre le premier si plusieurs
    
    questions.append({
        "concept": "Meilleure réponse (BR)",
        "question": f"Si J2 joue <b>{C[col_test]}</b>, quelle est la <b>meilleure réponse de J1</b> ?",
        "choix": {
            "A": f"{L[br_j1]} (gain {g1[br_j1][col_test]})",
            "B": f"{L[1-br_j1]} (gain {g1[1-br_j1][col_test]})",
            "C": "Indifférent",
            "D": "Aucune"
        },
        "reponse": "A" if len(sit["br1"][col_test]) == 1 else "C",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> BR(s₂) = stratégie de J1 qui <b>maximise son gain</b> quand J2 joue s₂</div>
<div class="step"><b>J2 joue {C[col_test]} :</b> on regarde la colonne {C[col_test]}<br>
• Si J1 joue {L[0]} → gain = {g1[0][col_test]}<br>
• Si J1 joue {L[1]} → gain = {g1[1][col_test]}</div>
<div class="step"><b>Comparaison :</b> {g1[0][col_test]} {">" if g1[0][col_test] > g1[1][col_test] else "<" if g1[0][col_test] < g1[1][col_test] else "="} {g1[1][col_test]}</div>
<div class="step"><b>Donc BR({C[col_test]}) = {L[br_j1]}</b></div>
<div class="tip">💡 <b>Méthode du soulignement :</b> On souligne le max de chaque colonne pour J1.</div>
"""
    })
    
    # ========== Q6: BR de J2 ==========
    lig_test = random.randint(0, 1)
    br_j2 = sit["br2"][lig_test][0]
    
    questions.append({
        "concept": "Meilleure réponse (BR)",
        "question": f"Si J1 joue <b>{L[lig_test]}</b>, quelle est la <b>meilleure réponse de J2</b> ?",
        "choix": {
            "A": f"{C[br_j2]} (gain {g2[lig_test][br_j2]})",
            "B": f"{C[1-br_j2]} (gain {g2[lig_test][1-br_j2]})",
            "C": "Indifférent",
            "D": "Aucune"
        },
        "reponse": "A" if len(sit["br2"][lig_test]) == 1 else "C",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> BR(s₁) = stratégie de J2 qui <b>maximise son gain</b> quand J1 joue s₁</div>
<div class="step"><b>J1 joue {L[lig_test]} :</b> on regarde la ligne {L[lig_test]}<br>
• Si J2 joue {C[0]} → gain J2 = {g2[lig_test][0]}<br>
• Si J2 joue {C[1]} → gain J2 = {g2[lig_test][1]}</div>
<div class="step"><b>Comparaison :</b> {g2[lig_test][0]} {">" if g2[lig_test][0] > g2[lig_test][1] else "<" if g2[lig_test][0] < g2[lig_test][1] else "="} {g2[lig_test][1]}</div>
<div class="step"><b>Donc BR({L[lig_test]}) = {C[br_j2]}</b></div>
"""
    })
    
    # ========== Q7: Méthode du soulignement ==========
    # Construire les soulignements
    soul_j1 = [(sit["br1"][j][0], j) for j in range(2)]  # (ligne, colonne)
    soul_j2 = [(i, sit["br2"][i][0]) for i in range(2)]  # (ligne, colonne)
    
    questions.append({
        "concept": "Méthode du soulignement",
        "question": "Appliquer la <b>méthode du soulignement</b>. Combien de cases ont <b>2 soulignements</b> ?",
        "choix": {
            "A": "1 case",
            "B": "2 cases",
            "C": "0 case",
            "D": "4 cases"
        },
        "reponse": "A",  # on a forcé 1 équilibre
        "explication": f"""
<div class="step"><b>📌 Méthode du soulignement :</b><br>
• Pour J1 : dans chaque <b>colonne</b>, souligner le max des gains J1<br>
• Pour J2 : dans chaque <b>ligne</b>, souligner le max des gains J2</div>

<div class="step"><b>Soulignements J1 (par colonne) :</b><br>
• Colonne {C[0]} : max({g1[0][0]}, {g1[1][0]}) → souligner <b>{L[soul_j1[0][0]]}</b><br>
• Colonne {C[1]} : max({g1[0][1]}, {g1[1][1]}) → souligner <b>{L[soul_j1[1][0]]}</b></div>

<div class="step"><b>Soulignements J2 (par ligne) :</b><br>
• Ligne {L[0]} : max({g2[0][0]}, {g2[0][1]}) → souligner <b>{C[soul_j2[0][1]]}</b><br>
• Ligne {L[1]} : max({g2[1][0]}, {g2[1][1]}) → souligner <b>{C[soul_j2[1][1]]}</b></div>

<div class="step"><b>Case avec 2 soulignements :</b> <b>({L[eq[0]]}, {C[eq[1]]})</b> = équilibre de Nash</div>
"""
    })
    
    # ========== Q8: Équilibre de Nash ==========
    eq_str = f"({L[eq[0]]}, {C[eq[1]]})"
    
    questions.append({
        "concept": "Équilibre de Nash",
        "question": "Quel est l'<b>équilibre de Nash</b> en stratégies pures ?",
        "choix": {
            "A": eq_str,
            "B": f"({L[1-eq[0]]}, {C[eq[1]]})",
            "C": f"({L[eq[0]]}, {C[1-eq[1]]})",
            "D": f"({L[1-eq[0]]}, {C[1-eq[1]]})"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> Un équilibre de Nash est un profil (s₁*, s₂*) tel que :<br>
• s₁* est BR à s₂* (J1 ne veut pas dévier)<br>
• s₂* est BR à s₁* (J2 ne veut pas dévier)</div>

<div class="step"><b>Vérification pour {eq_str} :</b><br>
• J2 joue {C[eq[1]]} → BR de J1 = {L[sit["br1"][eq[1]][0]]} ✓<br>
• J1 joue {L[eq[0]]} → BR de J2 = {C[sit["br2"][eq[0]][0]]} ✓</div>

<div class="step"><b>Conclusion :</b> {eq_str} est l'unique équilibre de Nash.</div>

<div class="tip">💡 À l'équilibre, <b>aucun joueur ne regrette</b> son choix une fois le choix adverse révélé.</div>
"""
    })
    
    # ========== Q9: Stratégie dominée J1 ==========
    dom = sit["dom_j1"]
    if dom:
        questions.append({
            "concept": "Stratégie dominée",
            "question": f"J1 a-t-il une <b>stratégie strictement dominée</b> ?",
            "choix": {
                "A": f"Oui, {dom[0]} est dominée par {dom[1]}",
                "B": f"Oui, {dom[1]} est dominée par {dom[0]}",
                "C": "Non, aucune stratégie strictement dominée",
                "D": "Les deux sont équivalentes"
            },
            "reponse": "A" if dom[2] == "stricte" else "C",
            "explication": f"""
<div class="step"><b>📌 Définition :</b><br>
• <b>Dominance stricte :</b> s₁ domine s₂ si g(s₁) > g(s₂) pour <b>toute</b> stratégie adverse<br>
• <b>Dominance faible :</b> s₁ domine s₂ si g(s₁) ≥ g(s₂) partout et > quelque part</div>

<div class="step"><b>Comparaison pour J1 :</b><br>
• Si J2 joue {C[0]} : {L[0]} → {g1[0][0]}, {L[1]} → {g1[1][0]}<br>
• Si J2 joue {C[1]} : {L[0]} → {g1[0][1]}, {L[1]} → {g1[1][1]}</div>

<div class="step"><b>Analyse :</b> {dom[1]} donne {g1[0 if dom[1]=="H" else 1][0]}, {g1[0 if dom[1]=="H" else 1][1]}<br>
{dom[0]} donne {g1[0 if dom[0]=="H" else 1][0]}, {g1[0 if dom[0]=="H" else 1][1]}</div>

<div class="step"><b>Conclusion :</b> {dom[0]} est dominée ({dom[2]}ment) par {dom[1]}</div>
"""
        })
    else:
        questions.append({
            "concept": "Stratégie dominée",
            "question": "J1 a-t-il une <b>stratégie strictement dominée</b> ?",
            "choix": {
                "A": "Non, aucune stratégie strictement dominée",
                "B": "Oui, H est dominée par B",
                "C": "Oui, B est dominée par H",
                "D": "Les deux sont dominées"
            },
            "reponse": "A",
            "explication": f"""
<div class="step"><b>📌 Définition :</b> s₁ domine strictement s₂ si g(s₁) > g(s₂) pour <b>toute</b> stratégie adverse</div>

<div class="step"><b>Comparaison pour J1 :</b><br>
• Si J2 joue {C[0]} : {L[0]} → {g1[0][0]}, {L[1]} → {g1[1][0]}<br>
• Si J2 joue {C[1]} : {L[0]} → {g1[0][1]}, {L[1]} → {g1[1][1]}</div>

<div class="step"><b>Analyse :</b><br>
• {L[0]} vs {L[1]} sur {C[0]} : {g1[0][0]} vs {g1[1][0]}<br>
• {L[0]} vs {L[1]} sur {C[1]} : {g1[0][1]} vs {g1[1][1]}</div>

<div class="step"><b>Conclusion :</b> Aucune stratégie n'est <b>toujours</b> meilleure → pas de dominance stricte</div>
"""
        })
    
    # ========== Q10: Jeu dans la stratégie ==========
    jeu_strat = sit["jeu_strategie_j1"]
    
    questions.append({
        "concept": "Jeu dans la stratégie",
        "question": "Y a-t-il <b>jeu dans la stratégie</b> pour J1 ?",
        "choix": {
            "A": "Oui" if jeu_strat else "Non",
            "B": "Non" if jeu_strat else "Oui",
            "C": "Ça dépend de J2",
            "D": "Impossible à déterminer"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> J1 a du <b>jeu dans la stratégie</b> si sa meilleure réponse <b>dépend</b> de ce que joue J2.</div>

<div class="step"><b>BR de J1 :</b><br>
• Si J2 joue {C[0]} → BR = {L[sit["br1"][0][0]]}<br>
• Si J2 joue {C[1]} → BR = {L[sit["br1"][1][0]]}</div>

<div class="step"><b>Comparaison :</b> {L[sit["br1"][0][0]]} {"≠" if jeu_strat else "="} {L[sit["br1"][1][0]]}</div>

<div class="step"><b>Conclusion :</b> {"La BR change selon J2 → J1 a du jeu dans la stratégie" if jeu_strat else "La BR est toujours la même → J1 n'a PAS de jeu dans la stratégie"}</div>

<div class="tip">💡 Pas de jeu dans la stratégie = stratégie dominante (faiblement ou strictement)</div>
"""
    })
    
    # ========== Q11: Jeu dans le paiement ==========
    jeu_paie = sit["jeu_paiement_j1"]
    
    questions.append({
        "concept": "Jeu dans le paiement",
        "question": "Y a-t-il <b>jeu dans le paiement</b> pour J1 ?",
        "choix": {
            "A": "Oui" if jeu_paie else "Non",
            "B": "Non" if jeu_paie else "Oui",
            "C": "Seulement si J1 joue H",
            "D": "Impossible à déterminer"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> J1 a du <b>jeu dans le paiement</b> si son gain <b>dépend</b> de ce que joue J2.</div>

<div class="step"><b>Gains de J1 :</b><br>
• Si J1 joue {L[0]} : gain = {g1[0][0]} (si J2 joue {C[0]}) ou {g1[0][1]} (si J2 joue {C[1]})<br>
• Si J1 joue {L[1]} : gain = {g1[1][0]} (si J2 joue {C[0]}) ou {g1[1][1]} (si J2 joue {C[1]})</div>

<div class="step"><b>Conclusion :</b> {"Les gains varient selon J2 → J1 a du jeu dans le paiement" if jeu_paie else "Les gains sont constants → J1 n'a PAS de jeu dans le paiement"}</div>

<div class="warning">⚠️ On peut avoir jeu dans le paiement SANS avoir jeu dans la stratégie (cf TD1 Ex.1)</div>
"""
    })
    
    # ========== Q12: Pareto ==========
    pareto = sit["pareto"]
    eq_pareto = eq in pareto
    
    questions.append({
        "concept": "Optimum de Pareto",
        "question": f"L'équilibre {eq_str} est-il <b>Pareto-optimal</b> ?",
        "choix": {
            "A": "Oui" if eq_pareto else "Non",
            "B": "Non" if eq_pareto else "Oui",
            "C": "Pareto ne s'applique pas ici",
            "D": "Tous les équilibres sont Pareto"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> Une issue est <b>Pareto-optimale</b> si on ne peut pas améliorer un joueur <b>sans détériorer</b> l'autre.</div>

<div class="step"><b>Gains à l'équilibre {eq_str} :</b> ({g1[eq[0]][eq[1]]}, {g2[eq[0]][eq[1]]})</div>

<div class="step"><b>Comparaison avec les autres issues :</b><br>
• ({L[0]}, {C[0]}) : ({g1[0][0]}, {g2[0][0]})<br>
• ({L[0]}, {C[1]}) : ({g1[0][1]}, {g2[0][1]})<br>
• ({L[1]}, {C[0]}) : ({g1[1][0]}, {g2[1][0]})<br>
• ({L[1]}, {C[1]}) : ({g1[1][1]}, {g2[1][1]})</div>

<div class="step"><b>Conclusion :</b> {"Aucune issue ne domine l'équilibre → Pareto-optimal ✓" if eq_pareto else "Une autre issue améliore les deux joueurs → PAS Pareto-optimal ✗"}</div>

<div class="warning">⚠️ <b>Dilemme du prisonnier :</b> L'équilibre de Nash n'est pas toujours Pareto-optimal !</div>
"""
    })
    
    # ========== Q13: Quelles issues sont Pareto ? ==========
    pareto_strs = [f"({L[p[0]]}, {C[p[1]]})" for p in pareto]
    
    questions.append({
        "concept": "Optimum de Pareto",
        "question": "Combien d'issues sont <b>Pareto-optimales</b> ?",
        "choix": {
            "A": str(len(pareto)),
            "B": str(len(pareto) + 1) if len(pareto) < 4 else "3",
            "C": str(max(1, len(pareto) - 1)),
            "D": "4"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Méthode :</b> Pour chaque issue, vérifier si une autre la <b>domine au sens de Pareto</b>.</div>

<div class="step"><b>Analyse :</b> Une issue (g₁, g₂) est dominée si ∃ une autre avec gains ≥ partout et > quelque part.</div>

<div class="step"><b>Issues Pareto-optimales :</b> {", ".join(pareto_strs)}</div>

<div class="step"><b>Total :</b> {len(pareto)} issue(s) Pareto-optimale(s)</div>
"""
    })
    
    # ========== Q14: Issue réaliste ? ==========
    pref = sit["pref_j1"]
    pref_realiste = pref == eq
    
    questions.append({
        "concept": "Issue réaliste",
        "question": f"L'issue préférée de J1, ({L[pref[0]]}, {C[pref[1]]}), est-elle <b>réaliste</b> ?",
        "choix": {
            "A": "Oui, c'est l'équilibre" if pref_realiste else "Non, J2 dévierait",
            "B": "Non, J2 dévierait" if pref_realiste else "Oui, c'est l'équilibre",
            "C": "Ça dépend",
            "D": "Toute issue est réaliste"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Question :</b> Si on se retrouve en ({L[pref[0]]}, {C[pref[1]]}), J2 a-t-il intérêt à <b>dévier</b> ?</div>

<div class="step"><b>À l'issue ({L[pref[0]]}, {C[pref[1]]}) :</b><br>
• Gain J2 si {C[pref[1]]} : {g2[pref[0]][pref[1]]}<br>
• Gain J2 si {C[1-pref[1]]} : {g2[pref[0]][1-pref[1]]}</div>

<div class="step"><b>BR de J2 à {L[pref[0]]} :</b> {C[sit["br2"][pref[0]][0]]}</div>

<div class="step"><b>Conclusion :</b> {"L'issue préférée de J1 est aussi l'équilibre → réaliste ✓" if pref_realiste else f"J2 préfère jouer {C[sit['br2'][pref[0]][0]]} → J1 ne peut pas imposer son issue préférée"}</div>
"""
    })
    
    # ========== Q15: Déviation unilatérale ==========
    # Choisir une case qui n'est PAS l'équilibre
    non_eq = [(i, j) for i in range(2) for j in range(2) if (i, j) != eq][0]
    
    questions.append({
        "concept": "Déviation unilatérale",
        "question": f"Si on est en ({L[non_eq[0]]}, {C[non_eq[1]]}), qui a intérêt à <b>dévier unilatéralement</b> ?",
        "choix": {
            "A": "J1" if non_eq[0] not in sit["br1"][non_eq[1]] else ("J2" if non_eq[1] not in sit["br2"][non_eq[0]] else "Aucun"),
            "B": "J2" if non_eq[0] not in sit["br1"][non_eq[1]] else "J1",
            "C": "Les deux",
            "D": "Aucun"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Définition :</b> Un joueur veut dévier si sa stratégie actuelle n'est <b>pas une BR</b> à l'autre.</div>

<div class="step"><b>En ({L[non_eq[0]]}, {C[non_eq[1]]}) :</b><br>
• J1 joue {L[non_eq[0]]}, J2 joue {C[non_eq[1]]}</div>

<div class="step"><b>BR de J1 à {C[non_eq[1]]} :</b> {L[sit["br1"][non_eq[1]][0]]} → {"J1 est content ✓" if non_eq[0] in sit["br1"][non_eq[1]] else "J1 veut dévier !"}</div>

<div class="step"><b>BR de J2 à {L[non_eq[0]]} :</b> {C[sit["br2"][non_eq[0]][0]]} → {"J2 est content ✓" if non_eq[1] in sit["br2"][non_eq[0]] else "J2 veut dévier !"}</div>

<div class="tip">💡 C'est pour ça que ({L[non_eq[0]]}, {C[non_eq[1]]}) n'est <b>pas</b> un équilibre de Nash.</div>
"""
    })
    
    # ========== Q16: Gains à l'équilibre ==========
    questions.append({
        "concept": "Gains à l'équilibre",
        "question": f"Quels sont les <b>gains</b> à l'équilibre {eq_str} ?",
        "choix": {
            "A": f"J1 gagne {g1[eq[0]][eq[1]]}, J2 gagne {g2[eq[0]][eq[1]]}",
            "B": f"J1 gagne {g2[eq[0]][eq[1]]}, J2 gagne {g1[eq[0]][eq[1]]}",
            "C": f"J1 gagne {g1[eq[0]][eq[1]] + g2[eq[0]][eq[1]]}, J2 gagne 0",
            "D": f"Chacun gagne {(g1[eq[0]][eq[1]] + g2[eq[0]][eq[1]])//2}"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>Équilibre :</b> {eq_str}</div>
<div class="step"><b>Case correspondante :</b> ({g1[eq[0]][eq[1]]}, {g2[eq[0]][eq[1]]})</div>
<div class="step"><b>Gains :</b><br>
• J1 obtient <b>{g1[eq[0]][eq[1]]}</b><br>
• J2 obtient <b>{g2[eq[0]][eq[1]]}</b></div>
"""
    })
    
    # ========== Q17: EISD applicable ? ==========
    eisd_possible = sit["dom_j1"] is not None or sit["dom_j2"] is not None
    
    questions.append({
        "concept": "EISD",
        "question": "Peut-on appliquer l'<b>EISD</b> (Élimination Itérée des Stratégies Dominées) ?",
        "choix": {
            "A": "Oui" if eisd_possible else "Non, aucune stratégie dominée",
            "B": "Non, aucune stratégie dominée" if eisd_possible else "Oui",
            "C": "Seulement pour J1",
            "D": "L'EISD ne s'applique pas aux jeux 2×2"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 EISD :</b> Éliminer tour à tour les stratégies (strictement) dominées.</div>

<div class="step"><b>Stratégies dominées :</b><br>
• J1 : {sit["dom_j1"][0] + " dominée par " + sit["dom_j1"][1] if sit["dom_j1"] else "Aucune"}<br>
• J2 : {sit["dom_j2"][0] + " dominée par " + sit["dom_j2"][1] if sit["dom_j2"] else "Aucune"}</div>

<div class="step"><b>Conclusion :</b> {"On peut simplifier le jeu par EISD ✓" if eisd_possible else "Pas de dominance stricte → EISD non applicable"}</div>

<div class="tip">💡 L'EISD préserve les équilibres de Nash (si dominance stricte).</div>
"""
    })
    
    # ========== Q18: Résumé final ==========
    questions.append({
        "concept": "Synthèse",
        "question": "Quelle affirmation est <b>VRAIE</b> pour ce jeu ?",
        "choix": {
            "A": f"L'équilibre est {eq_str} avec gains ({g1[eq[0]][eq[1]]}, {g2[eq[0]][eq[1]]})",
            "B": f"J1 préfère l'équilibre à toute autre issue",
            "C": f"Le jeu n'a pas d'équilibre en stratégies pures",
            "D": f"L'équilibre est Pareto-dominé" if eq_pareto else "L'équilibre est le seul optimum de Pareto"
        },
        "reponse": "A",
        "explication": f"""
<div class="step"><b>📌 Récapitulatif du jeu :</b></div>

<div class="step"><b>Équilibre de Nash :</b> {eq_str}<br>
Gains : J1 = {g1[eq[0]][eq[1]]}, J2 = {g2[eq[0]][eq[1]]}</div>

<div class="step"><b>Issue préférée J1 :</b> ({L[pref[0]]}, {C[pref[1]]}) avec gain {g1[pref[0]][pref[1]]}<br>
{"= équilibre ✓" if pref == eq else "≠ équilibre (non réaliste)"}</div>

<div class="step"><b>Pareto :</b> L'équilibre est {"" if eq_pareto else "NON "}Pareto-optimal</div>

<div class="step"><b>Dominance :</b> {("J1: " + sit["dom_j1"][0] + " dominée") if sit["dom_j1"] else "Pas de dominance stricte"}</div>
"""
    })
    
    return questions


# ============================================
# AFFICHAGE
# ============================================

def afficher_matrice(m, L, C):
    return f"""
    <div class="situation-box">
        <p style="color: #888; margin-bottom: 16px; font-size: 13px;">Jeu bimatriciel 2×2</p>
        <table style="width: 100%; max-width: 320px; margin: 0 auto; border-collapse: separate; border-spacing: 6px;">
            <tr>
                <td style="padding: 8px; width: 40px;"></td>
                <td style="padding: 8px; text-align: center; color: #aaa; font-weight: 600;">{C[0]}</td>
                <td style="padding: 8px; text-align: center; color: #aaa; font-weight: 600;">{C[1]}</td>
            </tr>
            <tr>
                <td style="padding: 8px; color: #aaa; font-weight: 600;">{L[0]}</td>
                <td style="padding: 14px; text-align: center; background: #2a2a2a; border-radius: 8px; font-size: 16px;">({m[0][0][0]}, {m[0][0][1]})</td>
                <td style="padding: 14px; text-align: center; background: #2a2a2a; border-radius: 8px; font-size: 16px;">({m[0][1][0]}, {m[0][1][1]})</td>
            </tr>
            <tr>
                <td style="padding: 8px; color: #aaa; font-weight: 600;">{L[1]}</td>
                <td style="padding: 14px; text-align: center; background: #2a2a2a; border-radius: 8px; font-size: 16px;">({m[1][0][0]}, {m[1][0][1]})</td>
                <td style="padding: 14px; text-align: center; background: #2a2a2a; border-radius: 8px; font-size: 16px;">({m[1][1][0]}, {m[1][1][1]})</td>
            </tr>
        </table>
        <p style="color: #666; font-size: 11px; margin-top: 14px; text-align: center;">J1 = ligne, J2 = colonne. Case = (gain J1, gain J2)</p>
    </div>
    """


# ============================================
# PAGES
# ============================================

def page_menu():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("# 🎯 Bloc A — Jeux Finis")
    st.markdown("*Exercice complet avec 18 questions*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    **Concepts couverts :**
    - Lire une matrice (gains J1, J2)
    - Issue préférée
    - Meilleure réponse (BR)
    - Méthode du soulignement
    - Équilibre de Nash
    - Stratégie dominée
    - Jeu dans la stratégie / dans le paiement
    - Optimum de Pareto
    - EISD
    - Déviation unilatérale
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Commencer l'exercice", use_container_width=True):
        sit = generer_situation()
        st.session_state.sit = sit
        st.session_state.questions = generer_questions(sit)
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected = None
        st.session_state.started = True
        st.rerun()


def page_question():
    sit = st.session_state.sit
    questions = st.session_state.questions
    idx = st.session_state.idx
    
    if idx >= len(questions):
        page_results()
        return
    
    q = questions[idx]
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Menu"):
            st.session_state.started = False
            st.rerun()
    with col2:
        st.progress(idx / len(questions))
    with col3:
        st.markdown(f"**Q{idx + 1}/{len(questions)}** — {st.session_state.score} ✓")
    
    # Matrice
    st.markdown(afficher_matrice(sit["matrice"], sit["lignes"], sit["colonnes"]), unsafe_allow_html=True)
    
    # Question
    st.markdown(f"<span style='background:#dbeafe;color:#1e40af;padding:3px 10px;border-radius:10px;font-size:12px;'>{q['concept']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;margin-top:10px;'>{q['question']}</p>", unsafe_allow_html=True)
    
    # Choix
    if not st.session_state.answered:
        for lettre, texte in q["choix"].items():
            if st.button(f"{lettre}. {texte}", key=f"btn_{lettre}", use_container_width=True):
                st.session_state.selected = lettre
                st.session_state.answered = True
                if lettre == q["reponse"]:
                    st.session_state.score += 1
                st.rerun()
    else:
        # Afficher résultat
        for lettre, texte in q["choix"].items():
            if lettre == q["reponse"]:
                st.markdown(f'<div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:8px;padding:10px;margin:4px 0;"><b style="color:#22c55e;">✓ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            elif lettre == st.session_state.selected:
                st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:10px;margin:4px 0;"><b style="color:#ef4444;">✗ {lettre}.</b> {texte}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#f5f5f5;border-radius:8px;padding:10px;margin:4px 0;opacity:0.5;">{lettre}. {texte}</div>', unsafe_allow_html=True)
        
        # Message
        if st.session_state.selected == q["reponse"]:
            st.markdown('<div class="correct-box"><b style="color:#22c55e;font-size:18px;">✓ Correct !</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="incorrect-box"><b style="color:#ef4444;font-size:18px;">✗ Incorrect</b><br>La bonne réponse était <b>{q["reponse"]}</b></div>', unsafe_allow_html=True)
        
        # Explication
        st.markdown(f'<div class="explication"><b style="color:#3b82f6;">💡 Explication détaillée</b>{q["explication"]}</div>', unsafe_allow_html=True)
        
        # Bouton suivant
        st.markdown("<br>", unsafe_allow_html=True)
        btn_txt = "Question suivante →" if idx < len(questions) - 1 else "Voir les résultats"
        if st.button(btn_txt, use_container_width=True, type="primary"):
            st.session_state.idx += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()


def page_results():
    score = st.session_state.score
    total = len(st.session_state.questions)
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
        st.markdown("<p style='text-align:center;font-size:20px;'>🏆 Excellent ! Tu maîtrises le Bloc A.</p>", unsafe_allow_html=True)
    elif pct >= 60:
        st.markdown("<p style='text-align:center;font-size:20px;'>👍 Bien joué ! Quelques révisions et c'est bon.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;font-size:20px;'>📚 Continue à réviser les concepts.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Menu", use_container_width=True):
            st.session_state.started = False
            st.rerun()
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True, type="primary"):
            sit = generer_situation()
            st.session_state.sit = sit
            st.session_state.questions = generer_questions(sit)
            st.session_state.idx = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()


# ============================================
# MAIN
# ============================================

if st.session_state.started:
    if st.session_state.idx < len(st.session_state.questions):
        page_question()
    else:
        page_results()
else:
    page_menu()
