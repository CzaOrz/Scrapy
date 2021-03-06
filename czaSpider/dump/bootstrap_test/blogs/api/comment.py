from tools.handler import get, post

logger = logging.getLogger(__name__)


@post('/api/new/comment/from/blog/{id}')
async def api_new_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIResourceError('请先登陆', 'No User')
    if not content or not content.strip():
        raise APIResourceError('评论不能为空', 'Comment Can Not Be None')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceError('该文章异常，无法评论')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image,
                      content=content.strip())
    await comment.save()
    return comment


@post('/api/new/son/comment/from/blog/{id}')
async def api_new_son_comment(id, request, *, comment_id, content):
    user = request.__user__
    if user is None:
        raise APIResourceError('请先登陆', 'No User')
    if not comment_id:
        raise APIResourceError('评论异常，请联系管理员', 'No User')
    if not content or not content.strip():
        raise APIResourceError('评论不能为空', 'Comment Can Not Be None')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceError('该文章异常，无法评论')
    comment = SonComment(blog_id=blog.id, user_id=user.id, user_name=user.name,
                         content=content.strip(), comment_id=comment_id)
    await comment.save()
    return comment


@post('/api/drop/comment/from/blog/{id}')
async def api_drop_comment(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceError('该评论状态异常', 'Comment Is Abnormal')
    await c.remove()
    return dict(id=id)


@get('/api/get/comments')
async def api_get_comments(*, page=1):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for c in comments:
        c.html_content = text2html(c.content)
    return dict(page=p, comments=comments)
