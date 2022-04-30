<h1>Employee-Management</h1>

<h2>🔗 Topics</h2>

<ul>

<li><a href="#about">About</a></li>
<li><a href="#tools">Tools</a></li>
<li><a href="#db">Database</a></li>
<li><a href="#project">See the project</a></li>
<ul>
    <li><a href="#routes-for-frontend">Routes for frontend</a></li>
    <li><a href="#performance">Performance</a></li>
    <li><a href="#admin">Custom admin</a></li>
</ul>
<li><a href="#project-doc">Project instructions</a></li>
<ul>
    <li><a href="#how-to-start">How to start</a></li>
    <li><a href="#how-to-use">How to use</a></li>
    <li><a href="#routes">Routes</a></li>
    <li><a href="#serializer">Serializer</a></li>
    <li><a href="#tests">Tests</a></li>
</ul>

</ul>
<br>

<h2 id="about">📖 About</h2>

<p>API for managing employees and for use with some frontend framework</p>

<br>
<h2 id="tools">🛠️ Tools</h2>

<ul>
<li>Django</li>
<li>Django Signals</li>
<li>Django Rest Framework</li>
<li>Simple JWT for authentication system</li>
<li>Fast</li>
<li>Docker</li>
<li>Docker Compose</li>
<li>Postgresql as database</li>
<li>Redis as cache</li>
</ul>

<br>
<h2 id="db">🗄️ Database</h2>
<br>

<h3>🏷️ User - main fields</h3>
<ul>
<li>Id</li>
<li>Username</li>
<li>Password</li>
</ul>

<br>
<h3>🏷️ Department</h3>
<ul>
<li>Id</li>
<li>Name</li>
</ul>

<br>
<h3>🏷️ Employee</h3>
<ul>
<li>Id</li>
<li>Name</li>
<li>Email</li>
<li>Department FK</li>
<li>Salary</li>
<li>Birth date</li>
</ul>

<p>Department like FK is better than charfield because it has more control</p>

<br>
<h2 id="project">🎥 See the project</h2>
<p>This project is divided in employee routes, jwt routes and admin routes</p>
<br>


<h2 id="routes-for-frontend">🔗 Routes for frontend</h2>
<br>

<br>
<h3>• /token</h3>
<img src="./readme/views/token.PNG">

<br>
<h3>• /token/refresh</h3>
<img src="./readme/views/refresh_token.PNG">

<br>
<h3>• /employees</h3>
<img src="./readme/views/employees.PNG">

<br>
<h3>• /employees/ID</h3>
<img src="./readme/views/employee_detail.PNG">

<br>
<h3>• /departments</h3>
<img src="./readme/views/departments.PNG">

<br>
<h3>• /departments/ID</h3>
<img src="./readme/views/department_detail.PNG">

<br>
<h3>• /reports/employees/age</h3>
<img src="./readme/views/age_report.PNG">

<br>
<h3>• /reports/employees/salary</h3>
<img src="./readme/views/salary_report.PNG">

<br>
<h2 id="performance">🚀 Performance</h2>
<p>This project has cache system using Redis, caching views after first access and updating cache when data changes</p>
<br>

<h3>Local where show load time</h3>
<img src="./readme/views/ms.PNG">
<br>
<h3>View</h3>
<img src="./readme/views/performance.gif">

<br>
<h2 id="admin">🛡️ Custom admin system</h2>
<br>
<kbd><img src="./readme/views/admin_login.PNG"></kbd>
<br>
<br>
<kbd><img src="./readme/views/admin_in.PNG"></kbd>
<br>

<br>
<br>
<h2 id="project-doc">📖 Project instructions</h2>
<br>

<br>
<h2 id="how-to-start">🎓 How to start</h2>
<p>This project use docker for simulate production environment. You can use project without docker, deleting setting.CACHES and replacing postgresql for sqlite in settings.DATABASES</p>
<br>

