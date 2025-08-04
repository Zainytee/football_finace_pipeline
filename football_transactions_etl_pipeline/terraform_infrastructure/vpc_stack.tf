resource "aws_vpc" "vpc_stack" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "vpc-stack"
  }
}


resource "aws_subnet" "vpc_subnet_a" {
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"
  vpc_id            = aws_vpc.vpc_stack.id

  tags = {
    Name = "vpc-subnet-a"
  }
}

resource "aws_subnet" "vpc_subnet_b" {
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1b"
  vpc_id            = aws_vpc.vpc_stack.id

  tags = {
    Name = "vpc-subnet-b"
  }
}

resource "aws_redshift_subnet_group" "vpc_subnet_group" {
  name       = "vpc-subnet-group"
  subnet_ids = [aws_subnet.vpc_subnet_a.id, aws_subnet.vpc_subnet_b.id]

}


resource "aws_internet_gateway" "vpc-IGW" {
  vpc_id = aws_vpc.vpc_stack.id

  tags = {
    Name = "IGW"
  }
}


resource "aws_route_table" "vpc-PRT" {
  vpc_id = aws_vpc.vpc_stack.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc-IGW.id
  }

  tags = {
    Name = "Route Table"
  }
}


resource "aws_route_table_association" "subnet-a" {
  subnet_id      = aws_subnet.vpc_subnet_a.id
  route_table_id = aws_route_table.vpc-PRT.id
}


resource "aws_route_table_association" "subnet-b" {
  subnet_id      = aws_subnet.vpc_subnet_b.id
  route_table_id = aws_route_table.vpc-PRT.id
}


resource "aws_security_group" "vpc_secure" {
  name        = "vpc_secure"
  description = "Allow TLS inbound traffic and all outbound traffic"
  vpc_id      = aws_vpc.vpc_stack.id

  tags = {
    Name = "Security Group"
  }
}

resource "aws_vpc_security_group_ingress_rule" "redshift_ingress" {
  security_group_id = aws_security_group.vpc_secure.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5439
  ip_protocol       = "tcp"
  to_port           = 5439
}


resource "aws_vpc_security_group_ingress_rule" "rds_ingress" {
  security_group_id = aws_security_group.vpc_secure.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5432
  ip_protocol       = "tcp"
  to_port           = 5432
}

resource "aws_vpc_security_group_egress_rule" "egress-ipv4" {
  security_group_id = aws_security_group.vpc_secure.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}
