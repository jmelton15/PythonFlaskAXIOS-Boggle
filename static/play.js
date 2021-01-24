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
        if (time > 10) {
            $(".timer").removeClass("too-close");
            $(".timer").addClass("ok");
        }
        else if (time <= 10) {
            $(".timer").removeClass("ok");
            $(".timer").addClass("too-close");
        }
        $(".timer").text(`Game Timer: ${time}`);
        time --;
        localStorage.setItem("time",time);
        
        if (time == -1) {
            $gameBoardTable.hide();
            $sendWords.show();
            localStorage.clear();
            $sendWords.on("click", async function() {
                await show_stats();
            })
            clearInterval(intervalId);
        }
    }
    let intervalId = setInterval(() => {countdown()}, 1000);

    function getTime() {
        if (localStorage.getItem("time") != null && typeof localStorage.getItem("time") != 'undefined') {
            let time = localStorage.getItem("time");
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
        for(let i=0;i< words.length;i++) {
            guesses[i] = words[i];
        }

        
        let response = await axios.post('http://127.0.0.1:5000/play', {
            guesses
        })
        console.log(response.data)
        return response.data
    }
    
    /**
     * This function is called when the submit words button is pressed
     * it runs through the data returned to us from the server and displays the stats
     * of the game session
     */
    async function show_stats(){
        $sendWords.off();
        let response = await postWords();
        showElements();
        $correctList.empty();
        $missingDictList.empty();
        $missingBoardList.empty();
        console.log(response.score)
        console.log(response.on_board)
        console.log(response.missing_board)
        console.log(response.missing_dict)
        let wordsOnBoard = response.on_board;
        let score = response.score;
        //let wordsInDict = response.in_dictionary;
        let missingDict = response.missing_dict;
        let missingBoard = response.missing_board;
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
