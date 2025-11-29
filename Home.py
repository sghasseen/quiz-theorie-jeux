"""
🎮 MIASHS - Quiz Théorie des Jeux
Page d'accueil avec authentification et guide
"""

import streamlit as st

st.set_page_config(
    page_title="MIASHS - Théorie des Jeux",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS NOIR ET BLANC
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    
    p, span, div, label, h1, h2, h3 { color: #000000 !important; }
    
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        margin: 40px 0 10px 0;
    }
    
    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
        color: #666 !important;
    }
    
    .stButton > button {
        background-color: #000000;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
    }
    .stButton > button:hover { background-color: #333; }
    
    .locked-icon {
        font-size: 80px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .guide-section {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #000;
    }
    
    .level-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CODES D'ACCÈS
# ============================================
VALID_CODES = {"TDJ2024", "NASH", "PARETO", "JEUX", "MIASHS"}

# ============================================
# SESSION STATE
# ============================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "guide_seen" not in st.session_state:
    st.session_state.guide_seen = False

# ============================================
# PAGE LOGIN
# ============================================
def page_login():
    st.markdown('<div class="locked-icon">🎮</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="main-title">🎮 Bienvenue !</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ton guide pour réussir l\'exam de Théorie des Jeux</div>', unsafe_allow_html=True)
    
    # Niveau 1
    st.markdown("""
    <div class="guide-section">
        <h3>📖 NIVEAU 1 — Découverte</h3>
        <p><b>T'es perdu ? Tu découvres le cours ?</b></p>
        <p>👉 Commence par le mode <b>"Étudier"</b> de chaque bloc</p>
        <ul>
            <li>🎯 Bloc A → Jeux Finis (matrices, Nash, BR)</li>
            <li>📈 Bloc B → Jeux Continus (dérivation, CPO)</li>
            <li>🎲 Bloc C → Stratégies Mixtes (p*, q*)</li>
            <li>⚖️ Bloc D → Somme Nulle (maximin, minimax)</li>
        </ul>
        <p>⏱️ <b>Temps :</b> 1h-2h &nbsp;&nbsp;|&nbsp;&nbsp; 📊 <b>Note estimée :</b> Tu survis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Niveau 2
    st.markdown("""
    <div class="guide-section">
        <h3>✏️ NIVEAU 2 — Absorption</h3>
        <p><b>Tu connais les concepts, tu veux les ancrer ?</b></p>
        <p>👉 Fais le mode <b>"Révision QCM"</b> de chaque bloc</p>
        <ul>
            <li>🎯 Bloc A : 18 questions</li>
            <li>📈 Bloc B : 12 questions</li>
            <li>🎲 Bloc C : 12 questions</li>
            <li>⚖️ Bloc D : 10 questions</li>
        </ul>
        <p><b>Total : 52 questions</b> avec explications détaillées</p>
        <p>⏱️ <b>Temps :</b> 2h-3h &nbsp;&nbsp;|&nbsp;&nbsp; 📊 <b>Note estimée : 10-12/20</b> ✅</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Niveau 3
    st.markdown("""
    <div class="guide-section">
        <h3>🎯 NIVEAU 3 — Application</h3>
        <p><b>Tu te sens à l'aise ? Tu veux te tester ?</b></p>
        <p>👉 Lance le <b>Quiz Chronométré</b></p>
        <ul>
            <li>⏱️ 30 questions en 20 minutes</li>
            <li>🔥 Conditions d'examen</li>
            <li>📊 Score final avec analyse</li>
        </ul>
        <p>⏱️ <b>Temps :</b> 20-30 min &nbsp;&nbsp;|&nbsp;&nbsp; 📊 <b>Note estimée : 12-15/20</b> 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Niveau 4
    st.markdown("""
    <div class="guide-section">
        <h3>🏆 NIVEAU 4 — Maîtrise</h3>
        <p><b>Tu veux la note parfaite ?</b></p>
        <p>👉 Fais les <b>Exercices Rédaction</b> <i>(bientôt disponible)</i></p>
        <ul>
            <li>📝 Vrais exercices type TD/exam</li>
            <li>✍️ Tu rédiges sur papier</li>
            <li>✅ Correction détaillée étape par étape</li>
        </ul>
        <p>⏱️ <b>Temps :</b> 3h-4h &nbsp;&nbsp;|&nbsp;&nbsp; 📊 <b>Note estimée : 15+/20</b> 🏆</p>
        <p style="font-size:12px;color:#888!important;">(sauf si t'es autiste, là c'est 20/20)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tableau récap
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    | Niveau | Mode | Note estimée |
    |--------|------|--------------|
    | 📖 1 | Étudier | Survie |
    | ✏️ 2 | QCM Révision | 10-12 |
    | 🎯 3 | Quiz chrono | 12-15 |
    | 🏆 4 | Rédaction | 15+ |
    """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 C'est parti !", use_container_width=True):
            st.session_state.guide_seen = True
            st.rerun()

# ============================================
# PAGE MENU PRINCIPAL
# ============================================
def page_menu():
    st.markdown('<div class="main-title">🎮 MIASHS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choisis ton mode de révision</div>', unsafe_allow_html=True)
    
    # Bouton guide
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📋 Guide", use_container_width=True):
            st.session_state.guide_seen = False
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Instructions
    st.info("👈 **Utilise le menu à gauche** pour naviguer entre les blocs et le quiz !")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Récap des blocs
    st.markdown("### 📚 Niveaux 1 & 2 — Étudier & QCM")
    
    blocs_info = """
    | Bloc | Contenu | Questions |
    |------|---------|-----------|
    | 🎯 Bloc A | Jeux Finis (matrices, Nash, BR, Pareto) | 18 |
    | 📈 Bloc B | Jeux Continus (dérivation, CPO, système) | 12 |
    | 🎲 Bloc C | Stratégies Mixtes (p*, q*, indifférence) | 12 |
    | ⚖️ Bloc D | Somme Nulle (maximin, minimax, point-selle) | 10 |
    """
    st.markdown(blocs_info)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Niveau 3 — Quiz Chronométré")
    st.markdown("⏱️ **30 questions en 20 minutes** — Conditions d'examen")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🏆 Niveau 4 — Exercices Rédaction")
    st.markdown("📝 *Bientôt disponible...*")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:20px;background:#f9f9f9;border-radius:12px;">
        <span style="font-size:32px;">📊</span><br>
        <b>52 questions disponibles</b><br>
        <span style="color:#666!important;">+ Quiz chronométré</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.guide_seen = False
            st.rerun()

# ============================================
# MAIN
# ============================================
if not st.session_state.authenticated:
    page_login()
elif not st.session_state.guide_seen:
    page_guide()
else:
    page_menu()
