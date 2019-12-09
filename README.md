# bookstore
## 第一次更新
1. 运行脚本命令
   ```
   ./script/test.sh
   ```
2. 吞吐量在app.log下
3. 数据库初始化（先建好bookstore数据库）
   ```
   python ./initialize_database/initialize_database.py
   ```
4. 第一次测试结果在test_result文件夹下
5. ER图和导出的关系模型在database_design文件下
6. 运行程序在app.py下添加
   ```
   import sys
   sys.path.append('D:\\印张悦\\大学\\学科\\大三第一学期\\数据库管理系统\\Homework3\\bookstore-master')
   ```
   中间为bookstore-master的位置
   然后在bookstore-master目录下
   ```
   python ./be/app.py
   ```
7. 请确保修改之前能运行脚本

