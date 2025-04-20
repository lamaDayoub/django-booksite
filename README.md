"""
Here’s the polished and formatted `README.md` file based on the details you provided. You can copy and paste this directly into your project:

```markdown
# **Bookssite**

## **Description**
Bookssite is a Django-based backend API designed to allow users to manage their book collections. Users can:
- Sign up, verify their accounts via email, log in, and log out.
- Update their profile information, including first name, last name, and bio.
- Add books to the database and organize them into shelves like "Want to Read," "Reading," "Read," and "Favourite."
- Rate books when shelving them as "Read" or "Favourite."
- Search for books by title or author.
- Change or reset their passwords securely.

This is a backend-only project, and all API endpoints are documented using Swagger for easy testing and integration with any frontend framework.

---

## **Features**
- **User Authentication**: Secure user registration, email activation, and JWT-based authentication.
- **Profile Management**: Users can update their first name, last name, and bio.
- **Password Security**:
  - Password change functionality ensures users cannot reuse their last six passwords.
  - Password reset via email verification.
- **Book Management**:
  - List all books or filter by shelf status.
  - Add new books to the database if they don’t already exist.
  - Shelve books into predefined categories.
  - Rate books when shelved as "Read" or "Favourite."
- **Search Functionality**: Search for books by title or author.
- **Token Refresh**: API endpoint to refresh expired access tokens using a refresh token.

---

## **Technologies Used**
- **Backend Framework**: Django, Django REST Framework (DRF)
- **Database**: SQLite3
- **Authentication**: JSON Web Tokens (JWT)
  - Access Token: Expires in 1 hour.
  - Refresh Token: Expires in 7 days.
- **Caching**: LocMemCache (local memory caching).
- **Email Backend**: Console-based email backend for account activation and password reset (currently for development purposes).
- **API Documentation**: Swagger for detailed endpoint documentation and testing.
- **Password Validation**: Prevents reusing the last six passwords during password changes.

---

## **Installation and Setup**

### **Prerequisites**
- Python 3.12
- Pipenv (Install it globally if not already installed: `pip install pipenv`)

### **Steps**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lamaDayoub/django-booksite
   cd booksite
   ```

2. **Install Dependencies with Pipenv**:
   Use Pipenv to create a virtual environment and install all dependencies:
   ```bash
   pipenv install django
   ```

3. **Activate the Virtual Environment**:
   Activate the virtual environment created by Pipenv:
   ```bash
   pipenv shell
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and contact me to tell you what to write inside it.  
   My email: lama1e2dayoub@gmail.com

5. **Run Migrations**:
   Apply database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   Run the Django development server:
   ```bash
   python manage.py runserver
   ```

7. **Access the API Documentation**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/swagger/
   ```
   Use the "Authorize" button in the top-right corner to authenticate with a JWT token.  
   Use the access token that will be returned when you log in.

---

## **API Documentation**
All API endpoints are documented using Swagger. To test the API:
1. Navigate to the Swagger interface at `http://127.0.0.1:8000/swagger/`.
2. Click the "Authorize" button in the top-right corner.
3. Enter your JWT token in the format:
   ```
   Bearer <your_access_token>
   ```
4. Test endpoints directly from the Swagger interface.

### **Key Endpoints**
- **User Registration**:
  - `POST /users/signup/`
  - Description: Register a new user. An activation email will be sent to the user's email address (visible in the console).

- **Account Activation**:
  - `POST /users/auth/users/activate/`
  - Description: Activate a user account using the token received in the activation email.

- **Login**:
  - `POST /users/login/`
  - Description: Log in a user and receive an access token and refresh token.

- **Refresh Token**:
  - `POST /api/token/refresh/`
  - Description: Refresh an expired access token using a valid refresh token.

- **Profile Update**:
  - `PATCH /users/profile/`
  - Description: Update user profile information (first name, last name, bio).

- **Password Change**:
  - `POST /users/auth/change-password/`
  - Description: Change the user's password. Prevents reusing the last six passwords.

- **Password Reset**:
  - `POST /users/auth/users/reset-password`
  - Description: Request a password reset email (visible in the console).

- **Password Reset Confirm**:
  - `POST /users/auth/users/reset-password-confirm`
  - Description: Use the link in the email sent to you. You need the `uid` and `token`.

- **List Books**:
  - `GET /books/`
  - Description: List all books or filter by shelf status, title, or author.

- **Shelve a Book**:
  - `POST /books/shelve/`
  - Description: Add a book to a shelf. Requires the author, title, shelf name, and rating (if the shelf is "Read" or "Favourite").

- **Get Book Status**:
  - `GET /books/{id}/`
  - Description: Retrieve the title, author, and shelf status of a specific book.

---

## **Future Improvements**
- **Email Integration**: Replace the console-based email backend with a third-party service (e.g., SendGrid, Gmail SMTP) to send real verification emails.
- **Custom Shelves**: Allow users to create custom shelves in addition to the predefined ones.
- **Profile Picture Upload**: Enable users to upload a profile picture.
- **Advanced Caching**: Replace `LocMemCache` with a more robust caching solution like Redis or Memcached.
- **Recommendation System**: Implement a recommendation system based on user preferences and shelving history.

---

## **Contributing**
If you'd like to contribute to this project, feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss your ideas.

---

## **Contact**
For questions or support, feel free to reach out to me at:  
📧 **Email**: lama1e2dayoub@gmail.com

---



---


   ```
"""
