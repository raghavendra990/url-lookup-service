import yaml

# from app.pynamoModels.url import Url 

state = "dev"

print(state)
config_data = {}

if state == "dev":
    with open("cfg/dev.yml", 'r') as stream_prod:
        config_data = yaml.load(stream_prod)


# if not Url.exists():
#         Url.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)