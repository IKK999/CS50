document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#greeting').addEventListener('animationstart', () => {
        const greetingElement = document.querySelector('#greeting');
        const animationDuration = parseFloat(window.getComputedStyle(greetingElement).animationDuration);
        
        const halfwayTime = animationDuration / 2 * 1000;  
        
        let startTime = performance.now();
    
        function checkHalfwayPoint(timestamp) {
            const elapsedTime = timestamp - startTime;
    
            if (elapsedTime >= halfwayTime) {
                document.querySelector('#menu-view').style.display = 'block';
                document.querySelector('#hiragana-view').style.display = 'none';
                document.querySelector('#katakana-view').style.display = 'none';
                document.querySelector('#profile-view').style.display = 'none';
                document.querySelector('#about-view').style.display = 'none';
    
                return;
            }
    
            requestAnimationFrame(checkHalfwayPoint);
        }
    
        requestAnimationFrame(checkHalfwayPoint);
    });

    document.querySelector('#menu').onclick = () => {
        document.querySelector('#menu-view').style.display = 'block';
        document.querySelector('#hiragana-view').style.display = 'none';
        document.querySelector('#katakana-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#about-view').style.display = 'none';
    }

    document.querySelector('#hiragana').onclick = () => {
        document.querySelector('#menu-view').style.display = 'none';
        document.querySelector('#hiragana-view').style.display = 'block';
        document.querySelector('#katakana-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#about-view').style.display = 'none';
        load_exercises("hiragana");
    }

    document.querySelector('#katakana').onclick = () => {
        document.querySelector('#menu-view').style.display = 'none';
        document.querySelector('#hiragana-view').style.display = 'none';
        document.querySelector('#katakana-view').style.display = 'block';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#about-view').style.display = 'none';
        load_exercises("katakana");
    }

    document.querySelector('#profile').onclick = () => {
        document.querySelector('#menu-view').style.display = 'none';
        document.querySelector('#hiragana-view').style.display = 'none';
        document.querySelector('#katakana-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'block';
        document.querySelector('#about-view').style.display = 'none';
        refresh_completions();
        load_profile();
    }

    document.querySelector('#about').onclick = () => {
        document.querySelector('#menu-view').style.display = 'none';
        document.querySelector('#hiragana-view').style.display = 'none';
        document.querySelector('#katakana-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#about-view').style.display = 'block';
    }

})


let hiragana_level = null
let katakana_level = null

let hiragana_completion = 0.0
let katakana_completion = 0.0

if (hiragana_level === null && katakana_level === null) {
    refresh_levels();
    refresh_completions();
}

function refresh_levels() {
    fetch('get_levels')
    .then(response => response.json())
    .then(results => {
        hiragana_level = results[0];
        katakana_level = results[1];
    });
}

function load_profile() {
    document.querySelector("#hiragana-level").innerHTML = `Hiragana Level: ${hiragana_level / 100.0}`;
    document.querySelector("#hiragana-completion").innerHTML = `Completion: ${(Math.floor(hiragana_completion * 10000) / 100).toFixed(2)}%`;
    document.querySelector("#hiragana-indication").style.width = `${15 * hiragana_completion}vw`;

    document.querySelector("#katakana-level").innerHTML = `Katakana Level: ${katakana_level / 100.0}`;
    document.querySelector("#katakana-completion").innerHTML = `Completion: ${(Math.floor(katakana_completion * 10000) / 100).toFixed(2)}%`;
    document.querySelector("#katakana-indication").style.width = `${15 * katakana_completion}vw`;
}

function refresh_completions() {
    refresh_levels();
    let count_total_h = 0.0
    let count_total_k = 0.0

    let count_done_h = 0.0
    let count_done_k = 0.0

    fetch('get_exercises')
    .then(response => response.json())
    .then(exercises => {
        for (let i = 0; i < exercises.length; i++) {
            if (exercises[i].type === "hiragana") {
                if (exercises[i].level % 100 !== 0) {
                    count_total_h++;
                    if (hiragana_level >= exercises[i].level) {
                        count_done_h++;
                    }
                }
            }
            else {
                if (exercises[i].level % 100 !== 0) {
                    count_total_k++;
                    if (katakana_level >= exercises[i].level) {
                        count_done_k++;
                    }
                }
            }
        }
        hiragana_completion = count_done_h / count_total_h;
        katakana_completion = count_done_k / count_total_k;
    });
}

