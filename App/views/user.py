from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from App.forms import Register, Login  # 导入表单注册类
from App.models import User  # User 模型类

user = Blueprint('user', __name__)

"""
# 注册步骤
1. 创建模型类
2. 加载flask-migrate扩展库（迁移）
3. 在视图函数中导入模型类
4. 验证用户名是否存在
5. 获取模板前台传递过来的数据
6. 存储
7. 明文密码变成密文密码（加密存储）
8. 消息闪现（注册成功，前去激活...）
"""


@user.route('/register/', methods=['GET', 'POST'])
def register():
    # 实例化注册表单类
    form = Register()
    u = User()
    if form.validate_on_submit():
        # 实例化存储注册表单数据
        u.username = form.username.data
        u.password = form.userpass.data
        u.email = form.email.data
        u.registerTime = datetime.now()
        u.status = '作者'
        u.save()
        flash('注册成功，以为您跳转到登录页面...')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('请输入正确的用户名')
        elif not u.check_password(form.userpass.data):
            flash('密码有误，请输入正确的密码...')
        elif u.status != '作者':
            flash('您不是投稿的作者哦~')
        else:
            # 修改登录时间
            u.lastLogin = datetime.now()
            u.save()
            login_user(u, remember=form.remember.data)  # 使用第三方扩展库处理登录状态的维持
            return redirect(url_for('user.main_page'))
    return render_template('user/login.html', form=form)


# 用户主页面
@user.route('/main_page/')
@login_required
def main_page():
    if current_user.status == '作者':  # 当前用户是作者，才会渲染下面的模板，否则渲染nocan.html
        u = current_user
        return render_template('main/main_user.html', user=u)
    else:
        return render_template('common/nocan.html', u=current_user.username)


# 退出登录
@user.route('/logout/')
def logout():
    logout_user()  # 清除当前用户所有数据
    return redirect(url_for('main.index'))
