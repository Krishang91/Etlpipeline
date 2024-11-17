
---

# Astronomer Project: ETL Pipeline with NASA API Integration

Welcome to Astronomer! This project was generated using the `astro dev init` command via the Astronomer CLI. It demonstrates how to develop and deploy Apache Airflow pipelines that pull data from NASA's API, process it, and store it in an **AWS PostgreSQL server**. It also includes GitHub Actions for automated deployment to Astronomer Cloud.

---

## **Project Contents**

Your Astronomer project contains the following files and folders:

### **1. DAGs**
This folder contains the Python files for your Airflow DAGs. It includes:
- **`example_astronauts`**: A sample ETL pipeline querying the list of astronauts currently in space from the Open Notify API.
- **`nasa_etl_pipeline`**: 
  - This DAG runs daily to perform the following:
    1. **Extract**: Pulls data from NASA’s API (e.g., APOD - Astronomy Picture of the Day or Mars Rover Photos API).
    2. **Transform**: Cleans and structures the data.
    3. **Load**: Inserts the transformed data into a PostgreSQL database.

### **2. `Dockerfile`**
A versioned Astro Runtime Docker image optimized for Apache Airflow. You can customize this file to include additional commands or runtime overrides.

### **3. `include/`**
Contains any additional files required by your project. It is empty by default.

### **4. `packages.txt`**
Install OS-level dependencies by listing them here. For example, you can add `curl`, `libpq-dev`, or other required system packages.

### **5. `requirements.txt`**
Add Python packages needed for your project. This project includes:
```text
requests
pandas
psycopg2-binary
```

### **6. `plugins/`**
Add custom or community Airflow plugins to extend functionality. It is empty by default.

### **7. `airflow_settings.yaml`**
Use this local-only file to define Airflow Connections, Variables, and Pools. This simplifies the management of settings during development.

---

## **Required Connections**

To run the `nasa_etl_pipeline` DAG, you need to configure two connections in the Airflow UI:

### **1. PostgreSQL Connection**
- **Connection ID**: `my_postgres_connection`
- **Connection Type**: Postgres
- **Host**: [Your host id or if you run it locally using docker then name of conatainer of postgres]
- **Database**: `postgres`
- **Login**: `postgres`
- **Password**: [Your password]
- **Port**: `5432`

> Use this connection to store the transformed NASA API data into the PostgreSQL database.

### **2. NASA API Connection**
- **Connection ID**: `nasa_api`
- **Connection Type**: HTTP
- **Host**: `http://api.nasa.gov/`
- **Extra**:
  ```json
  {
    "api_key": "enter your api key here"
  }
  ```

> Use this connection to fetch data from NASA's public APIs. Replace `"enter your api key here"` with your actual NASA API key.

---

## **Run Your Project Locally**

### **Start Airflow Locally**
Run the following command to start your Airflow environment:
```bash
astro dev start
```

This command creates 4 Docker containers:
- **Postgres**: Airflow's Metadata Database
- **Webserver**: Renders the Airflow UI
- **Scheduler**: Monitors and triggers tasks
- **Triggerer**: Executes deferred tasks

Verify that all containers are running with:
```bash
docker ps
```

### **Access the Local Environment**
- **Airflow UI**: [http://localhost:8080/](http://localhost:8080/)  
  Log in using `admin` for both the username and password.
- **Postgres Database**: Accessible at `localhost:5432/postgres`.

---

## **DAG: NASA ETL Pipeline**

### **Workflow**
1. **Extract**:
   - Fetch data from NASA's API.
2. **Transform**:
   - Clean and structure the data using Python and Pandas.
3. **Load**:
   - Insert the transformed data into a PostgreSQL database.

### **Code Structure**
- The DAG is defined in `dags/nasa_etl_pipeline.py` using the TaskFlow API.
- Required Python dependencies are installed via `requirements.txt`.

---

## **Automated Deployment with GitHub Actions**

This project includes a **GitHub Actions workflow** that automates deployment to Astronomer Cloud. The workflow:
1. Authenticates with Astronomer using API keys.
2. Deploys the Airflow project whenever changes are pushed to the `main` branch.

### **GitHub Workflow File**
The workflow is defined in `.github/workflows/deploy_to_astro.yml`. It performs the following steps:
1. **Checkout Code**: Clones the repository.
2. **Install Astro CLI**: Ensures the Astronomer CLI is installed.
3. **Authenticate**: Logs into Astronomer Cloud using API credentials.
4. **Deploy**: Deploys the project to the specified Astronomer Deployment.

---

## **Quick Links**

- [Astronomer Documentation](https://www.astronomer.io/docs)
- [Airflow API Reference](https://airflow.apache.org/docs)
- [NASA API Documentation](https://api.nasa.gov/)

---

## **Contact**
The Astronomer CLI is maintained with ❤️ by the Astronomer team. For support, report a bug or suggest a change:
- [Astronomer Support](https://support.astronomer.io/)
- [GitHub Issues](https://github.com/astronomer/issues)

---
