from flask import Flask, request
import requests
import os
import dataset


app = Flask(__name__)

rai_node_address = 'http://%s:%s' % ('127.0.0.1', '7076')
database_location = 'sqlite:///%s' % 'hashdata.db'

def get_work(hash):
     get_work = '{ "action" : "work_generate", "hash" : "%s", "use_peers": "true" }' % hash
     r = requests.post(rai_node_address, data = get_work)
     print(r.text)
     resulting_work = r.json()
     return resulting_work['work'].lower()

def get_account_from_hash(hash):
     get_account = '{ "action" : "block_account", "hash" : "%s"}' % hash
     r = requests.post(rai_node_address, data = get_account)
     resulting_data = r.json()
     if 'account' in resulting_data:
         account = resulting_data['account']
         return account
     else:
         return 'Error'

@app.route('/work', methods=['POST'])
def generate_work():
     hash = request.form['hash']
     print(hash)
     account_db = dataset.connect(database_location)
     account_table = account_db['account']
     account = get_account_from_hash(hash)
     if account == 'Error':
         work_output = get_work(hash)
         return_json = '{"work" :"%s"}' % work_output
         return return_json


     precache_work = account_table.find_one(account=account)
     if precache_work != None :
         print('Found cached work value')
         work_output = precache_work['work']
     else:
         work_output = get_work(hash)
         account_table.insert(dict(account=account, hash=hash, work=work_output))

     return_json = '{"work" :"%s"}' % work_output

     return return_json
