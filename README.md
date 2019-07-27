# spaced-learner
A spaced learning web app, based on the Leitner system of flashcards.


Deployment
 - Flask
 - Flask-WTF
 - Flask-SQLAlchemy

Implementation Timeline:
Milestone One: Get basic app working for one user
 - ~~Get basic tester working~~
 - ~~Implement the Leitener system for spaced repetition~~
 - ~~Switch internal logic from prototype mocks to objects~~
 
Milestone Two: Get Basic Login, DB capabilites
 - Add login, authentication, and multiple users
 - Save information about entries into database, and pull when needed
 - Refractor html; add basic template/ navbar for all pages
    - Switch from linking to pages to url_for's
 - Create user "hub" page


Milestone Three: Expand basic app for multiple users
 - Create page to create new entries
 - Create page to edit current entries
 - Implement "flashcard" type entries rather than just text entries
 - Create new feature; "Decks" of cards, with importing and exporting features
 - Create homepage to access decks
 - Create settings page to change basic features (how many displayed)
 - Begin deploying online
 
Milestone Four: Facelift
 - No specifics, but reform interface frontend
 - Add importing of flashcards from CSV
 