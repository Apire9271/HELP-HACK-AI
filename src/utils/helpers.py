"""
Módulo de funciones auxiliares y utilidades generales.
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime

def format_error_message(error: Exception, context: str = "") -> str:
    """
    Formatea un mensaje de error de manera consistente.
    
    Args:
        error: Excepción capturada
        context: Contexto adicional del error
    
    Returns:
        Mensaje de error formateado
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"❌ **Error en {context}**\n\n**Tipo:** {error_type}\n**Detalle:** {error_msg}"
    else:
        return f"❌ **Error**\n\n**Tipo:** {error_type}\n**Detalle:** {error_msg}"

def format_success_message(message: str) -> str:
    """
    Formatea un mensaje de éxito.
    
    Args:
        message: Mensaje a formatear
    
    Returns:
        Mensaje formateado
    """
    return f"✅ **{message}**"

def format_warning_message(message: str) -> str:
    """
    Formatea un mensaje de advertencia.
    
    Args:
        message: Mensaje a formatear
    
    Returns:
        Mensaje formateado
    """
    return f"⚠️ **{message}**"

def format_info_message(message: str) -> str:
    """
    Formatea un mensaje informativo.
    
    Args:
        message: Mensaje a formatear
    
    Returns:
        Mensaje formateado
    """
    return f"ℹ️ **{message}**"

def check_api_key() -> tuple[bool, Optional[str]]:
    """
    Verifica si la API key de OpenAI está configurada.
    
    Returns:
        Tupla (está_configurada, mensaje)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return False, "No se ha detectado la variable de entorno OPENAI_API_KEY"
    
    if len(api_key) < 20:
        return False, "La API key parece ser inválida (muy corta)"
    
    return True, None

def format_tokens_usage(usage: Dict[str, int]) -> str:
    """
    Formatea información de uso de tokens.
    
    Args:
        usage: Diccionario con información de tokens
    
    Returns:
        String formateado
    """
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    
    return f"""
**Uso de Tokens:**
- Entrada: {prompt_tokens:,} tokens
- Salida: {completion_tokens:,} tokens
- Total: {total_tokens:,} tokens
"""

def format_cost_estimate(cost_data: Dict[str, float]) -> str:
    """
    Formatea estimación de coste.
    
    Args:
        cost_data: Diccionario con información de coste
    
    Returns:
        String formateado
    """
    total_cost = cost_data.get("total_cost", 0)
    currency = cost_data.get("currency", "USD")
    
    return f"💰 Coste estimado: ${total_cost:.6f} {currency}"

def get_timestamp() -> str:
    """
    Obtiene timestamp actual formateado.
    
    Returns:
        Timestamp como string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_input_text(text: str, min_length: int = 10, max_length: int = 50000) -> tuple[bool, Optional[str]]:
    """
    Valida el texto de entrada.
    
    Args:
        text: Texto a validar
        min_length: Longitud mínima
        max_length: Longitud máxima
    
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not text or not text.strip():
        return False, "El texto está vacío"
    
    text_length = len(text)
    
    if text_length < min_length:
        return False, f"El texto es muy corto (mínimo {min_length} caracteres)"
    
    if text_length > max_length:
        return False, f"El texto es muy largo (máximo {max_length} caracteres)"
    
    return True, None

def create_markdown_section(title: str, content: str, level: int = 2) -> str:
    """
    Crea una sección de Markdown formateada.
    
    Args:
        title: Título de la sección
        content: Contenido
        level: Nivel de encabezado (1-6)
    
    Returns:
        Sección formateada
    """
    header = "#" * level
    return f"{header} {title}\n\n{content}\n"

def safe_get_env(key: str, default: str = "") -> str:
    """
    Obtiene una variable de entorno de manera segura.
    
    Args:
        key: Nombre de la variable
        default: Valor por defecto
    
    Returns:
        Valor de la variable o default
    """
    return os.getenv(key, default)

def format_file_size(size_bytes: int) -> str:
    """
    Formatea tamaño de archivo en formato legible.
    
    Args:
        size_bytes: Tamaño en bytes
    
    Returns:
        Tamaño formateado (KB, MB, etc.)
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def create_divider(char: str = "-", length: int = 50) -> str:
    """
    Crea un divisor visual.
    
    Args:
        char: Carácter a usar
        length: Longitud del divisor
    
    Returns:
        String divisor
    """
    return char * length