function load_exercises(type) {
    element = document.querySelector(`#${type}-view`);
    element.innerHTML = "";
    let cur_level = (type === "hiragana" ? hiragana_level : katakana_level);
    fetch('get_exercises')
    .then(response => response.json())
    .then(exercises => {
        for (let i = 0; i < exercises.length; i++) {
            if (exercises[i].type === type) {
                element.innerHTML = element.innerHTML + `
                <div onclick="${exercises[i].level % 100 === 0 ? `change_display(${exercises[i].level}, ${exercises[i].type})` : `start_exercise(${exercises[i].level}, ${exercises[i].type}, '${exercises[i].hint}')`}" ${exercises[i].level % 100 === 0 ? (cur_level + 1 >= exercises[i].level ? `style="display: block; background-color: rgb(242, 220, 166);"` : `style="display: block; background-color: rgb(207, 207, 207);"`) : (cur_level + 1 >= exercises[i].level ? `style="display: none; background-color: rgb(255, 239, 200); pointer-events: auto;"` : `style="display: none; background-color: rgb(237, 237, 237); pointer-events: none;"`)} 
                class="${exercises[i].level % 100 === 0 ? `${exercises[i].type}-parent` : `${exercises[i].type}-child`}" id="${exercises[i].level}">
                
                    <p>${exercises[i].level / 100.0} - ${exercises[i].representation}</p>

                </div>
                `;
            }
        }
    });
}

function change_display(level, type123) {
    let type = "";
    if (typeof type123 !== 'string') {
        type = type123.innerHTML;
    }
    else {
        type = type123;
    }
    type = type.toLowerCase();
    children = document.querySelectorAll(`.${type}-child`);
    children.forEach(function(child) {
        if (child.id > level && child.id < level + 100) {
            if (child.style.display === "none") {
                child.style.display = "block";
            }
            else {
                child.style.display = "none";
            }
        }
    });
}

function start_exercise(level, type123, hint) {
    document.querySelector('#main-interface').style.display = 'none';
    document.querySelector('#hiragana-view').style.display = 'none';
    document.querySelector('#katakana-view').style.display = 'none';
    document.querySelector('#exercise-view').style.display = 'block';

    type123 = type123.innerHTML
    exercise = document.querySelector('#exercise-view');


    exercise.innerHTML = `
    <h1>${type123} ${level / 100.0}</h1>
    <h1>${hint}</h1>
    <button onclick="begin_exercise(${level}, '${type123}')" class="confirmation" id="lets_go">Let's Go!</button>
    `;
}

