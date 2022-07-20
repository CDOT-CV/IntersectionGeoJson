import logging
from google.cloud import bigquery
import json
import os
from datetime import datetime
from cvmsg_functions import map_intersection_geometry_to_geojson


def get_map_data():

  client = bigquery.Client()
  table = os.environ["MAP_DB_NAME"]
  date = datetime.utcnow()

  query = "SELECT t.ip, t.geometry FROM " \
          f"(SELECT map.metadata.originIp as ip, " \
          f"map.metadata.odeReceivedAt as time, " \
          f"TO_JSON_STRING(map.payload.data.intersections.intersectionGeometry[ordinal(1)]) as geometry " \
          f"FROM `{table}` " \
          f"WHERE Year = {date.year} AND Month = {date.month} AND Day = {date.day}) AS t " \
          f"INNER JOIN " \
          f"(SELECT map.metadata.originIp as ip, MAX(map.metadata.odeReceivedAt) as time " \
          f"FROM `{table}` " \
          f"WHERE Year = {date.year} AND Month = {date.month} AND Day = {date.day} " \
          f"GROUP BY ip) AS t1 ON " \
          f"t1.time = t.time AND t1.ip = t.ip"

  logging.info(f"Running query on table `{table}`")

  query_job = client.query(query)

  geojson = {'type': 'FeatureCollection', 'features': []}

  for row in query_job:
    intersectionDataString = row.geometry
    intersectionData = json.loads(intersectionDataString)
    feature = map_intersection_geometry_to_geojson(row.ip, intersectionData)
    for entry in feature['features']:
      geojson['features'].append(entry)

  return geojson

# REST endpoint resource class
from flask_restful import Resource

class RsuMapInfo(Resource):
  options_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Max-Age': '3600'
  }

  headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
  }

  def options(self):
    # CORS support
    return ('', 204, self.options_headers)
  
  def get(self):
    logging.debug("RsuMapInfo GET requested")
    return (get_map_data(), 200, self.headers)