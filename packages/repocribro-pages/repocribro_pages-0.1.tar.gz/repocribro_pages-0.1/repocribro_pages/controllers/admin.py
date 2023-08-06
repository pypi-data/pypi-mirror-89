import flask

from repocribro.security import permissions

from repocribro_pages.models import Page


#: Pages public controller blueprint
admin_pages = flask.Blueprint('admin-pages', __name__, url_prefix='/admin-pages')

_page_props_defaults = {
    'title': '',
    'slug': '',
    'content': '',
    'custom_css': '',
    'custom_js': '',
    'parent_page_id': -1
}


def make_page_from_dict(dct, page=None):
    page = page or Page()
    for name, value in _page_props_defaults.items():
        setattr(page, name, dct.get(name, value))
    return page


def make_dict_from_page(page):
    return {name: getattr(page, name, _page_props_defaults[name])
            for name in _page_props_defaults.keys()}


@admin_pages.route('/create', methods=['GET'])
@permissions.roles.admin.require(404)
def create_page():
    db = flask.current_app.container.get('db')

    page = make_page_from_dict(flask.request.args)
    pages = db.session.query(Page).all()
    return flask.render_template('admin/form.html', page=page, pages=pages,
                                 form_title='Create new page', form_method='POST',
                                 form_action=flask.url_for('admin-pages.create_page'))


@admin_pages.route('/create', methods=['POST'])
@permissions.roles.admin.require(404)
def create_page_post():
    page = make_page_from_dict(flask.request.form)

    if page.slug == '' or page.title == '':
        flask.flash('Slug and title cannot be empty', 'danger')
        return flask.redirect(
            flask.url_for('admin-pages.create_page',
                          **make_dict_from_page(page))
        )

    db = flask.current_app.container.get('db')
    try:
        db.session.add(page)
        db.session.commit()
    except Exception:
        flask.flash('Couldn\'t create such page', 'danger')
        db.session.rollback()
        return flask.redirect(
            flask.url_for('admin-pages.create_page',
                          **make_dict_from_page(page))
        )

    flask.flash('Page created', 'success')
    return flask.redirect(
        flask.url_for('pages.show_page', slug=page.slug)
    )


@admin_pages.route('/<slug>/edit', methods=['GET'])
@permissions.roles.admin.require(404)
def edit_page(slug):
    db = flask.current_app.container.get('db')
    page = db.session.query(Page).filter_by(slug=slug).first()
    if page is None:
        flask.abort(404)
    pages = db.session.query(Page).all()
    return flask.render_template('admin/form.html', page=page,
                                 form_title='Edit page', pages=pages, form_method='POST',
                                 form_action=flask.url_for('admin-pages.edit_page_put', slug=slug))


@admin_pages.route('/<slug>/edit', methods=['PUT', 'POST'])
@permissions.roles.admin.require(404)
def edit_page_put(slug):
    db = flask.current_app.container.get('db')
    page = db.session.query(Page).filter_by(slug=slug).first()
    if page is None:
        flask.abort(404)
    page = make_page_from_dict(flask.request.form, page)
    try:
        db.session.commit()
    except Exception:
        flask.flash('Couldn\'t edit such page', 'danger')
        db.session.rollback()
        return flask.redirect(
            flask.url_for('admin-pages.edit_page',
                          **make_dict_from_page(page))
        )
    return flask.redirect(
        flask.url_for('pages.show_page', slug=slug)
    )


@admin_pages.route('/<slug>/delete')
@permissions.roles.admin.require(404)
def delete_page(slug):
    db = flask.current_app.container.get('db')

    page = db.session.query(Page).filter_by(slug=slug).first()
    if page is None:
        flask.abort(404)
    db.session.delete(page)
    db.session.commit()
    flask.flash('User account {} with the all related data'
                ' has been deleted'.format(page.slug), 'success')
    return flask.redirect(
        flask.url_for('admin.index', tab='pages')
    )
