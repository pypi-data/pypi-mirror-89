import pytest   # noqa: F401


def assert_instance_exist(obj, attr):
    instance = obj.objects.get(email=attr)

    return instance.email == attr
