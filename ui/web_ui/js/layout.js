// Layout management
class Layout {
    static init() {
        this.checkAuth();
        this.setupEventListeners();
    }

    static checkAuth() {
        const token = localStorage.getItem('authToken');
        if (!token) {
            window.location.href = '/login.html';
            return;
        }
        this.loadUserInfo();
        this.loadMenus();
    }

    static loadUserInfo() {
        ApiService.get(API_CONFIG.ENDPOINTS.AUTH.USER)
            .then(response => {
                $('#user-name, #sidebar-user-name').text(response.name_eng);
            })
            .catch(() => {
                localStorage.removeItem('authToken');
                window.location.href = '/login.html';
            });
    }

    static loadMenus() {
        ApiService.get(API_CONFIG.ENDPOINTS.MENUS)
            .then(response => {
                if (response.success) {
                    this.renderTopMenu(response.top_menus);
                    this.renderSideMenu(response.side_menus);
                }
            });
    }

    static renderTopMenu(menus) {
        const $topMenu = $('#top-menu');
        $topMenu.empty();
        
        menus.forEach(menu => {
            $topMenu.append(`
                <li class="nav-item">
                    <a class="nav-link" href="#${menu.url}">${menu.name}</a>
                </li>
            `);
        });
    }

    static renderSideMenu(menus) {
        const $sideMenu = $('#side-menu');
        $sideMenu.empty();

        menus.forEach(menu => {
            if (menu.submenu) {
                $sideMenu.append(this.renderSubmenu(menu));
            } else {
                $sideMenu.append(`
                    <li>
                        <a href="#${menu.url}">
                            <i class="bi ${menu.icon}"></i> ${menu.name}
                        </a>
                    </li>
                `);
            }
        });
    }

    static renderSubmenu(menu) {
        return `
            <li class="has-submenu">
                <a href="#">
                    <i class="bi ${menu.icon}"></i> ${menu.name}
                </a>
                <ul class="submenu">
                    ${menu.submenu.map(sub => `
                        <li>
                            <a href="#${sub.url}">${sub.name}</a>
                        </li>
                    `).join('')}
                </ul>
            </li>
        `;
    }

    static handleRoute() {
        const hash = window.location.hash.slice(1) || '/';
        this.loadContent(hash);
    }

    static loadContent(route) {
        ApiService.get(API_CONFIG.ENDPOINTS.CONTENT + route)
            .then(response => {
                // Load styles first
                if (response.styles) {
                    response.styles.forEach(style => {
                        if (!document.querySelector(`link[href="${style}"]`)) {
                            const link = document.createElement('link');
                            link.rel = 'stylesheet';
                            link.href = style;
                            document.head.appendChild(link);
                        }
                    });
                }

                // Load content
                $('#main-content').html(response.content);

                // Load scripts
                if (response.scripts) {
                    response.scripts.forEach(script => {
                        if (!document.querySelector(`script[src="${script}"]`)) {
                            const scriptEl = document.createElement('script');
                            scriptEl.src = script;
                            document.body.appendChild(scriptEl);
                        }
                    });
                }
            });
    }

    static setupEventListeners() {
        // Handle submenu toggles
        $(document).on('click', '.has-submenu > a', function(e) {
            e.preventDefault();
            $(this).parent().toggleClass('active');
        });

        // Logout handler
        $('#logout-btn').click(function(e) {
            e.preventDefault();
            ApiService.post(API_CONFIG.ENDPOINTS.AUTH.LOGOUT)
                .finally(() => {
                    localStorage.removeItem('authToken');
                    window.location.href = '/login.html';
                });
        });

        // Handle route changes
        $(window).on('hashchange', () => this.handleRoute());
        this.handleRoute(); // Handle initial route
    }
}

// Initialize layout when document is ready
$(document).ready(() => Layout.init()); 