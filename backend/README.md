# Startupilot

## Guide on Setting Up Backend Server on Your Localhost

Follow the steps below to set up the backend server for the project.

### 1. Navigate to the Backend Directory

```bash
cd backend
```

### 2. Create a .env File

In the `backend` directory, create a `.env` file with the following content:

```bash
SECRET_KEY=somerandomchacracterspretendingtobeasupperseccretkeythatnoneissupposedtoknow
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=elabwebdb
SQL_USER=postgresuser
SQL_PASSWORD=postgrespassword
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
MINIO_URL=storage:9000
MINIO_ACCESS_KEY=minioaccess
MINIO_SECRET_KEY=miniosecret
MINIO_BUCKET_NAME=elabweb
```

### 3. Run the Docker Container

Please, ensure that your Docker Desktop is on. Then, to build and run the backend server, use the following command:

```bash
docker-compose up --build -d
```

> **Note:** The --build flag is required each time you pull the repository to ensure any new changes are built into the container.

After the container is up, the backend server will be running at [http://localhost:8000](http://localhost:8000).
