document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-group input, .form-group select');
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
        if (input.name === 'password1' || input.name === 'password2') {
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
                const usernamePattern = /^[a-zA-Z0-9]+$/; // Chỉ cho phép chữ và số
                if (!value) {
                    errorMessage = 'Tên người dùng không được để trống';
                } else if (!usernamePattern.test(value)) {
                    errorMessage = 'Họ và tên chỉ có chữ cái và khoảng trắng, không chứa số hoặc ký tự đặc biệt';
                }
                break;
            case 'fullname':
                // Cập nhật biểu thức chính quy để chấp nhận ký tự có dấu và khoảng trắng
                const fullnamePattern = /^[\p{L} ]+$/u; // Sử dụng \p{L} để cho phép tất cả các ký tự chữ cái
                if (!value) {
                    errorMessage = 'Họ và tên không được để trống';
                } else if (!fullnamePattern.test(value)) {
                    errorMessage = 'Họ và tên chỉ có chữ cái và khoảng trắng';
                }
                break;
            case 'email':
                if (!value) {
                    errorMessage = 'Email không được để trống';
                } else if (!validateEmail(value)) {
                    errorMessage = 'Địa chỉ email không hợp lệ';
                }
                break;
            case 'phone_number':
                if (!value) {
                    errorMessage = 'Số điện thoại không được để trống';
                } else if (value.length < 10) {
                    errorMessage = 'Số điện thoại phải có ít nhất 10 chữ số';
                }
                break;
            case 'password1':
                if (!value) {
                    errorMessage = 'Mật khẩu không được để trống';
                } else if (!validatePassword(value)) {
                    errorMessage = 'Mật khẩu phải chứa ít nhất một chữ hoa, một chữ thường và một chữ số';
                }
                break;
            case 'password2':
                const password1 = document.querySelector('#id_password1').value.trim();
                if (!value) {
                    errorMessage = 'Nhập lại mật khẩu không được để trống';
                } else if (value !== password1) {
                    errorMessage = 'Mật khẩu không khớp nhau';
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

    function validatePassword(password) {
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        return hasUpperCase && hasLowerCase && hasNumber;
    }

    function validateEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }
});