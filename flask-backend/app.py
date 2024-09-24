from app import create_app
from app.auth import init_oauth

app = create_app()

# Initialize OAuth
init_oauth(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
