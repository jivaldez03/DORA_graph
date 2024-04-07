# DORA
###The Digital Operational Resilience Act, or DORA, is a European Union (EU) regulation that creates a binding, comprehensive information and communication technology ###(ICT) risk management framework for the EU financial sector.

## Required Tools:  Docker and Python 3.10+

# INSTALL AND LOAD XLSX FILE
## Python 3.10
### prepare a new environments for python (root: nist_Grap directory):
### python3 -m venv venv
### source venv/bin/activate
### pip3 install -r requirements.txt

## Docker
### ------- please change "your-user" label with a real value
1. 
sudo docker run -d --publish=7474:7474 --publish=7687:7687 --env=NEO4J_AUTH=none --volume=/home/jiduma/dockerback/dock_DORA/data:/data neo4j
sudo docker run -d --publish=7474:7474 --publish=7687:7687 --env=NEO4J_AUTH=none --volume=/home/jiduma/dockerback/dock_DORA/data:/data neo4j

sudo docker run -d --publish=7475:7474 --publish=7688:7687 --env=NEO4J_AUTH=none \
    -v $PWD/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    --volume=/home/your-user/dockerback/dock_DORA/data:/data neo4j


docker run \
    -p 7474:7474 -p 7687:7687 \
    -v $PWD/data:/data 
    -v $PWD/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    neo4j:4.0


## Loading NIST file
### To load file into docker execute: 
2. python3 main.py


# Exploring graph database (no user and password are needed)
http://0.0.0.0:7474/browser/   or http://localhost:7474/browser/


# Review complete schema - Neo4j Command: 
call db.schema.visualization()  

![schema visualization](schema_visualization.png)