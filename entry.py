from flaskr import create_app
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 5001)

app = create_app()

if __name__=='__main__':
    app.run(port=PORT, host="0.0.0.0")