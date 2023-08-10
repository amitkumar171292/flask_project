import sqlite3

class DbConfig():
    """This class will help in initializing the DB"""

    def __init__(self, app):
        app.config['DATABASE'] = 'macube.db'

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(app.config['DATABASE'])
            db.row_factory = sqlite3.Row
        return db

    def init_db():
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    @app.cli.command('initdb')
    def initdb_command():
        """Initialize the database."""
        init_db()
        print('Initialized the database.')
