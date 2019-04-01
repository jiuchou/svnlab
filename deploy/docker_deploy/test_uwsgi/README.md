# uwsgi --version
2.0.17.1

# 测试 uwsgi 是否可用
1. 编辑 test_wsgi.py 文件
2. 执行如下命令
uwsgi --http-socket 10.6.5.100:8090 --wsgi-file test_wsgi.py
3. 打开网页地址 htp://10.6.5.100:8090, 查看网页是否存在"Hello World"
