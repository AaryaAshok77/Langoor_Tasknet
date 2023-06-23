1. HTML Templates (front-end):
   > login.html: A form for user login with email and password inputs.
   > signup.html: A form for creating a new user account with email, password, and role selection.
   > dashboard.html: Displaying the project and task dashboard based on the user's role.
   > project_creation.html: A form for creating a new project with fields like name, timeline, budget, and description.
   - project_details.html: Displaying the details of a specific project, including the short description.
   - open_summary_forum.html: A form for entering a project description and displaying similar ongoing projects.
   ? task_creator.html: Displaying the task list, allowing users to create, edit, and delete tasks, attach documents, and add comments.
   > kanban.html: Displaying the Kanban board for personal and project tasks, allowing users to move tasks between columns.

2. CSS Styles (styling the HTML templates):
   - Define styles in a separate CSS file or use inline styles within the HTML templates.

3. Django Models (back-end):
   > User model: Define a custom User model with fields like email, password, and role.
   > Project model: Define a model for storing project information, including fields like name, timeline, budget, and description.
   > Task model: Define a model for storing task information, including fields like name, description, due date, status, and attachments.

4. Django Views (handling HTTP requests):
    Implement views for login, signup, dashboard, project creation, project details, open summary forum, task creator, and kanban.
   - Define view functions to handle form submissions, database operations, and rendering the appropriate templates.

5. Django Templates (rendering HTML):
   - Create Django templates for each HTML file and use template tags to dynamically display data from the backend.
   - Use template inheritance to define a base template and extend it in other templates.


admin: administrator
dir: directorlogin
prod: productownerlogin


login with email instead of username
fix the task creation screen (jquery, static)
add completed option to task/project details, project can only be deleted if it has no tasks associated to it
add the logout button
