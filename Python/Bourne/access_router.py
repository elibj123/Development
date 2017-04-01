import requests
import time

router_address = 'http://192.168.1.1'
router_login_address = '%s/goform/login' % router_address
router_ac_address = 'http://192.168.1.1/wlanAccess.asp'


def get_devices():
    wlan_access = requests.get(router_ac_address)
    html = wlan_access.content

    table_begin_pattern = ["<tr dir=ltr bgcolor=#99CCFF>", "<tr dir=ltr bgcolor=#9999CC>"]
    cur_pattern = 0
    cur_index = html.index(table_begin_pattern[cur_pattern]) + len(table_begin_pattern[cur_pattern])

    devices = list()

    while cur_index != -1:
        mac_address_start_index = html.index("<td>", cur_index) + len("<td>")
        mac_address_end_index = html.index("</td>", mac_address_start_index) - 1
        mac_address = html[mac_address_start_index:mac_address_end_index+1]

        age_start_index = html.index("<td>", mac_address_end_index + 1 + len("</td>")) + len("<td>")
        age_end_index = html.index("</td>", age_start_index) - 1
        age = html[age_start_index:age_end_index+1]

        rssi_start_index = html.index("<td>", age_end_index + 1 + len("</td>")) + len("<td>")
        rssi_end_index = html.index("</td>", rssi_start_index) - 1
        rssi = html[rssi_start_index:rssi_end_index+1]

        ip_start_index = html.index("<td>", rssi_end_index + 1 + len("</td>")) + len("<td>")
        ip_end_index = html.index("</td>", ip_start_index) - 1
        ip = html[ip_start_index:ip_end_index+1]

        host_start_index = html.index("<td>", ip_end_index + 1 + len("</td>")) + len("<td>")
        host_end_index = html.index("</td>", host_start_index) - 1
        host = html[host_start_index:host_end_index + 1]

        devices.append({'MacAddress': mac_address, 'Age': age, 'RSSI': rssi, 'IP': ip, 'HostName': host})

        cur_pattern = 1 - cur_pattern
        # noinspection PyBroadException
        try:
            cur_index = html.index(table_begin_pattern[cur_pattern], cur_index) + len(table_begin_pattern[cur_pattern])
        except:
            cur_index = -1

    return devices

tic = time.time()
print get_devices()
toc = time.time()

print "Time was %f" % (toc-tic)