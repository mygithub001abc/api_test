"""
作用 ： 主要用于所有接口的公共功能，使用一个基类(父类)

功能1 ：处理url
功能2 ：重新封装get方法，post方法
功能3:  处理头信息
功能4 : 登录
"""
from cacheout import Cache  # 导入缓存类，使用前要创建实例对象
from setting import BASE_URL, LOGIN_INFO
from loguru import logger
import requests

cache = Cache()  # 创建cache对象


class Base(object):

    # 实现url拼接
    def get_url(self, path, params=None):
        """
        返回一个完整的url
        :param path: 表示接口路径，如：/admin/admin/update
        :param params: 表示查询参数，如：page=1&limit=20&sort=add_time&order=desc
        :return:full_url 表示返回一个完整的url 如 http://121.196.13.152:8080/admin/auth/login
        """
        if params:  # params有参数
            full_url = BASE_URL + path + params
            return full_url
        return BASE_URL + path

    # 重写get方法
    def get(self, url):
        response = requests.get(url, headers=self.get_headers())
        result = None
        try:
            result = response.json()
            logger.success("请求URL：{}, 返回结果：{}".format(url, result))
            return result
        except Exception as e:
            logger.error("请求get方法异常,返回数据为：{}".format(result))

    # 重写post方法
    def post(self, url, data):
        """
        在原来post方法的基础上，新增日志及返回json格式
        :param url:
        :param data: 请求体
        :return: json格式
        """
        response = requests.post(url, json=data, headers=self.get_headers())
        result = None
        try:
            result = response.json()
            logger.success("请求URL：{},请求参数：{},返回结果：{}".format(url, data, result))
            return result
        except Exception as e:
            logger.error("请求post方法异常,返回结果为：{}".format(result))

    # 实现所有头信息的处理
    def get_headers(self):
        """
        处理请求头
        :return: 返回的是字典格式的请求头，主要包括了Content-Type ,X-Litemall-Admin-Token
        """
        headers = {'Content-Type': 'application/json'}
        token = cache.get('token')  # 从缓存中获取token值
        if token:
            headers.update({'X-Litemall-Admin-Token': token})
            return headers
        return headers

    # 实现登录功能
    def login(self):
        """
        通过调用登录接口获取token值，将其进行缓存 ，其它接口使用时直接从缓存中取数.
        若没有取到，再调用登录 ，将token值放在缓存中。
        :return:
        """
        login_path = '/admin/auth/login'
        login_url = self.get_url(login_path)  # 获取完整登录接口地址
        result = self.post(login_url, LOGIN_INFO)  # 请求登录接口，返回json格式数据
        try:
            if result.get('errno') == 0:
                logger.info('请求登录接口成功')
                token = result.get('data').get('token')  # 从结果中获取token值
                cache.set('token', token)  # 将获取的token值设置到缓存中
            else:
                logger.error('登录失败：{}'.format(result))
                return None
        except Exception as e:
            logger.error('请求登录接口返回异常，异常数据：{}'.format(result))
            logger.error('报错信息：{}'.format(e))


if __name__ == '__main__':
    base = Base()
    # print(base.get_url('/admin/auth/login'))
    # print(base.get_url('/admin/admin/list', '?page=1&limit=20&sort=add_time&order=desc'))
    login_url = base.get_url('/admin/auth/login')
    login_data = {"username": "admin123", "password": "admin123"}
    print(base.post(login_url, login_data))
