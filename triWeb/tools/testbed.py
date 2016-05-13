import yaml



class TestBed:
    def load(self, yaml_file):
        with open(yaml_file) as f:
            cf_dict = yaml.load(f)
        return cf_dict

    # parse configure dictory to json tree
    def parse_to_json_tree(self, dictory):
        level0_list = list()
        level1_list = list()

        for key1, value1 in dictory.items():
            level1_dict = {'text': key1}

            level2_list = list()
            if isinstance(value1, dict):
                for key2, value2 in value1.items():
                    level2_list.append({'text': '%s : %s' % (key2, value2)})
                # level1_list.append({key1: level2_list})
                level1_dict.update({'children': level2_list})
            else:
                level1_list.append({key1: value1})

            level0_list.append(level1_dict)

        return level0_list
