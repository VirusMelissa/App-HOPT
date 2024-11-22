$(document).ready(function() {
    // Xử lý tìm kiếm
    $('form').on('submit', function(e) {
        e.preventDefault();
        loadData();
    });

    // Hàm để tải dữ liệu
    function loadData(page = 1, sort = '', order = '') {
        $.ajax({
            url: "/user-management/",  // Thay đổi URL tại đây
            method: "GET",
            data: {
                page: page,
                sort: sort || $('input[name="sort"]').val(),  // Lấy giá trị sort từ input ẩn
                order: order || $('input[name="order"]').val(), // Lấy giá trị order từ input ẩn
                search: $('input[name="search"]').val() || '' // Lấy từ input tìm kiếm
            },
            success: function(data) {
                $('#userTable tbody').html(data);
            }
        });
    }

    // Sắp xếp
    $('th a').on('click', function(e) {
        e.preventDefault();
        const newSort = $(this).attr('href').split('sort=')[1].split('&')[0];
        const newOrder = $(this).attr('href').split('order=')[1].split('&')[0];
        loadData(1, newSort, newOrder);
    });

    // Phân trang
    $(document).on('click', '.pagination-btn', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        loadData(page);
    });
});
