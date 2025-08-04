resource "aws_s3_bucket" "data_file" {
  bucket = "football-transactions"
}


resource "aws_s3_bucket_versioning" "data_file_versioning" {
  bucket = aws_s3_bucket.data_file.id
  versioning_configuration {
    status = "Enabled"
  }
}