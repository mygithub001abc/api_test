# 主要实现的是用户添加，修改，删除，查询
from cacheout import Cache

from loguru import logger

from api.base import Base


class UserManager(Base):

    # 初始化管理员路径
    def __init__(self):

        # 新增管理员url
        self.add_user_url = self.get_url('/admin/admin/create')

        # 查询管理员url
        self.search_user_url = self.get_url('/admin/admin/list?page=1&limit=20&sort=add_time&order=desc')

        # 编辑管理员url
        self.edit_user_url = self.get_url('/admin/admin/update')

        # 删除管理员url
        self.delete_user_url = self.get_url('/admin/admin/delete')

    # 新增管理员
    def add_user(self, username, password, **kwargs):
        """
        请求添加管理员的接口
        :return: 返回添加管理员json数据
        """
        user_data = {'username': username, 'password': password}
        if kwargs:
            logger.info("添加管理员可选参数：{}", **kwargs)
            user_data.update(**kwargs)
        return self.post(self.add_user_url, user_data)

    # 查询管理员
    def search_user(self):
        """
        请求查询管理员接口
        :return: 返回查询管理员json数据
        """
        return self.get(self.search_user_url)

    # 修改管理员
    def edit_user(self, id, username, password, **kwargs):
        """
        请求修改管理员接口
        :return: 返回修改管理员json数据
        """
        user_data = {'id': id, 'username': username, 'password': password}
        if kwargs:
            logger.info("修改管理员可选参数：{}", **kwargs)
            user_data.update(**kwargs)
        return self.post(self.edit_user_url, user_data)

    # 删除管理员
    def delete_user(self, id, username, **kwargs):
        """
        请求删除管理员接口
        :return: 返回删除管理员json数据
        """
        user_data = {'id': id, 'username': username}
        if kwargs:
            logger.info("删除管理员可选参数：{}", **kwargs)
            user_data.update(**kwargs)
        return self.post(self.delete_user_url, user_data)


