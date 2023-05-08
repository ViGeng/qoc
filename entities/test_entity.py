from unittest import TestCase

from entities.entity import Entity


class TestEntity(TestCase):
    pass


class TestEntity(TestCase):
    def test_hi(self):
        self.fail()

    def test_add(self):
        self.fail()

    def test_print(self):
        e = Entity(1, "name", "desc")
        print(e)