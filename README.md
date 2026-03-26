## social network
A social network Django web application for making/liking posts and following users
### Demo
A live demo video is available at: https://www.youtube.com/watch?v=SvSnZ-YqaRs
### Installation
To run the project locally:
1. Make sure that Python is installed on your system.
2. Install the Django framework for Python.
3. Clone the repository.
4. From within the repository directory execute the following commands:
   - `python manage.py migrate` to synchronize the models with the database schema.
   - `python manage.py runserver` to run the local server.

### Tech Stack
- Back-end: Python (Django) 
- Front-end: HTML, pure CSS, Bootstrap, JavaScript.
- Database: SQLite
### Features
The application offers the following core features:
- **New Post**: Users who are signed in are able to submit a new text-based post.
- **All Posts**: The "All Posts" link in the navigation bar takes the user to a page where they can see all posts from all users ordered by latest first. Each post includes the post's content, "likes", date and time of creation and the poster's username.
- **Profile Page**: Clicking on a username loads that user's profile page, where all that user's posts are displayed. Also, every signed in user except the profile owner can click the follow/unfollow button to follow/unfollow that user. 
- **Following**: The "Following" link in the navigation bar takes the user to a page where they see all posts made by users that they follow.
- **Pagination**: On any page that includes posts, 10 posts are displayed per page, including navigation buttons.
- **Edit Post**: Users can click an "Edit" button on any of their posts to edit that post's content
- **"Like" & "Unlike"**: Users can click a "like" button on any post to toggle whether or not they "like" that post

### What I implemented
The distribution code is available at: https://cdn.cs50.net/web/2020/spring/projects/4/network.zip (accessed 25 March 2026). It includes: the login, logout and register routes as well as a basic HTML template for a navigation bar.

I studied, understood them and then completed the rest of the application. This includes:

- **Routes**: All the other routes (6), including the API routes.
- **JavaScript**: The entirety of the JavaScript code ,including the asynchronous API calls which achieve the "like" and edit post features
- **Models & ModelForms**: All of the Django Models and ModelForms for database handling
- **HTML Templates**: I substantially extended the HTML templates.
- **CSS styles**: The entirety of the CSS, including pure CSS and Bootstrap tools & utilities
