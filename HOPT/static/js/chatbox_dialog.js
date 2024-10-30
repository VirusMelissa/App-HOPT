// Mở hộp thoại chat và tải tin nhắn của phòng ban tương ứng
function openChatDialog(button) {
    // Lấy giá trị phòng ban từ thuộc tính data-department của nút được nhấn
    const department = button.getAttribute("data-department");

    // Gán giá trị phòng ban cho thuộc tính data-department của hộp thoại chat
    const chatDialog = document.getElementById("chatDialog");
    chatDialog.setAttribute("data-department", department);

    chatDialog.style.display = "block";
    loadChatMessages(department); // Tải tin nhắn khi mở hộp thoại
    markMessagesAsRead(department); // Đánh dấu tin nhắn là đã đọc
}

// Đóng hộp thoại chat
function closeChatDialog() {
    document.getElementById("chatDialog").style.display = "none";
}

// Tải các tin nhắn chat của phòng ban tương ứng
function loadChatMessages(department) {
    fetch(`/get-chat-messages/${department}/`)
        .then(response => response.json())
        .then(data => {
            const chatMessages = document.getElementById("chatMessages");
            const currentUserId = data.current_user_id;
            chatMessages.innerHTML = ""; // Xóa nội dung cũ
            data.messages.forEach(msg => {
                const newMessage = document.createElement("div");
                const isCurrentUser = msg.user_id === currentUserId;
                newMessage.className = `chat-message ${isCurrentUser ? "sent" : "received"}`;
                newMessage.innerHTML = `<strong>${msg.user}:</strong> ${msg.message}`;
                chatMessages.appendChild(newMessage);
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => console.error("Error loading chat messages:", error));
}

// Gửi tin nhắn
function sendMessage() {
    const chatInput = document.getElementById("chatInput");
    const message = chatInput.value.trim();
    // Lấy giá trị phòng ban từ thuộc tính data-department của hộp thoại chat
    const department = document.getElementById("chatDialog").getAttribute("data-department");

    if (message) {
        fetch(`/send-message/${department}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({ message: message })
        }).then(() => {
            chatInput.value = ""; // Reset input
            loadChatMessages(department); // Cập nhật lại tin nhắn
            updateUnreadCount(department); // Cập nhật lại số lượng tin nhắn chưa đọc
        });
    }
}

// Đánh dấu tất cả tin nhắn của phòng ban tương ứng là đã đọc
function markMessagesAsRead(department) {
    fetch(`/mark-messages-as-read/${department}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    }).then(response => response.json())
      .then(data => {
          if (data.status === "success") {
              document.querySelector(`[data-department="${department}"]`).innerHTML = `<i class="far fa-comment"></i> Chat`;
          }
      });
}

// Cập nhật số lượng tin nhắn chưa đọc của phòng ban tương ứng
function updateUnreadCount(department) {
    fetch(`/get-unread-count/${department}/`)
        .then(response => response.json())
        .then(data => {
            const chatButton = document.querySelector(`[data-department="${department}"]`);
            if (data.unread_count > 0) {
                chatButton.innerHTML = `<i class="far fa-comment"></i> Chat (${data.unread_count})`;
            } else {
                chatButton.innerHTML = `<i class="far fa-comment"></i> Chat`;
            }
        });
}

// Cập nhật số lượng tin nhắn chưa đọc khi tải trang cho đúng phòng ban
document.addEventListener("DOMContentLoaded", () => {
    // Lấy giá trị phòng ban từ nút chatButton
    const chatButton = document.getElementById("chatButton");
    if (chatButton) {
        const department = chatButton.getAttribute("data-department");
        updateUnreadCount(department);
    }
});

// Hàm lấy CSRF Token từ cookie
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return decodeURIComponent(value);
    }
    return null;
}
