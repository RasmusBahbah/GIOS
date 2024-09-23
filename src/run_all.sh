#!/bin/bash

#ROOT_DIR="/data/fileshare"
API_KEY='44154c44-ec27-46c5-945e-9f46bb102950'
DATAVERSE_SERVER='https://dataverse.geus.dk'

source activate "SICE_dataverse"

python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/1KMRCC' --folder $ROOT_DIR/SouthernArcticCanada;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/EXTTLR' --folder $ROOT_DIR/Svalbard;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/MCCESF' --folder $ROOT_DIR/SevernayaZemlya;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/E2HSXW' --folder $ROOT_DIR/NovayaZemlya;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/UFBNWZ' --folder $ROOT_DIR/Norway;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/47QXB1' --folder $ROOT_DIR/NorthernArcticCanada;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/OBUF5E' --folder $ROOT_DIR/Iceland;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/FBIFOX' --folder $ROOT_DIR/Greenland;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/1BO9GT' --folder $ROOT_DIR/FransJosefLand;
python dataverse_get.py --api_key $API_KEY --dataverse_server $DATAVERSE_SERVER --persistentId 'doi:10.22008/FK2/RTFM0K' --folder $ROOT_DIR/AlaskaYukon;
