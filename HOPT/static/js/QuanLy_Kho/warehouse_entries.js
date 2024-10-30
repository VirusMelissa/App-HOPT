document.addEventListener('DOMContentLoaded', function() { 
    const searchMainForm = document.querySelector('.searchMainForm');
    const filterForm = document.getElementById('filterForm');
    const sortLinks = document.querySelectorAll('.column-header');
    const paginationLinks = document.querySelectorAll('.pagination-btn');
    const itemPerPageSelect = document.querySelector('.items-per-page select');
    const yearSubSelect = document.querySelector('.year-sub-selector select');
    const searchSubForm = document.querySelector('.searchSubForm');
    
    // Thao tác tìm kiếm chính
    searchMainForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Ngăn chặn hành vi mặc định của form
        const searchMainInput = searchMainForm.querySelector('input[name="search_main"]').value;
        updateUrlWithParams({ search_main: searchMainInput });
        searchMainForm.submit();
    });

    // Thao tác lưu bộ lọc
    filterForm.addEventListener('click', function() {
        const year = filterForm.querySelector('input[name="year_main"]').value; // Cập nhật theo tên thực tế
        const productType = filterForm.querySelector('input[name="product_types"]').value; // Cập nhật theo tên thực tế
        updateUrlWithParams({ year_sub: year, product_type: productType });
        filterForm.submit();
    });

    // Thao tác sắp xếp
    sortLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Ngăn chặn hành vi mặc định của link
            const url = new URL(link.href);
            updateUrlWithParamsFromUrl(url);
            window.history.replaceState(null, '', url);
            window.location.href = link.href; // Điều hướng đến link sắp xếp
        });
    });

    // Thao tác chuyển trang
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Ngăn chặn hành vi mặc định của link
            const url = new URL(link.href);
            updateUrlWithParamsFromUrl(url);
            window.history.replaceState(null, '', url);
            window.location.href = link.href; // Điều hướng đến link phân trang
        });
    });

    // Thao tác phân trang
    itemPerPageSelect.addEventListener('change', function() {
        const selectedValue = itemPerPageSelect.value;
        updateUrlWithParams({ items_per_page: selectedValue });
        itemPerPageSelect.form.submit();
    });

    // Thao tác chọn năm trong sub-content
    yearSubSelect.addEventListener('change', function() {
        const selectedYear = yearSubSelect.value;
        updateUrlWithParams({ year_sub: selectedYear });
        yearSubSelect.form.submit();
    });

    // Thao tác tìm kiếm trong sub-content
    searchSubForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Ngăn chặn hành vi mặc định của form
        const searchSubInput = searchSubForm.querySelector('input[name="search_sub"]').value;
        updateUrlWithParams({ search_sub: searchSubInput });
        searchSubForm.submit();
    });

    function updateUrlWithParams(params) {
        const url = new URL(window.location);
        for (const [key, value] of Object.entries(params)) {
            if (value) {
                url.searchParams.set(key, value);
            } else {
                url.searchParams.delete(key);
            }
        }
        window.history.replaceState(null, '', url);
    }

    function updateUrlWithParamsFromUrl(url) {
        const paramsToDelete = ['page', 'sort', 'order', 'items_per_page', 'year_sub', 'year_main', 'product_type', 'search_sub', 'search_main'];
        paramsToDelete.forEach(param => {
            if (!url.searchParams.get(param) || url.searchParams.get(param) === '' || url.searchParams.get(param) === '[]') {
                url.searchParams.delete(param);
            }
        });
    }
});
