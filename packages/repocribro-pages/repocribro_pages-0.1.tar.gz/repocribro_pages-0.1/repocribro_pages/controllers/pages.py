import flask
from repocribro_pages.models import Page

#: Pages public controller blueprint
pages = flask.Blueprint('pages', __name__, url_prefix='/pages')


# TODO: security?
@pages.route('/<slug>')
def show_page(slug):
    db = flask.current_app.container.get('db')
    page = db.session.query(Page).filter_by(slug=slug).first()
    if page is None:
        flask.abort(404)
    return flask.render_template('pages/page.html', page=page)


@pages.route('/')
def list():
    db = flask.current_app.container.get('db')
    pages = db.session.query(Page).all()
    return flask.render_template('pages/list.html', pages=pages)
