#!/usr/bin/env python3
import os

bucket_name = input("What is the bucket name?\n")
input_directory = input("Input directory for download (blank for here)\n")

if input_directory == "":
    directory = " . "
else:
    directory = " " + input_directory + " "

os.system("aws s3 cp s3://springbuk-raw-storage-production/sftp/"
          + bucket_name
          + "/incoming"
          + directory
          + "--recursive")
