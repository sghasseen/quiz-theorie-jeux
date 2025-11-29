"""
Quiz Théorie des Jeux - Version Web (Streamlit)
Style minimaliste
"""

import streamlit as st
import time
from datetime import datetime

from config import QUIZ_FORMATS, DATABASE_PATH
from database.db_manager import DatabaseManager
from questions.question_loader import generer_quiz

# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Quiz TDJ",
    page_icon="◯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# STYLE CSS MINIMALISTE
# ============================================

st.markdown("""
<style>
    /* Fond blanc */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Cacher le menu hamburger et footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Titres */
    h1 {
        font-weight: 600;
        font-size: 28px;
        color: #1a1a1a;
    }
    
    h2 {
        font-weight: 500;
        font-size: 20px;
        color: #1a1a1a;
    }
    
    h3 {
        font-weight: 500;
        font-size: 16px;
        color: #1a1a1a;
    }
    
    /* Texte */
    p, .stMarkdown {
        color: #4a4a4a;
        font-size: 14px;
    }
    
    /* Boutons */
    .stButton > button {
        background-color: #1a1a1a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #333333;
        border: none;
    }
    
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
        text-align: center;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    /* Cards */
    .card {
        background: #fafafa;
        border-radius: 12px;
        padding: 24px;
        margin: 8px 0;
        border: 1px solid #f0f0f0;
    }
    
    /* Stats */
    .stat-number {
        font-size: 32px;
        font-weight: 600;
        color: #1a1a1a;
    }
    
    .stat-label {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #1a1a1a;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 24px 0;
    }
    
    /* Score circle */
    .score-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: #fafafa;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        border: 3px solid #1a1a1a;
    }
    
    /* Correct/Incorrect */
    .correct {
        color: #22c55e;
    }
    
    .incorrect {
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATABASE
# ============================================

@st.cache_resource
def get_database():
    return DatabaseManager(DATABASE_PATH)

db = get_database()


# ============================================
# SESSION STATE
# ============================================

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "quiz_session" not in st.session_state:
    st.session_state.quiz_session = None
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "quiz_start_time" not in st.session_state:
    st.session_state.quiz_start_time = None
if "quiz_duration" not in st.session_state:
    st.session_state.quiz_duration = None


# ============================================
# UTILS
# ============================================

def logout():
    st.session_state.user = None
    st.session_state.page = "login"
    st.session_state.quiz_session = None
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.responses = []


# ============================================
# PAGE: LOGIN
# ============================================

def page_login():
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Quiz TDJ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Théorie des Jeux</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        code = st.text_input(
            "Code d'accès",
            placeholder="XXXXXX",
            max_chars=6,
            label_visibility="collapsed"
        ).upper()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Continuer", use_container_width=True):
            if not code:
                st.error("Entre ton code")
            else:
                user = db.get_user_by_code(code)
                if user:
                    db.update_last_login(user['id'])
                    st.session_state.user = user
                    st.session_state.page = "menu"
                    st.rerun()
                else:
                    st.error("Code invalide")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        with st.expander("Comment ca marche"):
            st.markdown("""
            1. Demande ton code a l'administrateur
            2. Entre ton code ci-dessus
            3. Choisis un quiz (court ou long)
            4. Reponds aux questions
            5. Consulte ton score
            """)


# ============================================
# PAGE: MENU
# ============================================

def page_menu():
    
    user = st.session_state.user
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Bonjour {user['prenom']}")
    with col2:
        if st.button("Quitter", key="logout"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("##### Choisir un quiz")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <p style="font-weight: 600; margin-bottom: 8px;">Court</p>
            <p style="color: #888; font-size: 13px;">7 questions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Commencer", key="quiz_court", use_container_width=True):
            st.session_state.quiz_format = "court"
            st.session_state.page = "quiz_start"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <p style="font-weight: 600; margin-bottom: 8px;">Long</p>
            <p style="color: #888; font-size: 13px;">21 questions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Commencer", key="quiz_long", use_container_width=True):
            st.session_state.quiz_format = "long"
            st.session_state.page = "quiz_start"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("##### Statistiques")
    
    stats = db.get_user_stats(user['id'])
    session_stats = stats['sessions']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nb = session_stats['total_sessions'] or 0
        st.markdown(f"""
        <div style="text-align: center;">
            <p class="stat-number">{nb}</p>
            <p class="stat-label">Quiz</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        moy = session_stats['moyenne_score'] or 0
        st.markdown(f"""
        <div style="text-align: center;">
            <p class="stat-number">{moy:.0f}%</p>
            <p class="stat-label">Moyenne</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        niv = session_stats['meilleur_niveau'] or "N1"
        st.markdown(f"""
        <div style="text-align: center;">
            <p class="stat-number">{niv}</p>
            <p class="stat-label">Niveau</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# PAGE: QUIZ START
# ============================================

def page_quiz_start():
    
    format_quiz = st.session_state.quiz_format
    format_info = QUIZ_FORMATS[format_quiz]
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center;">
        <h2>{format_info['name']}</h2>
        <p style="color: #888;">{format_info['questions']} questions</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style="text-align: center;">
        <p style="color: #888; font-size: 13px;">Une fois lance, le quiz ne peut pas etre mis en pause.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    with col2:
        if st.button("Lancer", use_container_width=True, type="primary"):
            # Créer la session DB
            session_id = db.create_session(
                st.session_state.user['id'],
                format_quiz
            )
            
            # Générer les questions
            questions = generer_quiz(format_info['questions'])
            
            # Sauvegarder dans session state
            st.session_state.quiz_session = session_id
            st.session_state.quiz_questions = questions
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.responses = []
            st.session_state.quiz_start_time = time.time()
            st.session_state.quiz_duration = format_info['duree_minutes'] * 60  # en secondes
            st.session_state.page = "quiz"
            st.rerun()


# ============================================
# PAGE: QUIZ
# ============================================

def page_quiz():
    
    format_quiz = st.session_state.quiz_format
    format_info = QUIZ_FORMATS[format_quiz]
    total_questions = format_info['questions']
    current = st.session_state.current_question
    
    # Calculer le temps restant
    elapsed = time.time() - st.session_state.quiz_start_time
    remaining = st.session_state.quiz_duration - elapsed
    
    # Si temps écoulé → terminer le quiz
    if remaining <= 0:
        st.session_state.page = "results"
        st.rerun()
        return
    
    # Formater le temps restant (mm:ss)
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    time_display = f"{minutes:02d}:{seconds:02d}"
    
    # Couleur du timer (rouge si < 2 minutes)
    time_color = "#ef4444" if remaining < 120 else "#1a1a1a"
    
    # Récupérer la question actuelle
    questions = st.session_state.quiz_questions
    if current >= len(questions):
        st.session_state.page = "results"
        st.rerun()
        return
    
    q = questions[current]
    
    # Header avec timer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f"<p style='color: #888;'>Q{current + 1}/{total_questions}</p>", unsafe_allow_html=True)
    with col2:
        st.progress((current) / total_questions)
    with col3:
        st.markdown(f"<p style='text-align: right; color: {time_color}; font-weight: 600;'>{time_display}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Compétence
    st.markdown(f"**{q['competence']}**")
    
    # Situation avec tableau HTML
    st.markdown(f"""
    <div class="card">
        {q['situation']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Choix
    choix_liste = [f"{lettre} · {texte}" for lettre, texte in q['choix'].items()]
    
    reponse = st.radio(
        "Reponse",
        choix_liste,
        index=None,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Valider", use_container_width=True, type="primary"):
        if reponse is None:
            st.warning("Selectionne une reponse")
        else:
            # Extraire la lettre (premier caractère)
            lettre = reponse[0]
            is_correct = (lettre == q['reponse'])
            
            if is_correct:
                st.session_state.score += 1
            
            st.session_state.responses.append({
                "question": current + 1,
                "competence": q['competence'],
                "reponse_donnee": lettre,
                "reponse_correcte": q['reponse'],
                "correct": is_correct,
                "explication": q['explication']
            })
            
            st.session_state.current_question += 1
            
            if st.session_state.current_question >= total_questions:
                st.session_state.page = "results"
            
            st.rerun()
    
    # Auto-refresh toutes les secondes pour le timer
    time.sleep(1)
    st.rerun()


# ============================================
# PAGE: RESULTS
# ============================================

def page_results():
    
    format_quiz = st.session_state.quiz_format
    format_info = QUIZ_FORMATS[format_quiz]
    total = format_info['questions']
    score = st.session_state.score
    percentage = (score / total) * 100
    
    # Save to DB
    if st.session_state.quiz_session:
        db.update_session(
            st.session_state.quiz_session,
            date_fin=datetime.now(),
            score_total=score,
            questions_total=total,
            questions_reussies=score,
            complete=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Score
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="score-circle">
            <p style="font-size: 36px; font-weight: 600; margin: 0;">{score}/{total}</p>
            <p style="font-size: 14px; color: #888; margin: 0;">{percentage:.0f}%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Message
    if percentage >= 90:
        msg = "Excellent"
    elif percentage >= 75:
        msg = "Bien joue"
    elif percentage >= 60:
        msg = "Pas mal"
    else:
        msg = "A retravailler"
    
    st.markdown(f"<p style='text-align: center; font-size: 18px;'>{msg}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Corrections (uniquement les mauvaises réponses)
    mauvaises = [r for r in st.session_state.responses if not r['correct']]
    
    if mauvaises:
        st.markdown("##### Corrections")
        for resp in mauvaises:
            with st.expander(f"Q{resp['question']} - {resp['competence']}"):
                st.markdown(f"**Ta reponse:** {resp['reponse_donnee']}")
                st.markdown(f"**Bonne reponse:** {resp['reponse_correcte']}")
                st.markdown(f"**Explication:** {resp['explication']}")
    else:
        st.markdown("<p style='text-align: center; color: #22c55e;'>Aucune erreur !</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Menu", use_container_width=True):
            st.session_state.quiz_session = None
            st.session_state.quiz_questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.responses = []
            st.session_state.page = "menu"
            st.rerun()
    
    with col2:
        if st.button("Rejouer", use_container_width=True, type="primary"):
            st.session_state.quiz_session = None
            st.session_state.quiz_questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.responses = []
            st.session_state.page = "quiz_start"
            st.rerun()


# ============================================
# ROUTER
# ============================================

def main():
    if st.session_state.page == "login" or st.session_state.user is None:
        page_login()
    elif st.session_state.page == "menu":
        page_menu()
    elif st.session_state.page == "quiz_start":
        page_quiz_start()
    elif st.session_state.page == "quiz":
        page_quiz()
    elif st.session_state.page == "results":
        page_results()
    else:
        st.session_state.page = "login"
        st.rerun()


if __name__ == "__main__":
    main()
