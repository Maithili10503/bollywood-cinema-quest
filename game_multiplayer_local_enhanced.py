# game_multiplayer_local_enhanced.py
import time
import pandas as pd
from rapidfuzz import fuzz
import streamlit as st

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
    
    /* Specific button styles for different actions */
    div[data-testid="stButton"]:nth-of-type(1) button {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%) !important;
    }
    
    div[data-testid="stButton"]:nth-of-type(2) button {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%) !important;
    }
    
    /* Power-up buttons with equal sizing */
    .power-up-button {
        height: 80px !important;
        min-height: 80px !important;
        font-size: 13px !important;
        line-height: 1.2 !important;
        padding: 0.8rem !important;
        white-space: normal !important;
        text-align: center !important;
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
    
    .movie-hint:before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7, #ff6b6b);
        border-radius: 20px;
        z-index: -1;
        animation: borderRotate 4s linear infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .movie-hint:hover:before {
        opacity: 0.8;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress Indicators */
    .streak-indicator {
        background: linear-gradient(90deg, #ff6b6b, #ffd700, #4ecdc4, #ff6b6b);
        background-size: 300% 300%;
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
        animation: gradientShift 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title Enhancement */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin: 2rem 0;
        animation: titlePulse 4s ease-in-out infinite;
        position: relative;
        text-shadow: none;
    }
    
    @keyframes titlePulse {
        0%, 100% { 
            filter: drop-shadow(0 0 10px rgba(102,126,234,0.4));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 30px rgba(118,75,162,0.8));
            transform: scale(1.02);
        }
    }
    
    /* Enhanced Expander Styling */
    .streamlit-expander {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .streamlit-expander > div:first-child {
        background: transparent !important;
        color: #ffffff !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }
    
    .streamlit-expander > div:first-child:hover {
        background: rgba(255,255,255,0.1) !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(102,126,234,0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 4px 20px rgba(102,126,234,0.5);
    }
    
    /* Floating Animation for Game Elements */
    .floating {
        animation: floating 4s ease-in-out infinite;
    }
    
    @keyframes floating {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-8px) rotate(1deg); }
        50% { transform: translateY(-15px) rotate(0deg); }
        75% { transform: translateY(-8px) rotate(-1deg); }
    }
    
    /* Celebration Effects */
    .celebration {
        animation: celebrate 2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes celebrate {
        0% { transform: scale(1) rotate(0deg); }
        15% { transform: scale(1.1) rotate(-5deg); }
        30% { transform: scale(1.2) rotate(5deg); }
        45% { transform: scale(1.15) rotate(-3deg); }
        60% { transform: scale(1.25) rotate(3deg); }
        75% { transform: scale(1.1) rotate(-1deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    
    /* Additional UI Enhancements */
    .metric-card {
        background: linear-gradient(135deg, rgba(78,205,196,0.2) 0%, rgba(78,205,196,0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(78,205,196,0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(78,205,196,0.2);
        border-color: rgba(78,205,196,0.5);
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .stForm:hover {
        border-color: rgba(255,215,0,0.4);
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%);
    }
    
    /* Ensure all text remains visible */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #ffffff !important;
    }
    
    /* Fix any remaining white backgrounds */
    .stContainer, .main .block-container {
        background: transparent !important;
    }
    
    /* Enhanced mobile responsiveness */
    @media (max-width: 768px) {
        .main-title {
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
# Enhanced JavaScript for Custom Animations
# =========================
def show_success_animation():
    st.markdown("""
    <script>
    // Enhanced success animation with more particles
    function createFireworks() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#667eea', '#764ba2'];
        const particles = 30; // Increased particle count
        
        for(let i = 0; i < particles; i++) {
            const firework = document.createElement('div');
            const size = Math.random() * 6 + 3;
            firework.style.position = 'fixed';
            firework.style.left = Math.random() * window.innerWidth + 'px';
            firework.style.top = Math.random() * window.innerHeight + 'px';
            firework.style.width = size + 'px';
            firework.style.height = size + 'px';
            firework.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            firework.style.borderRadius = '50%';
            firework.style.pointerEvents = 'none';
            firework.style.zIndex = '9999';
            firework.style.animation = `firework ${2 + Math.random()}s ease-out forwards`;
            firework.style.boxShadow = `0 0 20px ${colors[Math.floor(Math.random() * colors.length)]}`;
            document.body.appendChild(firework);
            
            setTimeout(() => {
                firework.remove();
            }, 3000);
        }
    }
    
    // Add enhanced firework animation CSS
    if (!document.querySelector('#firework-style')) {
        const style = document.createElement('style');
        style.id = 'firework-style';
        style.textContent = `
            @keyframes firework {
                0% { 
                    transform: scale(0) rotate(0deg) translateY(0px); 
                    opacity: 1; 
                }
                25% { 
                    transform: scale(1.2) rotate(90deg) translateY(-50px); 
                    opacity: 0.9; 
                }
                50% { 
                    transform: scale(1.8) rotate(180deg) translateY(-100px); 
                    opacity: 0.7; 
                }
                75% { 
                    transform: scale(1.5) rotate(270deg) translateY(-150px); 
                    opacity: 0.4; 
                }
                100% { 
                    transform: scale(0.2) rotate(360deg) translateY(-200px); 
                    opacity: 0; 
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    createFireworks();
    </script>
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

# =========================
# Session State (multiplayer local)
# =========================
def init_state():
    ss = st.session_state
    if "players" not in ss:
        ss.players = {}
    if "current_player" not in ss:
        ss.current_player = None
    if "used_movies" not in ss:
        ss.used_movies = set()
    if "current_row" not in ss:
        pick_new_movie()
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

def push_message(kind, text):
    st.session_state.messages.append((kind, text, time.time()))

def prune_messages(seconds=10):
    now = time.time()
    st.session_state.messages = [(k,t,ts) for (k,t,ts) in st.session_state.messages if now - ts < seconds]

def finish_movie_and_advance(delay_sec=2):
    time.sleep(delay_sec)
    pick_new_movie()
    st.rerun()

init_state()

# =========================
# Enhanced Sidebar: players & controls
# =========================
with st.sidebar:
    st.markdown('<div class="floating">', unsafe_allow_html=True)
    st.markdown("# 👥 **Cinema Quest Players**")
    st.markdown('</div>', unsafe_allow_html=True)
    
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
# Main Layout Enhancement
# =========================
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
        • **💡 Hints available**: Actor, Actress, Song reveals (affects bonus)<br>
        • **⚡ Streak System**: Wrong guess = streak reset, but score stays!<br>
        • **🎪 Multiplayer**: Add friends and compete for cinema supremacy!<br>
        
        <small>💫 <em>Pro tip: Use initials wisely and trust your Bollywood knowledge!</em></small>
        </div>
        """, unsafe_allow_html=True)

    # Current player display
    cp = st.session_state.current_player
    if cp:
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
    else:
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
            <p><em>Refresh the page to start a new cinema quest...</em></p>
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

    # Enhanced Guess Form
    st.markdown("### 💭 **Make Your Guess**")
    with st.form(key="guess_form", clear_on_submit=True):
        guess_input = st.text_input(
            "🎯 Enter your guess (comma-separated for multiple attempts):", 
            value="",
            placeholder="Type movie name, actor, actress, or song...",
            key="guess_input"
        )
        submitted = st.form_submit_button("🚀 **Submit Guess**", use_container_width=True)
        
        if submitted:
            if not cp:
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
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Correct movie: {movie} (+2)")
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
                                        player["history"].append(f"{time.strftime('%H:%M:%S')} - 🎖️ Milestone: {milestone} (+{bonus})")
                                        push_message("success", f"🎊 {cp} reached {milestone} streak milestone! +{bonus} bonus points!")
                                    else:
                                        push_message("info", f"🎯 {cp} reached {milestone} streak but had wrong guesses — no bonus this time")
                                    player["milestones"].add(milestone)

                            finish_movie_and_advance(delay_sec=2)
                            break
                        else:
                            push_message("info", f"🎭 {cp}, you already guessed this movie!")
                    
                    # Other correct guesses
                    elif match_name(g, actor):
                        if not st.session_state.guessed.get("actor", False):
                            st.session_state.guessed["actor"] = True
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Actor guessed ({g})")
                            push_message("success", f"🕺 {cp} got the actor right!")
                    elif match_name(g, actress):
                        if not st.session_state.guessed.get("actress", False):
                            st.session_state.guessed["actress"] = True
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Actress guessed ({g})")
                            push_message("success", f"💃 {cp} got the actress right!")
                    elif match_name(g, song):
                        if not st.session_state.guessed.get("song", False):
                            st.session_state.guessed["song"] = True
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Song guessed ({g})")
                            push_message("success", f"🎵 {cp} got the song right!")
                    else:
                        # Wrong guess
                        push_message("error", f"❌ {cp}, '{g}' isn't correct. Keep trying!")
                        player["history"].append(f"{time.strftime('%H:%M:%S')} - ❌ Wrong guess: {g}")
                        player["streak_has_wrong"] = True
                        player["streak"] = 0

    # Enhanced Messages Display
    prune_messages(seconds=10)
    for kind, text, _ in st.session_state.messages:
        if kind == "success":
            st.markdown(f'<div class="success-message">✨ {text}</div>', unsafe_allow_html=True)
        elif kind == "error":
            st.markdown(f'<div class="error-message">💥 {text}</div>', unsafe_allow_html=True)
        else:
            st.info(text)

    st.markdown("---")

    # Enhanced Hints & Reveals Section with equal-sized buttons
    st.markdown("### 🧠 **Power-Ups & Reveals**")
    st.markdown("*Use these wisely - they might affect your streak bonus!*")
    
    # First row of power-ups (3 buttons)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🕺\n**Reveal Actor**", use_container_width=True, key="reveal_actor", help="Reveal the lead actor"):
            st.session_state.revealed["actor"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🕺 Actor Revealed: **{actor}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed actor")
            st.rerun()

    with col2:
        if st.button("💃\n**Reveal Actress**", use_container_width=True, key="reveal_actress", help="Reveal the lead actress"):
            st.session_state.revealed["actress"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"💃 Actress Revealed: **{actress}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed actress")
            st.rerun()

    with col3:
        if st.button("🎵\n**Reveal Song**", use_container_width=True, key="reveal_song", help="Reveal the notable song"):
            st.session_state.revealed["song"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🎵 Song Revealed: **{song}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed song")
            st.rerun()

    # Second row of power-ups (2 buttons)
    col4, col5 = st.columns(2)
    with col4:
        if st.button("🎬\n**Reveal Movie**\n(Skip)", use_container_width=True, key="reveal_movie", help="Skip this movie"):
            st.session_state.revealed["movie"] = True
            push_message("info", f"📜 Movie Revealed: **{movie}** (No points, streak reset)")

            if cp:
                p = st.session_state.players[cp]
                p["streak"] = 0
                p["streak_has_hint"] = False
                p["streak_has_wrong"] = False
                p["history"].append(f"{time.strftime('%H:%M:%S')} - ⏭️ Skipped movie: {movie}")

            st.session_state.hints_used_current_movie = True
            st.session_state.auto_advance = True
            st.session_state.advance_time = time.time() + 5

    with col5:
        if st.button("📦\n**Reveal All**\n(Auto Next)", use_container_width=True, key="reveal_all", help="Show everything and move to next"):
            st.session_state.revealed = {"movie": True, "actor": True, "actress": True, "song": True}
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🎬 **Movie:** {movie}")
            push_message("info", f"🕺 **Actor:** {actor}")
            push_message("info", f"💃 **Actress:** {actress}")
            push_message("info", f"🎵 **Song:** {song}")
            push_message("info", "⏩ Moving to next movie in **5 seconds**...")

            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 📦 Revealed all")

            st.session_state.auto_advance = True
            st.session_state.advance_time = time.time() + 5

    # Enhanced Auto-advance handling
    if st.session_state.get("auto_advance", False):
        remaining = int(st.session_state.advance_time - time.time())
        if remaining > 0:
            st.markdown(f"""
            <div class="game-card" style="text-align: center;">
                <h3>⏳ Next cinema challenge in <span style="color: #ffd700; font-size: 1.8rem; text-shadow: 0 0 15px rgba(255,215,0,0.6);">{remaining}</span> seconds...</h3>
                <div class="streak-indicator"></div>
            </div>
            """, unsafe_allow_html=True)
            if HAS_AUTOREFRESH:
                st_autorefresh(interval=1000, key="auto_refresh")
        else:
            st.session_state.auto_advance = False
            pick_new_movie()
            st.rerun()

    # Show revealed information
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
            player_class = "current-player" if is_current else "player-card"
            
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
                
                # Recent activity
                hist = pdata.get("history", [])[-8:]  # Show last 8 events
                if not hist:
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