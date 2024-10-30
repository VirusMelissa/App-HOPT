document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0 && messages[0].innerText.trim() !== '') {
        // Tạo modal chỉ khi có thông điệp
        const modal = document.createElement('div');
        modal.classList.add('modal');

        const modalContent = document.createElement('div');
        modalContent.classList.add('modal-content');

        const closeBtn = document.createElement('span');
        closeBtn.classList.add('close');
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = function() {
            modal.style.display = 'none';
        };

        const modalTitle = document.createElement('h2');
        modalTitle.innerText = 'Thông Báo'; // Tiêu đề cho hộp thoại

        const modalMessage = document.createElement('p');
        modalMessage.classList.add('modal-message');
        modalMessage.innerText = messages[0].innerText; // Lấy thông điệp đầu tiên

        const okButton = document.createElement('button');
        okButton.classList.add('ok-button');
        okButton.innerText = 'OK';
        okButton.onclick = function() {
            modal.style.display = 'none';
        };

        // Tạo nút "Đăng nhập tài khoản khác"
        const loginButton = document.createElement('button');
        loginButton.classList.add('login-button');
        loginButton.innerText = 'Đăng nhập tài khoản khác';
        loginButton.onclick = function() {
            window.location.href = '/login/'; // Đường dẫn đến trang đăng nhập
        };

        modalContent.appendChild(closeBtn); // Đặt nút đóng lên trên cùng
        modalContent.appendChild(modalTitle);
        modalContent.appendChild(modalMessage);
        modalContent.appendChild(okButton);
        modalContent.appendChild(loginButton); // Thêm nút vào modal

        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        modal.style.display = 'block'; // Hiện modal khi có thông báo
    }
});