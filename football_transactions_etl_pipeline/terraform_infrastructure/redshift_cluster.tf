resource "aws_redshift_parameter_group" "redshift_parameter_group" {
  name        = "parameter-group-for-redshift-cluster"
  family      = "redshift-2.0"
  description = "Parameter group"

  parameter {
    name  = "require_ssl"
    value = "false"
  }

}


resource "aws_iam_role" "redshift_cluster_role" {
  name = "redshift-cluster-role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "redshift_s3_access" {
  name        = "RedshiftS3AccessPolicy"
  description = "Policy allowing Redshift to access S3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ]
      Effect = "Allow"
      Resource = [
        "arn:aws:s3:::football-transactions",
        "arn:aws:s3:::football-transactions/*"
      ]
      },
      {
        "Effect" : "Allow",
        "Action" : "redshift-data:*",
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "redshift_attach_s3_policy" {
  role       = aws_iam_role.redshift_cluster_role.name
  policy_arn = aws_iam_policy.redshift_s3_access.arn
}



resource "random_password" "datawarehouse_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
  min_numeric      = 1
}


data "aws_ssm_parameter" "redshift_username" {
  name = "/production/datawarehouse/username/master_"
}

resource "aws_ssm_parameter" "password_secret" {
  name        = "/production/datawarehouse/password/master"
  description = "The redshift master password"
  type        = "String"
  value       = random_password.datawarehouse_password.result
}


resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier           = "tf-redshift-cluster"
  database_name                = "football_db"
  master_username              = data.aws_ssm_parameter.redshift_username.value
  master_password              = random_password.datawarehouse_password.result
  node_type                    = "ra3.large"
  cluster_type                 = "multi-node"
  number_of_nodes              = 2
  cluster_subnet_group_name    = aws_redshift_subnet_group.vpc_subnet_group.name
  iam_roles                    = [aws_iam_role.redshift_cluster_role.arn]
  vpc_security_group_ids       = [aws_security_group.vpc_secure.id]
  cluster_parameter_group_name = aws_redshift_parameter_group.redshift_parameter_group.name
  skip_final_snapshot          = true
  publicly_accessible          = true


}



