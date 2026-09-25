## ShopFlow Cloud Architecture

With an event-driven design, the Cloud Infrastructure handles the hardware scaling, networking, and event orchestration, while the Data Engineering pipeline remains fully isolated, focusing exclusively on data extraction, transformation, and loading.

```mermaid
flowchart TD
    %% Node Assignments
    IAM_Role{{Lambda Execution Role}}
    
    S3_Landing[(AWS S3 Landing Zone)]
    S3_DataLake[(AWS S3 Data Lake)]
    RDS[(AWS RDS PostgreSQL)]
    
    LambdaCompute(AWS Lambda Compute Context)
    
    Extractor[Extractor.py]
    Transformer[Transformer.py]
    Uploader[Uploader.py]
    Loader[Loader.py]

    %% Groupings
    subgraph Security [AWS IAM Security Bounds]
        IAM_Role
    end

    subgraph Cloud [Cloud Computing Resources]
        S3_Landing
        S3_DataLake
        RDS
    end

    subgraph DataEngineering [Data Engineering Pipeline]
        LambdaCompute
        Extractor
        Transformer
        Uploader
        Loader
        
        LambdaCompute --> Extractor
        Extractor --> Transformer
        Transformer --> Uploader
        Transformer --> Loader
    end

    %% Cloud Triggers
    S3_Landing -->|ObjectCreated trigger| LambdaCompute

    %% Security Authorizations
    IAM_Role -.->|Allows s3:GetObject| S3_Landing
    IAM_Role -.->|Allows s3:PutObject| S3_DataLake
    IAM_Role -.->|Allows VPCAccess| RDS
    IAM_Role -.->|Assumed by| LambdaCompute

    %% Cross-boundary connections
    Uploader -->|Uploads clean backup| S3_DataLake
    Loader -->|Bulk-Inserts rows| RDS
    
    %% Apply styles
    classDef cloud fill:#F0000,stroke:#333,stroke-width:2px,color:#000
    classDef data fill:#4B8BBE,stroke:#333,stroke-width:2px,color:#000
    classDef security fill:#E71D36,stroke:#333,stroke-width:2px,color:#FFF
    
    class S3_Landing,S3_DataLake,RDS cloud
    class LambdaCompute,Extractor,Transformer,Uploader,Loader data
    class IAM_Role security
```

### IAM Authorization & Security Model
ShopFlow utilizes a strictly scoped security model orchestrated through Terraform (`iam.tf`):
1. **Lambda Execution Role (`shopflow-lambda-exec-role`):** The AWS Lambda function assumes this role instantly when triggered.
2. **S3 Permissions:** The role must contain policies allowing `s3:GetObject` to pull the raw CSV from the bucket, and crucially, `s3:PutObject` to push the processed Data Lake backup back to the `processed/` prefix.
3. **VPC Networking (`AWSLambdaVPCAccessExecutionRole`):** Because the RDS instance sits securely inside a Virtual Private Cloud (VPC), the Lambda role must have VPC Access permissions to generate elastic network interfaces (ENIs) to reach the Database on port `5432`.
4. **Invocation Scopes:** S3 is granted selective permission to invoke the Lambda function, ensuring only your specific bucket triggers the pipeline.
