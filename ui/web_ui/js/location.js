class Location{
    constructor(tableId){
        this.tableId = tableId;
        this.initTable();
    }

    initTable(){
        this.dataTable = new DataTable(`#${this.tableId}`, {
            fixedColumns: {
                left: 1
            },
            paging: false,
            searching: false,
            info: false,
            scrollX: true,
            scrollY: 500,
            scrollCollapse: true,
            autoWidth: true,
            columnDefs: [
                {
                    targets: 0, // First column
                    data: null,
                    width: "120px",
                    className: "dt-center",
                    render: function(data, type, row) {
                        return `
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-sm btn-primary" title="Edit">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button type="button" class="btn btn-sm btn-info" title="View">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button type="button" class="btn btn-sm btn-danger" title="Delete">
                                    <i class="fas fa-trash"></i>
                                </button>
                                <button type="button" class="btn btn-sm btn-secondary" title="History">
                                    <i class="fas fa-history"></i>
                                </button>
                            </div>
                        `;
                    },
                    orderable: false
                }
            ]
        });
    }

    // Add methods to load data, update table, etc.
    loadData(data) {
        this.dataTable.clear();
        this.dataTable.rows.add(data);
        this.dataTable.draw();
    }

    fetchData() {
        const self = this;
        $.ajax({
            url: 'http://127.0.0.1:19846/api/locations',
            method: 'GET',
            beforeSend: function() {
                // Show loading state
                $(`#${self.tableId}_wrapper`).addClass('loading');
            },
            success: function(response) {
                // Transform API response to match datatable format
                const tableData = response['data'].map(item => [
                    null, // Empty value for action column
                    item.province,
                    item.region,
                    item.city,
                ]);
                self.loadData(tableData);
            },
            error: function(xhr) {
                console.error('Error fetching locations:', xhr.responseText);
                alert('Failed to load location data');
            },
            complete: function() {
                // Remove loading state
                $(`#${self.tableId}_wrapper`).removeClass('loading');
            }
        });
    }

    // Handle add location form submission
    setupAddLocationForm() {
        const self = this;
        $('#addLocationForm').on('submit', function(e) {
            e.preventDefault();
            
            const region = $('#region').val();
            const street = $('#street').val();

            $.ajax({
                url: 'http://127.0.0.1:19846/api/locations',
                method: 'POST',
                data: {
                    region: region,
                    street: street
                },
                beforeSend: function() {
                    $('#addLocationModal').find('.btn').prop('disabled', true);
                },
                success: function(response) {
                    // Add new row to DataTable
                    const newRow = [
                        null, // Action column
                        region,
                        street
                    ];
                    self.dataTable.row.add(newRow).draw();
                    
                    // Clear form and close modal
                    $('#addLocationForm')[0].reset();
                    $('#addLocationModal').modal('hide');
                },
                error: function(xhr) {
                    console.error('Error adding location:', xhr.responseText);
                    alert('Failed to add location');
                },
                complete: function() {
                    $('#addLocationModal').find('.btn').prop('disabled', false);
                }
            });
        });
    }
}
