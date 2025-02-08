// Simple JavaScript for category selection
document.querySelectorAll('.category-list li').forEach(item => {
    if (!item.classList.contains('category-header')) {
        item.addEventListener('click', function() {
            // Remove active class from all items
            document.querySelectorAll('.category-list li').forEach(li => {
                li.classList.remove('active');
            });
            // Add active class to clicked item
            this.classList.add('active');
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle voting on posts and answers
    document.querySelectorAll('.vote-up, .vote-down').forEach(button => {
        button.addEventListener('click', function() {
            const voteCell = this.closest('.vote-cell');
            const voteCount = voteCell.querySelector('.vote-count');
            const currentCount = parseInt(voteCount.textContent);
            
            if (this.classList.contains('voted')) {
                // Undo vote
                this.classList.remove('voted');
                voteCount.textContent = this.classList.contains('vote-up') ? 
                    currentCount - 1 : currentCount + 1;
            } else {
                // Add vote
                this.classList.add('voted');
                const oppositeButton = this.classList.contains('vote-up') ?
                    voteCell.querySelector('.vote-down') :
                    voteCell.querySelector('.vote-up');
                
                oppositeButton.classList.remove('voted');
                voteCount.textContent = this.classList.contains('vote-up') ?
                    currentCount + 1 : currentCount - 1;
            }
        });
    });

    // Handle comment voting
    document.querySelectorAll('.upvote-comment').forEach(button => {
        button.addEventListener('click', function() {
            const scoreSpan = this.closest('.comment')
                .querySelector('.comment-score');
            const currentScore = parseInt(scoreSpan.textContent);
            
            if (this.classList.contains('voted')) {
                scoreSpan.textContent = currentScore - 1;
                this.classList.remove('voted');
            } else {
                scoreSpan.textContent = currentScore + 1;
                this.classList.add('voted');
            }
        });
    });

    // Handle bookmark button
    document.querySelector('.bookmark').addEventListener('click', function() {
        this.classList.toggle('bookmarked');
    });

    // Left sidebar
    const leftMenuToggle = document.getElementById('leftMenuToggle');
    const closeLeftSidebar = document.getElementById('closeLeftSidebar');
    const leftSidebar = document.querySelector('.left-sidebar');

    leftMenuToggle?.addEventListener('click', () => {
        leftSidebar.classList.add('active');
    });

    closeLeftSidebar?.addEventListener('click', () => {
        leftSidebar.classList.remove('active');
    });

    // Right sidebar
    const rightMenuToggle = document.getElementById('rightMenuToggle');
    const closeRightSidebar = document.getElementById('closeRightSidebar');
    const rightSidebar = document.querySelector('.right-sidebar');

    rightMenuToggle?.addEventListener('click', () => {
        rightSidebar.classList.add('active');
    });

    closeRightSidebar?.addEventListener('click', () => {
        rightSidebar.classList.remove('active');
    });

    // Close sidebars when clicking outside
    document.addEventListener('click', (e) => {
        if (!leftSidebar.contains(e.target) && e.target !== leftMenuToggle) {
            leftSidebar.classList.remove('active');
        }
        if (!rightSidebar.contains(e.target) && e.target !== rightMenuToggle) {
            rightSidebar.classList.remove('active');
        }
    });
}); 