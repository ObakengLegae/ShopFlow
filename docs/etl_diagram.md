# ShopFlow Python ETL Execution & Flow

This diagram illustrates the step-by-step logic and class interactions defined inside the `src/shopflow/` source code. It outlines how raw data moves through the pipeline and ultimately lands in the database schemas.

```mermaid
flowchart TD
    %% Node Assignments
    RawData(["Raw CSV File"])
    ProcessedFile(["Processed CSV File"])
    S3Uploader[("AWS S3 Data Lake")]
    PostgresDB[("PostgreSQL Database")]

    RawDf(["Raw DataFrame"])
    CleanDataFrame(["Cleaned DataFrame"])

    DBClass["database.py"]
    Extractor["extractor.py"]
    Transformer["transformer.py"]
    Uploader["uploader.py"]
    Loader["loader.py"]

    Clean["Rename columns & fill Null values"]
    Cast["Convert timestamps"]
    Validate["Filter out future invalid dates"]
    FeatureEng["Generate dimensions"]
    Math["Calculate total amount"]

    DimCustomers(["Customers Table"])
    DimProducts(["Products Table"])
    DimDates(["Dates Table"])
    FactSales(["Sales Table"])

    %% Styles
    classDef file stroke:#FFFFFF,stroke-width:2px,color:#000
    classDef script stroke:#FFFFFF,stroke-width:2px,color:#000
    classDef df stroke:#FFFFFF,stroke-width:2px,color:#000
    classDef db stroke:#FFFFFF,stroke-width:2px,color:#000
    classDef ext stroke:#FFFFFF,stroke-width:2px,color:#000

    class RawData,ProcessedFile file
    class DBClass,Extractor,Transformer,Uploader,Loader script
    class RawDf,CleanDataFrame,DimCustomers,DimProducts,DimDates,FactSales df
    class PostgresDB db
    class S3Uploader ext

    subgraph PipelineOrchestration ["pipeline.py (Orchestrator)"]
        direction TB
        
        DBClass -->|"1. Executes schema"| PostgresDB
        
        RawData -->|"2. Read via Pandas"| Extractor
        Extractor -.->|"Returns"| RawDf
        
        RawDf -->|"3. Passes to"| Transformer
        
        subgraph TransformOperations ["Transform Logic"]
            direction TB
            Clean --> Cast --> Validate --> FeatureEng --> Math
        end
        
        Transformer --> Clean
        Math -.->|"Returns"| CleanDataFrame

        CleanDataFrame -->|"4. Save locally"| ProcessedFile
        ProcessedFile -->|"5. Upload triggered"| Uploader
        Uploader -->|"Puts Object"| S3Uploader

        CleanDataFrame -->|"6. Passes to"| Loader
        
        subgraph LoadOperations ["Dimensional Modeling"]
            direction TB
            DimCustomers
            DimProducts
            DimDates
            FactSales
        end
        
        Loader --> DimCustomers
        Loader --> DimProducts
        Loader --> DimDates
        Loader --> FactSales
        
        DimCustomers -->|"7. Insert Data"| DBClass
        DimProducts --> DBClass
        DimDates --> DBClass
        FactSales --> DBClass
        
        DBClass -->|"8. Bulk Insert"| PostgresDB
    end
```

### Flow Breakdown:
1. **Initialize Database:** `pipeline.py` starts by initializing the `Database` class, which connects to PostgreSQL and runs `./sql/schema.sql` to ensure tables (customers, products, dates, sales) exist.
2. **Extraction (`extractor.py`):** Uses pandas to read the raw `.csv` file directly from a filepath (either local or downloaded by Lambda), raising errors immediately if parsing fails.
3. **Transformation (`transformer.py`):** Accepts the raw DataFrame and systematically cleans it. This includes normalizing column names, safely replacing NULL IDs, enforcing date validation, and computing business-logic features (like `day_of_week` and `total_amount`).
4. **Data Backup (`uploader.py`):** The clean DataFrame is extracted back to a flat CSV file, which `uploader.py` then immediately uploads to Amazon S3 as a backup in the "Processed Data Lake", saving to S3 occurs if the pipeline is triggered by an uplaod.
5. **Loading (`loader.py` & `database.py`):** `loader.py` slices the singular clean DataFrame into distinct tables to enforce a Star Schema. By running `drop_duplicates` on primary keys, it guarantees data integrity before passing the subsets to `database.py`, which leverages `psycopg2.extras.execute_values` for high-speed batch database loading.
