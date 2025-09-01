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

# Enhanced CSS with dark mode and amazing animations
st.markdown("""
<style>
    /* Dark Mode Base */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Custom Card Styles */
    .game-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.4);
        border-color: rgba(255,215,0,0.5);
    }
    
    /* Player Stats Cards */
    .player-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
        transition: all 0.3s ease;
    }
    
    .player-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(255,107,107,0.5);
    }
    
    .current-player {
        background: linear-gradient(135deg, #ffd700 0%, #ffb700 100%);
        color: #000;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(255,215,0,0.3); }
        to { box-shadow: 0 8px 30px rgba(255,215,0,0.8); }
    }
    
    /* Leaderboard Styles */
    .leaderboard-item {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .rank-1 { border-left-color: #ffd700; }
    .rank-2 { border-left-color: #c0c0c0; }
    .rank-3 { border-left-color: #cd7f32; }
    .rank-other { border-left-color: #4ecdc4; }
    
    .leaderboard-item:hover {
        transform: translateX(10px);
        background: rgba(255,255,255,0.15);
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Reveal Button Styles */
    .reveal-movie { background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%) !important; }
    .reveal-actor { background: linear-gradient(135deg, #3742fa 0%, #2f3542 100%) !important; }
    .reveal-actress { background: linear-gradient(135deg, #ff6b9d 0%, #ff3d71 100%) !important; }
    .reveal-song { background: linear-gradient(135deg, #26c0d3 0%, #3d84a8 100%) !important; }
    .reveal-all { background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%) !important; }
    
    /* Input Field Enhancements */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(255,215,0,0.3);
        background: rgba(255,255,255,0.15);
    }
    
    /* Success/Error Message Enhancements */
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: slideInRight 0.5s ease;
    }
    
    .error-message {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: shake 0.5s ease;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 20%, 40%, 60%, 80% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    }
    
    /* Movie Info Cards */
    .movie-hint {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .movie-hint:hover {
        transform: scale(1.02);
        border-color: rgba(255,215,0,0.5);
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Progress Indicators */
    .streak-indicator {
        background: linear-gradient(90deg, #ff6b6b, #ffd700, #4ecdc4);
        height: 6px;
        border-radius: 3px;
        margin: 1rem 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Title Enhancement */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 5px rgba(102,126,234,0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(118,75,162,0.6)); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Floating Animation for Game Elements */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Celebration Effects */
    .celebration {
        animation: celebrate 1s ease-in-out;
    }
    
    @keyframes celebrate {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.1) rotate(-5deg); }
        50% { transform: scale(1.2) rotate(5deg); }
        75% { transform: scale(1.1) rotate(-3deg); }
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Enhanced JavaScript for Custom Animations
# =========================
def show_success_animation():
    st.markdown("""
    <script>
    // Custom success animation
    function createFireworks() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7'];
        for(let i = 0; i < 20; i++) {
            const firework = document.createElement('div');
            firework.style.position = 'fixed';
            firework.style.left = Math.random() * window.innerWidth + 'px';
            firework.style.top = Math.random() * window.innerHeight + 'px';
            firework.style.width = '4px';
            firework.style.height = '4px';
            firework.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            firework.style.borderRadius = '50%';
            firework.style.pointerEvents = 'none';
            firework.style.zIndex = '9999';
            firework.style.animation = 'firework 2s ease-out forwards';
            document.body.appendChild(firework);
            
            setTimeout(() => {
                firework.remove();
            }, 2000);
        }
    }
    
    // Add firework animation CSS
    if (!document.querySelector('#firework-style')) {
        const style = document.createElement('style');
        style.id = 'firework-style';
        style.textContent = `
            @keyframes firework {
                0% { transform: scale(0) rotate(0deg); opacity: 1; }
                50% { transform: scale(1.5) rotate(180deg); opacity: 0.8; }
                100% { transform: scale(0) rotate(360deg); opacity: 0; }
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
    
    # Enhanced player addition
    st.markdown("### Add New Player")
    new_player = st.text_input("🎭 Enter player name", value="", placeholder="Enter your cinema alias...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ Join Game", use_container_width=True):
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
        if st.button("🔄 Reset Game", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Enhanced player selection
    if st.session_state.players:
        st.markdown("### Current Player")
        player_list = list(st.session_state.players.keys())
        default_idx = player_list.index(st.session_state.current_player) if st.session_state.current_player in player_list else 0
        chosen = st.selectbox("🎬 Who's turn to guess?", player_list, index=default_idx)
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
            <span style="font-size: 2rem; color: #ffd700;">{get_initials(movie)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="movie-hint floating">
            💃 <strong>Actress Initials</strong><br>
            <span style="font-size: 2rem; color: #ff6b9d;">{get_initials(actress)}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="movie-hint floating">
            🕺 <strong>Actor Initials</strong><br>
            <span style="font-size: 2rem; color: #3742fa;">{get_initials(actor)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="movie-hint floating">
            🎵 <strong>Song Initials</strong><br>
            <span style="font-size: 2rem; color: #26c0d3;">{get_initials(song) if song else 'N/A'}</span>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Guess Form
    st.markdown("### 💭 **Make Your Guess**")
    with st.form(key="guess_form", clear_on_submit=True):
        guess_input = st.text_input(
            "🎯 Enter your guess (comma-separated for multiple attempts):", 
            value="",
            placeholder="Type movie name, actor, actress, or song..."
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
                        if not st.session_state.guessed["actor"]:
                            st.session_state.guessed["actor"] = True
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Actor guessed ({g})")
                            push_message("success", f"🕺 {cp} got the actor right!")
                    elif match_name(g, actress):
                        if not st.session_state.guessed["actress"]:
                            st.session_state.guessed["actress"] = True
                            player["history"].append(f"{time.strftime('%H:%M:%S')} - ✅ Actress guessed ({g})")
                            push_message("success", f"💃 {cp} got the actress right!")
                    elif match_name(g, song):
                        if not st.session_state.guessed["song"]:
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

    # Enhanced Hints & Reveals Section
    st.markdown("### 🧠 **Power-Ups & Reveals**")
    st.markdown("*Use these wisely - they might affect your streak bonus!*")
    
    col1, col2, col3, col4, col5 = st.columns(5)

    # Enhanced reveal buttons with custom styling
    with col1:
        if st.button("🎬 **Reveal Movie**\n(Skip)", use_container_width=True, key="reveal_movie"):
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

    with col2:
        if st.button("🕺 **Reveal Actor**", use_container_width=True, key="reveal_actor"):
            st.session_state.revealed["actor"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🕺 Actor Revealed: **{actor}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed actor")
            st.rerun()

    with col3:
        if st.button("💃 **Reveal Actress**", use_container_width=True, key="reveal_actress"):
            st.session_state.revealed["actress"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"💃 Actress Revealed: **{actress}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed actress")
            st.rerun()

    with col4:
        if st.button("🎵 **Reveal Song**", use_container_width=True, key="reveal_song"):
            st.session_state.revealed["song"] = True
            st.session_state.hints_used_current_movie = True
            push_message("info", f"🎵 Song Revealed: **{song}**")
            if cp:
                st.session_state.players[cp]["streak_has_hint"] = True
                st.session_state.players[cp]["history"].append(f"{time.strftime('%H:%M:%S')} - 💡 Revealed song")
            st.rerun()

    with col5:
        if st.button("📦 **Reveal All**\n(Auto Next)", use_container_width=True, key="reveal_all"):
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
            <div class="game-card">
                <h3>⏳ Next cinema challenge in <span style="color: #ffd700; font-size: 1.5rem;">{remaining}</span> seconds...</h3>
                <div class="streak-indicator"></div>
            </div>
            """, unsafe_allow_html=True)
            if HAS_AUTOREFRESH:
                st_autorefresh(interval=1000, key="auto_refresh")
        else:
            st.session_state.auto_advance = False
            pick_new_movie()
            st.rerun()

# Enhanced Right Panel
with right:
    st.markdown("### 📊 **Live Game Stats**")
    
    # Quick stats overview
    if st.session_state.players:
        total_players = len(st.session_state.players)
        total_score = sum(p["score"] for p in st.session_state.players.values())
        highest_streak = max((p["streak"] for p in st.session_state.players.values()), default=0)
        
        st.markdown(f"""
        <div class="game-card">
            <h4>🎮 Game Overview</h4>
            <p>👥 <strong>{total_players}</strong> players competing</p>
            <p>🏆 <strong>{total_score}</strong> total points scored</p>
            <p>🔥 <strong>{highest_streak}</strong> highest current streak</p>
            <p>🎬 <strong>{len(st.session_state.used_movies)}</strong> movies completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📜 **Player Chronicles**")
    
    if not st.session_state.players:
        st.markdown("""
        <div class="game-card">
            <p>🎭 No players yet in this cinema quest!</p>
            <p><em>Add some brave souls to begin the adventure...</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Enhanced player history display
        for pname, pdata in st.session_state.players.items():
            is_current = pname == st.session_state.current_player
            player_class = "current-player" if is_current else "player-card"
            
            with st.expander(f"{'🎭' if is_current else '🎪'} **{pname}** — 🏆 {pdata['score']} | 🔥 {pdata['streak']}", expanded=is_current):
                # Player stats summary
                st.markdown(f"""
                <div class="{player_class}" style="margin: 0.5rem 0;">
                    <small>
                    📈 <strong>Movies Guessed:</strong> {len(pdata.get('guessed_movies', []))}<br>
                    🎖️ <strong>Milestones:</strong> {len(pdata.get('milestones', set()))}<br>
                    ⚡ <strong>Current Streak:</strong> {pdata['streak']}<br>
                    💡 <strong>Used Hints:</strong> {'Yes' if pdata.get('streak_has_hint', False) else 'No'}
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                # Recent activity
                hist = pdata.get("history", [])[-10:]  # Show last 10 events
                if not hist:
                    st.write("🌟 *Ready to make cinema history...*")
                else:
                    st.markdown("**Recent Activity:**")
                    for h in reversed(hist):  # Most recent first
                        if "✅ Correct movie" in h:
                            st.markdown(f"🎉 {h}")
                        elif "❌ Wrong guess" in h:
                            st.markdown(f"💔 {h}")
                        elif "💡 Revealed" in h:
                            st.markdown(f"🔍 {h}")
                        elif "🎖️ Milestone" in h:
                            st.markdown(f"🌟 {h}")
                        else:
                            st.markdown(f"📝 {h}")

    st.markdown("---")
    st.markdown("### 🎪 **Live Activity Feed**")
    
    # Enhanced recent messages
    prune_messages(seconds=30)
    recent_messages = list(reversed(st.session_state.messages[-8:]))  # Last 8 messages, newest first
    
    if not recent_messages:
        st.markdown("""
        <div class="game-card">
            <p>🔮 <em>The cinema crystal ball awaits your first move...</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for kind, text, ts in recent_messages:
            tstr = time.strftime("%H:%M:%S", time.localtime(ts))
            if kind == "success":
                st.markdown(f"""
                <div class="success-message">
                    <small>{tstr}</small><br>
                    ✨ {text}
                </div>
                """, unsafe_allow_html=True)
            elif kind == "error":
                st.markdown(f"""
                <div class="error-message">
                    <small>{tstr}</small><br>
                    💥 {text}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0;">
                    <small style="color: #888;">{tstr}</small><br>
                    ℹ️ {text}
                </div>
                """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div class="game-card" style="text-align: center;">
    <h4>🎭 Welcome to Bollywood Cinema Quest! 🎬</h4>
    <p><em>Local multiplayer mode - perfect for family game nights and friendly competitions!</em></p>
    <p>🌟 <strong>Pro Tips:</strong> Trust your instincts, use hints strategically, and remember - every Bollywood fan has their specialty!</p>
    <small>💡 Want real-time multiplayer across devices? Let me know and I'll add WebSocket magic! ✨</small>
</div>
""", unsafe_allow_html=True)

# Add some floating elements for visual flair
st.markdown("""
<div style="position: fixed; top: 20px; right: 20px; font-size: 2rem; animation: floating 4s ease-in-out infinite; z-index: 1000;">
    🎭
</div>
<div style="position: fixed; bottom: 20px; left: 20px; font-size: 1.5rem; animation: floating 3s ease-in-out infinite reverse; z-index: 1000;">
    🎬
</div>
""", unsafe_allow_html=True)