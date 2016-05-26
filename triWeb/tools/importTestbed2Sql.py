import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django

django.setup()


def main():
    from triWeb.models import TestBedModel, DeviceModel
    from triWeb.tools.testbed import TestBed
    import re

    fp = "/Users/chenxuan/Workspace/django/auto/triWeb/tools/testbed.yaml"

    tb = TestBed()
    conf_dict = tb.load(fp)

    # print(conf_dict)
    if 'testbed' in conf_dict and 'name' in conf_dict['testbed']:
        testbed_name = conf_dict['testbed']['name']
    else:
        testbed_name = 'test'
    tb,flag=TestBedModel.objects.get_or_create(name=testbed_name)

    for key, subDict in conf_dict.items():
        print("%s :  %s" % (key, subDict))

        if re.search('cos[0-9]+', key):
            DeviceModel.objects.get_or_create(name=subDict['name'],
                                              ip=subDict['mgmtip'],
                                              user=subDict['user'],
                                              password=subDict['password'],
                                              type='cos',
                                              testbed=tb,
                                              )
        if re.search('cosbench[0-9]+', key):
            DeviceModel.objects.get_or_create(name=subDict['name'],
                                              ip=subDict['interip'],
                                              user=subDict['user'],
                                              password=subDict['password'],
                                              type='cosbench',
                                              testbed=tb,
                                              )
        if re.search('pam[0-9]+', key):
            DeviceModel.objects.get_or_create(name=subDict['name'],
                                              ip=subDict['mgmtip'],
                                              user=subDict['user'],
                                              password=subDict['password'],
                                              type='pam',
                                              testbed=tb,
                                              )


if __name__ == '__main__':
    main()
