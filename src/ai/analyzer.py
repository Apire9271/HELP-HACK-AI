"""
Módulo de análisis con IA para resultados de reconocimiento.
Gestiona la comunicación con OpenAI y el procesamiento de respuestas.
"""

from openai import OpenAI
import os
from typing import Optional, Dict, Any
from .prompts import get_system_prompt, get_analysis_prompt

class ReconAnalyzer:
    """
    Analizador de reconocimiento usando IA.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Inicializa el analizador.
        
        Args:
            api_key: API key de OpenAI (opcional, usa variable de entorno si no se proporciona)
            model: Modelo de OpenAI a utilizar
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_configured(self) -> bool:
        """
        Verifica si el analizador está correctamente configurado.
        
        Returns:
            True si tiene API key configurada
        """
        return self.client is not None
    
    def analyze(
        self,
        input_text: str,
        data_type: str = "Mixto",
        mode: str = "junior",
        temperature: float = 0.7,
        max_tokens: int = 2500
    ) -> Dict[str, Any]:
        """
        Analiza los datos de reconocimiento usando IA.
        
        Args:
            input_text: Texto con resultados de reconocimiento
            data_type: Tipo de datos ("Mixto", "Nmap", "WHOIS/DNS")
            mode: Modo de análisis ("junior" o "expert")
            temperature: Temperatura del modelo (0.0-1.0)
            max_tokens: Máximo de tokens en la respuesta
        
        Returns:
            Diccionario con el resultado del análisis y metadatos
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "API key de OpenAI no configurada",
                "result": None
            }
        
        if not input_text or not input_text.strip():
            return {
                "success": False,
                "error": "No se proporcionó texto para analizar",
                "result": None
            }
        
        try:
            # Construir prompts
            system_prompt = get_system_prompt(mode)
            user_prompt = get_analysis_prompt(input_text, data_type, mode)
            
            # Llamar a la API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extraer resultado
            analysis_result = response.choices[0].message.content
            
            # Metadatos de uso
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            return {
                "success": True,
                "error": None,
                "result": analysis_result,
                "metadata": {
                    "model": self.model,
                    "mode": mode,
                    "data_type": data_type,
                    "usage": usage
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al analizar: {str(e)}",
                "result": None
            }
    
    def set_model(self, model: str):
        """
        Cambia el modelo de OpenAI a utilizar.
        
        Args:
            model: Nombre del modelo (ej: "gpt-4o-mini", "gpt-4o")
        """
        self.model = model
    
    def get_available_models(self) -> list:
        """
        Retorna lista de modelos disponibles recomendados.
        
        Returns:
            Lista de nombres de modelos
        """
        return [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
    
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> Dict[str, float]:
        """
        Estima el coste aproximado de una llamada.
        
        Args:
            prompt_tokens: Tokens del prompt
            completion_tokens: Tokens de la respuesta
        
        Returns:
            Diccionario con estimación de coste
        """
        # Precios aproximados (actualizar según pricing de OpenAI)
        pricing = {
            "gpt-4o-mini": {
                "input": 0.150 / 1_000_000,  # $0.150 por 1M tokens
                "output": 0.600 / 1_000_000   # $0.600 por 1M tokens
            },
            "gpt-4o": {
                "input": 2.50 / 1_000_000,
                "output": 10.00 / 1_000_000
            }
        }
        
        model_pricing = pricing.get(self.model, pricing["gpt-4o-mini"])
        
        input_cost = prompt_tokens * model_pricing["input"]
        output_cost = completion_tokens * model_pricing["output"]
        total_cost = input_cost + output_cost
        
        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
            "currency": "USD"
        }


# Función de conveniencia para uso rápido
def quick_analyze(
    input_text: str,
    data_type: str = "Mixto",
    mode: str = "junior",
    model: str = "gpt-4o-mini"
) -> str:
    """
    Función de conveniencia para análisis rápido.
    
    Args:
        input_text: Texto a analizar
        data_type: Tipo de datos
        mode: Modo de análisis
        model: Modelo a utilizar
    
    Returns:
        Resultado del análisis como string
    """
    analyzer = ReconAnalyzer(model=model)
    result = analyzer.analyze(input_text, data_type, mode)
    
    if result["success"]:
        return result["result"]
    else:
        return f"❌ Error: {result['error']}"
