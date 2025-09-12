"""
Pacote core do ChatBot UFCA.
Importa classes principais para facilitar importações externas.
"""

from .chatbot import ChatBot
from .historico import Historico
from .aprendizado import Aprendizado
from .personalidade import Personalidade
from .estatisticas import Estatisticas

__all__ = ["ChatBot", "Historico", "Aprendizado", "Personalidade", "Estatisticas"]
