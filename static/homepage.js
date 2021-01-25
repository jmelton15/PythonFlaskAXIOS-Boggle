$(document).ready(function() {
    
    /**
     * this is here to clear the local storarge on a new game play
     * to refresh the timer when a new game is played
     */
    $("#start-btn").on("click", () => {
        localStorage.removeItem("time");
    })
    
    
})