"""
AI Recon Mapper v1.0
Aplicación profesional para análisis de reconocimiento de ciberseguridad con IA.
"""

import streamlit as st
from dotenv import load_dotenv
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from ai.analyzer import ReconAnalyzer
from utils.parser import (
    normalize_text, detect_data_type, get_text_stats,
    extract_ips, extract_domains, extract_ports
)
from utils.helpers import (
    check_api_key, format_error_message, format_tokens_usage,
    format_cost_estimate, validate_input_text, format_warning_message
)

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="AI Recon Mapper v1.0",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stat-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None

def init_analyzer(model: str):
    """Inicializa o actualiza el analizador."""
    if st.session_state.analyzer is None or st.session_state.analyzer.model != model:
        st.session_state.analyzer = ReconAnalyzer(model=model)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=AI+Recon+Mapper", use_container_width=True)
    
    st.markdown("## ⚙️ Configuración")
    
    # Verificar API key
    api_configured, api_message = check_api_key()
    
    if api_configured:
        st.success("✅ API Key configurada")
    else:
        st.error(f"❌ {api_message}")
        st.info("Configura la variable de entorno `OPENAI_API_KEY` para usar la aplicación.")
    
    st.markdown("---")
    
    # Selector de modelo
    st.markdown("### 🤖 Modelo de IA")
    model_options = {
        "GPT-4o Mini (Recomendado)": "gpt-4o-mini",
        "GPT-4o": "gpt-4o",
        "GPT-4 Turbo": "gpt-4-turbo",
        "GPT-3.5 Turbo": "gpt-3.5-turbo"
    }
    selected_model_name = st.selectbox(
        "Selecciona el modelo",
        options=list(model_options.keys()),
        index=0
    )
    selected_model = model_options[selected_model_name]
    
    # Modo de análisis
    st.markdown("### 👤 Nivel de Experiencia")
    mode = st.radio(
        "Selecciona tu nivel",
        options=["junior", "expert"],
        format_func=lambda x: "🎓 Junior (Principiante)" if x == "junior" else "🎯 Expert (Profesional)",
        index=0
    )
    
    # Tipo de datos
    st.markdown("### 📊 Tipo de Datos")
    data_type_options = ["Mixto (Auto-detectar)", "Nmap", "WHOIS/DNS"]
    data_type = st.selectbox(
        "Tipo de reconocimiento",
        options=data_type_options,
        index=0
    )
    
    st.markdown("---")
    
    # Configuración avanzada
    with st.expander("🔧 Configuración Avanzada"):
        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controla la creatividad de las respuestas"
        )
        max_tokens = st.slider(
            "Máximo de tokens",
            min_value=1000,
            max_value=4000,
            value=2500,
            step=500,
            help="Longitud máxima de la respuesta"
        )
    
    st.markdown("---")
    
    # Información
    with st.expander("ℹ️ Acerca de"):
        st.markdown("""
        **AI Recon Mapper v1.0**
        
        Herramienta profesional para análisis de reconocimiento de ciberseguridad con IA.
        
        **Características:**
        - Análisis inteligente con OpenAI
        - Modos Junior y Expert
        - Detección automática de tipo de datos
        - Estadísticas en tiempo real
        
        **Desarrollado con:**
        - Python 3.x
        - Streamlit
        - OpenAI API
        """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown('<h1 class="main-header">🕵️ AI Recon Mapper</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análisis profesional de reconocimiento de ciberseguridad con IA</p>', unsafe_allow_html=True)

# Descripción
st.markdown("""
Esta herramienta utiliza inteligencia artificial para analizar resultados de reconocimiento de ciberseguridad.
Pega los resultados de tus escaneos (Nmap, WHOIS, DNS, etc.) y obtén un análisis detallado con:
- 🎯 Identificación de activos (IPs, dominios, subdominios)
- 🔧 Servicios y tecnologías detectadas
- ⚠️ Análisis de riesgos (enfoque educativo)
- 💡 Recomendaciones de estudio y mejores prácticas
""")

st.markdown("---")

# Layout principal
col1, col2 = st.columns([1, 1])

# ============================================================================
# COLUMNA IZQUIERDA - ENTRADA
# ============================================================================

with col1:
    st.markdown("## 📥 Entrada de Datos")
    
    # Área de texto
    input_text = st.text_area(
        "Pega aquí tus resultados de reconocimiento",
        height=400,
        placeholder="""Ejemplo de escaneo Nmap:

Starting Nmap 7.80 ( https://nmap.org )
Nmap scan report for example.com (93.184.216.34)
Host is up (0.015s latency).

PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.9p1
80/tcp   open  http       nginx 1.18.0
443/tcp  open  ssl/https  nginx 1.18.0
3306/tcp open  mysql      MySQL 5.7.32

Service detection performed. Please report any incorrect results.
Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds
        """,
        key="input_text_area"
    )
    
    # Estadísticas del texto
    if input_text:
        stats = get_text_stats(input_text)
        
        st.markdown("### 📊 Estadísticas del Texto")
        
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("Caracteres", f"{stats['characters']:,}")
            st.metric("Líneas", stats['lines'])
        
        with stats_col2:
            st.metric("IPs detectadas", stats['ips'])
            st.metric("Dominios", stats['domains'])
        
        with stats_col3:
            st.metric("Puertos", stats['ports'])
            detected_type = detect_data_type(input_text)
            st.info(f"**Tipo detectado:** {detected_type}")
    
    # Botón de análisis
    st.markdown("---")
    analyze_button = st.button(
        "🤖 Analizar con IA",
        type="primary",
        use_container_width=True,
        disabled=not api_configured
    )

# ============================================================================
# COLUMNA DERECHA - SALIDA
# ============================================================================

with col2:
    st.markdown("## 📊 Análisis de IA")
    
    if not api_configured:
        st.error("⚠️ Configura tu API key de OpenAI para comenzar")
        st.info("""
        **Pasos para configurar:**
        1. Obtén tu API key en https://platform.openai.com/api-keys
        2. Crea un archivo `.env` en la raíz del proyecto
        3. Agrega: `OPENAI_API_KEY=tu_api_key_aqui`
        4. Reinicia la aplicación
        """)
    
    elif not input_text:
        st.info("""
        👈 **Instrucciones:**
        
        1. Pega tus resultados de reconocimiento en el área de texto
        2. Ajusta la configuración en el panel lateral si es necesario
        3. Haz clic en "Analizar con IA"
        4. Espera el análisis detallado
        
        **Tipos de datos soportados:**
        - Escaneos Nmap
        - Consultas WHOIS
        - Registros DNS (nslookup, dig)
        - Encabezados HTTP
        - Resultados mixtos
        """)
    
    elif analyze_button:
        # Validar entrada
        is_valid, error_msg = validate_input_text(input_text)
        
        if not is_valid:
            st.error(format_warning_message(error_msg))
        else:
            # Inicializar analizador
            init_analyzer(selected_model)
            
            # Normalizar texto
            normalized_text = normalize_text(input_text)
            
            # Determinar tipo de datos
            final_data_type = data_type
            if data_type == "Mixto (Auto-detectar)":
                final_data_type = detect_data_type(normalized_text)
            
            # Mostrar spinner durante el análisis
            with st.spinner(f"🔄 Analizando con {selected_model_name}... Esto puede tomar unos segundos."):
                result = st.session_state.analyzer.analyze(
                    input_text=normalized_text,
                    data_type=final_data_type,
                    mode=mode,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            if result["success"]:
                # Mostrar resultado
                st.markdown(result["result"])
                
                # Mostrar metadatos
                with st.expander("📈 Información del Análisis"):
                    metadata = result["metadata"]
                    
                    st.markdown(f"""
                    **Modelo utilizado:** {metadata['model']}  
                    **Modo:** {metadata['mode'].title()}  
                    **Tipo de datos:** {metadata['data_type']}
                    """)
                    
                    st.markdown(format_tokens_usage(metadata['usage']))
                    
                    # Estimación de coste
                    cost_estimate = st.session_state.analyzer.estimate_cost(
                        metadata['usage']['prompt_tokens'],
                        metadata['usage']['completion_tokens']
                    )
                    st.markdown(format_cost_estimate(cost_estimate))
                
                # Guardar en historial
                st.session_state.analysis_history.append({
                    "timestamp": st.session_state.analyzer.get_timestamp() if hasattr(st.session_state.analyzer, 'get_timestamp') else "N/A",
                    "model": selected_model,
                    "mode": mode,
                    "data_type": final_data_type,
                    "result": result["result"]
                })
            
            else:
                st.error(format_error_message(Exception(result["error"]), "análisis de IA"))

# ============================================================================
# SECCIÓN INFERIOR - AVISO LEGAL
# ============================================================================

st.markdown("---")

st.warning("""
⚠️ **AVISO LEGAL Y ÉTICO**

Esta herramienta es **exclusivamente educativa** y debe utilizarse únicamente con fines de aprendizaje en ciberseguridad.

**✅ Uso permitido:**
- Análisis de tus propios sistemas
- Laboratorios de práctica autorizados
- Entornos de prueba con permiso explícito
- Fines educativos y de aprendizaje

**❌ Uso prohibido:**
- Reconocimiento no autorizado de sistemas de terceros
- Análisis de infraestructuras sin permiso
- Actividades ilegales o no éticas

**El usuario es el único responsable del uso de esta herramienta.** El uso indebido puede ser ilegal según las leyes de tu jurisdicción.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>AI Recon Mapper v1.0 | Desarrollado con ❤️ para la comunidad de ciberseguridad</p>
    <p>Powered by OpenAI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
