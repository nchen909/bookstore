1.  注册
sql操作:插入用户id，密码，用户余额，token，termial信息至usr表。


2. 登录
1. 根据usr_id获取用户密码。
2. 与用户输入密码对比。
3. 更新token，terminal

3. 登出
1. 根据usr_id获查询是否存在user
2. 更新token

4. 注销
删除对应user表中条目

5. 更改密码
1. 根据usr_id获取用户原有密码。
2. 与用户输入的旧密码对比。
3. 若相同，更新用户密码。

6. 创建店铺
1. 插入用户id，新建店铺id至user_store表。

7. 上架图书
1. 根据book_id从book表查询是否存在对应book
2. 若不存在，首先将书本信息插入book表。
3. 将store_id, book_id, 出售价格插入store表。

8. 添加库存
1. 根据store_id, book_id寻找对应店家书本库存，并在store表中更新库存。

9. 充值
1.  根据usr_id获取用户密码。
2. 与用户输入密码对比。
3. 若密码正确，在usr表中更新用户余额。

10. 下单
1. 根据订单信息（book_id,购买数量，store_id）在store表中查找商户中是否存在对应书籍和足够的库存。
2. 若满足条件，则在库存中减去对应的数量，并在new_order_detail表中插入对应的订单id，book_id，购买价格，购买数量。计算总价格。
3. 若所有条件都满足，则在new_order_pend表中插入对应的订单id，买家id，店铺id，订单总价，下单时间。

11. 付款
1. 查询在new_order_pend表中是否存在属于用户的代付订单，获取订单总价，商户id。
2. 若存在，根据usr_id获取用户密码。
3. 与用户输入密码对比。
3. 若密码正确，且用户余额大于代付价格，则付款成功，否则失败。
4. 若付款成功，则根据卖家id在usr表中给卖家增加余额。
5. 从new_order_pend表中删除对应订单信息，在new_order_paid表中加入订单信息。

12. 卖家发货
1. 根据order_id在new_order_paid表中查询对应的订单状态，店铺id。
2. 检查订单状态是否为待发货，店铺id与卖家id是否对应。
3. 若符合条件，则更新订单状态为已发货。

测试用例：
正常情况/user_id与store_id不对应/order_id不存在/订单已发货

13. 买家收货
1. 根据order_id在new_order_paid表中查询对应的订单状态，买家id
2. 检查订单状态是否为已发货，订单id与买家id是否对应。
3. 若符合条件，则更新订单状态为已收货。

测试用例：
正常情况/user_id与order_id不对应/order_id不存在/订单已收货

14. 买家查询订单记录
1. 根据buyrer_id在new_order_paid表中筛选记录，然后根据book_id,order_id对book表,new_order_paid表和new_order_detail表进行merge操作，获取订单id，所购书名，价格，数量，购买时间，订单状态。
2. 在待付款表中进行相同的操作。
3. 根据order_id将获取的记录包装成json对象，每个order下包含由所购书名，价格，数量包含的数组。

测试用例：
正常情况/user_id不存在/用户无购买记录

15. 买家取消订单
只有未发货情况下才能取消订单
1. 根据order_id和buyer_id在new_order_pend或new_order_paid表中获取商户id，订单价格。
2. 确定订单未发货后。根据order_id，store_id在new_order_detail表中筛选记录，然后根据book_id对store表和new_order_detail表进行merge操作，在store表中加回库存。
3. 在usr表中更新买家余额。
4. 在usr表中更新卖家余额。
5. 将订单信息加入new_order_cancel表中。
6. 在待付款表/已付款表中删除对应记录。

测试用例：
已付款/未付款/user_id不存在/已发货
