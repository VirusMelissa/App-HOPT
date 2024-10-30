document.addEventListener('DOMContentLoaded', function () {
    // Chọn phần tử input đầu tiên
    const input = document.querySelector('.form-group input');
    const form = document.querySelector('form');
    const tooltip = input.nextElementSibling;

    // Khởi tạo kiểm tra lỗi ban đầu cho input
    validateInput(input, tooltip);

    // Thêm sự kiện focus cho input
    input.addEventListener('focus', () => {
        validateInput(input, tooltip);
    });

    // Kiểm tra khi người dùng rời khỏi ô
    input.addEventListener('blur', () => {
        validateInput(input, tooltip);
    });

    input.addEventListener('input', () => {
        validateInput(input, tooltip);
    });

    // Kiểm tra trường khi người dùng nhấn submit
    form.addEventListener('submit', (event) => {
        let hasError = false;
        validateInput(input, tooltip);
        if (tooltip.classList.contains('show')) {
            hasError = true;
        }

        // Nếu có lỗi, ngăn chặn việc submit
        if (hasError) {
            event.preventDefault();
            alert('Tên người dùng không được để trống');
        }
    });

    function validateInput(input, tooltip) {
        const value = input.value.trim();
        let errorMessage = '';

        if (!value) {
            errorMessage = 'Tên người dùng không được để trống';
        }

        if (errorMessage) {
            tooltip.querySelector('.tooltip-text').textContent = errorMessage;
            tooltip.classList.add('show');
        } else {
            tooltip.classList.remove('show');
        }
    }
});
