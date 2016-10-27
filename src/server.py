from core import Core
from crypto import Crypto
import json
from petlib import pack
import base64
import time
import msgpack
import json
import colorlog
import sys
import threading

class Server(Core):
    """ Server class """
    def __init__(self):
        # By doing this we automatically inherit the variables and methods of the parent class, without needing to initiate first
        super(Server, self).__init__()
        self.id = 1
        self.logger.info("Running in Server mode")
        self.public_keys = []
        self.test = []
        self.server_keypair = []
        self.clients = {}
        self.group_key = ''
        self.readings = {}
        self.count = {}
        self.tmp = ''
        self.node_values ={}

    def add_public_key(self,key):
        self.public_keys.append([key])

    def get_public_keys(self, key):
        return self.public_keys

    def genereate_keys(self):
        ''' Generate cryptographic keypairs '''
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)

        self.core.add_pub_key(pub)

    def setup(self):
        # Create necessary callbacks
        self._callbacks["GROUP_KEY_CREATE"] = self._compute_group_key
        self._callbacks["DECRYPT_GROUP_FINAL"] = self._decrypt_group_final
        self._callbacks["READINGS"] = self._track_readings

        self.get_nodes()
        self.crypto = Crypto()
        self.params = self.crypto.setup()
        self.priv, self.pub = self.crypto.key_gen(self.params)
        self.server_keypair.extend([self.priv, self.pub])
        self.add_public_key(self.pub)
        self.test.append(self.pub)

    def start(self):
        group_key_thread = threading.Thread(target=self._send_group_key)
        listening_thread = threading.Thread(target=self.listen)
        try:
            listening_thread.start()
            group_key_thread.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread();
            sys.exit()
        else:
            pass

    def _compute_group_key(self,json_decoded, ip):

        if json_decoded['ID'] not in self.clients.keys():
            self.test.append(pack.decode(base64.b64decode(json_decoded['PUB'])))
            #print("pub keys: {}").format(self.test)
            self.clients[json_decoded['ID']] = ip
            #self.clients.append(json_decoded['ID'])
            print("Clients: {}, Pub keys len: {}").format(len(self.clients),len(self.test))
        if len(self.test) == len(self.nodes):
            print("Generating group key")
            self.group_key = self.crypto.groupKey(self.params, self.test)
            print("Group_key: {}").format(self.group_key)
            self._send_group_key()

    def _send_group_key(self):
        cur_thread = threading.current_thread()
        print("[*] Processing _send_group_key() in thread: {}".format(cur_thread.name))
        for ip in self.nodes:
            if ip != self.nodes[0]:
                self.send(ip, json.dumps({"OPERATION": "RECEIVE_GROUP_KEY", "PUB": base64.b64encode(pack.encode(self.group_key))}))

    def _decrypt_group_final(self,json_decoded, ip):
        print("[*] Decrypting group final...")
        t4 = self.crypto.partialDecrypt(self.params, self.priv, pack.decode(base64.b64decode(json_decoded['reading'])), True)
        if not self.node_values.has_key(json_decoded['ID']):
            self.node_values.update({json_decoded['ID']: {"period": 1, "value": t4}})
        else:
            self.node_values[json_decoded['ID']]["period"] += 1
            self.node_values[json_decoded['ID']]["value"] += t4
        print("###########################################################")
        print("========= Node {} has aggregated value: {}").format(json_decoded['ID'], t4)
        print("========= Total value for period {}: {}".format(self.node_values[json_decoded['ID']]["period"], self.node_values[json_decoded['ID']]["value"]))
        print("###########################################################")

    def _track_readings(self,json_decoded, ip):
        if json_decoded['ID'] not in self.readings.keys():
            self.readings[json_decoded['ID']] = pack.decode(base64.b64decode(json_decoded['reading']))
            self.count[json_decoded['ID']] = 1
        else:
            if self.count.get(json_decoded['ID']) == 10:
                self.tmp = self.readings.get(json_decoded['ID'])
                self.readings[json_decoded['ID']] = pack.decode(base64.b64decode(json_decoded['reading']))
                self.count[json_decoded['ID']] = 1
                self.send(self.nodes[1], json.dumps({"ID": json_decoded['ID'],"OPERATION": "DECRYPT_GROUP_MSG", "PUB": base64.b64encode(pack.encode(self.group_key)), "reading": base64.b64encode(pack.encode(self.tmp))}))
            else:
                self.readings[json_decoded['ID']] = self.crypto.add(self.params, self.group_key, self.readings.get(json_decoded['ID']), pack.decode(base64.b64decode(json_decoded['reading'])))
                self.count[json_decoded['ID']] = self.count.get(json_decoded['ID']) + 1

