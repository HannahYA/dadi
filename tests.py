# -*- encoding=UTF-8 -*-

import unittest    #可以以一个单元测试例的方式跑测试
from dadi import app


class DadiTest(unittest.TestCase):
    def setUp(self):             #每次跑单元测试的时候都会跑，初始化
        app.config['TESTING'] = True
        self.app = app.test_client()    #这个app是测试的app，类似浏览器一样的东西
        print 'setUp'

    def tearDown(self):       #每次跑单元测试的时候都会跑，清理测试
        print 'teardown'
        pass

    def register(self, username, password):      #测试不再通过代码调用，而是通过http的方式
        return self.app.post('/reg/', data={"username":username, "password":password}, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login/', data={"username": username, "password": password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_logout_login(self):
        assert self.register("hello", "world").status_code == 200   #返回的是http的response
        assert '-hello' in self.app.open('/').data
        self.logout()
        assert '-hello' not in self.app.open('/').data
        self.login("hello", "world")
        assert '-hello' in self.app.open('/').data



    def test_profile(self):
        r = self.app.open('/profile/3/', follow_redirects=True)
        assert r.status_code == 200
        assert "password" in r.data
        self.register("hello2", "world")
        assert "hello2" in self.app.open('/profile/1/', follow_redirects=True).data