# system/context_processors.py
from system.models import User


def user_role(request):
    """让模板中能直接访问 user_roles"""
    user = request.user
    user_role = None
    if request.user.is_authenticated:
        user = User.objects.get(username=user)
        user_role = user.roles.first()  # 返回 Role 对象 或 None
        user_role = str(user_role)

    is_admin = user_role == '超级管理员'
    return {
        'user_role': user_role,
        'is_admin': is_admin,  # 方便模板中直接 {{ current_user.name }}
    }
