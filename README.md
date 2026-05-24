# VIBE - Community Rankings & Codex

VIBE is a modern, community-driven Django web application designed to curate pop
culture jargon, host tier lists (Rankings), and manage a community dictionary 
(Codex). It features robust Discord OAuth2 integration to gatekeep and validate 
users based on specific community guidelines.

This project serves as a technical showcase for a clean, secure, and production-
ready Django backend portfolio.


KEY FEATURES
--------------------------------------------------------------------------------
- Discord OAuth2 Authentication: Secure login flow integrated via Discord API.
- Gatekeeping System: Restricts features based on user validation hooks (e.g., 
  checking against a specific Discord Guild/Server ID).
- Dynamic Content Suggestion: Authenticated users can propose new characters 
  for tier rankings and new terms for the Codex.
- White-Label Architecture: Highly flexible configuration via environment 
  variables (.env) to instantly rebrand names, tiers, and security IDs.
- Modern UI: Fully responsive, cyberpunk/dark-themed frontend crafted with 
  Tailwind CSS and interactive vanilla JavaScript components.


INSTALLATION & LOCAL SETUP
--------------------------------------------------------------------------------
1. Clone the repository:
   git clone https://github.com/berkecuhadar/VIBE.git
   cd VIBE

2. Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac

3. Install dependencies:
   pip install -r requirements.txt

4. Configure environment variables:
   Rename `.env.example` to `.env` in the root directory and fill it.

5. Run database migrations:
   python manage.py makemigrations
   python manage.py migrate

6. Seed mock data (Optional):
   python manage.py import_characters

7. Create a superuser account to access the admin panel:
   python manage.py createsuperuser

8. Start the development server:
   python manage.py runserver


DISCORD OAUTH CONFIGURATION (CRITICAL STEP)
--------------------------------------------------------------------------------
To make the Discord Login flow fully functional in your local environment, you 
must link your Discord App credentials through the Django Admin Panel:

1. Navigate to the admin panel at http://127.0.0.1:8000/admin/ and log in using 
   the superuser credentials you created in step 7.
2. Under the "Sites" section, click on "Sites" and ensure your domain is 
   properly set (e.g., Change "example.com" to "127.0.0.1:8000" for local test).
3. Scroll down to the "Social Accounts" section and click on "Social applications".
4. Click "Add Social Application" and fill in the fields exactly as follows:
   - Provider: Select "Discord"
   - Name: Discord Auth
   - Client id: [Your Discord Developer Portal Client ID]
   - Secret key: [Your Discord Developer Portal Client Secret]
   - Sites: Choose "127.0.0.1:8000" from the list and move it to chosen sites.
5. Save the configuration. 

Now, the Discord connect/disconnect flow will seamlessly work via the frontend.


DISCLAIMER
--------------------------------------------------------------------------------
All analytical descriptions, rankings, and user submissions on this platform 
are strictly generated for entertainment, parody, and satirical purposes. This 
application does not intend to defame, infringe, or insult any real-world 
individuals, institutions, or intellectual properties.

Developer: BERKE
