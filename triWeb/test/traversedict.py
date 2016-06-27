jdict= {
    "build_server": {
        "image": "/auto/cds-build/release_builds/3.5.2/cos_3.5.2-b4/target/cos_repo-3.5.2-0b4-x86_64.iso",
        "mgmtip": "172.22.68.184",
        "name": "mpd-lnx1",
        "password": "rootroot",
        "user": "root"
    },
    "cos1": {
        "cf1": "20.0.51.161",
        "cf2": "20.0.51.162",
        "cf3": "20.0.51.163",
        "cf4": "20.0.51.164",
        "disks": [
            "csd1",
            "csd2",
            "csd3",
            "csd4",
            "csd5",
            "csd6"
        ],
        "disks_cnt": 36,
        "domain": "ab.colusa.com",
        "mgmtip": "172.22.117.15",
        "name": "cde465-a5",
        "password": "rootroot",
        "user": "root"
    },
    "cos2": {
        "cf1": "20.0.51.141",
        "cf2": "20.0.51.142",
        "cf3": "20.0.51.143",
        "cf4": "20.0.51.144",
        "disks_cnt": 36,
        "mgmtip": "172.22.117.17",
        "name": "cde465-b1",
        "password": "rootroot",
        "user": "root"
    },
    "cos3": {
        "cf1": "20.0.51.145",
        "cf2": "20.0.51.146",
        "cf3": "20.0.51.147",
        "cf4": "20.0.51.148",
        "disks_cnt": 36,
        "mgmtip": "172.22.117.18",
        "name": "cde465-b2",
        "password": "rootroot",
        "user": "root"
    },
    "cos4": {
        "cf1": "20.0.51.149",
        "cf2": "20.0.51.150",
        "cf3": "20.0.51.151",
        "cf4": "20.0.51.152",
        "disks_cnt": 36,
        "mgmtip": "172.22.117.19",
        "name": "cde465-b3",
        "password": "rootroot",
        "user": "root"
    },
    "cos5": {
        "cf1": "20.0.51.153",
        "cf2": "20.0.51.154",
        "cf3": "20.0.51.155",
        "cf4": "20.0.51.156",
        "disks_cnt": 36,
        "mgmtip": "172.22.117.20",
        "name": "cde465-b4",
        "password": "rootroot",
        "user": "root"
    },
    "cos6": {
        "cf1": "20.0.51.157",
        "cf2": "20.0.51.158",
        "cf3": "20.0.51.159",
        "cf4": "20.0.51.160",
        "disks_cnt": 36,
        "mgmtip": "172.22.117.21",
        "name": "cde465-b5",
        "password": "rootroot",
        "user": "root"
    },
    "cosbench1": {
        "interip": "20.0.50.36",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.36",
        "name": "cosben-a6",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench2": {
        "interip": "20.0.50.37",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.37",
        "name": "cosben-b1",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench3": {
        "interip": "20.0.50.38",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.38",
        "name": "cosben-b2",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench4": {
        "interip": "20.0.50.39",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.39",
        "name": "cosben-b3",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench5": {
        "interip": "20.0.50.40",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.40",
        "name": "cosben-b4",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench6": {
        "interip": "20.0.50.41",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.41",
        "name": "cosben-b5",
        "password": "cisco123",
        "user": "root"
    },
    "cosbench7": {
        "interip": "20.0.50.42",
        "jmeter": "/home/cosbench/jmeter/bin/jmeter",
        "mgmtip": "172.22.117.42",
        "name": "cosben-b6",
        "password": "cisco123",
        "user": "root"
    },
    "pam1": {
        "mgmtip": "172.22.117.67",
        "name": "charter-ha-pam2",
        "password": "default",
        "user": "admin"
    },
    "testbed": {
        "name": "charter_tb"
    }
}


def traverse(obj):
    if isinstance(obj, dict):
        return {k: traverse(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [traverse(elem) for elem in obj]
    else:
        return obj  # no container, just values (str, int, float)


def parse_to_jstree_format(dictory):
    level0_list = list()
    level1_list = list()

    for key1, value1 in dictory.items():
        level1_dict = {'text': key1}

        level2_list = list()
        if isinstance(value1, dict):
            for key2, value2 in value1.items():
                level2_list.append({'text': '%s : %s'%(key2,value2)})
            # level1_list.append({key1: level2_list})
            level1_dict.update({'children': level2_list})
        else:
            level1_list.append({key1: value1})

        level0_list.append(level1_dict)
    return level0_list



if  __name__=="__main__":

    # traverse(jdict)
    rtn_lst = parse_to_jstree_format(jdict)
    for dt in rtn_lst:
        print(dt)