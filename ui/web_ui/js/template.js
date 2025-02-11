class Template {
    constructor() {
        this.activeTopMenu = '';
        this.init();
    }

    async init() {
        // Check authentication
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '../pages/login.html';
            return;
        }

        // Create template structure
        document.body.innerHTML = `
            <div class="layout-wrapper">
                <!-- Sidebar -->
                <nav id="sidebar" class="sidebar">
                    ${await this.getSidebarHTML()}
                </nav>

                <div class="main-content">
                    <!-- Topbar -->
                    <header id="topbar" class="topbar">
                        ${this.getTopbarHTML()}
                    </header>

                    <!-- Main Content -->
                    <main id="content-wrapper" class="content-wrapper">
                        ${document.body.innerHTML}
                    </main>
                </div>
            </div>
        `;

        this.initializeEvents();
        await this.updateTopMenu();
        await this.updateUserInfo();
    }


    async getSidebarHTML() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/menus/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Failed to fetch menu items');

            const menuData = await response.json();

            // Filter side menu items based on active top menu
            const filteredSideMenus = menuData.side_menus.filter(item => {
                console.log('Filtering menu item:', item, 'activeTopMenu:', this.activeTopMenu);
                return item.top_menu === parseInt(this.activeTopMenu);  // Convert to integer for comparison
            });
            
            console.log('Filtered side menus:', filteredSideMenus);
            const menuItems = this.buildMenuHTML(filteredSideMenus);

            return `
                <div class="sidebar-header">
                    <div class="brand">
                        <h3>System</h3>
                    </div>
                </div>

                <div class="sidebar-content">
                    <ul class="sidebar-menu">
                        ${menuItems}
                    </ul>
                </div>
            `;
        } catch (error) {
            console.error('Error loading menu:', error);
            return this.getDefaultMenuHTML();
        }
    }


    buildMenuHTML(items) {
        return items.map(item => {
            const isActive = window.location.pathname.includes(item.url);
            const hasSubItems = item.submenu && item.submenu.length > 0;
            const submenuId = `submenu-${item.id || Math.random().toString(36).substr(2, 9)}`;
            
            return `
                <li class="menu-item ${isActive ? 'active' : ''} ${hasSubItems ? 'has-submenu' : ''}">
                    <a href="${hasSubItems ? '#' : (item.url || '#')}" 
                       ${hasSubItems ? 'data-bs-toggle="collapse" data-bs-target="#' + submenuId + '"' : ''} 
                       data-title="${item.name}"
                       ${hasSubItems ? 'role="button" aria-expanded="false" aria-controls="' + submenuId + '"' : ''}>
                        <span>${item.name}</span>
                        ${hasSubItems ? '<i class="fas fa-chevron-right submenu-arrow"></i>' : ''}
                    </a>
                    ${hasSubItems ? `
                        <ul class="submenu collapse" id="${submenuId}">
                            ${this.buildMenuHTML(item.submenu)}
                        </ul>
                    ` : ''}
                </li>
            `;
        }).join('');
    }

    getDefaultMenuHTML() {
        return `
            <div class="sidebar-header">
                <div class="brand">
                    <h3>Planning System</h3>
                </div>
            </div>
            
            <div class="sidebar-content">
                <ul class="sidebar-menu">
                    <li class="menu-item ${window.location.pathname.includes('dashboard') ? 'active' : ''}">
                        <a href="dashboard.html">
                            <span>Dashboard</span>
                        </a>
                    </li>
                    <li class="menu-item ${window.location.pathname.includes('planning') ? 'active' : ''}">
                        <a href="planning.html">
                            <span>Planning</span>
                        </a>
                    </li>
                    <li class="menu-item has-submenu">
                        <a href="#reportsSubmenu" data-bs-toggle="collapse">
                            <span>Reports</span>
                            <i class="fas fa-chevron-right submenu-arrow"></i>
                        </a>
                        <ul class="submenu collapse" id="reportsSubmenu">
                            <li><a href="reports/daily.html">Daily Report</a></li>
                            <li><a href="reports/weekly.html">Weekly Report</a></li>
                            <li><a href="reports/monthly.html">Monthly Report</a></li>
                        </ul>
                    </li>
                    <li class="menu-item ${window.location.pathname.includes('settings') ? 'active' : ''}">
                        <a href="settings.html">
                            <span>Settings</span>
                        </a>
                    </li>
                </ul>
            </div>
        `;
    }

    getTopbarHTML() {
        return `
            <div class="topbar-left">
                <button class="btn-toggle-sidebar">
                    <i class="fas fa-bars"></i>
                </button>
                <div class="page-title">
                    <h1>${document.title.split('-')[0].trim()}</h1>
                </div>
                <div class="top-menu">
                    <ul class="nav-menu" id="topMenuItems">
                        <!-- Top menu items will be inserted here -->
                    </ul>
                </div>
                <div class="topbar-search">
                    <input type="text" placeholder="Search..." aria-label="Search" />
                </div>
            </div>

            <div class="topbar-right">
                <div class="topbar-actions">
                    <button class="btn-icon">
                        <i class="far fa-bell"></i>
                        <span class="badge">3</span>
                    </button>
                    <div class="dropdown">
                        <button class="btn-user dropdown-toggle" data-bs-toggle="dropdown">
                            <div class="user-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                            <span class="user-name">Loading...</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="profile.html">
                                    <i class="fas fa-user"></i> Profile
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="#" id="btn-logout">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    async updateTopMenu() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/menus/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Failed to fetch menu items');
            
            const menuData = await response.json();
            const topMenuContainer = document.getElementById('topMenuItems');
            
            if (topMenuContainer && menuData.top_menus) {
                // Get current page path
                const currentPath = window.location.pathname;
                
                // Find active top menu based on current URL
                const activeTopMenu = menuData.top_menus.find(item => 
                    currentPath.includes(item.url) || 
                    (item.side_menus && item.side_menus.some(side => currentPath.includes(side.url)))
                );
                
                this.activeTopMenu = activeTopMenu ? activeTopMenu.id : menuData.top_menus[0].id;

                topMenuContainer.innerHTML = menuData.top_menus.map(item => `
                    <li class="nav-item ${item.id === this.activeTopMenu ? 'active' : ''}">
                        <a class="nav-link" href="#" data-menu-id="${item.id}">
                            ${item.name}
                        </a>
                    </li>
                `).join('');

                // Add click handlers for top menu items
                topMenuContainer.querySelectorAll('.nav-link').forEach(link => {
                    link.addEventListener('click', async (e) => {
                        e.preventDefault();
                        const menuId = e.currentTarget.dataset.menuId;
                        console.log('Clicked top menu ID:', menuId);
                        this.activeTopMenu = menuId;
                        
                        // Update active states
                        topMenuContainer.querySelectorAll('.nav-item').forEach(item => 
                            item.classList.remove('active')
                        );
                        e.currentTarget.parentElement.classList.add('active');
                        
                        // Get menu data again to ensure we have fresh data
                        const response = await fetch('http://localhost:5000/api/menus/', {
                            headers: {
                                'Authorization': `Bearer ${token}`,
                                'Content-Type': 'application/json'
                            }
                        });
                        const menuData = await response.json();
                        console.log('Menu data:', menuData);
                        
                        // Filter side menus
                        const filteredSideMenus = menuData.side_menus.filter(item => {
                            console.log('Comparing:', item.top_menu, parseInt(menuId));
                            return item.top_menu === parseInt(menuId);
                        });
                        console.log('Filtered side menus:', filteredSideMenus);

                        // Update sidebar with filtered items
                        const sidebarContent = await this.getSidebarHTML();
                        document.getElementById('sidebar').innerHTML = sidebarContent;
                        this.initializeEvents();

                        // Navigate to first sidebar item if available
                        if (filteredSideMenus.length > 0) {
                            const firstItem = filteredSideMenus[0];
                            if (firstItem.submenu && firstItem.submenu.length > 0) {
                                window.location.href = firstItem.submenu[0].url;
                            } else {
                                window.location.href = firstItem.url;
                            }
                        }
                    });
                });

                // Initial sidebar update
                const sidebarContent = await this.getSidebarHTML();
                document.getElementById('sidebar').innerHTML = sidebarContent;
                this.initializeEvents();

                // Initial navigation if needed
                if (!currentPath || currentPath === '/' || currentPath === '/index.html') {
                    const filteredSideMenus = menuData.side_menus.filter(item => 
                        item.top_menu === this.activeTopMenu
                    );
                    if (filteredSideMenus.length > 0) {
                        const firstItem = filteredSideMenus[0];
                        if (firstItem.submenu && firstItem.submenu.length > 0) {
                            window.location.href = firstItem.submenu[0].url;
                        } else {
                            window.location.href = firstItem.url;
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error loading top menu:', error);
        }
    }

    async updateUserInfo() {
        try {
            const token = localStorage.getItem('token');
            const userInfo = JSON.parse(localStorage.getItem('user'));
            
            if (userInfo) {
                const userNameElement = document.querySelector('.user-name');
                if (userNameElement) {
                    userNameElement.textContent = userInfo.name_eng || userInfo.username;
                }
            }
        } catch (error) {
            console.error('Error updating user info:', error);
        }
    }

    initializeEvents() {
        // Remove existing event listeners first
        document.querySelectorAll('.btn-toggle-sidebar').forEach(btn => {
            btn.replaceWith(btn.cloneNode(true));
        });

        // Add new event listeners
        document.querySelectorAll('.btn-toggle-sidebar').forEach(btn => {
            btn.addEventListener('click', () => {
                document.body.classList.toggle('sidebar-collapsed');
                console.log('Toggle sidebar clicked');
            });
        });

        // Update submenu toggle
        document.querySelectorAll('.has-submenu > a').forEach(item => {
            item.addEventListener('click', (e) => {
                const parent = e.currentTarget.parentElement;
                parent.classList.toggle('open');
            });
        });

        // Logout handler
        document.getElementById('btn-logout').addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:5000/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('user');
                    window.location.href = '../pages/login.html';
                }
            } catch (error) {
                console.error('Logout error:', error);
            }
        });
    }
}
