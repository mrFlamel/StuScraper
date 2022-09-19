#!/usr/bin/python3

# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import configparser
import json
import os

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

host = config['host']['hostname'] + '_'

# Return user data by id
def id_search(uid:int, data, config=config):
    for user in data[config['host']['hostname']]:
        if int(user['id']) == uid:
            return user

# Return all matching user IDs as an array in a asssending order
def username_search(query, config=config):
    response = []
    data = json.load(open('user_database.json', 'r'))

    for user in data[config['host']['hostname']]:
        if query.lower() in user['name_first'].lower() + ' ' + user['name_last'].lower():
            response.append(int(user['id']))
    response.sort()
    return response

def get_user_by_description(config, query):
    data = json.load(open('./user_database.json', 'r'))
    query = str(query).lower()
    usercout = int(config['host']['usercount'])
    response = []
    for i in range(usercout):
        for item in id_search(i + 1, data=data, config=config)['user_type_labels']:
            if str(query).lower() in str(item).lower():
                response.append(i + 1)
    return response

def main(config):
    list = username_search(str(input('Insert query: ').capitalize()), config=config)
    print('\n')
    data = json.load(open('./user_database.json', 'r'))

    for user in list:
        descriprion = ''

        userdata = id_search(user, data=data, config=config)
        names = f'{userdata["name_first"]} {userdata["name_last"]}'

        if userdata['user_type_labels'] != None:
            for i in range(len(userdata['user_type_labels'])):
                descriprion += ' ' + userdata['user_type_labels'][i]
                # if i is not the last element add a comma
                if i != len(userdata['user_type_labels']) - 1:
                    descriprion += ','

        #print user id, names and description with uniform spacing in a form of a table
        print(f'{userdata["id"]:<6} {names:<30} {descriprion:<20}')

if __name__ == '__main__':
    main(config)
