import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto.settings")

import django

django.setup()


def main():
    from triWeb.models import TestBedModel, DeviceModel
    from triWeb.tools.testbed import TestBed
    import re

    TestBedModel.objects.all().delete()
    DeviceModel.objects.all().delete()

    tb_dir = "/Users/chenxuan/Workspace/django/auto/triWeb/testbeds"
    fps = os.listdir(tb_dir)

    for fp in fps:
        abs_fp = os.path.join(tb_dir,fp)
        tb = TestBed()
        conf_dict = tb.load(abs_fp)

        # print(conf_dict)
        if 'testbed' in conf_dict and 'name' in conf_dict['testbed']:
            testbed_name = conf_dict['testbed']['name']
        else:
            testbed_name = 'test'
        tb,flag=TestBedModel.objects.get_or_create(name=testbed_name,path=fp)

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
                                                  ip=subDict['mgmtip'],
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