function begin_exercise(level, type123) {
    let type = type123.toLowerCase();
    exercise = document.querySelector('#exercise-view');
    exercise.innerHTML = `<h1>${type123} ${level / 100.0}</h1>`;

    fetch(`get_tasks/${type}/${level}`)
    .then(response => response.json())
    .then(tasks => {
        console.log(type);
        console.log(level);
        let for_match = [];
        let exercise_ids = [];
        let stance_count = 0;
        for (let i = 0; i < tasks.length; i++) {
            console.log(tasks[i]);
            if (tasks[i].min_level == level) {
            if (tasks[i].priority) {
                for_match.push(i);
            }

            let question_type = Math.floor(Math.random() * 4) + 1;
            if (question_type == 1) {

                let answers = []
                let ans = tasks[i].romaji
                answers.push(ans);
                while (answers.length < 4) {
                    while (answers.includes(ans)) {
                        ans = tasks[Math.floor(Math.random() * tasks.length)].romaji;
                    }
                    answers.push(ans);
                }

                for (let j = 3; j > 0; j--) {
                    const k = Math.floor(Math.random() * (j + 1));
                    [answers[j], answers[k]] = [answers[k], answers[j]];
                }

                let corr = null
                for (let j = 0; j < 4; j++) {
                    if (tasks[i].romaji === answers[j]) {
                        corr = j;
                    }
                }

                exercise.innerHTML = exercise.innerHTML + `
                <div class="choose_romaji" id="exercise_${i + 1}" ${i + 1 === 1 ? `style="display: block;"` : `style="display: none;"`}>
                    <div class="question">
                        <h1>${tasks[i].japanese}</h1>
                    </div>

                    <form id="guess_form_${i + 1}">
                        <p>Select the right answer</p>
                        <label>
                            <input type="radio" name="guess" value="${answers[0] === tasks[i].romaji ? "correct" : "incorrect"}" />
                            ${answers[0]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[1] === tasks[i].romaji ? "correct" : "incorrect"}" />
                            ${answers[1]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[2] === tasks[i].romaji ? "correct" : "incorrect"}" />
                            ${answers[2]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[3] === tasks[i].romaji ? "correct" : "incorrect"}" />
                            ${answers[3]}
                        </label><br>
                        <input class="confirmation" type="submit" value="Submit" />
                    </form>

                </div>
                `;

                exercise_ids.push(i + 1);

                setTimeout(() => {
                    document.getElementById(`guess_form_${i + 1}`).addEventListener("submit", function(event) {
                        event.preventDefault();
                        selected_guess = document.querySelector(`input[name="guess"]:checked`);
                        let guesses = document.getElementsByName("guess");
                        guesses.forEach(function(radio) {
                            radio.checked = false;
                        });

                        if (selected_guess) {

                            document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "none";
                            if (exercise_ids[1] === undefined) {
                                if (selected_guess.value === "incorrect") {
                                    document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "block";
                                }
                                else {
                                    console.log("Regular questions done");
                                    refresh_match();
                                }
                            }
                            else {
                                document.querySelector(`#exercise_${exercise_ids[1]}`).style.display = "block";
                            }
                            if (selected_guess.value === "correct") {
                                console.log("Correct");
                                notify_result(true);
                                exercise_ids.shift();
                            }
                            else {
                                console.log("Incorrect");
                                notify_result(false);
                                exercise_ids.push(exercise_ids.shift());
                            }
                            console.log(exercise_ids[0]);
                            
                        }
                        else {
                            alert("Not selected!");
                        }
                    });
                }, 0);

            }
            else if (question_type == 2) {

                let answers = []
                let ans = tasks[i].japanese
                answers.push(ans);
                while (answers.length < 4) {
                    while (answers.includes(ans)) {
                        ans = tasks[Math.floor(Math.random() * tasks.length)].japanese;
                    }
                    answers.push(ans);
                }

                for (let j = 3; j > 0; j--) {
                    const k = Math.floor(Math.random() * (j + 1));
                    [answers[j], answers[k]] = [answers[k], answers[j]];
                }

                let corr = null
                for (let j = 0; j < 4; j++) {
                    if (tasks[i].japanese === answers[j]) {
                        corr = j;
                    }
                }

                exercise.innerHTML = exercise.innerHTML + `
                <div class="choose_japanese" id="exercise_${i + 1}" ${i + 1 === 1 ? `style="display: block;"` : `style="display: none;"`}>
                    <div class="question">
                        <h1>${tasks[i].romaji}</h1>
                    </div>

                    <form id="guess_form_${i + 1}">
                        <p>Select the right answer</p>
                        <label>
                            <input type="radio" name="guess" value="${answers[0] === tasks[i].japanese ? "correct" : "incorrect"}" />
                            ${answers[0]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[1] === tasks[i].japanese ? "correct" : "incorrect"}" />
                            ${answers[1]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[2] === tasks[i].japanese ? "correct" : "incorrect"}" />
                            ${answers[2]}
                        </label><br>
                        <label>
                            <input type="radio" name="guess" value="${answers[3] === tasks[i].japanese ? "correct" : "incorrect"}" />
                            ${answers[3]}
                        </label><br>
                        <input class="confirmation" type="submit" value="Submit" />
                    </form>

                </div>
                `;

                exercise_ids.push(i + 1);

                setTimeout(() => {
                    document.getElementById(`guess_form_${i + 1}`).addEventListener("submit", function(event) {
                        event.preventDefault();
                        selected_guess = document.querySelector(`input[name="guess"]:checked`);
                        let guesses = document.getElementsByName("guess");
                        guesses.forEach(function(radio) {
                            radio.checked = false;
                        });

                        if (selected_guess) {

                            document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "none";
                            if (exercise_ids[1] === undefined) {
                                if (selected_guess.value === "incorrect") {
                                    document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "block";
                                }
                                else {
                                    console.log("Regular questions done");
                                    refresh_match();
                                }
                            }
                            else {
                                document.querySelector(`#exercise_${exercise_ids[1]}`).style.display = "block";
                            }
                            if (selected_guess.value === "correct") {
                                console.log("Correct");
                                notify_result(true);
                                exercise_ids.shift();
                            }
                            else {
                                console.log("Incorrect");
                                notify_result(false);
                                exercise_ids.push(exercise_ids.shift());
                            }
                            console.log(exercise_ids[0]);
                            
                        }
                        else {
                            alert("Not selected!");
                        }
                    });
                }, 0);

            }
            else if (question_type == 3) {

                exercise.innerHTML = exercise.innerHTML + `
                <div class="input_romaji" id="exercise_${i + 1}" ${i + 1 === 1 ? `style="display: block;"` : `style="display: none;"`}>
                    <div class="question">
                        <h1>${tasks[i].japanese}</h1>
                    </div>

                    <form id="guess_form_${i + 1}">
                        <p>Input the equivalent romaji</p>
                        <label for="stance">Romaji:</label>
                        <input type="text" id="stance_${i + 1}" name="stance"><br><br>
                        <input class="confirmation" type="submit" value="Submit">
                    </form>
                </div>
                `;

                exercise_ids.push(i + 1);

                setTimeout(() => {
                    document.getElementById(`guess_form_${i + 1}`).addEventListener("submit", function(event) {
                        event.preventDefault();
                        selected_guess = (document.querySelector(`#stance_${i + 1}`)).value
                        let stances = document.querySelectorAll(`input[name="stance"]`);
                        stances.forEach(function(input) {
                            input.value = "";
                        });

                        if (selected_guess) {

                            document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "none";
                            if (exercise_ids[1] === undefined) {
                                if (selected_guess !== tasks[i].romaji) {
                                    document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "block";
                                }
                                else {
                                    console.log("Regular questions done");
                                    refresh_match();
                                }
                            }
                            else {
                                document.querySelector(`#exercise_${exercise_ids[1]}`).style.display = "block";
                            }
                            if (selected_guess === tasks[i].romaji) {
                                console.log("Correct");
                                notify_result(true);
                                exercise_ids.shift();
                            }
                            else {
                                console.log("Incorrect");
                                notify_result(false);
                                exercise_ids.push(exercise_ids.shift());
                            }
                            console.log(exercise_ids[0]);
                            
                        }
                        else {
                            alert("Not selected!");
                        }
                    });
                }, 0);

            }
            else if (question_type == 4) {
                exercise.innerHTML = exercise.innerHTML + `
                <div class="input_japanese" id="exercise_${i + 1}" ${i + 1 === 1 ? `style="display: block;"` : `style="display: none;"`}>
                    <div class="question">
                        <h1>${tasks[i].romaji}</h1>
                    </div>

                    <form id="guess_form_${i + 1}">
                        <p>Input the equivalent ${type}</p>
                        <label for="stance">${type123}:</label>
                        <br><input type="text" id="stance_${i + 1}" name="stance"><br><br>
                        <input class="confirmation" type="submit" value="Submit">
                    </form>
                </div>
                `;

                exercise_ids.push(i + 1);

                setTimeout(() => {
                    document.getElementById(`guess_form_${i + 1}`).addEventListener("submit", function(event) {
                        event.preventDefault();
                        selected_guess = (document.querySelector(`#stance_${i + 1}`)).value
                        let stances = document.querySelectorAll(`input[name="stance"]`);
                        stances.forEach(function(input) {
                            input.value = "";
                        });

                        if (selected_guess) {

                            document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "none";
                            if (exercise_ids[1] === undefined) {
                                if (selected_guess !== tasks[i].japanese) {
                                    document.querySelector(`#exercise_${exercise_ids[0]}`).style.display = "block";
                                }
                                else {
                                    console.log("Regular questions done");
                                    refresh_match();
                                }
                            }
                            else {
                                document.querySelector(`#exercise_${exercise_ids[1]}`).style.display = "block";
                            }
                            if (selected_guess === tasks[i].japanese) {
                                console.log("Correct");
                                notify_result(true);
                                exercise_ids.shift();
                            }
                            else {
                                console.log("Incorrect");
                                notify_result(false);
                                exercise_ids.push(exercise_ids.shift());
                            }
                            console.log(exercise_ids[0]);
                            
                        }
                        else {
                            alert("Not selected!");
                        }
                    });
                }, 0);

            }
        }
        }
        
        let num = 0;
        if (for_match[0]) {
            num = for_match[0];
        }
        while (for_match.length < 5) {
            while (for_match.includes(num) || tasks[num].min_level != level) {
                num = Math.floor(Math.random() * tasks.length);
            }
            for_match.push(num);
        }

        for (let i = for_match.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [for_match[i], for_match[j]] = [for_match[j], for_match[i]];
        }

        for (let i = 0; i < for_match.length; i++) {
            exercise.innerHTML = exercise.innerHTML + `
            <div onclick="match_operator('match_romaji_${i + 1}', '${tasks[for_match[i]].romaji}', ${level}, '${type}')" class="match_options_romaji" id="match_romaji_${i + 1}" style="display: none; position: absolute; top: ${(i + 1) * 15}%;">
                <p>${tasks[for_match[i]].romaji}</p>
            </div>
            `;
        }

        for (let i = for_match.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [for_match[i], for_match[j]] = [for_match[j], for_match[i]];
        }

        for (let i = 0; i < for_match.length; i++) {
            exercise.innerHTML = exercise.innerHTML + `
            <div onclick="match_operator('match_japanese_${i + 1}', '${tasks[for_match[i]].romaji}', ${level}, '${type}')" class="match_options_japanese" id="match_japanese_${i + 1}" style="display: none; position: absolute; top: ${(i + 1) * 15}%;">
                <p>${tasks[for_match[i]].japanese}</p>
            </div>
            `;
        }

        
        
        function refresh_match() {
            document.querySelectorAll(".match_options_romaji").forEach(function(element) {
                element.style.display = "block";
            });
            document.querySelectorAll(".match_options_japanese").forEach(function(element) {
                element.style.display = "block";
            });
        }
        
    });
}

