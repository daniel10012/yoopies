from app import app, db
from app import Salary


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Salary': Salary}