provider "aws" {
  region = "us-east-1"
}

data "aws_subnets" "default" {
    filter {
        name   = "vpc.id"
        values = [data.aws_vpc.default.id]
    }
}

resource "aws_security_group" "rds_sg" {
    name         = "shopflow-rds-sg"
    description  = "Security for RDS postgres instance"
    vpc_id       = data.aws_vpc.default.id

    ingres {
        from_port    = 5432
        to_port      = 5432
        protocol     = "tcp"
        cidr_blocks  = [data.aws_vpc.default.cidr_block]
    }

    egress {
        from_port    = 0
        to_port      = 0
        protocol     = "-1"
        cidr_blocks  = ["0.0.0.0/0"]
    }
}

resource "aws_db_subnet_group" "default" {
    name = "shopflow-db-subnet-group"
    subnet_ids = data.aws_subnets.default.ids

    tags = {
        Name = "shopflow-db-subnet-group"
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

    aws_db_subnet_group_name = aws_db_subnet_group.default.name
    vpc_security_group_ids = [aws_security_group.rds_sg.id]

    skip_final_snapshot  = true
    publicly_accessible    = false

    tags = {
        Project = "ShopFlow"
    }
}

output "db_endpoint" {
    description = "The connection endpoint for the RDS instance"
    value = aws_db_instance.postgres.endpoint
}