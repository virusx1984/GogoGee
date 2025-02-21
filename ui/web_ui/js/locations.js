class Locations {
    constructor() {
        this.table = $('#locationsTable').DataTable({
            ajax: {
                url: '/api/locations',
                dataSrc: ''
            },
            columns: [
                { data: 'id' },
                { data: 'name' },
                { data: 'address' },
                { data: 'type' },
                { data: 'status' },
                {
                    data: null,
                    render: function(data) {
                        return `
                            <div class="btn-group">
                                <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${data.id}">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${data.id}">
                                    <i class="fas fa-trash"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-info history-btn" data-id="${data.id}">
                                    <i class="fas fa-history"></i>
                                </button>
                            </div>
                        `;
                    }
                }
            ]
        });

        this.initEventHandlers();
    }

    initEventHandlers() {
        // Add new location
        $('#addLocationBtn').click(() => this.showModal());

        // Save location
        $('#saveLocationBtn').click(() => this.saveLocation());

        // Edit location
        $('#locationsTable').on('click', '.edit-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.editLocation(id);
        });

        // Delete location
        $('#locationsTable').on('click', '.delete-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.deleteLocation(id);
        });

        // View history
        $('#locationsTable').on('click', '.history-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.viewHistory(id);
        });

        // Reset form when modal is hidden
        $('#locationModal').on('hidden.bs.modal', () => {
            this.resetForm();
        });
    }

    showModal(data = null) {
        if (data) {
            $('#locationName').val(data.name);
            $('#locationAddress').val(data.address);
            $('#locationType').val(data.type);
            $('#locationStatus').val(data.status);
            $('#locationModalLabel').text('Edit Location');
            $('#locationModal').data('id', data.id);
        } else {
            $('#locationModalLabel').text('Add Location');
        }
        $('#locationModal').modal('show');
    }

    async saveLocation() {
        const formData = {
            name: $('#locationName').val(),
            address: $('#locationAddress').val(),
            type: $('#locationType').val(),
            status: $('#locationStatus').val()
        };

        const id = $('#locationModal').data('id');
        const url = id ? `/api/locations/${id}` : '/api/locations';
        const method = id ? 'PUT' : 'POST';

        try {
            const response = await $.ajax({
                url: url,
                method: method,
                contentType: 'application/json',
                data: JSON.stringify(formData)
            });

            this.table.ajax.reload();
            $('#locationModal').modal('hide');
            this.showToast('Location saved successfully');
        } catch (error) {
            console.error('Error saving location:', error);
            this.showToast('Error saving location', 'danger');
        }
    }

    async editLocation(id) {
        try {
            const response = await $.getJSON(`/api/locations/${id}`);
            this.showModal(response);
        } catch (error) {
            console.error('Error fetching location:', error);
            this.showToast('Error fetching location', 'danger');
        }
    }

    async deleteLocation(id) {
        if (confirm('Are you sure you want to delete this location?')) {
            try {
                await $.ajax({
                    url: `/api/locations/${id}`,
                    method: 'DELETE'
                });
                this.table.ajax.reload();
                this.showToast('Location deleted successfully');
            } catch (error) {
                console.error('Error deleting location:', error);
                this.showToast('Error deleting location', 'danger');
            }
        }
    }

    async viewHistory(id) {
        try {
            const response = await $.getJSON(`/api/locations/${id}/history`);
            this.populateHistoryTable(response);
            $('#historyModal').modal('show');
        } catch (error) {
            console.error('Error fetching history:', error);
            this.showToast('Error fetching history', 'danger');
        }
    }

    populateHistoryTable(data) {
        const table = $('#historyTable').DataTable({
            data: data,
            destroy: true,
            columns: [
                { data: 'timestamp' },
                { data: 'action' },
                { data: 'changed_by' },
                { data: 'details' }
            ],
            order: [[0, 'desc']]
        });
    }

    resetForm() {
        $('#locationForm')[0].reset();
        $('#locationModal').removeData('id');
    }

    showToast(message, type = 'success') {
        const toast = $(`
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `);

        $('.toast-container').append(toast);
        new bootstrap.Toast(toast[0]).show();
        setTimeout(() => toast.remove(), 5000);
    }
}

// Initialize Locations when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Locations();
});
