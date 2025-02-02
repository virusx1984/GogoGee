class Dashboard {
    static init() {
        this.initCharts();
        this.loadActivityLog();
    }

    static initCharts() {
        this.initSalesChart();
        this.initProjectChart();
    }

    static initSalesChart() {
        const salesCtx = document.getElementById('salesChart')?.getContext('2d');
        if (salesCtx) {
            new Chart(salesCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Sales',
                        data: [12, 19, 3, 5, 2, 3],
                        borderColor: '#4CAF50',
                        tension: 0.1
                    }]
                }
            });
        }
    }

    // ... rest of dashboard methods ...
}

// Initialize dashboard when document is ready
$(document).ready(() => Dashboard.init()); 