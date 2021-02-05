function triggerContent(event) {
    event = event || window.event;
    var source = event.target || event.srcElement;
    for (var elem of document.getElementsByClassName('contentItem')) {
        elem.className = 'contentItem hiddenItem';
    }
    document.getElementById(source.getAttribute('data-trigger-content')).className = 'contentItem';
}

function toggleDescription(event) {
    event = event || window.event;
    var source = event.target || event.srcElement;
    if (source.nextElementSibling.className == 'hiddenItem') {
        source.nextElementSibling.className = '';
    } else {
        source.nextElementSibling.className = 'hiddenItem';
    }
}

window.onload = function () {
    for (var elem of document.getElementsByClassName('navbutton')) {
        elem.addEventListener('click', triggerContent);
    }
}
