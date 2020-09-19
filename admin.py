# admin是后台模块，可以在这里添加后台管理数据项，增删之后要相应的在models层中修改
from django.contrib import admin
from firstapp.models import People,Article,UserProfile,Comment,Ticket


# Register your models here.
# 下面是管理后台数据项的添加
admin.site.register(People)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Ticket)
