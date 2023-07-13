Project Objectives:
Tasknet aims to improve task management and collaboration within large-scale companies by providing a centralized platform for teams to organize, assign, and track tasks and projects. The goal is to reduce miscommunication, duplication of work, and increase visibility across different business groups. A key feature of Tasknet is the open forum that summarizes ongoing projects, allowing users to discover and potentially collaborate on similar projects.

 Features:
User registration and login functionality.
Project creation, editing, and deletion with fields like name, timeline, and description.
Task creation, editing, and deletion with fields like name, description, due date, and assigned user.
Simple Kanban board for visualizing project and task progress.
Chat functionality for members of a task to communicate and share updates.
User roles and permissions to ensure appropriate access levels.
Inbox for managing conversations and notifications.

Project Plan:
Requirement Gathering: Gather detailed requirements and specifications for the project, including user roles, functionality, and design.
Design and Architecture: Design the application architecture, database schema, and user interface. Create wireframes and mockups to visualize the design.
Tech Stack Selection: Choose appropriate technologies and frameworks for the project. Based on the requirements, select Django as the backend framework and HTML/CSS/JavaScript for the frontend.
Database Design: Design the database schema based on the defined models and their relationships.
Frontend Development: Develop the HTML templates and CSS styles based on the wireframes and mockups. Implement JavaScript functionality for interactive elements.
Backend Development: Implement the Django models, views, and templates to handle user authentication, project management, task management, chat functionality, and user roles.
Integration: Integrate the frontend and backend components. Test the integration to ensure seamless communication between the frontend and backend.
Testing: Develop a test plan to verify the functionality of the application. Write unit tests and integration tests to ensure the quality and reliability of the code.
Deployment: Choose a hosting stack and architecture for hosting the application. Deploy the application to an AWS EC2 instance with Nginx as the web server and Gunicorn as the application server.
Testing and Bug Fixing: Conduct thorough testing to identify and fix any bugs or issues in the application.
Documentation: Create comprehensive documentation for the project, including installation instructions, user guide, and API documentation.
User Acceptance Testing: Involve stakeholders and end users in the testing process to gather feedback and ensure that the application meets their requirements.
Deployment to Production: Deploy the application to the production environment, ensuring scalability, security, and performance.



Tech Stack:
Backend Framework: Django (Python)
Frontend: HTML, CSS, JS
Database: sqlite3
Hosting: AWS (Amazon Web Services)
Testing: Django testing framework, Selenium

Application Architecture:
The application follows a client-server architecture. The client-side consists of HTML templates and CSS styles rendered by Django views. The server-side includes Django models, views, and templates, which handle user requests, interact with the database, and generate dynamic HTML responses.

Code Explanation:
1. HTML Templates (front-end):
base.html: A html file that contains the base template that all the other templates are built on.
login.html: A form for user login with email and password inputs.
signup.html: A form for creating a new user account with email, password, and role selection.

board.html: Displaying the Kanban board for personal and project tasks, allowing users to move tasks between columns.
create_project.html: A form for creating a new project with fields like name, assigned to, timeline and description.
project_delete.html: Delete a project.
project_details.html: Displaying the details of a specific project, including the short description.
project_edit.htm: Displaying the edit page of a project.
project_list.html: Displays list of all projects.
create_task.html: A form for creating a new task with fields like name, assign to, timeline and description.
task_delete.html: Delete a task.
task_detail.html: Displaying the details of a specific project, including the short description.
task_edit.html: Displaying the edit page of a task.
task_list.html: Displaying the list of all tasks.
update_task_status.html: Update the tasks status in the Kannan board.

detail.html: Displays the chat.
Inbox.html:Acts as the inbox for all chats.
new.html: The template for a new chat.

2. Django Models (back-end):
CustomUser model: Define a custom User model with fields like email, password, and role.
Project model: Define a model for storing project information, including fields like name, description, start_date, end_date, creator, assigned_users and status.
Task model: Define a model for storing task information, including fields like project, title, description, created_at, created_by, assigned_to, status and due_date.
Conversation model: Define a model for storing conversation information including fields like task, members, modified at.
Comment model: Define a model for storing comment information including fields like conversation, content, file, sent at, created by.

3. Django Views (handling HTTP requests):
Implement views,
Login View:
Handles the GET request to render the login form template.
Handles the POST request to process the form submission, authenticate the user, and redirect them to the dashboard.
Signup View:
Handles the GET request to render the signup form template.
Handles the POST request to process the form submission, create a new user account, and redirect them to the login page.
Board View:
Handles the GET request to render the Kanban board template.
Retrieves the projects and tasks from the database and passes them to the template for rendering.
Project Creation View:
Handles the GET request to render the project creation form template.
Handles the POST request to process the form submission, create a new project in the database, and redirect to the project details page.
Project Details View:
Handles the GET request to render the project details template.
Retrieves the project details and related tasks from the database and passes them to the template for rendering.

Task Creator View:
Handles the GET request to render the task creation form template.
Handles the POST request to process the form submission, create a new task in the database, and redirect to the project details page.
etc…
Define view functions to handle form submissions, database operations, and rendering the appropriate templates.

4. Django Templates (rendering HTML):
Create Django templates for each HTML file and use template tags to dynamically display data from the backend.
Use template inheritance to define a base template and extend it in other templates.

Hosting Stack:
The application is hosted on AWS, leveraging services like EC2 for server hosting.

Hosting Architecture:
The application is deployed on an EC2 instance running a web server Nginx and Gunicorn as the application server.




Test Plan:
1. Unit Testing: Write unit tests for models, views, and any custom functions or utilities.
2. Integration Testing: Test the interaction between different components of the application.
3. User Interface Testing: Ensure that HTML templates render correctly and are responsive across devices.
4. User Acceptance Testing: Involve stakeholders and end users to test the application against the defined requirements and user stories.
5. Performance Testing: Test the application's performance under different load conditions using tools like JMeter or Gatling.
6. Security Testing: Conduct security testing to identify and fix vulnerabilities, including authentication, authorization, and data protection.

Summary:
The project aims to develop a project and task management web application using Django as the backend framework and HTML/CSS for the frontend. The application allows users to register, log in, create projects, manage tasks, and visualize project progress using a Kanban board. The tech stack includes Django, HTML, CSS, SQLlite, and the application is hosted on AWS. Thorough testing and documentation ensure the application's functionality, security, and performance.

dir: Katy Fernandez
po1: Yusuf Cameron
po2: Mariah Reid
d1: Neil Merritt
d2: Amber Gates
d3: Alexandra Estes
qa1: Rory Dixon
qa2: Chanelle Bean