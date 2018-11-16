#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import socket
import binascii

def get_script_info(data=None):
    script_info = {
        "name": "ms17_010",
        "info": "ms17_010.",
        "level": "high",
        "type": "info",
    }
    return script_info



def prove(data):
    data = init(data,'smb')
    # socket.setdefaulttimeout(data['timeout'])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    negotiate_protocol_request = binascii.unhexlify(
        "00000054ff534d42720000000018012800000000000000000000000000002f4b0000c55e003100024c414e4d414e312e3000024c4d312e325830303200024e54204c414e4d414e20312e3000024e54204c4d20302e313200")
    session_setup_request = binascii.unhexlify(
        "00000063ff534d42730000000018012000000000000000000000000000002f4b0000c55e0dff000000dfff02000100000000000000000000000000400000002600002e0057696e646f7773203230303020323139350057696e646f7773203230303020352e3000")

    try:
        s.settimeout(10)
        s.connect((data['target_host'], data['target_port']))
        s.send(negotiate_protocol_request)
        s.recv(1024)
        s.send(session_setup_request)
        res = s.recv(1024)
        user_id = res[32:34]
        tree_connect_andx_request = "000000%xff534d42750000000018012000000000000000000000000000002f4b%sc55e04ff000000000001001a00005c5c%s5c49504324003f3f3f3f3f00" % (
        (58 + len(data['target_host'])), user_id.hex(), bytes(data['target_host'],'utf-8').hex())
        s.send(binascii.unhexlify(tree_connect_andx_request))
        res = s.recv(1024)
        allid = res[28:36]
        payload = "0000004aff534d422500000000180128000000000000000000000000%s1000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00" % allid.hex()
        s.send(binascii.unhexlify(payload))
        res = s.recv(1024)
        s.close()
        if "\x05\x02\x00\xc0" in str(res):
            data['flag'] = 1
            data['data'].append({"info": "MS17_010"})
            data['res'].append({"info": "The vul is exist!", "MS17_010":res})
    except:
        pass
    return data