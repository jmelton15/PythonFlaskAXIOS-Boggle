$(document).ready(function() {

    let $sendWords = $("#send-words");
    let $textArea = $("#floatingTextarea2");
    let $textAreaLabel = $("#text-label");
    let $stats = $("#stats-div");
    let $scoreHeader = $("#score-header");
    let $pOnBoard = $("#p-on-board");
    let $pMissingDict = $("#p-missing-dict");
    let $correctList = $("#on-board-list");
    let $missingDictList = $("#missing-dict-list");
    let $pMissingBoard = $("#p-missing-board");
    let $missingBoardList = $("#missing-board-list");
    let $gameBoardTable = $("#game-board-table");
    let timeSpan = document.querySelector(".timer.minute .hand span");
/**
 * The below code is the code for the timer.
 * Until the time is up the user can type words at will into the text area, but
 *    they cannot submit their words until time is up.
 * Once timer hits zero the button appears and the board dissapears (no one can cheat time!!!! hahaahah)
 * When a user submits their words, the button losses its click functionality so the user cannot keep 
 * calling the show_stats() function
 */
    $sendWords.hide();
    
    let time = getTime();
    

    /**
     * local storage is used here to allow the user to refresh the page or go back on accident 
     * and still have their timer going. That way the user cannot cheat time
     */
    function countdown() {
        //console.log(time)
        if (time <= 10) {
            $(".face p").css("color","red");
        }
        $("#lazy").text(`${time}`);
        time --;
        localStorage.setItem("time",time);
        if (time == -1) {
            timeSpan.style.border = "none";
            $gameBoardTable.hide();
            $sendWords.show();
            localStorage.removeItem("time");
            $sendWords.on("click", async function() {
                await show_stats();
            })
            clearInterval(intervalId);
        }
    }
    let intervalId = setInterval(() => {countdown()}, 1000);



    /**
     * this function checks to see if we already have stored timer in local storage yet
     *  if we have, then we return the time that was in local storage
     * otherwise start new timer at 60 seconds
     * This prevents time from being lost when the page is refreshed
     */
    function getTime() {
        if (localStorage.getItem("time") != null && typeof localStorage.getItem("time") != 'undefined') {
            let time = localStorage.getItem("time");
            // $(".timer.minute .hand span").css("animation-duration",time)
            timeSpan.style.animationDuration = `${time}s`
            return time;
        }
        else{
            let time = 60;
            localStorage.setItem("time",time);
            return time;
        }
    }
    

    hideElements();

    /**
     * keypress function to hide the bootstrap placeholder text when user starts typing
     */
    $textAreaLabel.show();
    $textArea.keypress(function() {
        $textAreaLabel.hide();
    })


    /**
     * function to post the words in our textarea back to the server
     * its stored as an object called guesses
     * we then await the response from the server which will return another object
     * of data for us to use on our page
     */
    async function postWords() {
        let words = $textArea.val().match(/\S+/g);
        let guesses = {}; 
        if (words == null) {
            $scoreHeader.text("You did not type any words in time. But Hey, we will allow you to take your best guess now!")
        }
        else {
            $sendWords.off();
            for(let i=0;i< words.length;i++) {
                guesses[i] = words[i];
            }
    
            let response = await axios.post('http://127.0.0.1:5000/play', {
                data: {
                    guesses,
                    "top-score": localStorage.getItem("top-score"),
                }
            })
            
            return response.data
        }
    }
    
    /**
     * This function is called when the submit words button is pressed
     * it runs through the data returned to us from the server and displays the stats
     * of the game session
     */
    async function show_stats(){
        let response = await postWords();
        showElements();
        $correctList.empty();
        $missingDictList.empty();
        $missingBoardList.empty();
        let wordsOnBoard = response.on_board;
        let score = response.score;
        let missingDict = response.missing_dict;
        let missingBoard = response.missing_board;
        storeTopScore(score);
        $scoreHeader.text(`Your Score This Round Was: ${score}`);
        if (wordsOnBoard.length < 1  ) {
            $pOnBoard.hide();
        }else{
            $pOnBoard.text("The Words You Guessed Below Were Valid on the Board and in The Dictionary");
        }
        
        for(let i=0;i < wordsOnBoard.length; i++) {
            let li = document.createElement("li");
            li.innerText = wordsOnBoard[i];
            $correctList.append(li);
        }

        if (missingBoard.length < 1 ) {
            $pMissingBoard.hide();
        }else{
            $pMissingBoard.text("The Words You Guessed Below Were Not On The Board");
        }

        for(let i=0;i < missingBoard.length; i++) {
            let li = document.createElement("li");
            li.innerText = missingBoard[i];
            $missingBoardList.append(li);
        }

        if (missingDict.length < 1 ) {
            $pMissingDict.hide();
        }else{
            $pMissingDict.text("The Words You Guessed Below Were Not Valid in The Dictionary");
        }
        
        for(let i=0;i < missingDict.length; i++) {
            let li = document.createElement("li");
            li.innerText = missingDict[i];
            $missingDictList.append(li);
        }
    }
    /**
     * 
     * This is a function that currently is only used to store local storage 
     * of the local user's top-score. Above, I do send it back to the server in a post request
     * however, at this point I do not use it for anything. Normally, instead of just using 
     * session on the server side, we would store the user's statistics in a database of some sort
     */
    function storeTopScore(score) {
        if (localStorage.getItem("top-score") == null) {
            localStorage.setItem("top-score",score);
        }
        else if (localStorage.getItem("top-score") < score) {
            localStorage.setItem("top-score",score);
        }
    }
    
    

    /**
     * simple hide and show functions for all the elements 
     */
    function hideElements() {
        $stats.hide(); 
        $scoreHeader.hide();
        $pOnBoard.hide(); 
        $pMissingDict.hide();
        $correctList.hide(); 
        $missingDictList.hide();
        $missingBoardList.hide();
        $pMissingBoard.hide();
    }
    function showElements() {
        $stats.show(); 
        $scoreHeader.show();
        $pOnBoard.show(); 
        $pMissingDict.show();
        $correctList.show(); 
        $missingDictList.show();
        $missingBoardList.show();
        $pMissingBoard.show();
    }
    


});
