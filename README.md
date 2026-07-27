## Breast Cancer Data Pipeline: MySQL to PostgreSQL ETL

An automated Extract, Transform, and Load (ETL) pipeline engineered to process and migrate breast cancer datasets from a source MySQL database to a destination PostgreSQL database. The architecture utilizes Python to implement memory-efficient data chunking and pagination during extraction, ensuring reliable performance over large volumes of data.

## System Architecture and Workflow

* **Extract (MySQL):** Connects to the source MySQL database and reads records incrementally using automated pagination and chunking (`pagination.py`). This prevents memory overload and ensures stable data retrieval.
* **Transform (Python):** Processes the raw data chunks in memory (`transform.py`), applying data cleaning, normalization, and structural modifications required for downstream analytics.
* **Load (PostgreSQL):** Establishes a secure connection to the target PostgreSQL database and writes the transformed data chunks into the destination schema (`load.py`).

## Project Structure

```text
Breast_cancer/
│
├── task/
│   ├── main.py          # Application entry point orchestrating the ETL workflow
│   ├── pagination.py    # MySQL database connection, query pagination, and chunking logic
│   ├── transform.py     # Data cleaning, type casting, and schema transformation rules
│   ├── load.py          # PostgreSQL database connection and batch insertion logic
│   ├── test.py          # Automated test suite for database connections and module integrity
│   └── pyproject.toml   # Project configuration and dependency management
│
├── .gitignore           # Specifies intentionally untracked files to ignore
└── README.md            # Project documentation
