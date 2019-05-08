from django.test import TestCase

from xml.etree.ElementTree import parse

# Create your tests here.

class mod_test(TestCase):
    def test_getxml(self):
        with open('CHECKINOUT.XML', 'r') as f:
            et = parse(f)
            print(et)
        root = et.getroot()
        checkinouts = []
        for childone in root:
            item = []
            for childtwo in childone:
                item.append(childtwo.text)
                # print(childtwo.tag, ":", childtwo.text)
            checkinouts.append(item)
            # print(item)
        print(len(checkinouts))
