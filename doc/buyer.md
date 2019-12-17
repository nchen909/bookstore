## 买家下单

#### URL：
POST http://[address]/buyer/new_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
store_id | string | 商铺ID | N
books | class | 书籍购买列表 | N

books数组：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 初始库存，大于等于0 | N
count | string | 购买数量 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 下单成功
5XX | 买家用户ID不存在
5XX | 商铺ID不存在
5XX | 购买的图书不存在
5XX | 商品库存不足

##### Body:
```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单号，只有返回200时才有效 | N


## 买家付款

#### URL：
POST http://[address]/buyer/payment

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "order_id": "order_id"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
order_id | string | 订单ID | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 付款成功
5XX | 账户余额不足
5XX | 无效参数


## 买家充值

#### URL：
POST http://[address]/buyer/add_funds

#### Request



##### Body:
```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
add_value | int | 充值金额，以分为单位 | N


Status Code:

码 | 描述
--- | ---
200 | 充值成功
401 | 授权失败
5XX | 无效参数

## 买家收货


#### URL

POST http://[address]/buyer/receive_books

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "buyer_id": "$buyerer id$",
  "order_id": "$order id$"
}
```
key | 类型 | 描述 | 是否可为空
---|---|---|---
buyer_id | string | 买家用户ID | N
order_id | string | 订单ID | N
#### Response

Status Code:

码 | 描述
--- | ---
200 | 成功
522| 未发货
523 | 已收货
401| 授权失败
518 | 用户id，订单不匹配

## 搜索历史订单

#### URL：
POST http://[address]/buyer/search_order

#### Request
Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N
##### Body:
```json
{
  "buyer_id": "user_id"
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
buyer_id | string | 买家用户ID | N

Status Code:

码 | 描述
--- | ---
200 | 搜索成功
511 | 无效用户id

##### 搜索返回格式：
```json
[
 { "order_id": "order_id1",
  "status": "status",
  "pt": "time",
  "total_price": 432,
  "detail": [
    {
      "title": "三毛",
      "count": 1,
      "price": 23
    },
    {
      "title": "安妮的世界",
      "count": 1,
      "price": 23
    }
  ]
  },
  { "order_id": "order_id2",
  "status": "status",
  "pt": "time",
  "total_price": 432,
  "detail": [
    {
      "title": "鸡汤",
      "count": 1,
      "price": 23
    },
    {
      "title": "小王子",
      "count": 1,
      "price": 23
    }
  ]
  }
]  

```
