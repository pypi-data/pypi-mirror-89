import sqlalchemy
import datetime


from repocribro.database import db
from repocribro.models import SearchableMixin, SerializableMixin


class Page(db.Model, SearchableMixin, SerializableMixin):
    """Release from GitHub"""
    __tablename__ = 'Page'
    __searchable__ = ['slug', 'title', 'content']
    __serializable__ = ['id', 'slug', 'title', 'content', 'custom_css',
                        'custom_js', 'privilege', 'parent_page_id']
    #: Unique identifier of the page
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    #: URL slug for the page
    slug = sqlalchemy.Column(sqlalchemy.String(100), unique=True)
    #: Title of the page
    title = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: HTML page contents
    content = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: Custom CSS for the page
    custom_css = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: Custom JS to include while showing the page
    custom_js = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: Privilege to see the page
    privilege = sqlalchemy.Column(sqlalchemy.String(60), nullable=True)
    #: ID of the repository where push belongs to
    parent_page_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('Page.id')
    )
    #: Parent page
    parent_page = sqlalchemy.orm.relationship(
        'Page', remote_side=[id]
    )
    #: Child pages
    child_pages = sqlalchemy.orm.relationship(
        'Page', backref=sqlalchemy.orm.backref('parent', remote_side=[id])
    )

    #: Timestamp when page was created
    created_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    #: Timestamp when page was last updated
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now,
                                   onupdate=datetime.datetime.now)

    def __repr__(self):
        """Standard string representation of DB object
        :return: Unique string representation
        :rtype: str
        """
        return '<Page {} (#{})>'.format(self.slug, self.id)
