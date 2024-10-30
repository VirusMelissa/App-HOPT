document.addEventListener('DOMContentLoaded', function() {
    const countdownElement = document.getElementById('countdown');

    // Lấy thời gian gửi mã từ sessionStorage
    const sentTimeStr = sessionStorage.getItem('code_sent_time2');
    if (!sentTimeStr) {
        countdownElement.textContent = '0:00';
        return;
    }

    // Chuyển đổi chuỗi thành đối tượng thời gian
    const sentTime = new Date(sentTimeStr);
    const currentTime = new Date();
    const countdownDuration = 2 * 60 * 1000; // 2 phút tính bằng milliseconds

    // Tính thời gian còn lại
    const timeElapsed = currentTime - sentTime;
    const timeRemaining = countdownDuration - timeElapsed;

    if (timeRemaining <= 0) {
        countdownElement.textContent = '0:00';
        return;
    }

    // Chuyển đổi thời gian còn lại thành phút và giây
    let countdownTime = Math.floor(timeRemaining / 1000);
    function updateCountdown() {
        const minutes = Math.floor(countdownTime / 60);
        const seconds = countdownTime % 60;
        countdownElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (countdownTime > 0) {
            countdownTime--;
        } else {
            countdownElement.textContent = '0:00';
        }
    }

    // Cập nhật mỗi giây
    updateCountdown();
    setInterval(updateCountdown, 1000);
});
