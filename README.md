# ShopFlow

ShopFlow is an e-commerce data platform designed to demonstrate both **data engineering** and **cloud computing** concepts.

The project implements an ETL pipeline that extracts raw transactional data, transforms and validates it using Python, and loads it into PostgreSQL.

The same pipeline can run locally using Docker or in AWS using S3, Lambda and RDS.

## Architecture Overviews

### Local Development (ETL to DB)

In the local development environment, the pipeline processes data via local Python scripts and loads it into a 
containerized database.

**Workflow:**

```text
Local CSV
    |
    v
Python ETL
    |
    +--> Extractor
    |
    +--> Transformer
    |
    +--> Loader
    |
    v
PostgreSQL (Docker)
```

### Cloud Deployment (AWS)
In the cloud, the pipeline adopts a serverless, event-driven architecture using Infrastructure as Code (Terraform) and 
AWS services.

```text
   CSV
    |
    v
 Amazon S3
    |
    | S3 Event
    v
 AWS Lambda
    |
    v
 Python ETL
    |
    v
 Amazon RDS (PostgreSQL)
    

```

**Security:**

AWS IAM roles and policies strictly manage permissions across S3, Lambda, and RDS to ensure secure resource access.

For more information, see: docs/

## Project Focus

### Data Engineering

ShopFlow demonstrates:

- ETL pipeline design
- Data extraction and transformation
- Data validation
- Relational data modelling
- PostgreSQL
- SQL
- Pipeline testing
- Local development with Docker

### Cloud Computing

ShopFlow demonstrates:

- AWS S3
- AWS Lambda
- AWS RDS
- IAM
- Infrastructure as Code with Terraform
- Serverless execution
- Cloud-based object storage
- Cloud deployment

## Repository Structure

```text
ShopFlow/
│
├── README.md             # Project documentation
│
├── data/                 # Raw and processed CSV data files
├── docs/                 # Detailed architectural diagrams and documentation
├── sql/                  # SQL schema
│
├── src/                  # Python source code
│   └── shopflow/         # ETL Python package
│       ├── lambda_function.py # AWS Lambda handler for cloud execution
│       ├── pipeline.py        # Entry point for the local ETL execution
│       ├── extractor.py       # Module to read data from CSV (local) or S3 (cloud)
│       ├── transformer.py     # Module for data cleaning, mapping, and engineering
│       ├── uploader.py        # Helper to upload raw CSV to S3
│       └── loader.py          # Module to insert data into PostgreSQL (Local or RDS)
│
├── tests/               # Pytest unit and integration tests
│
├── terraform/            # Infrastructure as Code setup
│   ├── lambda.tf         # AWS Lambda function provisioning
│   ├── rds.tf            # Amazon RDS (PostgreSQL) provisioning
│   ├── s3.tf             # Amazon S3 bucket configuration and event triggers
│   ├── iam.tf            # AWS IAM roles and least-privilege security policies
│   └── variables.tf      # Infrastructure input variables definition
│
├── compose.yaml          # Docker Compose configuration for local Postgres database
├── requirements.txt      # Python package dependencies
└── .gitignore            # Untracked files skipped by git
```

## Dependencies
- **Python 3.10+** (Core language)
- **pandas**, **psycopg2-binary** (Data manipulation and database interfacing)
- **boto3** (AWS SDK for Python)
- **Docker** & **Docker Compose** (For spinning up the local DB)
- **Terraform** (For cloud infrastructure provisioning)
- **AWS CLI** (Configured with appropriate access credentials for deployment)

## Setup and Run

### Local Environment

1. **Setup virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your desired local database credentials.
4. **Start the local Database:**
   ```bash
   docker-compose up -d
   ```
5. **Execute pipeline locally:**
   ```bash
   python -m src.shopflow.pipeline
   ```

### Cloud Environment (AWS)

1. **Configure AWS & Terraform:**
   Ensure your AWS CLI is authenticated (`aws configure`).
2. **Navigate to Terraform directory:**
   ```bash
   cd terraform
   ```
3. **Initialize Terraform:**
   ```bash
   terraform init
   ```
4. **Plan and Apply the Infrastructure:**
   ```bash
   terraform plan
   terraform apply -auto-approve
   ```
5. **Trigger the Pipeline:**
   Upload your raw customer/sales `.csv` file to the S3 bucket created by Terraform. The upload event will automatically trigger the AWS Lambda function to run the ETL code and ingest the data into your RDS instance.
6. **(Optional) Teardown:**
   When finished, cleanly destroy your cloud resources to halt billing.
   ```bash
   terraform destroy
   ```

---

WTC-FKAABD4Z

WTC-SJTTMHVP