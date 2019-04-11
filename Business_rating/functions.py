from Business_rating.constants import CATEGORIES


def is_valid_business(name, category):
    if not name:
        return {'success': False, 'message': 'wrong name format, name should not be empty'}
    if category not in get_categories():
        return {'success': False, 'message': 'wrong category format, check accepted categories list in constants.py'}
    return {'success': True}


def get_categories():
    return [cat[0] for cat in CATEGORIES]
