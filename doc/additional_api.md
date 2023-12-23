---
title: Bookstore_SQL v1.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.17"

---

# Bookstore_SQL

> v1.0.0

Base URLs:

* <a href="http://dev-cn.your-api-server.com">开发环境: http://dev-cn.your-api-server.com</a>

# Authentication

# 后40%/seller

## POST 发货

POST /seller/send

卖家发货

> Body Parameters

```json
{
  "user_id": "string",
  "order_id": "string"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|token|header|string| no |用户token|
|body|body|object| no |none|
|» user_id|body|string| yes |卖家ID|
|» order_id|body|string| yes |要发货的订单ID|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|518|Unknown|无效订单|Inline|
|528|Unknown|数据库错误|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

# 后40%/buyer

## POST search_global

POST /buyer/search_global

根据传入的关键词进行全局的图书搜索，支持传入多个关键词和分页。

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|key|query|string| yes |搜索的关键词|
|pageIndex|query|integer| no |>0的整数，表示第几页|
|pageSize|query|integer| no |>0的整数，表示每页有几条数据|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|520|Unknown|缺少参数key|Inline|
|521|Unknown|无效的pageIndex或pageSize|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

## POST search_store

POST /buyer/search_store

根据传入的关键词和书店ID进行店内图书搜索，支持传入多个关键词和分页。

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|key|query|string| yes |搜索的关键词|
|pageIndex|query|integer| no |>0的整数，表示第几页|
|pageSize|query|integer| no |>0的整数，表示每页有几条数据|
|store_id|query|string| no |书店ID|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|520|Unknown|缺少参数key|Inline|
|521|Unknown|无效的pageIndex或pageSize|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

## POST delete_order

POST /buyer/delete_order

手动删除订单

> Body Parameters

```json
{
  "user_id": "string",
  "order_id": "string"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|body|body|object| no |none|
|» user_id|body|string| yes |用户ID|
|» order_id|body|string| yes |要删除的订单ID|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|认证失败|Inline|
|528|Unknown|数据库错误|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

## POST 搜索订单

POST /buyer/search_order

搜索历史订单

> Body Parameters

```json
{
  "buyer_id": "string",
  "search_state": "string"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|body|body|object| no |none|
|» buyer_id|body|string| yes |买家ID|
|» search_state|body|string| yes |搜索的订单状态；-1：全部订单， 0: 未支付, 1: 已支付未发货, 2: 已发货未收货, 3: 已收货, 4: 已取消|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|511|[Network Authentication Required](https://tools.ietf.org/html/rfc6585#section-6)|用户不存在|Inline|
|528|Unknown|数据库错误|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

## POST 收货

POST /buyer/receive

用户收货

> Body Parameters

```json
{
  "user_id": "string",
  "order_id": "string",
  "token": "string"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|body|body|object| no |none|
|» user_id|body|string| yes |买家ID|
|» order_id|body|string| yes |要收货的订单ID|
|» token|body|string| yes |用户token|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|认证失败|Inline|
|528|Unknown|数据库错误|Inline|
|530|Unknown|其他错误|Inline|

### Responses Data Schema

# Data Schema