let num_matches = 0
let selected_id = "";
let selected_equalizer = "";

function match_operator(id, equalizer, level, type) {
    if (selected_id === "" || selected_id.startsWith(id.slice(0, 7))) {

        if (selected_id !== "") {
            document.querySelector(`#${selected_id}`).style.opacity = 1;
        }
        document.querySelector(`#${id}`).style.opacity = 0.66;

        selected_id = id;
        selected_equalizer = equalizer;
    }
    else {
        if (selected_equalizer === equalizer) {
            console.log("Correct");
            notify_result(true);
            num_matches++;

            document.querySelector(`#${selected_id}`).style.opacity = 0.33;
            document.querySelector(`#${id}`).style.opacity = 0.33;
            document.querySelector(`#${selected_id}`).style.pointerEvents = "none";
            document.querySelector(`#${id}`).style.pointerEvents = "none";
            selected_id = "";
            selected_equalizer = "";

            if (num_matches === 5) {
                num_matches = 0;
                finish_exercise(level, type);
            }
        }
        else {
            console.log("Incorrect");
            notify_result(false);
            document.querySelector(`#${selected_id}`).style.opacity = 1;
            document.querySelector(`#${id}`).style.opacity = 1;
            document.querySelector(`#${selected_id}`).style.pointerEvents = "block";
            document.querySelector(`#${id}`).style.pointerEvents = "block";
            selected_id = "";
            selected_equalizer = "";
        }
    }
}

