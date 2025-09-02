# game_multiplayer_local_enhanced.py
import time
import pandas as pd
from rapidfuzz import fuzz
import streamlit as st
import random

# try import autorefresh; fallback gracefully if not installed
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except Exception:
    HAS_AUTOREFRESH = False

# =========================
# Enhanced UI Configuration
# =========================
st.set_page_config(
    page_title="🎬 Bollywood Cinema Quest", 
    page_icon="🎭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with complete dark mode and amazing animations
st.markdown("""
<style>
    /* Global Dark Mode Base */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff !important;
    }
    
    /* Fix Streamlit's default white backgrounds */
    .stApp > header {
        background: transparent !important;
    }
    
    /* Dark theme for main header bar */
    .stApp > header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        height: 60px;
        border-bottom: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Dark sidebar styling */
    .css-1d391kg, .css-1outpf7, .stSidebar {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        border-right: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    .css-1d391kg .stMarkdown, .stSidebar .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Sidebar content styling */
    .stSidebar > div > div > div {
        background: transparent !important;
    }
    
    /* Fix white container backgrounds */
    .element-container, .stBlock, .block-container {
        background: transparent !important;
    }
    
    /* Welcome Screen Styles */
    .welcome-screen {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 30px;
        padding: 4rem 3rem;
        margin: 3rem auto;
        text-align: center;
        max-width: 800px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        animation: welcomeFloat 4s ease-in-out infinite alternate;
    }
    
    @keyframes welcomeFloat {
        0% { transform: translateY(0px) scale(1); }
        100% { transform: translateY(-10px) scale(1.02); }
    }
    
    .welcome-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        animation: titleShimmer 3s ease-in-out infinite;
    }
    
    @keyframes titleShimmer {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(255,107,107,0.5)); }
        50% { filter: drop-shadow(0 0 40px rgba(78,205,196,0.8)); }
    }
    
    .mode-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1.5rem 3rem;
        margin: 1rem;
        font-size: 1.3rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 30px rgba(102,126,234,0.4);
        position: relative;
        overflow: hidden;
    }
    
    .mode-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 50px rgba(102,126,234,0.7);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .mode-button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .mode-button:hover:before {
        left: 100%;
    }
    
    /* Custom Card Styles */
    .game-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .game-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        border-color: rgba(255,215,0,0.6);
        background: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.12) 100%);
    }
    
    /* Player Stats Cards */
    .player-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        box-shadow: 0 6px 25px rgba(255,107,107,0.35);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .player-card:before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
        opacity: 0;
    }
    
    .player-card:hover:before {
        opacity: 1;
        transform: rotate(45deg) translate(50%, 50%);
    }
    
    .player-card:hover {
        transform: scale(1.03);
        box-shadow: 0 12px 40px rgba(255,107,107,0.6);
    }
    
    .current-player {
        background: linear-gradient(135deg, #ffd700 0%, #ffb700 100%);
        color: #000;
        animation: currentPlayerGlow 3s ease-in-out infinite alternate;
        border: 2px solid rgba(255,215,0,0.8);
    }
    
    @keyframes currentPlayerGlow {
        0% { 
            box-shadow: 0 6px 25px rgba(255,215,0,0.4);
            transform: scale(1);
        }
        100% { 
            box-shadow: 0 12px 50px rgba(255,215,0,0.9);
            transform: scale(1.02);
        }
    }
    
    /* Enhanced Leaderboard Styles */
    .leaderboard-item {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.6rem 0;
        border-left: 5px solid;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .rank-1 { 
        border-left-color: #ffd700; 
        background: linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,215,0,0.1) 100%);
    }
    .rank-2 { 
        border-left-color: #c0c0c0; 
        background: linear-gradient(135deg, rgba(192,192,192,0.2) 0%, rgba(192,192,192,0.1) 100%);
    }
    .rank-3 { 
        border-left-color: #cd7f32; 
        background: linear-gradient(135deg, rgba(205,127,50,0.2) 0%, rgba(205,127,50,0.1) 100%);
    }
    .rank-other { border-left-color: #4ecdc4; }
    
    .leaderboard-item:hover {
        transform: translateX(15px) scale(1.02);
        background: linear-gradient(135deg, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0.15) 100%);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Fixed-size Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 1.5rem !important;
        font-weight: bold !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.4) !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 14px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 60px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102,126,234,0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Success Animation */
    .success-explosion {
        animation: successExplosion 2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes successExplosion {
        0% { 
            transform: scale(1) rotate(0deg);
            background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        }
        15% { 
            transform: scale(1.2) rotate(-5deg);
            background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 100%);
        }
        30% { 
            transform: scale(1.4) rotate(5deg);
            background: linear-gradient(135deg, #4ecdc4 0%, #667eea 100%);
        }
        45% { 
            transform: scale(1.3) rotate(-3deg);
            background: linear-gradient(135deg, #ff6b6b 0%, #ffd700 100%);
        }
        60% { 
            transform: scale(1.5) rotate(3deg);
            background: linear-gradient(135deg, #00b894 0%, #4ecdc4 100%);
        }
        75% { 
            transform: scale(1.2) rotate(-1deg);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        100% { 
            transform: scale(1) rotate(0deg);
            background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        }
    }
    
    /* Countdown Animation */
    .countdown-timer {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255,107,107,0.5);
        animation: countdownPulse 1s ease-in-out infinite;
    }
    
    @keyframes countdownPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 10px 30px rgba(255,107,107,0.5);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 15px 50px rgba(255,107,107,0.8);
        }
    }
    
    /* Input Field Enhancements - BLACK TEXT */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.95) !important;
        color: #000000 !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 25px rgba(255,215,0,0.4) !important;
        background: rgba(255,255,255,0.98) !important;
        color: #000000 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
        opacity: 0.8 !important;
    }
    
    /* Selectbox Enhancements - FIX WHITE TEXT ISSUE */
    .stSelectbox > div > div > div {
        background: rgba(255,255,255,0.95) !important;
        color: #000000 !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 15px !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Fix selectbox dropdown */
    .stSelectbox [data-baseweb="select"] {
        background: rgba(255,255,255,0.95) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.95) !important;
        color: #000000 !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 15px !important;
    }
    
    .stSelectbox [data-baseweb="popover"] {
        background: rgba(255,255,255,0.98) !important;
        color: #000000 !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }
    
    .stSelectbox [data-baseweb="popover"] ul {
        background: rgba(255,255,255,0.98) !important;
        color: #000000 !important;
        border-radius: 15px !important;
    }
    
    .stSelectbox [data-baseweb="popover"] li {
        background: transparent !important;
        color: #000000 !important;
    }
    
    .stSelectbox [data-baseweb="popover"] li:hover {
        background: rgba(102,126,234,0.1) !important;
        color: #000000 !important;
    }
    
    /* Success/Error Message Enhancements */
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        box-shadow: 0 6px 20px rgba(0,184,148,0.3);
        animation: slideInRight 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .success-message:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .success-message:hover:before {
        left: 100%;
    }
    
    .error-message {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        box-shadow: 0 6px 20px rgba(225,112,85,0.3);
        animation: shake 0.6s ease;
    }
    
    @keyframes slideInRight {
        0% { 
            transform: translateX(100%) scale(0.8); 
            opacity: 0; 
        }
        50% { 
            transform: translateX(10%) scale(1.05); 
            opacity: 0.8; 
        }
        100% { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
    }
    
    @keyframes shake {
        0%, 20%, 40%, 60%, 80% { transform: translateX(0) scale(1); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-8px) scale(1.02); }
    }
    
    /* Movie Info Cards */
    .movie-hint {
        background: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .movie-hint:hover {
        transform: scale(1.05) rotateY(5deg);
        border-color: rgba(255,215,0,0.6);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    /* Hint Card Styles */
    .hint-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,215,0,0.08) 100%);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(255,215,0,0.3);
        border-radius: 18px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        animation: hintGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes hintGlow {
        0% { 
            box-shadow: 0 5px 20px rgba(255,215,0,0.3);
            border-color: rgba(255,215,0,0.3);
        }
        100% { 
            box-shadow: 0 10px 40px rgba(255,215,0,0.6);
            border-color: rgba(255,215,0,0.6);
        }
    }
    
    /* Enhanced mobile responsiveness */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 2.5rem;
        }
        
        .movie-hint {
            font-size: 1.1rem;
            padding: 1.5rem;
        }
        
        .game-card {
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Setup & Data
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("bollywood_clean_augmented_v2.csv").dropna(subset=['movie_name']).reset_index(drop=True)
    expected_cols = ["movie_name", "lead_male_actor", "lead_female_actor", "notable_song"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    return df

df = load_data()
COMMON_ACTOR_LASTNAMES = {"khan", "kapoor", "bachchan", "kumar"}

def get_initials(text):
    if pd.isna(text) or str(text).strip() == "":
        return ""
    return " ".join([w[0].upper() + "." for w in str(text).split()])

def match_name(user_guess, actual_name):
    if not user_guess or not actual_name:
        return False
    user_guess = str(user_guess).strip().lower()
    actual_name = str(actual_name).strip().lower()
    guess_parts = user_guess.split()
    actual_parts = actual_name.split()
    if len(actual_parts) > 1 and actual_parts[-1] in COMMON_ACTOR_LASTNAMES:
        if fuzz.ratio(guess_parts[-1], actual_parts[-1]) > 80:
            return True
    if len(guess_parts) == 1:
        if fuzz.ratio(guess_parts[0], actual_parts[0]) > 80:
            return True
    return fuzz.ratio(user_guess, actual_name) > 80

def get_movie_hint(row):
    """Generate contextual hints for the movie"""
    hints = [
        f"This movie was released around the {row.get('year', 'unknown')}s",
        f"It's a {row.get('genre', 'Bollywood')} film",
        f"The story is about love and drama typical of Bollywood cinema",
        f"This movie features popular songs and dance sequences",
        f"It was a box office hit with memorable performances"
    ]
    
    # Add specific hints based on actors
    if not pd.isna(row['lead_male_actor']):
        actor = str(row['lead_male_actor']).split()[0]
        hints.append(f"The male lead is known for his versatile acting skills")
        hints.append(f"This actor has been in many successful Bollywood films")
    
    if not pd.isna(row['lead_female_actor']):
        actress = str(row['lead_female_actor']).split()[0]
        hints.append(f"The female lead is a renowned Bollywood actress")
        hints.append(f"She has won several awards for her performances")
    
    return random.choice(hints)

# =========================
# Session State Management
# =========================
def init_state():
    ss = st.session_state
    if "game_mode" not in ss:
        ss.game_mode = None
    if "players" not in ss:
        ss.players = {}
    if "current_player" not in ss:
        ss.current_player = None
    if "used_movies" not in ss:
        ss.used_movies = set()
    if "current_row" not in ss:
        ss.current_row = None
    if "messages" not in ss:
        ss.messages = []
    if "revealed" not in ss:
        ss.revealed = {"movie": False, "actor": False, "actress": False, "song": False}
    if "auto_advance" not in ss:
        ss.auto_advance = False
    if "advance_time" not in ss:
        ss.advance_time = 0.0
    if "show_celebration" not in ss:
        ss.show_celebration = False
    if "hint_used" not in ss:
        ss.hint_used = False
    if "current_hint" not in ss:
        ss.current_hint = ""

def add_player(name):
    ss = st.session_state
    if name in ss.players:
        return False
    ss.players[name] = {
        "score": 0,
        "streak": 0,
        "milestones": set(),
        "guessed_movies": [],
        "history": [],
        "streak_has_hint": False,
        "streak_has_wrong": False
    }
    return True

def pick_new_movie():
    ss = st.session_state
    available_df = df[~df['movie_name'].isin(ss.used_movies)]
    if available_df.empty:
        ss.current_row = None
        return
    ss.current_row = available_df.sample().iloc[0]
    ss.used_movies.add(ss.current_row['movie_name'])
    ss.guessed = {"movie": False, "actor": False, "actress": False, "song": False}
    ss.hints_used_current_movie = False
    ss.wrong_guess_this_movie = False
    ss.revealed = {"movie": False, "actor": False, "actress": False, "song": False}
    ss.messages = []
    ss.show_celebration = False
    ss.hint_used = False
    ss.current_hint = ""
    ss.auto_advance = False
    ss.advance_time = 0.0

def push_message(kind, text):
    st.session_state.messages.append((kind, text, time.time()))

def prune_messages(seconds=8):
    now = time.time()
    st.session_state.messages = [(k,t,ts) for (k,t,ts) in st.session_state.messages if now - ts < seconds]

def show_success_animation():
    st.markdown("""
    <script>
    // Enhanced success animation with fireworks
    function createCelebrationFireworks() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#667eea', '#764ba2', '#ffd700'];
        const particles = 50;
        
        for(let i = 0; i < particles; i++) {
            const firework = document.createElement('div');
            const size = Math.random() * 8 + 4;
            firework.style.position = 'fixed';
            firework.style.left = Math.random() * window.innerWidth + 'px';
            firework.style.top = Math.random() * window.innerHeight + 'px';
            firework.style.width = size + 'px';
            firework.style.height = size + 'px';
            firework.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            firework.style.borderRadius = '50%';
            firework.style.pointerEvents = 'none';
            firework.style.zIndex = '9999';
            firework.style.animation = `celebrationFirework ${2 + Math.random() * 2}s ease-out forwards`;
            firework.style.boxShadow = `0 0 20px ${colors[Math.floor(Math.random() * colors.length)]}`;
            document.body.appendChild(firework);
            
            setTimeout(() => {
                firework.remove();
            }, 4000);
        }
    }
    
    // Add enhanced firework animation CSS
    if (!document.querySelector('#celebration-style')) {
        const style = document.createElement('style');
        style.id = 'celebration-style';
        style.textContent = `
            @keyframes celebrationFirework {
                0% { 
                    transform: scale(0) rotate(0deg) translateY(0px); 
                    opacity: 1; 
                }
                20% { 
                    transform: scale(1.5) rotate(72deg) translateY(-100px); 
                    opacity: 0.9; 
                }
                40% { 
                    transform: scale(2.2) rotate(144deg) translateY(-200px); 
                    opacity: 0.8; 
                }
                60% { 
                    transform: scale(2.8) rotate(216deg) translateY(-300px); 
                    opacity: 0.6; 
                }
                80% { 
                    transform: scale(2.5) rotate(288deg) translateY(-400px); 
                    opacity: 0.3; 
                }
                100% { 
                    transform: scale(0.5) rotate(360deg) translateY(-500px); 
                    opacity: 0; 
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    createCelebrationFireworks();
    
    // Create screen flash effect
    const flash = document.createElement('div');
    flash.style.position = 'fixed';
    flash.style.top = '0';
    flash.style.left = '0';
    flash.style.width = '100vw';
    flash.style.height = '100vh';
    flash.style.background = 'radial-gradient(circle, rgba(255,215,0,0.3) 0%, transparent 70%)';
    flash.style.pointerEvents = 'none';
    flash.style.zIndex = '9998';
    flash.style.animation = 'flashEffect 1s ease-out forwards';
    document.body.appendChild(flash);
    
    setTimeout(() => {
        flash.remove();
    }, 1000);
    
    if (!document.querySelector('#flash-style')) {
        const flashStyle = document.createElement('style');
        flashStyle.id = 'flash-style';
        flashStyle.textContent = `
            @keyframes flashEffect {
                0% { opacity: 0; }
                20% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(flashStyle);
    }
    </script>
    """, unsafe_allow_html=True)

init_state()

# =========================
# Welcome Screen
# =========================
if st.session_state.game_mode is None:
    st.markdown("""
    <div class="welcome-screen">
        <h1 class="welcome-title">🎭 Bollywood Cinema Quest 🎬</h1>
        <p style="font-size: 1.5rem; margin: 2rem 0; opacity: 0.9;">
            Test your Bollywood knowledge in this exciting movie guessing game!
        </p>
        <p style="font-size: 1.2rem; margin: 2rem 0; opacity: 0.8;">
            Choose your adventure mode:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Single Player Mode", key="single_mode", use_container_width=True):
            st.session_state.game_mode = "single"
            add_player("Cinema Master")
            st.session_state.current_player = "Cinema Master"
            pick_new_movie()
            st.rerun()
    
    with col2:
        if st.button("👥 Multiplayer Mode", key="multi_mode", use_container_width=True):
            st.session_state.game_mode = "multi"
            st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem;">
        <h3 style="color: #4ecdc4;">🌟 Game Features:</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
            <div class="game-card">
                <h4>🎬 Movie Mysteries</h4>
                <p>Guess Bollywood movies from clever initial clues</p>
            </div>
            <div class="game-card">
                <h4>💡 Smart Hints</h4>
                <p>Get contextual hints without breaking your streak</p>
            </div>
            <div class="game-card">
                <h4>🏆 Scoring System</h4>
                <p>Earn points and milestone bonuses</p>
            </div>
            <div class="game-card">
                <h4>🎪 Fun Animations</h4>
                <p>Celebrate victories with spectacular effects</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =========================
# Game Interface
# =========================
# Enhanced Sidebar: players & controls
with st.sidebar:
    st.markdown('<div class="floating">', unsafe_allow_html=True)
    st.markdown("# 👥 **Cinema Quest Players**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.game_mode == "multi":
        # Enhanced player addition with equal-sized buttons
        st.markdown("### ✨ Add New Player")
        new_player = st.text_input("🎭 Enter player name", value="", placeholder="Enter your cinema alias...")
        
        # Equal-sized buttons using columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Join Game", use_container_width=True, key="join_btn"):
                if new_player.strip():
                    added = add_player(new_player.strip())
                    if added:
                        st.success(f"🎉 Welcome, {new_player.strip()}!")
                        st.session_state.current_player = new_player.strip()
                        if st.session_state.current_row is None:
                            pick_new_movie()
                        st.rerun()
                    else:
                        st.warning("🎭 This alias is already taken!")
                else:
                    st.error("🚫 Please enter a valid name")
        
        with col2:
            if st.button("🔄 Reset Game", use_container_width=True, key="reset_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # Enhanced player selection
        if st.session_state.players:
            st.markdown("### 🎬 Current Player")
            player_list = list(st.session_state.players.keys())
            default_idx = player_list.index(st.session_state.current_player) if st.session_state.current_player in player_list else 0
            chosen = st.selectbox("🎯 Who's turn to guess?", player_list, index=default_idx, key="player_select")
            st.session_state.current_player = chosen
    else:
        # Single player mode
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Main Menu", use_container_width=True, key="main_menu_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("🔄 New Game", use_container_width=True, key="new_game_btn"):
                st.session_state.used_movies = set()
                st.session_state.players["Cinema Master"] = {
                    "score": 0, "streak": 0, "milestones": set(),
                    "guessed_movies": [], "history": [],
                    "streak_has_hint": False, "streak_has_wrong": False
                }
                pick_new_movie()
                st.rerun()

    st.markdown("---")
    
    # Enhanced Leaderboard
    st.markdown("### 🏆 **Cinema Champions**")
    if st.session_state.players:
        leaderboard = sorted(st.session_state.players.items(), key=lambda kv: kv[1]["score"], reverse=True)
        
        for i, (pname, pdata) in enumerate(leaderboard, start=1):
            rank_class = f"rank-{i}" if i <= 3 else "rank-other"
            is_current = "current-player" if pname == st.session_state.current_player else ""
            
            trophy = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖️"
            
            st.markdown(f"""
            <div class="leaderboard-item {rank_class} {is_current}">
                <strong>{trophy} #{i} {pname}</strong><br>
                <small>🏆 Score: {pdata['score']} | 🔥 Streak: {pdata['streak']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎭 No players yet — join the cinema quest!")

# =========================
# Main Game Layout
# =========================
if st.session_state.current_row is None:
    pick_new_movie()

left, right = st.columns([2.2, 1.3])

with left:
    # Enhanced Title
    st.markdown('<h1 class="main-title">🎭 Bollywood Cinema Quest 🎬</h1>', unsafe_allow_html=True)

    # Enhanced How to Play
    with st.expander("📜 **Game Rules & Scoring** (Click to expand)", expanded=False):
        st.markdown("""
        <div class="game-card">
        <h3>🎯 How to Master the Cinema Quest</h3>
        
        • **🎬 Guess the Movie** correctly = **+2 points** + streak bonus!<br>
        • **🎭 Bonus Milestones**: Every 5 correct movies = massive bonus!<br>
        &nbsp;&nbsp;→ 5 movies: +10-15 bonus | 10 movies: +20 bonus | 15+: Even more!<br>
        • **💡 Hints available**: Get movie clues without breaking streak!<br>
        • **⚡ Streak System**: Wrong guess = streak reset, but score stays!<br>
        • **🎪 Multiplayer**: Add friends and compete for cinema supremacy!<br>
        
        <small>💫 <em>Pro tip: Use hints strategically and trust your Bollywood knowledge!</em></small>
        </div>
        """, unsafe_allow_html=True)

    # Current player display
    cp = st.session_state.current_player
    if cp and cp in st.session_state.players:
        pdata = st.session_state.players[cp]
        st.markdown(f"""
        <div class="player-card current-player">
            <h3>🎭 Current Player: <strong>{cp}</strong></h3>
            <div style="display: flex; justify-content: space-between;">
                <span>🏆 <strong>{pdata['score']}</strong> points</span>
                <span>🔥 <strong>{pdata['streak']}</strong> streak</span>
            </div>
            <div class="streak-indicator"></div>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.game_mode == "multi":
        st.markdown("""
        <div class="game-card">
            <h3>🎭 Ready to Start Your Cinema Quest?</h3>
            <p>Add a player in the sidebar to begin your Bollywood adventure!</p>
        </div>
        """, unsafe_allow_html=True)

    # Game over check
    if st.session_state.current_row is None:
        st.markdown("""
        <div class="game-card celebration">
            <h2>🎉 Congratulations! Quest Complete! 🎊</h2>
            <p>You've mastered all movies in our Bollywood database!</p>
            <p><em>Click "New Game" in the sidebar to start fresh...</em></p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    row = st.session_state.current_row
    movie = row["movie_name"]
    actor = row["lead_male_actor"]
    actress = row["lead_female_actor"]
    song = row.get("notable_song", "")

    # Enhanced Movie Hints Display
    st.markdown("### 🔍 **Cinema Clues**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="movie-hint floating">
            🎬 <strong>Movie Initials</strong><br>
            <span style="font-size: 2.2rem; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.5);">{get_initials(movie)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="movie-hint floating" style="animation-delay: 0.5s;">
            💃 <strong>Actress Initials</strong><br>
            <span style="font-size: 2.2rem; color: #ff6b9d; text-shadow: 0 0 10px rgba(255,107,157,0.5);">{get_initials(actress)}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="movie-hint floating" style="animation-delay: 0.25s;">
            🕺 <strong>Actor Initials</strong><br>
            <span style="font-size: 2.2rem; color: #3742fa; text-shadow: 0 0 10px rgba(55,66,250,0.5);">{get_initials(actor)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="movie-hint floating" style="animation-delay: 0.75s;">
            🎵 <strong>Song Initials</strong><br>
            <span style="font-size: 2.2rem; color: #26c0d3; text-shadow: 0 0 10px rgba(38,192,211,0.5);">{get_initials(song) if song else 'N/A'}</span>
        </div>
        """, unsafe_allow_html=True)

    # Movie Hint Section
    if st.session_state.hint_used and st.session_state.current_hint:
        st.markdown(f"""
        <div class="hint-card">
            <h4>💡 Movie Hint</h4>
            <p style="font-size: 1.1rem; margin: 0;">{st.session_state.current_hint}</p>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Guess Form
    st.markdown("### 💭 **Make Your Guess**")
    with st.form(key="guess_form", clear_on_submit=True):
        guess_input = st.text_input(
            "🎯 Enter your guess (comma-separated for multiple attempts):", 
            value="",
            placeholder="Type movie name, actor, actress, or song...",
            key="guess_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("🚀 **Submit Guess**", use_container_width=True)
        with col2:
            hint_clicked = st.form_submit_button("💡 **Hint**", use_container_width=True)
        
        if hint_clicked:
            if not cp or cp not in st.session_state.players:
                st.error("🚫 Please select a player first in the sidebar.")
            else:
                st.session_state.hint_used = True
                st.session_state.current_hint = get_movie_hint(row)
                push_message("info", f"💡 {cp} used a hint: {st.session_state.current_hint}")
                st.rerun()
        
        if submitted:
            if not cp or cp not in st.session_state.players:
                st.error("🚫 Please select a player first in the sidebar.")
            else:
                guesses = [g.strip() for g in guess_input.split(",") if g.strip()]
                player = st.session_state.players[cp]
                
                for g in guesses:
                    # Movie check with enhanced feedback
                    if match_name(g, movie):
                        if movie not in player["guessed_movies"]:
                            # Award points and update streak
                            player["score"] += 2
                            player["guessed_movies"].append(movie)
                            player["history"].append(movie)
                            player["streak"] += 1
                            
                            if st.session_state.hints_used_current_movie or player["streak_has_hint"]:
                                player["streak_has_hint"] = True
                            if st.session_state.wrong_guess_this_movie or player["streak_has_wrong"]:
                                player["streak_has_wrong"] = True

                            push_message("success", f"🎉 {cp} nailed it! Movie: {movie} (+2 points)")
                            
                            # Enhanced celebration
                            st.session_state.show_celebration = True
                            show_success_animation()

                            # Milestone bonus logic
                            streak_now = player["streak"]
                            if streak_now % 5 == 0:
                                milestone = streak_now
                                if milestone not in player["milestones"]:
                                    bonus = 10 * (milestone // 5)
                                    if not player["streak_has_wrong"]:
                                        if milestone == 5 and player["streak_has_hint"]:
                                            bonus = 5
                                        player["score"] += bonus
                                        push_message("success", f"🎊 {cp} reached {milestone} streak milestone! +{bonus} bonus points!")
                                    else:
                                        push_message("info", f"🎯 {cp} reached {milestone} streak but had wrong guesses — no bonus this time")
                                    player["milestones"].add(milestone)

                            # Auto advance after 2 seconds
                            st.session_state.auto_advance = True
                            st.session_state.advance_time = time.time() + 2
                            st.rerun()
                            break
                        else:
                            push_message("info", f"🎭 {cp}, you already guessed this movie!")
                    
                    # Other correct guesses
                    elif match_name(g, actor):
                        if not st.session_state.guessed.get("actor", False):
                            st.session_state.guessed["actor"] = True
                            push_message("success", f"🕺 {cp} got the actor right!")
                    elif match_name(g, actress):
                        if not st.session_state.guessed.get("actress", False):
                            st.session_state.guessed["actress"] = True
                            push_message("success", f"💃 {cp} got the actress right!")
                    elif match_name(g, song):
                        if not st.session_state.guessed.get("song", False):
                            st.session_state.guessed["song"] = True
                            push_message("success", f"🎵 {cp} got the song right!")
                    else:
                        # Wrong guess
                        push_message("error", f"❌ {cp}, '{g}' isn't correct. Keep trying!")
                        player["streak_has_wrong"] = True
                        player["streak"] = 0

    # Enhanced Auto-advance handling with better countdown
    if st.session_state.get("auto_advance", False):
        remaining = max(0, int(st.session_state.advance_time - time.time()))
        if remaining > 0:
            st.markdown(f"""
            <div class="countdown-timer">
                <h3>⏳ Next cinema challenge in <span style="font-size: 2.5rem; color: #ffd700;">{remaining}</span> seconds...</h3>
                <div style="width: 100%; background: rgba(255,255,255,0.2); border-radius: 10px; margin-top: 1rem;">
                    <div style="width: {(2-remaining)/2*100}%; background: linear-gradient(90deg, #ffd700, #ff6b6b); height: 8px; border-radius: 10px; transition: width 0.1s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if HAS_AUTOREFRESH:
                st_autorefresh(interval=100, key="auto_refresh")
        else:
            st.session_state.auto_advance = False
            pick_new_movie()
            st.rerun()

    st.markdown("---")

    # Enhanced Hints & Reveals Section with equal-sized buttons
    st.markdown("### 🧠 **Power-Ups & Reveals**")
    st.markdown("*Use these wisely - some might affect your streak bonus!*")
    
    # First row of power-ups (3 buttons)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🕺\n**Reveal Actor**", use_container_width=True, key="reveal_actor", help="Reveal the lead actor"):
            st.session_state.revealed["actor"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🕺 Actor Revealed: **{actor}**")
            if cp and cp in st.session_state.players:
                st.session_state.players[cp]["streak_has_hint"] = True
            st.rerun()

    with col2:
        if st.button("💃\n**Reveal Actress**", use_container_width=True, key="reveal_actress", help="Reveal the lead actress"):
            st.session_state.revealed["actress"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"💃 Actress Revealed: **{actress}**")
            if cp and cp in st.session_state.players:
                st.session_state.players[cp]["streak_has_hint"] = True
            st.rerun()

    with col3:
        if st.button("🎵\n**Reveal Song**", use_container_width=True, key="reveal_song", help="Reveal the notable song"):
            st.session_state.revealed["song"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🎵 Song Revealed: **{song}**")
            if cp and cp in st.session_state.players:
                st.session_state.players[cp]["streak_has_hint"] = True
            st.rerun()

    # Second row of power-ups (2 buttons)
    col4, col5 = st.columns(2)
    with col4:
        if st.button("🎬\n**Reveal Movie**\n(Skip)", use_container_width=True, key="reveal_movie", help="Skip this movie"):
            st.session_state.revealed["movie"] = True
            push_message("info", f"📜 Movie Revealed: **{movie}** (No points, streak reset)")

            if cp and cp in st.session_state.players:
                p = st.session_state.players[cp]
                p["streak"] = 0
                p["streak_has_hint"] = False
                p["streak_has_wrong"] = False

            st.session_state.hints_used_current_movie = True
            st.session_state.auto_advance = True
            st.session_state.advance_time = time.time() + 3
            st.rerun()

    with col5:
        if st.button("📦\n**Reveal All**\n(Auto Next)", use_container_width=True, key="reveal_all", help="Show everything and move to next"):
            st.session_state.revealed = {"movie": True, "actor": True, "actress": True, "song": True}
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🎬 **Movie:** {movie}")
            push_message("info", f"🕺 **Actor:** {actor}")  
            push_message("info", f"💃 **Actress:** {actress}")
            push_message("info", f"🎵 **Song:** {song}")

            if cp and cp in st.session_state.players:
                st.session_state.players[cp]["streak_has_hint"] = True

            st.session_state.auto_advance = True
            st.session_state.advance_time = time.time() + 5
            st.rerun()

    # Show revealed information in a consolidated section
    if any(st.session_state.revealed.values()):
        st.markdown("### 🔓 **Revealed Information**")
        revealed_info = []
        
        if st.session_state.revealed["movie"]:
            revealed_info.append(f"🎬 **Movie:** {movie}")
        if st.session_state.revealed["actor"]:
            revealed_info.append(f"🕺 **Actor:** {actor}")
        if st.session_state.revealed["actress"]:
            revealed_info.append(f"💃 **Actress:** {actress}")
        if st.session_state.revealed["song"]:
            revealed_info.append(f"🎵 **Song:** {song}")
        
        for info in revealed_info:
            st.markdown(f"""
            <div class="game-card" style="background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,215,0,0.08) 100%); border-color: rgba(255,215,0,0.4);">
                <p style="text-align: center; font-size: 1.2rem; margin: 0;">{info}</p>
            </div>
            """, unsafe_allow_html=True)

# Enhanced Right Panel
with right:
    st.markdown("### 📊 **Live Game Stats**")
    
    # Quick stats overview
    if st.session_state.players:
        total_players = len(st.session_state.players)
        total_score = sum(p["score"] for p in st.session_state.players.values())
        highest_streak = max((p["streak"] for p in st.session_state.players.values()), default=0)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎮 Game Overview</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: #4ecdc4;">👥</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{total_players}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Players</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: #ffd700;">🏆</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{total_score}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Total Points</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: #ff6b6b;">🔥</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{highest_streak}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Top Streak</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: #667eea;">🎬</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{len(st.session_state.used_movies)}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Completed</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📜 **Player Chronicles**")
    
    if not st.session_state.players:
        st.markdown("""
        <div class="game-card">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎭</div>
                <h3>No Players Yet!</h3>
                <p style="opacity: 0.8;"><em>Add some brave souls to begin the cinema adventure...</em></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Enhanced player history display
        for pname, pdata in st.session_state.players.items():
            is_current = pname == st.session_state.current_player
            
            with st.expander(f"{'🎭' if is_current else '🎪'} **{pname}** — 🏆 {pdata['score']} | 🔥 {pdata['streak']}", expanded=is_current):
                # Enhanced player stats summary
                movies_count = len(pdata.get('guessed_movies', []))
                milestones_count = len(pdata.get('milestones', set()))
                
                st.markdown(f"""
                <div class="metric-card" style="margin: 0.5rem 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: center;">
                        <div>
                            <div style="font-size: 1.5rem; color: #4ecdc4;">🎬</div>
                            <div style="font-weight: bold; font-size: 1.2rem;">{movies_count}</div>
                            <div style="font-size: 0.8rem; opacity: 0.8;">Movies</div>
                        </div>
                        <div>
                            <div style="font-size: 1.5rem; color: #ffd700;">🎖️</div>
                            <div style="font-weight: bold; font-size: 1.2rem;">{milestones_count}</div>
                            <div style="font-size: 0.8rem; opacity: 0.8;">Milestones</div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span>⚡ <strong>Streak:</strong> {pdata['streak']}</span>
                            <span>💡 <strong>Hints Used:</strong> {'Yes' if pdata.get('streak_has_hint', False) else 'No'}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Recent movies guessed
                recent_movies = pdata.get("history", [])[-6:]  # Show last 6 movies
                if not recent_movies:
                    st.markdown("""
                    
                    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 10px; margin: 1rem 0;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌟</div>
                        <p style="opacity: 0.8;"><em>Ready to make cinema history...</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("**📈 Recent Activity:**")
                    for h in reversed(hist):  # Most recent first
                        if "✅ Correct movie" in h:
                            st.markdown(f"🎉 {h}", unsafe_allow_html=True)
                        elif "❌ Wrong guess" in h:
                            st.markdown(f"💔 {h}", unsafe_allow_html=True)
                        elif "💡 Revealed" in h:
                            st.markdown(f"🔍 {h}", unsafe_allow_html=True)
                        elif "🎖️ Milestone" in h:
                            st.markdown(f"🌟 {h}", unsafe_allow_html=True)
                        else:
                            st.markdown(f"📝 {h}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎪 **Live Activity Feed**")
    
    # Enhanced recent messages
    prune_messages(seconds=30)
    recent_messages = list(reversed(st.session_state.messages[-6:]))  # Last 6 messages, newest first
    
    if not recent_messages:
        st.markdown("""
        <div class="game-card">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem; animation: floating 3s ease-in-out infinite;">🔮</div>
                <p><em>The cinema crystal ball awaits your first move...</em></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for kind, text, ts in recent_messages:
            tstr = time.strftime("%H:%M:%S", time.localtime(ts))
            if kind == "success":
                st.markdown(f"""
                <div class="success-message">
                    <small style="opacity: 0.8;">{tstr}</small><br>
                    <strong>✨ {text}</strong>
                </div>
                """, unsafe_allow_html=True)
            elif kind == "error":
                st.markdown(f"""
                <div class="error-message">
                    <small style="opacity: 0.8;">{tstr}</small><br>
                    <strong>💥 {text}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%); 
                           backdrop-filter: blur(8px); padding: 1rem; border-radius: 10px; margin: 0.4rem 0;
                           border: 1px solid rgba(255,255,255,0.2);">
                    <small style="color: #aaa;">{tstr}</small><br>
                    <strong>ℹ️ {text}</strong>
                </div>
                """, unsafe_allow_html=True)

# Enhanced Footer with additional visual elements
st.markdown("---")
st.markdown("""
<div class="game-card celebration" style="text-align: center;">
    <h4>🎭 Welcome to Bollywood Cinema Quest! 🎬</h4>
    <p><em>Local multiplayer mode - perfect for family game nights and friendly competitions!</em></p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0; flex-wrap: wrap;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Trust Your Instincts</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Use Hints Strategically</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Every Fan Has Specialty</div>
        </div>
    </div>
    <small style="opacity: 0.7;">💡 Want real-time multiplayer across devices? Let me know and I'll add WebSocket magic! ✨</small>
</div>
""", unsafe_allow_html=True)

# Add enhanced floating elements for visual flair
st.markdown("""
<div style="position: fixed; top: 80px; right: 30px; font-size: 2.5rem; 
           animation: floating 5s ease-in-out infinite; z-index: 1000; opacity: 0.7;
           text-shadow: 0 0 20px rgba(255,215,0,0.6);">
    🎭
</div>
<div style="position: fixed; bottom: 30px; left: 30px; font-size: 2rem; 
           animation: floating 4s ease-in-out infinite reverse; z-index: 1000; opacity: 0.7;
           text-shadow: 0 0 20px rgba(78,205,196,0.6);">
    🎬
</div>
<div style="position: fixed; top: 50%; right: 20px; font-size: 1.8rem; 
           animation: floating 6s ease-in-out infinite; z-index: 1000; opacity: 0.5;
           text-shadow: 0 0 15px rgba(255,107,107,0.6);">
    🍿
</div>
<div style="position: fixed; top: 200px; left: 20px; font-size: 1.5rem; 
           animation: floating 3.5s ease-in-out infinite reverse; z-index: 1000; opacity: 0.6;
           text-shadow: 0 0 15px rgba(102,126,234,0.6);">
    🎪
</div>
""", unsafe_allow_html=True)

# Add some background particles for extra visual appeal
st.markdown("""
<div id="particles-background">
    <script>
    // Create floating background particles
    function createBackgroundParticles() {
        const particleCount = 15;
        const particles = [];
        
        for(let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            const size = Math.random() * 4 + 2;
            const duration = Math.random() * 20 + 15;
            const delay = Math.random() * 5;
            
            particle.style.position = 'fixed';
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.background = '#ffffff';
            particle.style.borderRadius = '50%';
            particle.style.opacity = '0.1';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '1';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = '100%';
            particle.style.animation = `floatUp ${duration}s linear infinite`;
            particle.style.animationDelay = delay + 's';
            
            document.body.appendChild(particle);
            particles.push(particle);
        }
        
        // Clean up after 60 seconds
        setTimeout(() => {
            particles.forEach(p => p.remove());
        }, 60000);
    }
    
    // Add floating animation for background particles
    if (!document.querySelector('#particle-style')) {
        const style = document.createElement('style');
        style.id = 'particle-style';
        style.textContent = `
            @keyframes floatUp {
                0% { 
                    transform: translateY(0px) translateX(0px) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 0.1;
                }
                90% {
                    opacity: 0.1;
                }
                100% { 
                    transform: translateY(-100vh) translateX(50px) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    createBackgroundParticles();
    </script>
</div>
""", unsafe_allow_html=True)