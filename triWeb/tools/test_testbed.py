from testbed import TestBed
import json

def test_load_yaml():
    fp = "./testbed.yaml"
    tb = TestBed()
    conf_dict = tb.load(fp)
    # for key, value in conf_dict.items():
    #     print("%s : %s" % (key, value))
    # print(conf_dict)

    # print(json.dumps(conf_dict,sort_keys=True,indent=4))
    rtn_lst = tb.parse_to_json_tree(conf_dict)
    print(rtn_lst)


if __name__ == "__main__":
    test_load_yaml()
