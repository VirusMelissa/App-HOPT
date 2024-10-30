document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.form-group input');
    const form = document.querySelector('form');

    // Khởi tạo kiểm tra lỗi ban đầu cho tất cả các trường
    inputs.forEach(input => {
        const tooltip = input.nextElementSibling;

        // Gọi validateInput để kiểm tra lỗi ban đầu
        validateInput(input, tooltip);

        // Thêm sự kiện focus cho tất cả các input
        input.addEventListener('focus', () => {
            validateInput(input, tooltip);
        });

        // Đối với mật khẩu, chỉ kiểm tra khi người dùng rời khỏi ô
        if (input.name === 'password') {
            input.addEventListener('blur', () => {
                validateInput(input, tooltip);
            });
        } else {
            input.addEventListener('input', () => {
                validateInput(input, tooltip);
            });
        }
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
            case 'username':
                if (!value) {
                    errorMessage = 'Tên người dùng không được để trống';
                }
                break;
            case 'password':
                if (!value) {
                    errorMessage = 'Mật khẩu không được để trống';
                }
                break;
        }

        // Hiển thị hoặc ẩn tooltip
        if (errorMessage) {
            tooltip.querySelector('.tooltip-text').textContent = errorMessage;
            tooltip.classList.add('show');
        } else {
            tooltip.classList.remove('show');
        }
    }
});
