from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..models import TopBarMenu, SideBarMenu
from .auth_routes import token_required

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menus')

@menu_bp.route('/', methods=['GET', 'OPTIONS'])
@cross_origin(
    origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
    max_age=3600
)
@token_required
def get_menus_with_token(current_user):
    try:
        # Get all top menus ordered by order
        top_menus = TopBarMenu.query.order_by(TopBarMenu.order).all()
        
        # Get all side menus ordered by order
        side_menus = SideBarMenu.query.order_by(SideBarMenu.order).all()
        
        # Format side menus with hierarchy first
        def format_side_menu(menu):
            menu_dict = {
                'id': menu.id,
                'name': menu.name,
                'url': menu.url,
                'order': menu.order,
                'top_menu': menu.top_bar_menu_id,
                'icon': 'bi-folder'
            }
            
            # Get children menus
            children = SideBarMenu.query.filter_by(parent_id=menu.id).order_by(SideBarMenu.order).all()
            if children:
                menu_dict['submenu'] = [format_side_menu(child) for child in children]
                
            return menu_dict
        
        # Get root side menus and format them
        root_side_menus = SideBarMenu.query.filter_by(parent_id=None).order_by(SideBarMenu.order).all()
        formatted_side_menus = [format_side_menu(menu) for menu in root_side_menus]
        
        # Format top menus with URLs from their first sidebar items
        formatted_top_menus = []
        for menu in top_menus:
            # Find first sidebar item for this top menu
            first_sidebar = SideBarMenu.query.filter_by(top_bar_menu_id=menu.id, parent_id=None).order_by(SideBarMenu.order).first()
            url = '#'
            
            if first_sidebar:
                # If first sidebar item has submenu, use its first child's URL
                first_child = SideBarMenu.query.filter_by(parent_id=first_sidebar.id).order_by(SideBarMenu.order).first()
                if first_child:
                    url = first_child.url
                else:
                    url = first_sidebar.url
                    
            formatted_top_menus.append({
                'id': menu.id,
                'name': menu.name,
                'url': url,
                'order': menu.order
            })
        
        return jsonify({
            'success': True,
            'top_menus': formatted_top_menus,
            'side_menus': formatted_side_menus
        })
    except Exception as e:
        print(f"Error in get_menus_with_token: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 