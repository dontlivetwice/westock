import core.models.base as base
from server.views import exceptions


def get_interest_list():
    return base.managers.interest_manager.get_many()


def add_interests_for_user(user_id, interests):
    # 1. get the user
    user = base.managers.user_manager.get_one(id=user_id)

    if not user:
        raise exceptions.AuthenticationFailed()

    # 2. make sure the user did not go through the interest flow already
    if user.get_interest_flow_state():
        raise exceptions.InvalidParams()

    # 3. add interests to users
    for interest in interests:
        interest = base.managers.interest_manager.get_one(name=interest)
        user.add_interest_to_user(interest.get('id'))
        interest.increase_followers()
        base.managers.interest_manager.update_one(interest)

    # 4. mark the flow as done
    user.set_interest_flow_state(True)


def get_interests_for_user(user_id):
    if user_id:
        user = base.managers.user_manager.get_one(id=user_id)
        if user:
            return user.get_interests_for_user()

    return []


def get_interest_flow_state(user_id):
    if user_id:
        user = base.managers.user_manager.get_one(id=user_id)

        if user:
            return user.get_interest_flow_state()

    return False
