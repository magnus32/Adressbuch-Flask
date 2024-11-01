# Flask Adressbuch App

Diese Anwendung ist ein einfaches Adressbuch, das mit Flask erstellt wurde. Folgen Sie den unten stehenden Schritten, um die Anwendung zu installieren und auszuführen.

## Installation

1. **Repository klonen**  
   ```bash
   git clone https://github.com/yourusername/Adressbuch.git
   cd Adressbuch
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**  
   Configure your database settings in `config.py`.

5. **Run the migrations**  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Start the application**  
   ```bash
   flask run
   ```

## Usage

Navigate to `http://127.0.0.1:5000` in your browser to use the app.

