my_project/
│
├── app/                     # 主应用目录
│   ├── __init__.py
│   │
│   ├── controller/         # 接口层（类似 Spring Controller）
│   │   ├── __init__.py
│   │   └── user_controller.py
│   │
│   ├── service/            # 业务逻辑层（类似 Service）
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   ├── dao/                # 数据访问层（类似 Mapper / Repository）
│   │   ├── __init__.py
│   │   └── user_dao.py
│   │
│   ├── model/              # 实体类（类似 Entity / POJO）
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── utils/              # 工具类
│   │   ├── __init__.py
│   │   ├── date_utils.py
│   │   ├── file_utils.py
│   │   └── http_utils.py
│   │
│   └── config/             # 配置文件
│       ├── __init__.py
│       └── config.py
│
├── tests/                  # 单元测试
│   └── test_user.py
│
├── main.py                 # 项目启动入口
├── requirements.txt        # 依赖
└── README.md