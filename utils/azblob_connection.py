# This script is used to correctly generate as `wasb` connection string for Airflow
# which can be used in an environment variable to define an azure storage connection string
# Like so `export AIRFLOW_CONN_WASB_FILE_UPLOAD=<ScriptURLOutputHere>`

from airflow.models import Connection
from urllib import parse
from sys import argv

if len(argv) < 3:
    print("Expect 2 arguments `AzureStorageAccountName` and `AzureStorageKey`")
    exit()


# Make sure the password is URL escaped
pw=argv[2]
quoted = parse.quote_plus(pw)

# Build the connection URL
url = "wasb://{}:{}@azure".format(argv[1], quoted)

# Check worked correctly 
conn = Connection()
conn.parse_from_uri(url)

print("Found these details are they correct?")
print("Account Name: {}".format(conn.login))
print("Account Key: {}".format(conn.password))

print("\nAirflow Connection URL for this account:")
print(url)
