# coding=gbk
import sys
from abc import ABCMeta, abstractmethod

from memory_cache.algorithms import LRU
from memory_cache.storage import SimpleStorage

"""
������API
"""


class BaseCacheAPI(metaclass=ABCMeta):
    def __init__(self, storage=None, algorithms=None, max_size=1024, memory_limit=True):
        """
        :param storage: �洢�࣬[storage.BaseStorage]
        :param max_size: Ĭ�ϴ洢����ڴ�Ϊ1024�ֽڵ�����
        """
        self._storage = storage if storage is not None else SimpleStorage()
        self._alg = algorithms if algorithms is not None else LRU(self._storage)
        self.max_size = max_size
        self.memory_limit = memory_limit

    @abstractmethod
    def set(self, key, value, expire=-1):
        """
        �洢key-value����
        :param key: �洢��key
        :param value: �洢��key��Ӧ��ֵ
        :param expire: �洢��ʱʱ�䣬Ĭ���ǲ������
        """
        if self.memory_limit:
            if sys.getsizeof(value) > self.max_size:
                assert ValueError('�����ڴ�����')
        return self._alg.set(key, value, expire)

    @abstractmethod
    def get(self, key):
        """
        ����keyȡֵ
        :param key: �洢�ļ�
        :return: value: ��ȡ��ֵ
        """
        return self._alg.get(key)

    @abstractmethod
    def delete(self, key):
        """
        ɾ���洢�ļ�ֵ��
        :param key: ��
        :return: items: �洢�ļ���ֵ
        """
        return self._alg.delete(key)


class SimpleCacheAPI(BaseCacheAPI):
    def __init__(self, storage=None, algorithms=None, max_size=1024):
        super().__init__(storage, algorithms, max_size)

    def set(self, key, value, expire=-1):
        return super().set(key, value, expire)

    def get(self, key):
        return super().get(key)

    def delete(self, key):
        return super().delete(key)


if __name__ == '__main__':
    api = SimpleCacheAPI()
    SET_KEY = 'get_user_count'
    api.set(SET_KEY, 1)
    for i in range(10):
        count = api.get(SET_KEY)
        print(count)
        api.set(SET_KEY, count + 1)

    print(api.get(SET_KEY))
