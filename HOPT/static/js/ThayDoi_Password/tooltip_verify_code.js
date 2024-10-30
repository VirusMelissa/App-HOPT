document.addEventListener('DOMContentLoaded', function () {
    const codeInput = document.getElementById('id_code');
    const form = document.querySelector('form');
    const codeTooltip = codeInput.nextElementSibling;

    // Validate code on input
    codeInput.addEventListener('input', () => {
        validateCodeInput(codeInput, codeTooltip);
    });

    // Validate code when form is submitted
    form.addEventListener('submit', (event) => {
        validateCodeInput(codeInput, codeTooltip);
        if (codeTooltip.classList.contains('show')) {
            event.preventDefault(); // Ngăn submit nếu có lỗi
        }
    });

    function validateCodeInput(input, tooltip) {
        const value = input.value.trim();
        let errorMessage = '';

        if (!value) {
            errorMessage = 'Mã xác nhận không được để trống';
        } else if (value.length !== 6) {
            errorMessage = 'Mã xác nhận phải có 6 ký tự';
        }

        if (errorMessage) {
            tooltip.querySelector('.tooltip-text').textContent = errorMessage;
            tooltip.classList.add('show');
        } else {
            tooltip.classList.remove('show');
        }
    }
});
