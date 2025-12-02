"""
Módulo de parsing y procesamiento de texto.
Funciones para limpiar, normalizar y detectar tipos de datos de reconocimiento.
"""

import re
from typing import Optional, Dict, List

def clean_text(text: str) -> str:
    """
    Limpia el texto de entrada eliminando caracteres innecesarios.
    
    Args:
        text: Texto a limpiar
    
    Returns:
        Texto limpio
    """
    if not text:
        return ""
    
    # Eliminar múltiples líneas en blanco
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    return text

def normalize_text(text: str) -> str:
    """
    Normaliza el texto para análisis consistente.
    
    Args:
        text: Texto a normalizar
    
    Returns:
        Texto normalizado
    """
    if not text:
        return ""
    
    # Limpiar primero
    text = clean_text(text)
    
    # Normalizar saltos de línea
    text = text.replace('\r\n', '\n')
    
    # Eliminar caracteres de control excepto \n y \t
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text

def detect_data_type(text: str) -> str:
    """
    Detecta el tipo de datos de reconocimiento basándose en patrones.
    
    Args:
        text: Texto a analizar
    
    Returns:
        Tipo detectado: "Nmap", "WHOIS", "DNS", "Mixto"
    """
    if not text:
        return "Desconocido"
    
    text_lower = text.lower()
    
    # Patrones de detección
    nmap_patterns = [
        r'nmap',
        r'starting nmap',
        r'port\s+state\s+service',
        r'\d+/tcp',
        r'\d+/udp',
        r'host is up'
    ]
    
    whois_patterns = [
        r'domain name:',
        r'registrar:',
        r'registrant',
        r'creation date:',
        r'expiry date:',
        r'name server:'
    ]
    
    dns_patterns = [
        r'nslookup',
        r'dig',
        r'answer section',
        r'authority section',
        r'a record',
        r'mx record',
        r'txt record'
    ]
    
    # Contar coincidencias
    nmap_count = sum(1 for pattern in nmap_patterns if re.search(pattern, text_lower))
    whois_count = sum(1 for pattern in whois_patterns if re.search(pattern, text_lower))
    dns_count = sum(1 for pattern in dns_patterns if re.search(pattern, text_lower))
    
    # Determinar tipo
    counts = {
        "Nmap": nmap_count,
        "WHOIS": whois_count,
        "DNS": dns_count
    }
    
    max_count = max(counts.values())
    
    if max_count == 0:
        return "Mixto"
    
    # Si hay múltiples tipos con conteos similares
    high_counts = [k for k, v in counts.items() if v >= max_count * 0.7]
    
    if len(high_counts) > 1:
        return "Mixto"
    
    return max(counts, key=counts.get)

def extract_ips(text: str) -> List[str]:
    """
    Extrae direcciones IP del texto.
    
    Args:
        text: Texto a analizar
    
    Returns:
        Lista de IPs encontradas
    """
    # Patrón para IPv4
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    ips = re.findall(ipv4_pattern, text)
    
    # Filtrar IPs válidas (0-255 en cada octeto)
    valid_ips = []
    for ip in ips:
        octets = ip.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            valid_ips.append(ip)
    
    # Eliminar duplicados manteniendo orden
    return list(dict.fromkeys(valid_ips))

def extract_domains(text: str) -> List[str]:
    """
    Extrae dominios del texto.
    
    Args:
        text: Texto a analizar
    
    Returns:
        Lista de dominios encontrados
    """
    # Patrón para dominios
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    
    domains = re.findall(domain_pattern, text)
    
    # Eliminar duplicados manteniendo orden
    return list(dict.fromkeys(domains))

def extract_ports(text: str) -> List[int]:
    """
    Extrae números de puerto del texto.
    
    Args:
        text: Texto a analizar
    
    Returns:
        Lista de puertos encontrados
    """
    # Patrón para puertos (formato común: 80/tcp, 443/udp, etc.)
    port_pattern = r'\b(\d{1,5})/(?:tcp|udp)\b'
    
    ports = re.findall(port_pattern, text)
    
    # Convertir a int y filtrar puertos válidos (1-65535)
    valid_ports = [int(p) for p in ports if 1 <= int(p) <= 65535]
    
    # Eliminar duplicados y ordenar
    return sorted(list(set(valid_ports)))

def get_text_stats(text: str) -> Dict[str, int]:
    """
    Obtiene estadísticas básicas del texto.
    
    Args:
        text: Texto a analizar
    
    Returns:
        Diccionario con estadísticas
    """
    if not text:
        return {
            "characters": 0,
            "lines": 0,
            "words": 0,
            "ips": 0,
            "domains": 0,
            "ports": 0
        }
    
    return {
        "characters": len(text),
        "lines": len(text.split('\n')),
        "words": len(text.split()),
        "ips": len(extract_ips(text)),
        "domains": len(extract_domains(text)),
        "ports": len(extract_ports(text))
    }

def truncate_text(text: str, max_length: int = 10000) -> str:
    """
    Trunca el texto si excede la longitud máxima.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
    
    Returns:
        Texto truncado si es necesario
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "\n\n[... texto truncado ...]"
