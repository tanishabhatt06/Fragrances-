import streamlit as st
import pickle
import numpy as np
import time

# Set page config
st.set_page_config(
    page_title="AI Perfume Recommendation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load model & encoders
model = pickle.load(open("model.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))

# Custom CSS with modern design
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #f5f0ff 0%, #ffe8f0 50%, #e3f2fd 100%);
            min-height: 100vh;
        }
        
        .main {
            background: transparent;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f0ff 0%, #ffe8f0 50%, #e3f2fd 100%);
        }
        
        /* Header Styling */
        .header {
            text-align: center;
            padding: 60px 20px 30px;
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
            border-radius: 30px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .header p {
            font-size: 1.1rem;
            color: #666;
            margin-top: 10px;
            font-weight: 300;
        }
        
        /* Glass Morphism Card */
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.8);
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            margin-bottom: 30px;
        }
        
        .glass-card h2 {
            color: #1f2937;
            font-size: 1.3rem;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        /* Input Grid */
        .input-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .input-item {
            display: flex;
            flex-direction: column;
        }
        
        .input-label {
            font-size: 0.95rem;
            color: #374151;
            margin-bottom: 8px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Button Styling */
        .cta-button {
            width: 100%;
            padding: 16px 32px;
            background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
            margin-top: 20px;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
        }
        
        .cta-button:active {
            transform: translateY(0);
        }
        
        /* Result Card */
        .result-card {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 2px solid rgba(168, 85, 247, 0.3);
            padding: 40px;
            text-align: center;
            animation: slideUp 0.6s ease, glow 2s ease-in-out infinite;
            margin-top: 30px;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
            }
            50% {
                box-shadow: 0 0 40px rgba(168, 85, 247, 0.6);
            }
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-spinner {
            display: inline-block;
            animation: spin 1s linear infinite;
            font-size: 2rem;
        }
        
        .perfume-name {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 15px 0;
            font-weight: 700;
        }
        
        .perfume-tagline {
            color: #666;
            font-size: 1.1rem;
            margin-top: 10px;
            font-weight: 300;
        }
        
        .perfume-icon {
            font-size: 4rem;
            margin-bottom: 15px;
            animation: bounce 1.5s ease-in-out infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            color: #999;
            font-size: 0.9rem;
            font-weight: 300;
            margin-top: 50px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .input-grid {
                grid-template-columns: 1fr;
            }
            
            .perfume-name {
                font-size: 1.8rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Perfume icons mapping
perfume_icons = {
    "Rose": "🌹",
    "Lavender": "🪻",
    "Jasmine": "🌼",
    "Vanilla": "🍦",
    "Sandalwood": "🌳",
    "Musk": "✨",
    "Amber": "🟧",
    "Citrus": "🍊",
    "Marine": "🌊",
    "Floral": "🌸",
    "Fresh": "🌿",
    "Sweet": "🍫",
    "Minty": "❄️"
}

# Taglines for perfumes
perfume_taglines = {
    "Rose": "Timeless elegance and romance",
    "Lavender": "Calm and soothing serenity",
    "Jasmine": "Mysterious and enchanting",
    "Vanilla": "Warm and comforting sweetness",
    "Sandalwood": "Rich and sophisticated",
    "Musk": "Modern and alluring",
    "Amber": "Deep and sensual warmth",
    "Citrus": "Fresh citrus vibe for your day",
    "Marine": "Crisp aquatic freshness",
    "Floral": "Blooming garden elegance",
    "Fresh": "Clean and revitalizing",
    "Sweet": "Delightfully sugary notes",
    "Minty": "Cool and refreshing burst"
}

# Header
st.markdown("""
    <div class="header">
        <h1>✨ AI Perfume Recommendation</h1>
        <p>Discover your perfect fragrance using artificial intelligence</p>
    </div>
""", unsafe_allow_html=True)

# Create the main layout with columns
input_col, result_col = st.columns([1, 1])

with input_col:
    # Main Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2>🧪 Personalize Your Selection</h2>', unsafe_allow_html=True)

    # Input Grid Layout
    sub_col1, sub_col2 = st.columns(2)

    with sub_col1:
        st.markdown('<div class="input-label">🌡️ Temperature (°C)</div>', unsafe_allow_html=True)
        temperature = st.slider("Temperature", 20, 40, 25, key="temp_widget", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">⏰ Time of Day</div>', unsafe_allow_html=True)
        time_of_day = st.selectbox("Time", ["Morning", "Afternoon", "Evening"], key="time_widget", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">🌫️ AQI (Air Quality Index)</div>', unsafe_allow_html=True)
        aqi = st.slider("AQI", 50, 300, 150, key="aqi_widget", label_visibility="collapsed")

    with sub_col2:
        st.markdown('<div class="input-label">💧 Humidity (%)</div>', unsafe_allow_html=True)
        humidity = st.slider("Humidity", 40, 100, 60, key="humidity_widget", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">😊 Mood</div>', unsafe_allow_html=True)
        mood = st.selectbox("Mood", ["Calm", "Fresh", "Romantic", "Energetic"], key="mood_widget", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">🎯 Occasion</div>', unsafe_allow_html=True)
        occasion = st.selectbox("Occasion", ["Home", "Office", "Date", "Gym"], key="occasion_widget", label_visibility="collapsed")

    st.markdown('<div class="input-label">🌸 Preferred Type</div>', unsafe_allow_html=True)
    ptype = st.selectbox("Type", ["Floral", "Citrus", "Sweet", "Minty"], key="ptype_widget", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Recommend Perfume", use_container_width=True):
        st.session_state['show_result'] = True
        st.session_state['saved_temp'] = temperature
        st.session_state['saved_humidity'] = humidity
        st.session_state['saved_aqi'] = aqi
        st.session_state['saved_time'] = time_of_day
        st.session_state['saved_mood'] = mood
        st.session_state['saved_occasion'] = occasion
        st.session_state['saved_ptype'] = ptype

# Encode inputs
def encode(col, value):
    return encoders[col].transform([value])[0]

with result_col:
    st.markdown('<div style="min-height: 100px;"></div>', unsafe_allow_html=True)
    if 'show_result' in st.session_state and st.session_state.get('show_result'):
        # Loading animation
        with st.spinner(""):
            st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div class='loading-spinner'>✨</div>
                    <p style='color: #666; font-size: 1.1rem; margin-top: 10px;'>Finding your perfect fragrance...</p>
                </div>
            """, unsafe_allow_html=True)
            import time as time_module
            time_module.sleep(1)
        
        # Prediction
        input_data = np.array([[
            st.session_state.get('saved_temp'),
            st.session_state.get('saved_humidity'),
            st.session_state.get('saved_aqi'),
            encode("TimeOfDay", st.session_state.get('saved_time')),
            encode("Mood", st.session_state.get('saved_mood')),
            encode("Occasion", st.session_state.get('saved_occasion')),
            encode("PreferredType", st.session_state.get('saved_ptype'))
        ]])

        prediction = model.predict(input_data)[0]
        perfume = encoders["Perfume"].inverse_transform([prediction])[0]
        
        # Get icon and tagline
        icon = perfume_icons.get(perfume, "🌸")
        tagline = perfume_taglines.get(perfume, "Experience luxury and elegance")
        
        # Result Card
        st.markdown(f"""
            <div class="result-card">
                <div class="perfume-icon">{icon}</div>
                <h2 style='color: #1f2937; margin: 0;'>Your Perfect Match</h2>
                <div class="perfume-name">{perfume}</div>
                <div class="perfume-tagline">{tagline}</div>
                <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(168, 85, 247, 0.2);'>
                    <p style='color: #666; font-size: 0.95rem; margin: 10px 0;'>
                        <strong>Environment:</strong> {st.session_state.get('saved_temp')}°C, {st.session_state.get('saved_humidity')}% humidity, AQI {st.session_state.get('saved_aqi')}
                    </p>
                    <p style='color: #666; font-size: 0.95rem; margin: 10px 0;'>
                        <strong>Your Preferences:</strong> {st.session_state.get('saved_time')}, {st.session_state.get('saved_mood')} mood, {st.session_state.get('saved_occasion')}, {st.session_state.get('saved_ptype')} type
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.session_state['show_result'] = False

# Footer
st.markdown("""
    <div class="footer">
        <p>🤖 Powered by AI | Premium Fragrance Intelligence</p>
    </div>
""", unsafe_allow_html=True)