function notify_result(is_correct) {
    if (is_correct) {
        document.querySelector("#result-notifier").innerHTML = `<p style="color: green;">Correct!</p>`;
    }
    else {
        document.querySelector("#result-notifier").innerHTML = `<p style="color: red;">Incorrect!</p>`;
    }
    document.querySelector("#result-notifier").style.display = "block";
    document.querySelector("#result-notifier").classList.add("animate");

    document.querySelector("#result-notifier").addEventListener('animationend', () => {
        document.querySelector("#result-notifier").style.display = "none";
        document.querySelector("#result-notifier").classList.remove("animate");
    });
}

function finish_exercise(level, type) {
    console.log("The exercise is now over");
    exercise = document.querySelector('#exercise-view');
    exercise.innerHTML = `<h1>${type.charAt(0).toUpperCase() + type.slice(1)} ${level / 100.0}<br></h1>`;
    exercise.innerHTML = exercise.innerHTML + `
    <div>
        <h2>Good Job!<br></h2>
        <h3>Congrats with the level ${level} of ${type}!<br></h3>
        <h4>Click next to continue.<br></h4>
        <button onclick="go_back(${level}, '${type}')" class="confirmation" id="next">Next</button>
    </div>
    `;
}

async function go_back(level, type) {

    await fetch(`update_level`, {
        method: "PUT",
        body: JSON.stringify({
            type: type,
            level: level
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (type === "hiragana") {
            hiragana_level = result;
        }
        else {
            katakana_level = result;
        }

        refresh_completions();
        document.querySelector('#main-interface').style.display = 'block';
        document.querySelector(`#${type}-view`).style.display = 'block';
        document.querySelector('#exercise-view').style.display = 'none';
        load_exercises(type);
    });

}