<h3>• Create virtual environment and use dependencies</h3>
<p>Docker use requirements.txt for install dependencies</p>
<br>

```
python3 -m venv venv
```

```
pip install -r requirements.txt
```

```
pip freeze > requirements.txt
```

<h3>• Make migrations</h3>

```
docker-compose run web python3 project/manage.py makemigrations
```

```
docker-compose run web python3 project/manage.py migrate
```

<h3>• Create admin user</h3>

```
docker-compose run web python3 project/manage.py createsuperuser
```

<img src="./readme/doc/create_user.PNG">

<h3>• Run project</h3>
<br>
<p>Use when create or update dependencies</p>

```
docker-compose up --build
```

<p>Usually</p>

```
docker-compose up
```

<p>Without logs</p>

```
docker-compose up -d
```

<h3>• Down project</h3>

```
docker-compose down
```

<br>
<h2 id="how-to-use">🎓 How to use</h2>
<br>

<br>
<h3>• Get your tokens in /token/</h3>

<br>
<img src="./readme/doc/get_tokens.PNG">
<br>

<br>
<br>
<h3>• Access any frontend router sending your access token in header</h3>

<br>
<img src="./readme/doc/access.PNG">

<br>
<br>
<h3>• Refresh your access token in /token/refresh/ when access token is expired</h3>

<br>
<img src="./readme/doc/refresh_token.PNG">


<br>
<br>
<h2 id="routes">🔗 Routes</h2>
<p>All routes and your main http methods</p>


<br>
<hr>
<p>POST</p>
<p>/token/</p>
<p>Get refresh and access token</p>
<img src="./readme/doc/routes/token.gif">
<hr>

<br>
<hr>
<p>POST</p>
<p>/token/refresh/</p>
<p>Refresh your access token</p>
<img src="./readme/doc/routes/token_refresh.gif">
<hr>

<br>
<hr>
<p>GET | POST</p>
<p>/employees/</p>
<p>GET: List employees</p>
<p>POST: Create employee</p>
<img src="./readme/doc/routes/employees.gif">
<hr>

<br>
<hr>
<p>GET | PUT | PATCH | DELETE</p>
<p>/employees/[ID]/</p>
<p>GET: See the employee data corresponding to the id parameter</p>
<p>PUT: Update employee data sending all fields</p>
<p>PATCH: Update employee data sending your selected fields</p>
<p>DELETE: delete employee</p>
<img src="./readme/doc/routes/employee_detail.gif">
<hr>

<br>
<hr>
<p>GET | POST</p>
<p>/departments/</p>
<p>GET: List departments</p>
<p>POST: Create department</p>
<img src="./readme/doc/routes/departments.gif">
<hr>

<br>
<hr>
<p>GET | PUT | PATCH | DELETE</p>
<p>/departments/[ID]/</p>
<p>GET: See the department data corresponding to the id parameter</p>
<p>PUT: Update department data sending all fields</p>
<p>PATCH: Update department data sending your selected fields</p>
<p>DELETE: delete department</p>
<img src="./readme/doc/routes/department_detail.gif">
<hr>

<br>
<hr>
<p>GET</p>
<p>/reports/employees/age/</p>
<p>See age report</p>
<img src="./readme/doc/routes/age_report.PNG">
<hr>

<br>
<hr>
<p>GET</p>
<p>/reports/employees/salary/</p>
<p>See salary report</p>
<img src="./readme/doc/routes/salary_report.PNG">
<hr>


<br>
<h2 id="tests">🧪 Tests</h2>
<br>

<p>Usually</p>

```
docker-compose run web python3.10 project/manage.py test backend --pattern="*_t.py"
```

<p>When many changes or one change with a big impact</p>

```
docker-compose run web python3.10 project/manage.py test backend --pattern="*_t.py" --failfast
```

<br>
<img src="./readme/doc/test.PNG">

<h2>❌ End</h2>