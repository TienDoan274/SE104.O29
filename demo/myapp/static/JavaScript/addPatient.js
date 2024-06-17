document.getElementById('themBN').addEventListener('submit', function(event) {
    event.preventDefault();

    var hoTen = document.getElementById('hoten').value;
    var ngayKham = document.getElementById('ngaykham').value;
    console.log(hoTen)
    $.ajax({
        url: '/kiem-tra-benh-nhan/',
        data: {
            'hoTen': hoTen,
            'ngayKham': ngayKham
        },
        dataType: 'json',
        success: function (data) {
            if (data.is_taken) {
                var confirmAdd = confirm("Bệnh nhân đã tồn tại trong ngày khám. Bạn có muốn thêm bệnh nhân này không?");
                if (confirmAdd) {
                    document.getElementById('themBN').submit();
                }
            } else {
                document.getElementById('themBN').submit();
            }
        }
    });
});