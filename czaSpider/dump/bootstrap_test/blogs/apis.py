import json
import markdown

from aiohttp import web

from handler import get, post
from tools import _RE_EMAIL, _RE_SHA1
from tools import *

logger = logging.getLogger(__name__)


# 模板页面 #

@get('/')
async def index(): return {'__template__': 'index.html'}


@get('/register')
async def register(): return {'__template__': 'register.html'}


@get('/register/root')
async def root_register(): return {'__template__': 'register_root.html'}


@get('/blogs')
async def blogs(): return {'__template__': 'blogs.html'}


@get('/root/manage/users')
async def root_manage_users(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'root_manage_users.html',
        'page_index': get_page_index(page)
    }


@get('/blogs/blog/{id}')
async def detail_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown.markdown(blog.content)
    return {
        '__template__': 'blog_detail.html',
        'blog': blog,
        'comments': comments
    }


# 用户登陆认证、注册、退出、删除模块 #

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email or not passwd:
        raise APIResourceError('请输入有效的: 用户名/密码', 'apis-authenticate')
    user = await User.findAll('email=?', [email])
    if len(user) == 0:
        raise APIResourceError('用户名不存在', 'apis-authenticate')
    user = user[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode())
    sha1.update(b':')
    sha1.update(passwd.encode())
    if user.passwd != sha1.hexdigest():
        raise APIResourceError('密码错误', 'apis-authenticate')
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@post('/api/new/user')
async def api_register_user(*, name, email, passwd):
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if not email or not _RE_EMAIL.match(email):
        raise APIResourceError('邮箱格式错误', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@post('/api/new/root/user')
async def api_register_root_user(*, name, email, passwd):
    root = await User.findAll('email=?', ['root@ioco.com'])
    if len(root) > 0:
        raise APIResourceError('root用户已存在，请勿创建', 'root user has already existed!')
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if email != 'root@ioco.com':
        raise APIResourceError('无法识别root邮箱', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, admin=True,
                passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    webResponse = web.HTTPFound(referer or '/')
    webResponse.set_cookie(COOKIE_NAME, '-deleted-', max_age=0)
    logger.info('user signed out!')
    return webResponse


@post('/api/drop/user')
async def api_drop_user(request, *, name, email):
    check_admin(request)
    user = await User.findAll('email=?', [email])
    await user.remove()
    return {'warning': 'drop %s success!' % name}


# json请求接口 #

@get('/api/get/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


@get('/api/get/blogs')
async def api_get_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


# 博客创建、删除模块 #


# 评论穿件、删除模块 #

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
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image,content=content.strip())
    print(blog.id, 'from blog')
    await comment.save()
    return comment

@post('/api/drop/comment/from/blog/{id}')
async def api_drop_comment(id, request):
    check_admin(request)
    print(id)
    c = await Comment.find(id)
    print(c)
    if c is None:
        raise APIResourceError('该评论状态异常', 'Comment Is Abnormal')
    await c.remove()
    return dict(id=id)