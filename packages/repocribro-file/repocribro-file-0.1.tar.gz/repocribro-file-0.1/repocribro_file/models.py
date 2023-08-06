import datetime
import sqlalchemy

from repocribro.database import db
from repocribro.models import SearchableMixin, SerializableMixin,\
                              Repository


class FileDescriptor(db.Model, SearchableMixin, SerializableMixin):
    """Descriptor of kind of files with info"""
    # TODO: allow some schemas for loading and processing files
    __tablename__ = 'FileDescriptor'
    __searchable__ = ['filename', 'description', 'filetype']
    __serializable__ = ['id', 'filename', 'description', 'filetype']
    #: Unique identifier of the page
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    #: Filename (including path) for the file to be retrieved from repo
    filename = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: Custom description
    description = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: Specification of the file type for further processing
    filetype = sqlalchemy.Column(sqlalchemy.String(100))
    #: Instances of this file type
    instances = sqlalchemy.orm.relationship(
        'FileInstance', back_populates='descriptor',
        cascade='all, delete-orphan'
    )

    filetypes = ['unspecified', 'YAML', 'JSON']

    def __init__(self, filename, description, filetype='unspecified'):
        self.filename = filename
        self.description = description
        self.filetype = filetype

    def __repr__(self):
        """Standard string representation of DB object

        :return: Unique string representation
        :rtype: str
        """
        return f'<FileDescriptor #{self.id}>'


class FileInstance(db.Model, SearchableMixin, SerializableMixin):
    """Instance of kind of files with info"""
    __tablename__ = 'FileInstance'
    __searchable__ = ['content']
    __serializable__ = ['id', 'content', 'timestamp', 'descriptor_id',
                        'repository_id']
    #: Unique identifier of the page
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    #: Contents of the file instance
    content = sqlalchemy.Column(sqlalchemy.UnicodeText)
    #: When this record was retrieved from repository
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(),
                                  default=datetime.datetime.utcnow)
    #: ID of the file descriptor for this file instance
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('FileDescriptor.id')
    )
    #: File descriptor for this file instance
    descriptor = sqlalchemy.orm.relationship(
        'FileDescriptor', back_populates='instances'
    )
    #: ID of the repository to which file belongs
    repository_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('Repository.id')
    )
    #: Repository to which file belongs
    repository = sqlalchemy.orm.relationship(
        'Repository', back_populates='files'
    )

    def __init__(self, content, repository_id, fd_id):
        self.content = content
        self.descriptor_id = fd_id
        self.repository_id = repository_id

    def __repr__(self):
        """Standard string representation of DB object

        :return: Unique string representation
        :rtype: str
        """
        return f'<FileInstance #{self.id}>'

    def update(self, content):
        self.content = content
        self.timestamp = datetime.datetime.utcnow()


Repository.files = sqlalchemy.orm.relationship(
    'FileInstance', back_populates='repository',
    cascade='all, delete-orphan'
)


all_models = [FileDescriptor, FileInstance]
