from .pages import pages
from .admin import admin_pages

all_blueprints = [pages, admin_pages]

__all__ = ['all_blueprints', 'pages', 'admin_pages']
