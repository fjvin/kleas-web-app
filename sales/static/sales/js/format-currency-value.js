function check() {
    let val = document.getElementById("price-num-input").value
    val = val.replace(',', '');
    val = val.replace(/[^0-9,.]*/, '');
    val = parseFloat(val);
    document.getElementById('price-num-input').value = val;
} 