from firstapp.models import Article
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication





# 这里定义api来方便取数据


# 定义一个序列化器，将Article的model的数据序列化，页面渲染json形式需要数据的序列化
class ArticleSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(min_length=1)
    class Meta:
        model = Article
        fields = '__all__'
        # fields='('headline','content','cover','popular_choice')'
#         # fields = '('title','content',)' 如果你用元组的形式调用部分属性，千万别忘了每个属性后面加逗号
# 这是渲染嵌套的对应关系，设置1之后访问api时就可以多渲染出1层json结构
        depth = 1
#
#
# @api_view(['GET'])
# def article(request):
#     video_list = Article.objects.all()
#     serializer = ArticleSerializer(video_list, many=True)
#     return Response(serializer.data)




# 查找和发布  get查看 post发布
# 使用一个python装饰器
@api_view(['GET', 'POST'])
# 使用Token的方式识别身份
@authentication_classes((TokenAuthentication,))
def article(request):
    # 把访问者的用户名和身份token打印出来
    print(request.user)
    print(request.auth)
    # -id是倒序查找，这样post添加新id的文章时，新文章就能排在前面
    video_list = Article.objects.order_by('-id')
    if request.method == 'GET':
        # 判断请求token，如果是用户则返还所有文章，不是的话就只返还5个文章
        if request.auth:
            serializer = ArticleSerializer(video_list, many=True)
            return Response(serializer.data)
        else:
            serializer = ArticleSerializer(video_list[:5], many=True)
            return Response(serializer.data)
#         # 这里把model层里的数据拿了出来，访问的时候可以选择json方式展示
# # 这里是提交表单的功能
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 建立body字典
        body = {
            'body': serializer.errors,
            'msg': '40001'
        }
#         # 如果提交错误表单的话可以在检查器里的preview查到body的40001
        return Response(body, status=status.HTTP_400_BAD_REQUEST)
#
# # 修改点赞和删除文章
@api_view([ 'PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def video_card(request, id):
     # 获取id对应的文章
    video_card = Article.objects.get(id=id)
    # 只有这篇文章的作者或者超级管理员才能删
    # 可是为什么管理员不能删。。。。
    USER_CAN = {
        "DELETE": request.user == video_card.owner or (
                    request.user == 'admin')
    }
    if request.method == 'PUT':
#         # 修改文章
        serializer = ArticleSerializer(video_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if USER_CAN["DELETE"]:
            video_card.delete()
            return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'You cant touch this'}, status=status.HTTP_403_FORBIDDEN)
