from unittest import TestCase

from entities.link import Link


class TestLink(TestCase):
    def test_hi(self):
        l = Link()
        print(l)
