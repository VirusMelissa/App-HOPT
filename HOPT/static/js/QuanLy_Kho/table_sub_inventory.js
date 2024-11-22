// Đồng bộ chiều rộng giữa 2 bảng tiêu đề và giá trị
document.addEventListener("DOMContentLoaded", function () {
    const headerTable = document.querySelector(".table-monthly_totals-header");
    const scrollTable = document.querySelector(".table-scroll table");

    function syncWidths() {
        const tableWidth = scrollTable.offsetWidth;
        headerTable.style.width = `${tableWidth}px`;
    }

    // Đồng bộ khi tải trang
    syncWidths();

    // Đồng bộ lại khi thay đổi kích thước cửa sổ
    window.addEventListener("resize", syncWidths);
});