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

## git版本控制
我们试用了 Orgnizations，在github.com/1012598167下建仓库并添加合作作者直接clone我们的项目，以及fork到另两位组员的仓库并向该仓库发起pull request请求三种方式，最终采用第二种三者地位都平等的方式。

![image-20191214224431689](README.assets/image-20191214224431689.png)

![image-20191214224628115](README.assets/image-20191214224628115.png)

理由是使用第二种方法可以避免发起pull request再手动通过的方式，实现多人快速平等合作。（可以直接clone github.com/1012598167，并可以直接push）并且每个人在origin/下维护自己的分支，如我的为origin/developercn，

![image-20191215123707874](README.assets/image-20191215123707874.png)

并及时pull request至master分支。

若有更新，成员确保及时fetch并merge -s ours origin/master到本地（每人的pycharm配置文件不同），成员自己本地会维护多个分支，以防本地编写错误的急救以及各功能的控制。

![image-20191214225745199](README.assets/image-20191214225745199.png)

具体使用如下：

- 个人控制：

本地维护多个branch，以作为备份和多功能的分离实现，若需合并再使用merge。

- 多人合作：

  个人提交：采用git push origin developerxxx的方式，上传至远程的个人分支，并及时pull request至master，而每次写自己部分的代码时：

  及时拉取至本地：

  先使用git fetch origin master，至origin/master,再get merge并进行检查，以确保每人编写代码时代码内容都为最新。并且不使用rebase，本地对除master外的分支只能从master中合并再编写。

![image-20191214231256923](README.assets/image-20191214231256923.png)

##测试驱动开发
即先写测试用例，再实现功能（写函数）
如test_add_book.py 先写test（助教给定），将self.seller.create_store self.seller.add_book留空，以作为待实现功能
再如test_search（新建）,将self.auth.search_author留空，后续再实现，这样便先有了程序的框架，结构不会紊乱

重视测试驱动开发、测试逻辑和效果展示 展示时先讲测试再讲功能实现
##注意事项

测试覆盖率请暂时移除 (覆盖率总时间没有代表性因为有延时1min 即test_new_order.py中test_auto_cancel函数，可以删) 
be\model2\try.py                     20     20      2      0     0%
be\model\buyer.py                   111    111     48      0     0%
be\model\db_conn.py                  22     22      6      0     0%
be\model\error.py                    25     25      0      0     0%
be\model\seller.py                   49     49     22      0     0%
be\model\user.py                    117    117     38      0     0%

## sqlite与postgresql数据传输
## 全文索引搜素（感知哈希+post拉取superset作图） 取消订单（自定义class起线程）
## 前端（专家系统）
## 部署到云端
## 反代分离负载及nginx

注：由于postgresql的zhparser在全文索引查询优化上也需要新建分词索引，所以手工创建索引也可
