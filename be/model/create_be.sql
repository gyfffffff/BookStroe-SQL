-- public.book definition

-- Drop table

-- DROP TABLE book;

CREATE TABLE book (
	id text NOT NULL, -- 书籍id
	title text NULL, -- 书名
	publisher text NULL, -- 出版社
	author text NULL, -- 作者
	original_title text NULL, -- 原书名
	translator text NULL, -- 译者
	pub_year text NULL, -- 出版年份
	pages int4 NULL, -- 页数
	currency_unit text NULL, -- 货币单位
	binding text NULL, -- 装订
	isbn text NULL, -- ISBN
	author_intro text NULL, -- 作者介绍
	book_intro text NULL, -- 书籍介绍
	"content" text NULL, -- 内容
	tags text NULL, -- 标签
	picture text NULL, -- 图片
	"_ts" tsvector NULL, -- 用于搜索的分词
	CONSTRAINT book_pkey PRIMARY KEY (id)
);
CREATE INDEX book_ts_idx ON public.book USING gin (_ts);

-- Column comments

COMMENT ON COLUMN public.book.id IS '书籍id';
COMMENT ON COLUMN public.book.title IS '书名';
COMMENT ON COLUMN public.book.publisher IS '出版社';
COMMENT ON COLUMN public.book.author IS '作者';
COMMENT ON COLUMN public.book.original_title IS '原书名';
COMMENT ON COLUMN public.book.translator IS '译者';
COMMENT ON COLUMN public.book.pub_year IS '出版年份';
COMMENT ON COLUMN public.book.pages IS '页数';
COMMENT ON COLUMN public.book.currency_unit IS '货币单位';
COMMENT ON COLUMN public.book.binding IS '装订';
COMMENT ON COLUMN public.book.isbn IS 'ISBN';
COMMENT ON COLUMN public.book.author_intro IS '作者介绍';
COMMENT ON COLUMN public.book.book_intro IS '书籍介绍';
COMMENT ON COLUMN public.book."content" IS '内容';
COMMENT ON COLUMN public.book.tags IS '标签';
COMMENT ON COLUMN public.book.picture IS '图片';
COMMENT ON COLUMN public.book."_ts" IS '用于搜索的分词';


-- public."user" definition

-- Drop table

-- DROP TABLE "user";

CREATE TABLE "user" (
	user_id text NOT NULL, -- 用户ID
	"password" text NOT NULL, -- 密码
	balance int4 NOT NULL, -- 余额
	"token" text NULL, -- 用户token，登录时更新
	terminal text NULL, -- 登录终端
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

-- Column comments

COMMENT ON COLUMN public."user".user_id IS '用户ID';
COMMENT ON COLUMN public."user"."password" IS '密码';
COMMENT ON COLUMN public."user".balance IS '余额';
COMMENT ON COLUMN public."user"."token" IS '用户token，登录时更新';
COMMENT ON COLUMN public."user".terminal IS '登录终端';


-- public.bookstore definition

-- Drop table

-- DROP TABLE bookstore;

CREATE TABLE bookstore (
	store_id text NOT NULL, -- 书店ID
	user_id text NULL, -- 店主ID
	CONSTRAINT bookstore_pkey PRIMARY KEY (store_id),
	CONSTRAINT bookstore_fk FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE SET DEFAULT ON UPDATE CASCADE
);

-- Column comments

COMMENT ON COLUMN public.bookstore.store_id IS '书店ID';
COMMENT ON COLUMN public.bookstore.user_id IS '店主ID';


-- public."order" definition

-- Drop table

-- DROP TABLE "order";

CREATE TABLE "order" (
	order_id text NOT NULL, -- 订单ID
	user_id text NULL, -- 买家ID
	store_id text NULL, -- 书店ID
	create_time timestamp NULL, -- 订单创建时间
	pay_ddl timestamp NULL, -- 支付截止时间
	status int4 NULL, -- 订单状态，0: 未支付, 1: 已支付未发货, 2: 已发货未收货, 3: 已收货, 4: 已取消
	price int4 NULL, -- 订单总价
	CONSTRAINT order_pkey PRIMARY KEY (order_id),
	CONSTRAINT order_fk FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT order_fk_2 FOREIGN KEY (store_id) REFERENCES bookstore(store_id)
);

-- Column comments

COMMENT ON COLUMN public."order".order_id IS '订单ID';
COMMENT ON COLUMN public."order".user_id IS '买家ID';
COMMENT ON COLUMN public."order".store_id IS '书店ID';
COMMENT ON COLUMN public."order".create_time IS '订单创建时间';
COMMENT ON COLUMN public."order".pay_ddl IS '支付截止时间';
COMMENT ON COLUMN public."order".status IS '订单状态，0: 未支付, 1: 已支付未发货, 2: 已发货未收货, 3: 已收货, 4: 已取消';
COMMENT ON COLUMN public."order".price IS '订单总价';


-- public.order_book definition

-- Drop table

-- DROP TABLE order_book;

CREATE TABLE order_book (
	order_id text NOT NULL, -- 订单ID
	book_id text NOT NULL, -- 书籍ID
	count int4 NULL, -- 购买数量
	CONSTRAINT order_book_pkey PRIMARY KEY (order_id, book_id),
	CONSTRAINT order_book_fk FOREIGN KEY (book_id) REFERENCES book(id)
);

-- Column comments

COMMENT ON COLUMN public.order_book.order_id IS '订单ID';
COMMENT ON COLUMN public.order_book.book_id IS '书籍ID';
COMMENT ON COLUMN public.order_book.count IS '购买数量';


-- public.store definition

-- Drop table

-- DROP TABLE store;

CREATE TABLE store (
	book_id text NOT NULL, -- 书籍ID
	store_id text NOT NULL, -- 书店ID
	stock_level int4 NULL, -- 库存数量
	price int4 NULL, -- 书籍在该书店的价格
	CONSTRAINT store_pkey PRIMARY KEY (book_id, store_id),
	CONSTRAINT store_fk FOREIGN KEY (book_id) REFERENCES book(id),
	CONSTRAINT store_fk_1 FOREIGN KEY (store_id) REFERENCES bookstore(store_id)
);

-- Column comments

COMMENT ON COLUMN public.store.book_id IS '书籍ID';
COMMENT ON COLUMN public.store.store_id IS '书店ID';
COMMENT ON COLUMN public.store.stock_level IS '库存数量';
COMMENT ON COLUMN public.store.price IS '书籍在该书店的价格';