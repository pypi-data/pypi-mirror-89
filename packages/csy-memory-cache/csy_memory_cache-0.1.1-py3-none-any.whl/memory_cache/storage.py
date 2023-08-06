# coding=gbk
from abc import ABCMeta, abstractmethod

"""
�洢��
"""


class BaseStorage(metaclass=ABCMeta):
    def __init__(self):
        self._hash_storage = dict()

    @abstractmethod
    def set(self, key, value):
        """
        �洢key-value����
        :param key: �洢��key
        :param value: �洢��key��Ӧ��ֵ
        """
        self._hash_storage[key] = value

    @abstractmethod
    def get(self, key):
        """
        ����keyȡֵ
        :param key: �洢�ļ�
        :return: value: ��ȡ��ֵ
        """
        return self._hash_storage.get(key, None)

    @abstractmethod
    def delete(self, key):
        """
        ɾ���洢�ļ�ֵ��
        :param key: ��
        :return: items: �洢�ļ���ֵ
        """
        value = self._hash_storage.get(key, None)
        del self._hash_storage[key]
        return value


class SimpleStorage(BaseStorage):
    def set(self, key, value):
        super(SimpleStorage, self).set(key, value)

    def get(self, key):
        return super(SimpleStorage, self).get(key)

    def delete(self, key):
        return super(SimpleStorage, self).delete(key)
