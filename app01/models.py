from django.db import models

class User(models.Model):
    """ 用户表 """
    user_id = models.AutoField(verbose_name="用户ID", primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=128)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    phone = models.CharField(verbose_name="联系电话", max_length=15, null=True, blank=True)
    registration_date = models.DateTimeField(verbose_name="注册日期", auto_now_add=True)
    
    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员"),
        (3, "ROOT"),
    )
    role = models.SmallIntegerField(verbose_name="角色", choices=ROLE_CHOICES, default=1, null=True, blank=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    """ 图书表 """
    book_id = models.AutoField(verbose_name="图书ID", primary_key=True)
    book_name = models.CharField(verbose_name="图书名", max_length=64)
    author = models.CharField(verbose_name="作者", max_length=64)
    publisher = models.CharField(verbose_name="出版社", max_length=64)
    category = models.CharField(verbose_name="分类", max_length=32)
    stock_quantity = models.IntegerField(verbose_name="库存数量")
    borrow_count = models.IntegerField(verbose_name="借阅次数", default=0)
    score = models.DecimalField(verbose_name="评分", max_digits=3, decimal_places=2, default=0.00)
    img = models.FileField(verbose_name="图书图片展示", max_length=128, upload_to='book/', default='book/default.jpg')

    def __str__(self):
        return self.book_name


class BorrowRecord(models.Model):
    """ 借阅表 """
    record_id = models.AutoField(verbose_name="记录ID", primary_key=True)
    user_id = models.ForeignKey(User, verbose_name="用户ID", on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, verbose_name="图书ID", on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(verbose_name="借阅日期", auto_now_add=True)
    return_date = models.DateTimeField(verbose_name="归还日期", null=True, blank=True)
    
    STATUS_CHOICES = (
        (1, "借阅中"),
        (2, "已归还"),
        (3, "逾期"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return f"{self.user_id.username} - {self.book_id.book_name}"

class ScoreRecord(models.Model):
    """ 评分和评论表 """
    record_id = models.AutoField(verbose_name="记录ID", primary_key=True)
    user_id = models.ForeignKey(User, verbose_name="用户ID", on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, verbose_name="图书ID", on_delete=models.CASCADE)
    rating = models.DecimalField(verbose_name="评分", max_digits=2, decimal_places=1)
    review = models.TextField(verbose_name="评论", null=True, blank=True)

    def __str__(self):
        return f"{self.user_id.username} - {self.book_id.book_name} - {self.rating}"


































# from django.db import models


# class XX(models.Model):
#     title = models.CharField(verbose_name="名称", max_length=32)
#     image = models.FileField(verbose_name="头像", upload_to="avatar/")


# class Admin(models.Model):
#     """ 管理员 """
#     username = models.CharField(verbose_name="用户名", max_length=32)
#     password = models.CharField(verbose_name="密码", max_length=128)

#     def __str__(self):
#         return self.username


# class Department(models.Model):
#     """ 部门表 """
#     name = models.CharField(verbose_name='部门', max_length=32)

#     def __str__(self):
#         return self.name


# class UserInfo(models.Model):
#     """ 员工表 """
#     name = models.CharField(verbose_name="姓名", max_length=16)
#     password = models.CharField(verbose_name="密码", max_length=64)
#     age = models.IntegerField(verbose_name="年龄")
#     account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
#     # create_time = models.DateTimeField(verbose_name="入职时间")
#     create_time = models.DateTimeField(verbose_name="入职时间")

#     # 无约束
#     # depart_id = models.BigIntegerField(verbose_name="部门ID")
#     # 1.有约束
#     #   - to，与那张表关联
#     #   - to_field，表中的那一列关联
#     # 2.django自动
#     #   - 写的depart
#     #   - 生成数据列 depart_id
#     # 3.部门表被删除
#     # ### 3.1 级联删除
#     depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
#     # ### 3.2 置空
#     # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

#     # 在django中做的约束
#     gender_choices = (
#         (1, "男"),
#         (2, "女"),
#         (3, "其他"),
#     )
#     gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True)



# class City(models.Model):
#     """ 监测站 """
#     name = models.CharField(verbose_name="监测站名称", max_length=32,unique=True)
#     count = models.IntegerField(verbose_name="终端数量")
#     jingdu = models.FloatField(verbose_name="经度")
#     weidu = models.FloatField(verbose_name="纬度")
    
#     #info
#     linkuser = models.CharField(verbose_name="联系人", max_length=32,null=True,blank=True)
#     linkphone = models.CharField(verbose_name="联系人手机", max_length=11,null=True,blank=True)
#     linkpath = models.CharField(verbose_name="联系人信息", max_length=64,null=True,blank=True)

#     # 本质上数据库也是CharField，自动保存数据。
#     img = models.FileField(verbose_name="监测站图片展示", max_length=128, upload_to='city/')



# class Catch(models.Model):
#     """ 采集信息 """

#     #采集信息 温度、风速、湿度、PM25 等
#     name = models.CharField(verbose_name="来源监测站", max_length=32)
#     wendu = models.FloatField(verbose_name="温度")
#     fengsu = models.FloatField(verbose_name="风速")
#     shidu = models.FloatField(verbose_name="湿度")
#     pm25 = models.FloatField(verbose_name="PM2.5")

#     # create_time = models.DateField(verbose_name="创建时间")
#     create_time = models.DateTimeField(verbose_name="创建时间")
    
    

