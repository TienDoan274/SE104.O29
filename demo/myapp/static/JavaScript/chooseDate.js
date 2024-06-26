document.getElementById('ngaykham').valueAsDate = new Date();

document.getElementById('dateForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const dateInput = document.getElementById('ngaykham').value;
    if (dateInput) {
        const date = new Date(dateInput);
        const day = date.getDate();
        const month = date.getMonth() + 1; // Lưu ý: getMonth() trả về giá trị từ 0-11
        const year = date.getFullYear();
        const formattedDate = `${year.toString().padStart(4, '0')}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`; // Định dạng ngày thành mm/dd/yyyy
        // Tạo URL với các tham số ngày, tháng và năm
        const url = `../dsKhambenh/${formattedDate}`;

        // Chuyển hướng tới URL mới
        window.location.href = url;
    } else {
        alert('Vui lòng chọn một ngày.');
    }
});