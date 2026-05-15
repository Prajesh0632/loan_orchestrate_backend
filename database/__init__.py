"""Database module for Firebase configuration and utilities."""
from .firebase import init_firebase, get_db

__all__ = ["init_firebase", "get_db"]