from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..models import TopBarMenu, SideBarMenu
from .auth_routes import token_required

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menus')

@menu_bp.route('/', methods=['GET', 'OPTIONS'])
@cross_origin()
@token_required
def get_menus(current_user):
    # Get all top menus ordered by order
    top_menus = TopBarMenu.query.order_by(TopBarMenu.order).all()
    
    # Get all side menus ordered by order
    side_menus = SideBarMenu.query.order_by(SideBarMenu.order).all()
    
    # Format top menus
    formatted_top_menus = [{
        'id': menu.id,
        'name': menu.name,
        'order': menu.order
    } for menu in top_menus]
    
    # Format side menus with hierarchy
    def format_side_menu(menu):
        menu_dict = {
            'id': menu.id,
            'name': menu.name,
            'url': menu.url,
            'order': menu.order,
            'icon': 'bi-folder' # Default icon, you can add an icon field to the model if needed
        }
        
        # Get children menus
        children = SideBarMenu.query.filter_by(parent_id=menu.id).order_by(SideBarMenu.order).all()
        if children:
            menu_dict['submenu'] = [format_side_menu(child) for child in children]
            
        return menu_dict
    
    # Get only root menus (no parent)
    root_side_menus = SideBarMenu.query.filter_by(parent_id=None).order_by(SideBarMenu.order).all()
    formatted_side_menus = [format_side_menu(menu) for menu in root_side_menus]
    
    return jsonify({
        'success': True,
        'top_menus': formatted_top_menus,
        'side_menus': formatted_side_menus
    }) 