document.addEventListener('DOMContentLoaded', function() {
    next = document.querySelector("#next");
    previous = document.querySelector("#previous");
    page1 = document.querySelector("#page1");
    page2 = document.querySelector("#page2");
    next.addEventListener('click', function() {
        page1.style.display = 'none';
        page2.style.display = 'block';
    })
    previous.addEventListener('click', function() {
        page2.style.display = 'none';
        page1.style.display = 'block';
    })
})

document.addEventListener('DOMContentLoaded', function() {
    maintainance_checkbox = document.querySelector('#maintainance_checkbox');
    maintainance = document.querySelector('#maintainance');
    maintainance_checkbox.addEventListener('click', function() {
        if (maintainance.style.display == 'block') {
            maintainance.style.display = 'none';
        }
        else {
            maintainance.style.display = 'block';
        }
    })
})

