# Password-Manager
### Video Demo:  <URL HERE>
### Description:
This Web Application is a password manager built using Python, Flask and SQLite3.

#### Overview
I opted to use Python because it is the language I am most comfortable with. I chose Flask and SQLite3 because even though I am more experienced with other tools they were the ones covered in the course and I wanted to challenge myself to build something using only things covered in the course.

#### CSS
Design and CSS wise, I mainly used Boostrap CSS Framework but used so custom CSS also, to shape elements to my liking.

#### Features:
 - Register an account. Details are saved to SQLite3 database and password is encrypted using werkzeug.security Python library.
 - Log in to your account. Queries the database to see if your account exists and then checks that password is correct.
 - Main page displays all users saved accounts.
 - Option to add another account. User enters a website name, an email and a username for the account, the password manager generates a super strong password, encrypts it using the Fernet Python library and stores it in the database.

#### 