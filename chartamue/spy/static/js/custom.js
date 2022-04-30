$('#close-popup').click(function() {
    let popup = document.getElementById('popup');
    popup.style.opacity = "0";
    popup.style.zIndex = "-1";
});

$('.open-popup').click(function() {
    let popup = document.getElementById('popup');
    popup.style.opacity = "1";
    popup.style.zIndex = "1";
});