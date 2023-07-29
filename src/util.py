from ast import literal_eval
from margaret.settings import ADM


def authorized(member_id):
    """
    Validate if member is authorized to execute the command
    """
    admins = literal_eval(ADM)
    return member_id in admins
