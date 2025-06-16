$(document).ready(function() {
    // Edit Product
    $('.edit-product').click(function() {
        var productId = $(this).data('id');
        var productName = $(this).data('name');
        var price = $(this).data('price');
        var category = $(this).data('category');
        var description = $(this).data('description');
        
        $('#edit_product_id').val(productId);
        $('#edit_product_name').val(productName);
        $('#edit_price').val(price);
        $('#edit_category').val(category);
        $('#edit_description').val(description);
        
        // Show current images
        var productRow = $('#product-row-' + productId);
        var currentProductImage = productRow.find('td:first-child img').clone();
        var currentCertification = productRow.find('td:nth-child(6) img').clone();
        
        $('#current_product_image').html('Current: ').append(currentProductImage);
        $('#current_certification').html('Current: ').append(currentCertification);
        
        $('#editProductModal').modal('show');
    });

    $('#saveEdit').click(function() {
        var productId = $('#edit_product_id').val();
        var formData = new FormData();
        
        formData.append('product_name', $('#edit_product_name').val());
        formData.append('price', $('#edit_price').val());
        formData.append('category', $('#edit_category').val());
        formData.append('description', $('#edit_description').val());
        
        var productImage = $('#edit_product_image')[0].files[0];
        var certification = $('#edit_certification')[0].files[0];
        
        if (productImage) {
            formData.append('product_image', productImage);
        }
        if (certification) {
            formData.append('certification', certification);
        }
        
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        formData.append('csrfmiddlewaretoken', csrfToken);

        $.ajax({
            url: '/farmer/dashboard/update/' + productId + '/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if(response.status === 'success') {
                    location.reload();
                }
            },
            error: function(xhr, status, error) {
                alert('Error updating product: ' + error);
            }
        });
    });

    // Delete Product
    $('.delete-product').click(function() {
        if (confirm('Are you sure you want to delete this product?')) {
            var productId = $(this).data('id');
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            
            $.ajax({
                url: '/farmer/dashboard/delete/' + productId + '/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrfToken
                },
                success: function(response) {
                    if(response.status === 'success') {
                        $('#product-row-' + productId).remove();
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error deleting product: ' + error);
                }
            });
        }
    });
});
