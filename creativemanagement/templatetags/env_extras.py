from django import template
import os
from dotenv import load_dotenv
load_dotenv()

register = template.Library()


@register.filter
def get_env_var(key):
    return os.getenv(key)

