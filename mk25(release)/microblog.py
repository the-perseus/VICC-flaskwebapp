from app import app, db
from app.models import User, Post, Logbooktable


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Logbooktable': Logbooktable}
#Logbooktable ergänzt um Logbuchdatenbank als Dictionary in der Flask Shell verfügbar zu machen