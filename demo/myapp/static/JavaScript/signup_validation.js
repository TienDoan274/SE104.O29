document.getElementById('id_date_of_birth').addEventListener('change', function() {
    var dob = new Date(this.value);
    var today = new Date();
    var age = today.getFullYear() - dob.getFullYear();
    var monthDiff = today.getMonth() - dob.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    if (age < 18) {
        alert('You must be at least 18 years old to register.');
        this.value = ''; // Xóa giá trị ngày sinh
    }
});