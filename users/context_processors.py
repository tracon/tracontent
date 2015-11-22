# encoding: utf-8


from .models import UserMeta


def users_context(request):
    user_meta = UserMeta.get_for_user(request.user)

    vars = dict(
        user_meta=user_meta,
    )

    return vars
