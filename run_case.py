import unittest

from HTMLTestRunner import HTMLTestRunner

test_report = 'test_report.html'

if __name__ == '__main__':
    # 创建一个套件
    suite = unittest.TestLoader().discover('cases', pattern='test*.py')

    with open(test_report, 'wb') as f:
        runner = HTMLTestRunner(f, title='wshop测试报告', description='简化版的测试报告')
        runner.run(suite)
