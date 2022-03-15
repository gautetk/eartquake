import sys
from datetime import datetime
import requests
import json
import argparse

api_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson'

parser = argparse.ArgumentParser(description='Display earthquake data for the last hour.')
parser.add_argument('--fields', action='store_true', help='Available fields')
parser.add_argument('--display', type=str, help='Fields to display, separated by ","')
parser.add_argument('--sort', type=str, help='Sort earthquakes by field')
parser.add_argument('--min_magnitude', type=float, help='Minimum earthquake magnitude')

args = parser.parse_args()


def load_json(url):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print(f'Unable to load earthquake. Status code {response.status_code}', file=sys.stderr)
        exit(1)


def parse_quake(f):
    q = {**f['properties'], **f['geometry']}
    q['time'] = datetime.fromtimestamp(q['time'] / 1000.0)
    q['updated'] = datetime.fromtimestamp(q['updated'] / 1000.0)
    return q


def sort_quakes(quakes, sort):
    return sorted(quakes, key=lambda q: q[sort])


def min_mag(quakes, min_magnitude):
    return filter(lambda q: q['mag'] >= min_magnitude, quakes)


def list_print(li):
    print(', '.join([str(x) for x in li]))


def display(quakes, displays):
    displays = args.display.split(',')
    for q in quakes:
        list_print([f'{d}:{q[d]}' for d in displays])


quakes_raw = load_json(api_url)

quakes = [parse_quake(f) for f in quakes_raw['features']]

if args.fields:
    list_print(sorted(quakes[0].keys()))
    exit(1)

if args.min_magnitude:
    quakes = min_mag(quakes, args.min_magnitude)

if args.sort:
    quakes = sort_quakes(quakes, args.sort)

display(quakes, display)
displays = args.display.split(',')
