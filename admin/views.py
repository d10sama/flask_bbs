# admin模块
from admin import admin_blueprint


@admin_blueprint.route('/login')
def login():
    return 'login'

