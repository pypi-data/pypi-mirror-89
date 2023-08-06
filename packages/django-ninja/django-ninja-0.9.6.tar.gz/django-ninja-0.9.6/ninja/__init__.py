"""Django Ninja - Fast Django REST framework"""

__version__ = "0.9.6"

from ninja.main import NinjaAPI
from ninja.params import Query, Path, Header, Cookie, Body, Form
from ninja.router import Router
from ninja.schema import Schema
