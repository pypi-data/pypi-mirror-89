# Springbuk DE S3 Bucket Download

Bucket Download is a python script to download an aws s3 bucket to expedite getting the files for a mapping

## Instalation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install springbuk_de_bucket_download
```

## Usage

The user must have the aws cli downloaded and configured successfully for this to work. 
Only Those with acces to the springbuk aws s3 will be able to use this, and this will only
function to download the incoming folder of any specified bucket.

```bash
$ dt
What is the bucket name?
user input here (example: name_mi_1)
Input directory for download (blank for here)
user input here
```

This is a command line tool. In the command line the user can type `dt` to activate it.
This will prompt the user to enter the bucket name for their mapping.
Next, the user will be prompted to input the directory they would like the files downloaded.
Hitting enter with nothing written will default to the directory the user is currently in.
