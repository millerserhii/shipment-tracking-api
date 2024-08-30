resource "aws_db_instance" "webapp_postgres_db" {
  allocated_storage           = 20
  storage_type                = "standard"
  engine                      = "postgres"
  engine_version              = "14"
  instance_class              = "db.t3.micro"
  publicly_accessible         = false
  vpc_security_group_ids      = [aws_security_group.webapp_db_sg.id]
  db_subnet_group_name        = aws_db_subnet_group.webapp_db_subnet.id
  username                    = var.DB_USERNAME
  password                    = var.DB_PASSWORD  # pragma: allowlist secret
  skip_final_snapshot         = true
  auto_minor_version_upgrade  = true

  tags = {
    Name        = "${var.app_name}-postgres-db"
    Environment = var.app_environment
  }
}

resource "aws_security_group" "webapp_db_sg" {
  name        = "${var.app_name}-${var.app_environment}-rds-sg"
  description = "Security group for RDS instance"
  vpc_id      = aws_vpc.aws-vpc.id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [for subnet in var.private_subnets : subnet]  # Allowing inbound traffic from private subnets
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All traffic
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-rds-sg"
    Environment = var.app_environment
  }
}

resource "aws_db_subnet_group" "webapp_db_subnet" {
  name       = "${var.app_name}-${var.app_environment}-db-subnet"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name        = "${var.app_name}-db-subnet-group"
    Environment = var.app_environment
  }
}
