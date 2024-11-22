document.addEventListener("DOMContentLoaded", function() {
    const messageBox = document.querySelector(".success-message");
    const overlay = document.querySelector(".overlay");
    const closeBtn = document.querySelector(".success-message .close-btn");

    // Hiển thị lớp phủ và thông báo
    if (messageBox) {
        overlay.style.display = "block";  // Hiển thị lớp phủ
        setTimeout(function() {
            messageBox.style.display = "none";
            overlay.style.display = "none";  // Ẩn lớp phủ sau 5 giây
        }, 5000);
    }

    // Ẩn thông báo và lớp phủ khi nhấn nút đóng
    if (closeBtn) {
        closeBtn.addEventListener("click", function() {
            messageBox.style.display = "none";
            overlay.style.display = "none";  // Ẩn lớp phủ khi đóng thông báo
        });
    }
});
