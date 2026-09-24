provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "rds_sg" {
    name         = "shopflow-rds-sg"
    description  = "Security for RDS postgres instance"

    ingres {
        from_port    = 5432
        to_port      = 5432
        protocol     = "tcp"
        cidr_blocks  = ["0.0.0.0/0"]
    }

    egress {
        from_port    = 0
        to_port      = 0
        protocol     = "-1"
        cidr_blocks  = ["0.0.0.0/0"]
    }
}

resource "aws_db_instance" "postgres" {
    identifier           = "shopflow-db"
    engine               = "postgres"
    engine_version       = "15.4"
    instance_class       = "db.t3.micro"
    allocated_storage    = 20

    db_name              = "shopflow"
    username             = var.db_username
    password             = var.db_password

    publicly_accessible    = true
    vpc_security_group_ids = [aws_security_group.rds_sg.id]


    skip_final_snapshot  = true

    tags = {
        Project = "ShopFlow"
    }
}

output "db_endpoint" {
    description = "The connection endpoint for the RDS instance"
    value = aws_db_instance.postgres.endpoint
}