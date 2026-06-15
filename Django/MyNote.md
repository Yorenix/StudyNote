

## 下载别人的django项目迁移项目，报错1146

https://blog.csdn.net/LanlanDeming/article/details/103941075



## 零散

只有get请求才能在url里串数据

![image-20231012220122121](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231012220122121.png)

![image-20231012215815104](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231012215815104.png)

![image-20231012220153556](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231012220153556.png)



创建超级管理员

```manage.py
createsuperuser
```



## 快捷键

- 加粗： `Ctrl + B`

- 撤销： `Ctrl + Z`

- 字体倾斜 ：`Ctrl+I`

- 下划线：`Ctrl+U`

- 多级标题： `Ctrl + 1~6`

- 有序列表：`Ctrl + Shift + [`

- 无序列表：`Ctrl + Shift + ]`

- 降级快捷键 ：`Tab`

- 升级快捷键：`Shift + Tab`

- 插入链接： `Ctrl + K`

- 插入公式： `Ctrl + Shift + M`

- 行内代码： `Ctrl + Shift + K`

- 插入图片： `Ctrl + Shift + I`

- 返回Typora顶部：`Ctrl+Home`

- 返回Typora底部 ：`Ctrl+End`

- 创建表格 ：`Ctrl+T`

- 选中某句话 ：`Ctrl+L`

- 选中某个单词 ：`Ctrl+D`

- 选中相同格式的文字 ：`Ctrl+E`

- 搜索: `Ctrl+F`

- 搜索并替换 ：`Ctrl+H`

- 删除线 ：`Alt+Shift+5`

- 引用 ：`Ctrl+Shift+Q`

- 生成目录：`[TOC]+Enter`

  

## 创建项目流程

### 1APP设置

#### 	1.1新建app

```manage.py
startapp app01
```

#### 			1.2注册app

```settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
]
......
```

### 2数据库设置`

#### 	2.1连接数据库

​	

```settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gx_day15',  # 数据库名字
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',  # 那台机器安装了MySQL
        'PORT': 3306,
    }
}
```



#### 	2.2设计表结构

```models.py
from django.db import models


class Department(models.Model):
    """部门表  """
    title = models.CharField(verbose_name='标题', max_length=32)  # verbose_name:注解

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """"靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)

```

#### 2.3运行表结构

```manage.py
makemigrations
migrate
```

​		

neo4j

