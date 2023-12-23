| **课程名称：当代数据管理系统** | **项目名称：bookstore-SQL** |
| --- | --- |
| **姓名：高宇菲** | **学号：10215501422** |

<a name="svgEd"></a>
# 一，项目概述
本项目使用的是简化的MVC架构，实现了用户管理，买家购买和订单管理，卖家开店和订单处理，搜索图书和自动取消订单等功能。<br />本项目使用的是Postgresql数据库、python语言和psycopg2库来连接数据库；考虑到orm并不符合一般思维，时间较紧迫，没有使用这种实现方式。<br />**二，项目运行**

1. 启动Postgresql服务，建立be数据库
2. 确保fe/data下有book.db
3. 在be/model/store.py修改数据库连接
4. 运行以下命令
```python
pip install requestments.txt
python app.py
```
<a name="atgQ6"></a>
# 三，数据库设计
<a name="rZHbq"></a>
## 3.1 ER图
![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703167900792-b073a006-5cee-4b35-822f-2c510e9d9289.png#averageHue=%23fcfbfa&clientId=u9cefa7a8-9f38-4&from=paste&height=657&id=u38b0422f&originHeight=985&originWidth=1196&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=134463&status=done&style=none&taskId=u0e6618c2-cdb3-4c7a-9345-c3c334a843f&title=&width=797.3333333333334)<br />在我的数据库设计中，共有四个对象（用户，商店，书籍，订单），没有多值属性；有两个多对多关系（库存，购买）。
<a name="gtGxG"></a>
## 3.2 从ER图导出关系模式
根据ER图，自然生成六张数据表，以下是数据表的字段和结构：<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703168890365-4577b0c9-c72f-4c75-b5c1-841e4ff2da48.png#averageHue=%23fdfcfc&clientId=u9cefa7a8-9f38-4&from=paste&height=534&id=udfc835cf&originHeight=801&originWidth=1129&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=71943&status=done&style=none&taskId=uc55ae4ac-6812-492c-b0b3-5d79d6a752a&title=&width=752.6666666666666)

数据schema：<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338082344-61f9f5b5-a3d4-403b-908f-5f9421f2cdd0.png#averageHue=%23110f0e&clientId=u721df291-075f-4&from=paste&height=441&id=u9617b9ca&originHeight=661&originWidth=1239&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=108262&status=done&style=none&taskId=u037d3015-3c3c-475f-869d-cf8618c7d11&title=&width=826)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338099553-b4a6eaa2-038a-4f97-84a9-2d2fb05929c4.png#averageHue=%23110f0e&clientId=u721df291-075f-4&from=paste&height=254&id=u121a613e&originHeight=381&originWidth=1652&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=72096&status=done&style=none&taskId=u1c988fd0-aef3-474d-8878-1dfe76926ed&title=&width=1101.3333333333333)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338118038-50725f43-a202-4fd6-9c22-3a514cb7c966.png#averageHue=%2312100f&clientId=u721df291-075f-4&from=paste&height=235&id=ue72c7130&originHeight=353&originWidth=1301&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=61164&status=done&style=none&taskId=ua2a2e988-77ea-4b5b-8340-036cc90ada5&title=&width=867.3333333333334)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338140356-661d87bf-7fa1-4be6-829d-630880bc7edc.png#averageHue=%23110f0e&clientId=u721df291-075f-4&from=paste&height=245&id=u62089a80&originHeight=367&originWidth=1266&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=59786&status=done&style=none&taskId=u9c16a24f-d1f6-4de6-b6b6-5896581009c&title=&width=844)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338161491-039fb5d1-2af8-4232-a2a7-b6601f3ff829.png#averageHue=%230f0e0e&clientId=u721df291-075f-4&from=paste&height=339&id=u37cc2c81&originHeight=509&originWidth=1880&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=91689&status=done&style=none&taskId=uefc8acfc-e9d5-4c37-8654-173badbf8b9&title=&width=1253.3333333333333)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703338183668-d81814ff-8bd7-497d-a298-d5624b47e5b6.png#averageHue=%2311100f&clientId=u721df291-075f-4&from=paste&height=215&id=u7b22429b&originHeight=322&originWidth=1099&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=47369&status=done&style=none&taskId=u85d78d95-1ce3-4945-bd63-b251883d665&title=&width=732.6666666666666)<br />**冗余：**

- book表中的`_ts`字段（用于搜索）
- order表中的price字段。这个字段代表该订单所购买书籍的总价，可以通过订单信息计算出来。为了加速执行，提升用户体验，在新建订单的时候就顺便计算并存入数据库。

**索引：**

- store库存表，order_book订单-书籍表（两个表示“联系”的表）使用双键索引，其余表都是ID索引。
- 没有使用额外的索引，原因是在建表时已经考虑到了查询等因素，故不建立其他索引也能有较好的表现。
<a name="EbZ8m"></a>
## 3.3 与文档数据库相比，这个数据库的改动：

- **减少重复的书籍信息，进一步符合数据库规范。**在文档数据库中，我们将书籍看做**一“本”书，**book_id和bookstore_id是复合索引**，**那么book_id和bookstore_id只要有一个不同，书籍的所以基本信息就要存一遍。关系数据库的设计中，book和bookstore是分离的，book表中仅包含**一“部”书**的信息，而bookstore表中仅包含商店ID和店主ID，“库存”关系是通过store表体现的。

这样做的好处：

   - **减少重复存储书籍信息**，因为不同的店可能上架相同的书籍，这样设计数据库，只有第一个上架一本书的卖家才需要插入book表，其他卖家可以跳过这一步。
- **主体之间关系的存储方式不同。**文档数据库较灵活，可以存储列表、允许嵌套，所以可以在订单文档集中直接存一个列表，里面是所有的该订单购买的书籍；但是关系型数据库必须新建一张表。这是由数据库类型天然决定的。
- **顺便计算了订单总额，一劳永逸。**

这样做的好处：

   - **减少访问数据库的次数**，提高用户体验；
   - **及时记录下单时价格**，防止之后价格变动引起业务错误。
- **增加了外键（如下图）**

         ![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703313384032-d3a63f1c-b77c-4348-9b10-e5ae11ecf260.png#averageHue=%23fcfbfb&clientId=u721df291-075f-4&from=paste&height=453&id=ufe1e97ed&originHeight=786&originWidth=794&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=60125&status=done&style=none&taskId=u5debeed9-d700-4524-80c5-229b775a0d0&title=&width=457.3333740234375)<br />增加外键约束的好处：

   - 保证了业务正确性，一定程度避免脏数据
   - 减少了**存在性检查以及各种检查**，提高了效率。
<a name="gFt6Q"></a>
# 四，功能实现
<a name="x0RI2"></a>
## 4.1 前60%
前60%首先要实现数据库的连接和建表。建表的所有sql保存在create_be.sql文件中。在`be/store.py`中，检查be数据库是否为空，如果为空就执行`create_be.sql`，否则就不执行。
```python
    def init_tables(self):
        try:
            cursor = self.database.cursor()
            cursor.execute(   # 判断数据库是否为空
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'book'
                );
                """
            )
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                with open('be/model/create_be.sql', 'r', encoding="utf-8") as file:
                    sql_commands = file.read()
                cursor.execute(sql_commands)

    def get_db_conn(self):
        return self.database.cursor()
	#  增加的
    def get_db(self):
        return self.database
```
考虑到psycopg2库的设计，后面需要psycopg2.connect对象来执行事务提交，所以我增加了一个get_db函数（如上），并在be/conn.py中调用：
```python
# be/store.py
def get_db():
    global database_instance
    return database_instance.get_db()

# be/conn.py 中调用
class DBConn:
    def __init__(self):
        self.database = store.get_db()
        self.cursor = store.get_db_conn()
```
在`be/conn.py`中进行的用户、商店、书籍的存在性检查设计简单的SQL语句，不再赘述。
<a name="NhLuw"></a>
### 4.1.1 用户权限接口
`view/auth.py`中的接口，共5个，分别是注册，注销，登录，登出，更改密码。
<a name="YyZmC"></a>
#### 注册

- 功能实现
   1. 插入新用户 (user_id, password, balance, token, terminal) 到 users 表中
   2. 如果用户存在，会触发psycopg2.error
- 性能分析：一次插入user表，**访问数据库一次**
<a name="uYd1f"></a>
#### 登录

- 功能实现
   1. 密码检查，token检查
   2. 如果均正确就登录成功
- 性能分析：一次查询 user表, 一次更新 user表，**访问数据库两次**
<a name="aCrSs"></a>
#### 登出

- 功能实现
   1. 根据 user_id 在 users table 中查询，判断登录token是否失效
   2. 更新用户 token，terminal
- 性能分析：一次查询 user表，一次更新 user表，**访问数据库两次**
<a name="r0C3l"></a>
#### 注销

- 功能实现
   1. 核对密码
   2. 删除 users table中该用户条目
- 性能分析：一次查询 user表, 一次更新 user表 ，**访问数据库两次**
<a name="tNnOV"></a>
#### 更改密码

- 功能实现
   1. 根据 user_id 在 users table 中判断用户原先密码和用户新密码是否相同
   2. 若相同，更新password，token, terminal
   3. 若不同，则更新 users table 中该用户的 password
- 性能分析：一次查询 user表, 一次更新 user表，**访问两次数据库**
<a name="tdtQF"></a>
### 4.1.2 买家用户接口
因为使用了外键约束，之前所有的存在性检查全部汇集到`psycopg2.Error 528`, 所以增加一个错误：
```python
error_code = {
    528: "数据库操作出错，请检查您提供的用户、商店或订单是否存在",
}
def error_database(e):
    return 528, e+error_code[528]
```
<a name="TktYC"></a>
#### 下单`new_order`接口

1. 通过`user_id`，`store_id`，和唯一标识符相连生成`uid`，作为订单ID；
2. 在`order表`中得到该商店的书籍库存和价格
3. 对每一本书，若查询成功，那么就再检查是否库存充足；
4. 若符合条件，就减少商店中的库存数量，并累加价格；
5. 最后，在`order表`中插入以下信息, 其中设置30分钟内付款：
```python
create_time = self.get_current_time()
pay_ddl = self.get_time_after_30_min() 
status = 0  # 0: 未支付, 1: 已支付未发货, 2: 已发货未收货, 3: 已收货, 4: 已取消
self.cursor.execute(
    'INSERT INTO "order"(order_id, user_id, store_id, create_time, pay_ddl, status, price) '
    "VALUES(%s, %s, %s, %s, %s, %s, %s);",
    (uid, user_id, store_id, create_time, pay_ddl, status, order_price),
)
```
性能分析：（1（插入新订单）+3*k（k是买书数量））次访问数据库
<a name="w1xKz"></a>
#### 支付`payment接口`

1. 获取购买的商店和价格
2. 核对密码后，检查余额是否充足
3. 若足够付款，就减少用户的balance, 相应增加卖家balance
4. 最后修改订单状态信息；

性能分析：访问6次数据库
<a name="PgGIw"></a>
#### 充值接口`add_funds`

1. 从`user表`中查询密码并核对用户密码。
2. 若密码正确，那么就在`user表`中更新用户余额；

性能分析：2次访问数据库
<a name="ACfU1"></a>
### 4.1.3 卖家用户接口
<a name="cEqt5"></a>
#### 创建商店`create_store接口`

1. 检查token
2. 将store_id和user_id插入`store表`；

性能分析：访问两次数据库
<a name="ab5bn"></a>
#### 商家图书`add_book接口`
实现以下功能：

1. 解析并插入`书籍信息`到`book表`中；
2. 将`book_id`,`store_id`, `stock_level`, `price`插入库存表中。

性能分析：访问两次数据库
<a name="FgIvX"></a>
#### 添加库存`add_stock_level接口`
实现以下功能：

1. 根据`store_id`、`book_id`增加stock_level。

性能分析：访问一次数据库
<a name="cMWzw"></a>
### 4.1.4 前60% 测试结果
![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1702902681731-f29b8734-38c6-42a3-89d4-fd1e1711f671.png#averageHue=%23f3f3f1&clientId=u2ecfeac2-7e20-4&from=paste&height=22&id=qS8aI&originHeight=33&originWidth=1220&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=4401&status=done&style=none&taskId=ua76b997d-dc48-4834-a554-772e5c7c4d2&title=&width=813.3333333333334)
```python
Name                              Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------
be\__init__.py                        0      0      0      0   100%
be\model\__init__.py                  0      0      0      0   100%
be\model\buyer.py                   113     24     44     10    75%
be\model\db_conn.py                  23      0      6      0   100%
be\model\error.py                    23      2      0      0    91%
be\model\seller.py                   55     14     24      1    73%
be\model\store.py                    32      3      0      0    91%
be\model\user.py                    119     23     38      6    76%
be\serve.py                          35      1      2      1    95%
be\view\__init__.py                   0      0      0      0   100%
be\view\auth.py                      43      0      0      0   100%
be\view\buyer.py                     37      0      2      0   100%
be\view\seller.py                    31      0      0      0   100%
fe\__init__.py                        0      0      0      0   100%
fe\access\__init__.py                 0      0      0      0   100%
fe\access\auth.py                    33      0      0      0   100%
fe\access\book.py                    70      1     12      2    96%
fe\access\buyer.py                   39      0      4      0   100%
fe\access\new_buyer.py                8      0      0      0   100%
fe\access\new_seller.py               8      0      0      0   100%
fe\access\seller.py                  31      0      0      0   100%
fe\bench\__init__.py                  0      0      0      0   100%
fe\bench\run.py                      13      0      6      0   100%
fe\bench\session.py                  47      0     12      1    98%
fe\bench\workload.py                125      1     22      2    98%
fe\conf.py                           11      0      0      0   100%
fe\conftest.py                       17      0      0      0   100%
fe\test\gen_book_data.py             49      1     16      1    97%
fe\test\test_add_book.py             37      0     10      0   100%
fe\test\test_add_funds.py            23      0      0      0   100%
fe\test\test_add_stock_level.py      45      0      8      0   100%
fe\test\test_bench.py                 6      2      0      0    67%
fe\test\test_create_store.py         20      0      0      0   100%
fe\test\test_login.py                28      0      0      0   100%
fe\test\test_new_order.py            40      0      0      0   100%
fe\test\test_password.py             33      0      0      0   100%
fe\test\test_payment.py              60      1      4      1    97%
fe\test\test_register.py             31      0      0      0   100%
-------------------------------------------------------------------
TOTAL                              1285     73    210     25    92%
```
<a name="IInxF"></a>
## 4.2 后40%
后40%接口文档在`doc/addtional_api.md`(由APIfox导出) 中，在此不再占用篇幅。
<a name="Q88tJ"></a>
### 4.2.1 发货 -> 收货
考虑到后续订单状态查询和取消的需求，设定order文档集中的state取值为以下四种。

| **state** | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| **含义** | 下单未付款 | 已付款未发货 | 已发货未收货 | 已收货 | 已取消 |

所以当卖家发货以及买家收货时，只需要修改相应order条目的state即可。但是需要注意的是，订单状态的修改是**无法越级**的（无法从状态0跳转到状态2）。
<a name="u5xyf"></a>
#### 发货

1. 根据订单号获取订单状态
2. 检查订单状态是否为已支付
3. 更新订单状态为已发货
<a name="vhtg5"></a>
#### 收货

1. 根据订单号获取订单状态
2. 检查订单状态是否为已发货
3. 更新订单状态为已收货
<a name="zpM8C"></a>
#### 测试实现

1. 测试正常情况
2. 测试用户token失效的情况
3. 测试订单状态错误的情况
4. 测试订单号错误的情况

test_receive.py与test_send.py大同小异，在此不再赘述。
<a name="BD7Bw"></a>
### 4.2.2 图书搜索
<a name="G4AEq"></a>
#### 需求分析
搜索功能可以通过`like`语句实现，但是这样做有三个明显的缺点：

- Seq Scan， O(n)复杂度。
- 包含了所有出现过关键词的数据，不能做到精确搜索。
- 当有多个关键词时，表达式较复杂，不利于维护。

因此，考虑使用全文索引。<br />下图是是否创建索引在100条数据上的小测试：<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1702948056169-0f3b9f22-8646-4f63-87f8-f1afc4f73a76.png#averageHue=%23100f0e&clientId=u54e47b6a-066a-4&from=paste&height=303&id=ua0feb255&originHeight=455&originWidth=1531&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=77119&status=done&style=none&taskId=u0cde8dcd-098f-4824-b9ab-176a8ba8490&title=&width=1020.6666666666666)
<a name="RkTY6"></a>
#### 分析Postgresql支持情况
Postgresql的全文搜索一般解决方案是使用**GIN索引+tsvector+tsquery。**但经查阅资料和实际试验，Postgresql**不支持中文的分词**，仅支持空格和标点分词。所以不论何种语言，Postgresql都会按照**空格**分词，而这样的分词结果往往不是用户的搜索关键词。zhparser是常用的PG数据库中文分词插件，但是该插件对win系统并不友好。常用的中文分词库还有jieba。<br />我还发现Postgersql可以自动去除标点符号，这为我们提供了便利。
<a name="CsaOv"></a>
#### 拟解决方案
使用结巴中文分词，对题目，标签，目录，内容进行分词后，使用空格分隔，另外存储到一个book表中名为`_ts`的条目，数据类型为tsvector**（这是一个冗余条目）**。在这个冗余条目上建立GIN索引。这个过程在卖家添加书籍时完成。
<a name="ssdf5"></a>
#### 过程：
<a name="dTTlK"></a>
#### 准备工作
a. 在建表时，book表多添加一个类型为“_ts”的字段，用于存储所有搜索源的分词；<br />b. 在建完book表后，加一个添加GIN索引的操作。
```python
cursor.execute(
                "CREATE INDEX IF NOT EXISTS book_ts_idx ON book USING gin(_ts);"
            )
```
<a name="sAiqM"></a>
#### jieba分词并添加冗余属性
在卖家be/model/utils.py实现字段分词和汇聚函数cut，然后在seller添加书籍时，调用cut, 并和书籍信息一同插入book表。
```python
self.cursor.execute(
    "SELECT * FROM book WHERE id = %s", (book_id,)
)
if self.cursor.fetchone() is None: 
    tsvec = cut(book_info)   # 返回一个空格分割的字符串
    self.cursor.execute(
        'INSERT into book(id, title, publisher, author, original_title, translator, pub_year, pages,currency_unit, binding, isbn, author_intro, book_intro, "content", tags, picture)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (
            book_id, 
            book_info['title'], 
            ..., 
            tsvec
        ),
    )
```
效果如下：![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703254720638-1ae7357a-9359-4808-9f28-3bb67dd114fb.png#averageHue=%23e8efbf&clientId=u5f72ddc5-4afc-4&from=paste&height=488&id=u6d2d76ed&originHeight=732&originWidth=1780&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=302076&status=done&style=none&taskId=u58aecb96-5b1e-4b0d-a062-cd2cfcdec47&title=&width=1186.6666666666667)
<a name="E0Fv7"></a>
#### 实现搜索

- 对搜索实现两个接口，分别是`search_global`, `search_store`;
- `search_global` 接受三个参数，`keyword`，`pageIndex`(可缺省) ,`pageSize`(可缺省) ;`search_store`还要接受`store_id`;
- 首先，对用户输入的keyword分词处理成tsquery接受的格式，然后调用使用全文索引查询数据库：
```python
key = jieba.cut(key)
key = " | ".join(key)
offset = (int(pageIndex) - 1) * int(pageSize)
self.cursor.execute(
    "select * from book where _ts @@ %s::tsquery LIMIT %s OFFSET %s",
    (key, pageSize, offset),
)
```

- 店内搜索还要检查店铺是否存在：
```python
if not self.store_id_exist(store_id):
    return error.error_non_exist_store_id(store_id) + ([],)
key = jieba.cut(key)
key = " | ".join(key)
offset = (int(pageIndex) - 1) * int(pageSize)
self.cursor.execute(
    "select * from book where _ts @@ %s::tsquery LIMIT %s OFFSET %s",
    (key, pageSize, offset),
)
```

- 如果pageIndex为None或page为0，默认第一页；如果pageSize为None或page为0，默认5条数据。
<a name="qxl9q"></a>
#### 效果展示
![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703255161335-620128c5-05a1-4896-89a4-9ec7f5fcac3b.png#averageHue=%23fefefd&clientId=u5f72ddc5-4afc-4&from=paste&height=557&id=u11ee984b&originHeight=835&originWidth=1423&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=176806&status=done&style=none&taskId=u2afcc612-315c-4715-b141-69c40a47eb2&title=&width=948.6666666666666)
<a name="WLj15"></a>
#### 测试
对pageIndex和pageSize置空、小于1、非数字的情况都做了测试；对参数缺失情况做了测试；对会让非法搜索关键词也做了测试。
<a name="f0pM7"></a>
#### 性能分析
全局搜索访问数据库一次，店铺搜索访问数据库两次，都可以视为![](https://cdn.nlark.com/yuque/__latex/a2006f1ac61cb1902beacb3e29fff089.svg#card=math&code=O%281%29&id=RR5YJ)复杂度。
<a name="pYzTS"></a>
### 4.2.3 订单搜索
这部分实现较简单，我的设计是如果搜索状态为-1，就搜索全部订单，否则搜索对应状态的订单。
```python
if search_state == -1:
    self.cursor.execute(
        'SELECT * FROM "order" WHERE user_id = %s', (user_id,)
    )
else:
    self.cursor.execute(
        'SELECT * FROM "order" WHERE user_id = %s and status = %s',
        (user_id, search_state),
    )
```
<a name="OApR7"></a>
### 4.2.4 订单取消
<a name="ogokU"></a>
#### 手动取消：
手动取消通过发送请求实现

- 根据订单号取出订单状态，如果订单状态已经是取消状态了，就直接返回200
- 如果不是，就相应地退款，还原库存。
<a name="kuNnY"></a>
#### 自动取消：
自动取消目的是取消超时未支付的订单。可以新建一个线程实现，也可以在每次调用接口之前检查是否有超时。这里介绍多线程的解决方式：<br />创建文件`autocancel.py`：
```python
from be.model.buyer import Buyer
def delete_order_time():
    buyer = Buyer()
    while True:
        buyer.delete_order_time()
if __name__ == '__main__':
    delete_order_time()
```
实现自动取消订单的功能可以在`app.py`中单开一个进程运行自动取消订单的程序`autocancel.py`，然后在运行`app.run()`
```python
if __name__ == '__main__':
    p = multiprocessing.Process(target=subprocess.call, args=(["python", "auto_cancel.py"],))
    p.start()
    server.be_run()
```
<a name="ZNler"></a>
### 4.3 总体测试结果
经过一番努力，**在保证业务逻辑和必要的错误捕捉的前提下，**将覆盖率提升到了95%。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703333734840-a6ef1682-9186-43ba-b5d3-c584106d83ad.png#averageHue=%23f3f1ed&clientId=u721df291-075f-4&from=paste&height=17&id=u2bf57724&originHeight=26&originWidth=1178&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=5303&status=done&style=none&taskId=u09593ad8-80eb-4362-b3cd-ae805240ddc&title=&width=785.3333333333334)
```python
Name                              Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------
be\__init__.py                        0      0      0      0   100%
be\model\__init__.py                  0      0      0      0   100%
be\model\buyer.py                   215     31     64      5    84%
be\model\db_conn.py                  23      0      6      0   100%
be\model\error.py                    27      0      0      0   100%
be\model\seller.py                   75     14     26      2    80%
be\model\store.py                    31      3      2      1    88%
be\model\user.py                    115     23     30      2    77%
be\model\utils.py                    10      0      4      0   100%
be\serve.py                          35      1      2      1    95%
be\view\__init__.py                   0      0      0      0   100%
be\view\auth.py                      43      0      0      0   100%
be\view\buyer.py                     82      0      2      0   100%
be\view\seller.py                    40      0      0      0   100%
fe\__init__.py                        0      0      0      0   100%
fe\access\__init__.py                 0      0      0      0   100%
fe\access\auth.py                    31      0      0      0   100%
fe\access\book.py                    69      0     12      0   100%
fe\access\buyer.py                   71      0      2      0   100%
fe\access\new_buyer.py                8      0      0      0   100%
fe\access\new_seller.py               8      0      0      0   100%
fe\access\seller.py                  38      0      0      0   100%
fe\bench\__init__.py                  0      0      0      0   100%
fe\bench\run.py                      13      0      6      0   100%
fe\bench\session.py                  47      0     12      1    98%
fe\bench\workload.py                125      1     22      2    98%
fe\conf.py                           11      0      0      0   100%
fe\conftest.py                       17      0      0      0   100%
fe\test\gen_book_data.py             47      0     14      0   100%
fe\test\test_add_book.py             37      0     10      0   100%
fe\test\test_add_funds.py            23      0      0      0   100%
fe\test\test_add_stock_level.py      45      0      8      0   100%
fe\test\test_bench.py                 6      2      0      0    67%
fe\test\test_create_store.py         27      0      0      0   100%
fe\test\test_delete_order.py         59      0      2      0   100%
fe\test\test_login.py                28      0      0      0   100%
fe\test\test_new_order.py            40      0      0      0   100%
fe\test\test_password.py             33      0      0      0   100%
fe\test\test_payment.py              70      0      2      0   100%
fe\test\test_receive.py              59      0      2      0   100%
fe\test\test_register.py             31      0      0      0   100%
fe\test\test_search_global.py        54      0      0      0   100%
fe\test\test_search_order.py         67      0     10      0   100%
fe\test\test_search_store.py         59      0      2      0   100%
fe\test\test_send.py                 61      0      2      0   100%
fe\test\utils.py                     13      0      4      0   100%
-------------------------------------------------------------------
TOTAL                              1893     75    246     14    95%
```
<a name="XpGc2"></a>
# 五，实验心得

1. 文档数据库和关系型数据库区别和优势比较：

**关系数据库的优势：**

- **设计简单。**这次我几乎没有花时间在数据库设计上，因为对关系数据库来说，数据库结构是很明确的、固定的，不需要考虑吧关系存在哪一边。
- **存储高度结构化。**相比于文档数据库的半结构化，关系型数据库使用表格结构存储数据，易于保持严格一致性和完整性。
- **事务处理。**本次实验利用了Postgresql的事务处理，确保数据的一致性、隔离性、持久性和原子性（ACID属性）。这在我们的在线交易活动中非常重要。
- **外键和级联操作。**在关系型数据库中，可以容易地建立外键，可以保证数据的**一致性和完整性**。

**关系数据库的劣势：**

- **不够灵活。**我使用两个数据库后，最大的感觉是关系数据库不够灵活。所有的主键、外键、数据类型以及各种规则都要在一开始明确定义好；而且不能像文档数据库一样嵌套，有时为了得到一个字段值，就多增加一次访问开销。
- **不适合存图片等格式的文件。**关系数据库的设计就不是用来存大文件的；在里面存大文件会让数据库大小激增，导致查询速度下降。最好是存一个图片url， 图片存在其他服务器中。
2. 认识到团队合作的重要性。和上次作业对比，这种开发任务最好还是团队分工合作效率更高。
<a name="PKK45"></a>
# 六，实验亮点
**为了方便助教老师查阅，这里列出了实验的完成度和可加分项：**

1. 使用了版本控制， 有较好的版本控制规范 ：**+3**

以下是仓库提交截图，可以看到我每实现一个功能就提交一次，版本控制给我的开发提供了便利，允许我大胆实践自己的猜想，不担心丢失原来的版本。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703334986891-a1316c75-9348-4852-a461-4c0d4224bf5c.png#averageHue=%23fefdfd&clientId=u721df291-075f-4&from=paste&height=442&id=u5db4ecf0&originHeight=834&originWidth=520&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=65148&status=done&style=none&taskId=ucd63fda6-5a74-4625-8d48-76b4ed8870b&title=&width=275.66668701171875)![image.png](https://cdn.nlark.com/yuque/0/2023/png/34343420/1703335251988-eab0e95e-54c1-46d1-a84f-08f089f4355f.png#averageHue=%23fefdfd&clientId=u721df291-075f-4&from=paste&height=523&id=u04a35919&originHeight=836&originWidth=583&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=74343&status=done&style=none&taskId=u6f4bfd12-1b21-49dc-89a9-efc0d0a3816&title=&width=365)<br />这是github地址：[https://github.com/gyfffffff/BookStroe-SQL](https://github.com/gyfffffff/BookStroe-SQL)

2. 使用了测试驱动开发，以下是测试驱动开发的流程：

![](https://cdn.nlark.com/yuque/0/2023/jpeg/40512603/1699624262240-ad3b2d0d-a1a7-47e4-a420-96487c38bc32.jpeg)
<a name="YjlYW"></a>
#### TDD的优势：
a. 更高的软件质量：在编写代码之前编写测试用例，有助于捕获和修复潜在的问题和缺陷，编写更稳健更可靠的软件代码。<br />b. 更好的文档和示例：在编写代码之前，首先通过需求编写后端接口文档，然后根据文档编写测试用例。	该单元测试描述了每个功能的预期行为，快速理清逻辑。<br />c. 增量开发：TDD通过小步骤进行迭代开发，逐渐构建功能，避免了开发后期修复大量问题的发生。<br />在前60%中，我根据项目的已有的单元测试进行开发。在后40%中，我先确定功能需求，编写单元测试用例，然后根据测试用例进行新功能的开发。 **+2**

3. 有较高覆盖率：在不牺牲必要的错误捕捉前提下，精简代码，去除冗余，得到了95%的覆盖率。**+5**
4. 实现完整度：前60%和后40%的功能全部实现，测试全部通过；并对每个接口分析了访问次数。  **+1**
5. 正确地使用数据库和设计分析工具： **+1**
- [ER 图](#rZHbq)
- [从ER图导出关系模式](#gtGxG)
- 规范化，事务处理，索引 这些在数据库设计和功能实现时都有体现。
6. 从文档型数据库到关系型数据库的改动，以及改动的理由在上面已经写过。
<a name="hDJed"></a>
# 七，总结
本次实验我专注于后端开发和测试，

1. 对[关系数据库和文档数据库的区别](#XpGc2)有了更深入的理解，
2. 加深了对pytest使用上的理解。
3. 巩固了SQL的使用
4. 积累了一定实践经验和debug经验，

为今后学习打下基础。实验中遇到的困难大多予以解决。最后，程序通过了66个测试，覆盖率达 **95%**（不考虑except出现的严重数据库错误，覆盖率达到了 **97% **），取得了较为满意的结果。


