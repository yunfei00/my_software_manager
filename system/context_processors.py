def user_role(request):
    """
    全局传递用户角色给模板
    """
    role_name = None
    # user = getattr(request, "user", None)
    # if user and user.is_authenticated:
    #     if hasattr(user, "roles") and user.roles:
    #         print(f'fuck user.roles.name is {user.roles.name}')
    #         role_name = user.roles.name.strip()  # 去掉前后空格
    #         # user = User.objects.get(username=user)
    #         # user_role = user.roles.first()  # 返回 Role 对象 或 None

    print(f'user_role is {user_role}')
    return {"user_role": role_name}
