#!/usr/bin/env python3

from app import create_app

# Create the Flask app
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
