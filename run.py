from app import create_app
from app.models import db

app = create_app()

@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
