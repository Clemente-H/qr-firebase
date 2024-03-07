import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from st_pages import Page, add_page_title, show_pages

# cred = credentials.Certificate('../firebaseCredentials.json')
# print(cred)
# firebase_admin.initialize_app(cred)
# db = firestore.client()



"## Declaring the pages in your app:"

show_pages(
    [
        Page("./app.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("./registros.py", "Registros", ":books:"),
    ]
)

add_page_title()  # Optional method to add title and icon to current page