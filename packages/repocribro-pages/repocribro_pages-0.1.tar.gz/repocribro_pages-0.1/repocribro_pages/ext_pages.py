from repocribro.extending import Extension
from repocribro.extending.helpers import Badge, ViewTab

from repocribro_pages.models import Page


class RepocribroPages(Extension):
    #: Name of pages extension
    NAME = 'pages'
    #: Category of pages extension
    CATEGORY = 'basic'
    #: Author of pages extension
    AUTHOR = 'Marek Suchánek'
    #: GitHub URL of pages extension
    GH_URL = 'https://github.com/MarekSuchanek/repocribro-pages'
    #: Priority of pages extension
    PRIORITY = 10

    def view_admin_index_tabs(self, tabs_dict):
        """Prepare tabs for index view of admin controller
        :param tabs_dict: Target dictionary for tabs
        :type tabs_dict: dict of str: ``repocribro.extending.helpers.ViewTab``
        """
        pages = self.db.session.query(Page).all()

        tabs_dict['pages'] = ViewTab(
            'pages', 'Pages', 0,
            self.app.jinja_env.get_template('admin/tabs/pages.html').render(
                pages=pages
            ),
            octicon='browser',
            badge=Badge(len(pages))
        )

    @staticmethod
    def provide_blueprints():
        from .controllers import all_blueprints
        return all_blueprints

    @staticmethod
    def provide_template_loader():
        from jinja2 import PackageLoader
        return PackageLoader('repocribro_pages', 'templates')

    @staticmethod
    def provide_models():
        return [Page]

    @staticmethod
    def provide_dropdown_menu_items():
        return {
            'pages.list': 'Pages',
        }

def make_extension(*args, **kwargs):
    return RepocribroPages(*args, **kwargs)
