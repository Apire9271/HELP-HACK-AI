"""
Módulo de prompts para el análisis de reconocimiento con IA.
Contiene plantillas de prompts para diferentes modos y niveles de experiencia.
"""

# Prompt del sistema base
SYSTEM_ROLE = """Eres un experto en ciberseguridad y hacking ético con amplia experiencia en:
- Análisis de reconocimiento (Nmap, WHOIS, DNS, Shodan, etc.)
- Identificación de vulnerabilidades
- Arquitecturas de red y sistemas
- Mejores prácticas de seguridad

Tu objetivo es ayudar a profesionales y estudiantes a comprender los resultados de reconocimiento
de manera educativa, clara y profesional."""

# Prompt para modo Junior (principiantes)
JUNIOR_MODE_INSTRUCTIONS = """
MODO: JUNIOR (Principiante)

Adapta tu respuesta para alguien que está aprendiendo ciberseguridad:
- Explica conceptos básicos cuando sea necesario
- Define términos técnicos
- Proporciona contexto adicional
- Usa analogías cuando sea apropiado
- Incluye recursos de aprendizaje recomendados
- Sé más detallado en las explicaciones
"""

# Prompt para modo Experto (profesionales)
EXPERT_MODE_INSTRUCTIONS = """
MODO: EXPERTO (Profesional)

Adapta tu respuesta para un profesional de ciberseguridad:
- Sé conciso y directo
- Asume conocimiento técnico previo
- Enfócate en hallazgos críticos
- Proporciona análisis técnico profundo
- Incluye referencias a CVEs cuando sea relevante
- Sugiere herramientas avanzadas de análisis
"""

# Plantilla de análisis estructurado
ANALYSIS_TEMPLATE = """
Analiza los siguientes datos de reconocimiento y proporciona un informe estructurado.

DATOS A ANALIZAR:
```
{input_text}
```

TIPO DE DATOS: {data_type}

FORMATO DE SALIDA OBLIGATORIO (Markdown):

## 📋 Resumen Ejecutivo
[Breve descripción de los hallazgos más importantes]

## 🎯 Activos Detectados
### IPs Identificadas
[Lista de direcciones IP con contexto]

### Dominios y Subdominios
[Dominios y subdominios encontrados]

### Otros Activos
[Cualquier otro activo relevante]

## 🔧 Servicios y Tecnologías
### Puertos Abiertos
[Lista de puertos con servicios asociados]

### Tecnologías Detectadas
[Servidores web, frameworks, CMS, etc.]

### Versiones de Software
[Versiones específicas identificadas]

## ⚠️ Análisis de Riesgos (Educativo)
### Riesgos Potenciales
[Posibles vulnerabilidades o configuraciones inseguras]

### Nivel de Exposición
[Evaluación del nivel de exposición]

### Contexto de Seguridad
[Explicación educativa de por qué estos hallazgos son relevantes]

## 💡 Recomendaciones
### Acciones Sugeridas
[Recomendaciones generales de seguridad]

### Recursos de Aprendizaje
[Temas para estudiar y profundizar]

### Próximos Pasos
[Qué hacer con esta información]

---

RESTRICCIONES IMPORTANTES:
- NO proporciones comandos de explotación
- NO incluyas instrucciones para realizar ataques
- Mantén un enfoque educativo y ético
- Si detectas información sensible, recomienda protegerla
- Enfócate en la comprensión, no en la explotación
"""

# Plantilla para análisis de Nmap específico
NMAP_ANALYSIS_TEMPLATE = """
Analiza este escaneo de Nmap con enfoque en:
- Puertos abiertos y servicios
- Versiones de software detectadas
- Scripts NSE ejecutados y sus resultados
- Fingerprinting del sistema operativo
- Posibles vectores de ataque (educativo)
"""

# Plantilla para análisis de WHOIS/DNS
WHOIS_DNS_TEMPLATE = """
Analiza esta información de WHOIS/DNS con enfoque en:
- Información del dominio y registrante
- Servidores de nombres
- Registros DNS (A, MX, TXT, etc.)
- Fechas de registro y expiración
- Información de contacto y privacidad
"""

# Plantilla para análisis mixto
MIXED_ANALYSIS_TEMPLATE = """
Analiza estos datos de reconocimiento mixto identificando:
- Tipo de cada sección de datos
- Correlación entre diferentes fuentes
- Panorama completo del objetivo
- Hallazgos cruzados y patrones
"""

def get_system_prompt(mode: str = "junior") -> str:
    """
    Construye el prompt del sistema según el modo seleccionado.
    
    Args:
        mode: "junior" o "expert"
    
    Returns:
        Prompt del sistema completo
    """
    base_prompt = SYSTEM_ROLE
    
    if mode.lower() == "expert":
        return f"{base_prompt}\n\n{EXPERT_MODE_INSTRUCTIONS}"
    else:
        return f"{base_prompt}\n\n{JUNIOR_MODE_INSTRUCTIONS}"

def get_analysis_prompt(input_text: str, data_type: str = "Mixto", mode: str = "junior") -> str:
    """
    Construye el prompt de análisis completo.
    
    Args:
        input_text: Texto a analizar
        data_type: Tipo de datos ("Mixto", "Nmap", "WHOIS/DNS")
        mode: Modo de análisis ("junior" o "expert")
    
    Returns:
        Prompt completo para el análisis
    """
    # Seleccionar plantilla adicional según el tipo
    additional_context = ""
    if "nmap" in data_type.lower():
        additional_context = NMAP_ANALYSIS_TEMPLATE
    elif "whois" in data_type.lower() or "dns" in data_type.lower():
        additional_context = WHOIS_DNS_TEMPLATE
    else:
        additional_context = MIXED_ANALYSIS_TEMPLATE
    
    # Construir prompt completo
    base_analysis = ANALYSIS_TEMPLATE.format(
        input_text=input_text,
        data_type=data_type
    )
    
    return f"{additional_context}\n\n{base_analysis}"

def get_prompts_info() -> dict:
    """
    Retorna información sobre los prompts disponibles.
    
    Returns:
        Diccionario con información de los prompts
    """
    return {
        "modes": ["junior", "expert"],
        "data_types": ["Mixto", "Nmap", "WHOIS/DNS"],
        "templates": {
            "system": "SYSTEM_ROLE",
            "analysis": "ANALYSIS_TEMPLATE",
            "nmap": "NMAP_ANALYSIS_TEMPLATE",
            "whois_dns": "WHOIS_DNS_TEMPLATE",
            "mixed": "MIXED_ANALYSIS_TEMPLATE"
        }
    }
