"""
EventFlow AI Package
"""

from .eventflow_ai import EventFlowAI
from .database import Database
from .prospector import Prospector
from .message_generator import MessageGenerator
from .qualifier import Qualifier
from .utils import Utils, ROICalculator

__version__ = "1.0.0"
__all__ = [
    'EventFlowAI',
    'Database',
    'Prospector',
    'MessageGenerator',
    'Qualifier',
    'Utils',
    'ROICalculator'
]
