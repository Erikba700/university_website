document.addEventListener("DOMContentLoaded", function() {
    const programs = document.querySelectorAll(".et-hero-tab");
    const programsPerPage = 3;
    let currentPage = 0;

    function displayPrograms() {
        programs.forEach((program, index) => {
            if (index >= currentPage * programsPerPage && index < (currentPage + 1) * programsPerPage) {
                program.style.display = "block";
            } else {
                program.style.display = "none";
            }
        });
    }

    displayPrograms();

    document.getElementById("custom-next-btn").addEventListener("click", function() {
        const maxPage = Math.ceil(programs.length / programsPerPage) - 1;
        if (currentPage < maxPage) {
            currentPage++;
            displayPrograms();
        }
    });

    document.getElementById("custom-prev-btn").addEventListener("click", function() {
        if (currentPage > 0) {
            currentPage--;
            displayPrograms();
        }
    });
});
