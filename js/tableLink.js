window.onload = function() {
    var cells = document.querySelectorAll('.project-table td');

    for (var i = 0; i < cells.length; i++) {
        cells[i].addEventListener('click', function() {
            var link = this.getAttribute('data-link');
            if (link && link != "blank") {
                window.location = link;
            }
        });
    }
};