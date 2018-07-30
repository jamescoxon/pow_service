import dataset
import requests
import json
import time

rai_node_address = 'http://%s:%s' % ('127.0.0.1', '7076')
database_location = 'sqlite:///%s' % 'hashdata.db'

db = dataset.connect(database_location)
account_table = db['account']

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
     account = resulting_data['account']
     return account

while 1:
  for user in db['account']:
     print(user)
     print(user['account'])
     get_frontier = '{ "action" : "account_info", "account" : "%s" }' % user['account']
     r = requests.post(rai_node_address, data = get_frontier)
     results = r.json()
     print(results['frontier'])
     if results['frontier'] == user['hash']:
         print("Uptodate")
     else:
         print("Not upto date, precache")
         work_output = get_work(results['frontier'])
         account_table.update(dict(account=user['account'], hash=results['frontier'], work=work_output), ['account'])
     time.sleep(10)
