window.onload = function() {
    var cells = document.querySelectorAll('.project-table td');

    for (var i = 0; i < cells.length; i++) {
        cells[i].addEventListener('click', function() {
            var link = this.querySelector('a');
            if (link) {
                window.location = link.href;
            }
        });
    }
};