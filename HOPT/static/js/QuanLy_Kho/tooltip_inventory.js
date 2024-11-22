document.addEventListener('DOMContentLoaded', function () {
    // Khởi tạo Select2 cho tất cả các select
    $('select.select-field').select2({
        placeholder: 'Chọn một giá trị', // Thay đổi placeholder nếu cần
        allowClear: true
    });

    const inputs = document.querySelectorAll('.form-group input, .form-group select'); // Lấy tất cả các input và select trong form
    const form = document.getElementById('form'); // Thay đổi ID này nếu cần

    // Khởi tạo kiểm tra lỗi ban đầu cho tất cả các trường
    inputs.forEach(input => {
        const tooltip = input.nextElementSibling;

        // Gọi validateInput để kiểm tra lỗi ban đầu
        validateInput(input, tooltip);

        // Thêm sự kiện focus cho tất cả các input
        input.addEventListener('focus', () => {
            validateInput(input, tooltip);
        });

        input.addEventListener('input', () => {
            validateInput(input, tooltip);
        });
    });

    // Kiểm tra tất cả các trường khi người dùng nhấn submit
    form.addEventListener('submit', (event) => {
        let hasError = false; // Biến kiểm tra xem có lỗi hay không
        inputs.forEach(input => {
            const tooltip = input.nextElementSibling;
            validateInput(input, tooltip);
            if (tooltip.classList.contains('show')) {
                hasError = true; // Nếu có lỗi, đặt hasError là true
            }
        });

        // Nếu có lỗi, ngăn chặn việc submit
        if (hasError) {
            event.preventDefault();
        }
    });

    function validateInput(input, tooltip) {
        const value = input.value.trim();
        let errorMessage = '';
    
        // Kiểm tra các trường cụ thể
        switch (input.name) {
            case 'min_inventory':
                if (!value) {
                    errorMessage = 'Mức tồn tối thiểu không được để trống.';
                } else if (isNaN(value) || value < 0) {
                    errorMessage = 'Mức tồn tối thiểu phải là một số dương.';
                }
                break;
            case 'inventory_valuation':
                if (!value) {
                    errorMessage = 'Tồn kho TT không được để trống.';
                } else if (isNaN(value) || value < 0) {
                    errorMessage = 'Tồn kho TT phải là một số dương.';
                }
        }
    
        // Hiển thị hoặc ẩn tooltip nếu tooltip tồn tại
        if (tooltip) {
            if (errorMessage) {
                tooltip.querySelector('.tooltip-text').textContent = errorMessage;
                tooltip.classList.add('show');
            } else {
                tooltip.classList.remove('show');
            }
        }
    }
});