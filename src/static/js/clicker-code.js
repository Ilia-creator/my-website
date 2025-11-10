function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    headers: { "X-CSRFToken": csrftoken }
});

// === BASE VARIABLES ===
let money = 0;
let moneyForClick = 1;
let autoclicker = 0;

const $hamster = $("#hamster-img");


// === THRESHOLDS & IMAGES ===
const thresholds = [1000, 100000, 1000000, 10000000, 100000000];
let thresholdIndex = 0;

const images = [
    "/media/hamsters/hamster1_gNWqbzk.jpg",
    "/media/hamsters/hamster2_m5RCr4O.jpg",
    "/media/hamsters/hamster3_W1yqIRj.jpg",
    "/media/hamsters/hamster4_Q2cejq9.png",
    "/media/hamsters/hamster5_ra2l8rr.png",
    "/media/hamsters/hamster6_LgRjE36.png",
];

// === DOM ELEMENTS ===
const scoreText = document.getElementById("score-text");
const clickPowerText = document.getElementById("show-money-for-click");

// === UPDATE UI ===
function updateUI() {
    $("#score-text").text("Moneys: " + money);
    $("#show-money-for-click").text("+" + moneyForClick + " moneys for click");
    $("#show-autoclicker").text(autoclicker + " money per second");
}

// === CHANGE IMAGE ===
const hamsterImg = document.getElementById("hamster-img");
imageIndex = 0

function changeHamster(index) {
    hamsterImg.src = images[index];
    imageIndex += 1;
}

if (money >= 1000 || imageIndex === 0) {
    changeHamster(1)
}
if (money >= 1000000 || imageIndex === 1) {
    changeHamster(2)
}
if (money >= 1000000000 || imageIndex === 2) {
    changeHamster(3)
}
if (money >= 1000000000000  || imageIndex === 3) {
    changeHamster(4)
}
if (money >= 1000000000000000 || imageIndex === 4) {
    changeHamster(5)
}
// === PROGRESS BAR ===
function updateProgressBar() {
    const progressBar = $("#progress-bar");
    if (thresholdIndex >= thresholds.length) {
        progressBar.css("width", "100%");
        return;
    }

    const prev = thresholdIndex > 0 ? thresholds[thresholdIndex - 1] : 0;
    const next = thresholds[thresholdIndex];
    const pct = Math.min(((money - prev) / (next - prev)) * 100, 100);
    progressBar.css("width", pct + "%");

    if (money >= next) {
        thresholdIndex++;
        changeHamster(thresholdIndex);
    }
}

// === CLICK ON HAMSTER ===
$hamster.on("click", function (event) {
    money += moneyForClick;
    updateUI();
    updateProgressBar();

    // flying coin animation
    const coin = $('<div class="coin">🪙</div>').appendTo("body");
    coin.css({
        position: "absolute",
        left: event.pageX + "px",
        top: event.pageY + "px",
        pointerEvents: "none",
        animation: "coinFly 1s ease-out forwards",
    });
    setTimeout(() => coin.remove(), 1000);
});

// === AUTOCLICKER ===
function Autoclicker() {
    money += autoclicker;
    updateUI();
    updateProgressBar();
}

// === UPGRADE FUNCTIONS ===
function PlayerAutoclickerUpgrade() {
    let amount = parseInt(prompt("How much autoclicker to add?"), 10);
    if (isNaN(amount) || amount <= 0) return;
    let price = amount * 100;
    let name = prompt("Enter a name for your button:");
    if (!name) return;

    let button = document.createElement("button");
    button.textContent = `${name} (+${amount} autoclicker for ${price} moneys)`;
    button.className = "shop-item";
    button.onclick = () => UpgradeAutoclickerCustom(price, amount);
    document.getElementById("shop-content").appendChild(button);
}

function PlayerAddMoneyForClick() {
    let amount = parseInt(prompt("Enter the number of money for click:"), 10);
    if (isNaN(amount) || amount <= 0) {
        alert("Invalid input!");
        return;
    }

    let price = amount * 10;
    let name = prompt("Enter a name for the button:");
    if (!name) return;

    let button = document.createElement("button");
    button.textContent = `${name} (+${amount} money/click for ${price} moneys)`;
    button.className = "shop-item";
    button.onclick = () => AddMoneyForClickCustom(price, amount);
    document.getElementById("shop-content").appendChild(button);
}

function AddMoneyForClickCustom(price, moneyUp) {
    if (money >= price) {
        moneyForClick += moneyUp;
        money -= price;
        updateUI();
    } else {
        alert("Not enough money!");
    }
}

function UpgradeAutoclickerCustom(price, up) {
    if (money >= price) {
        autoclicker += up;
        money -= price;
        updateUI();
    } else {
        alert("Not enough money!");
    }
}

// === CODES ===
let usedCodes = {};

function Code() {
    let code = prompt("Enter code:");
    if (!code) return;

    if (usedCodes[code]) {
        alert("You already used this code!");
        return;
    }

    switch (code) {
        case "FREE_moneys":
            money += 1000;
            break;
        case "FREE_moneys_and_upgrades":
            money += 1000;
            moneyForClick += 10;
            autoclicker += 10;
            break;
        case "Steve_Shuba":
            money += 100000;
            break;
        case "NewYear25":
            autoclicker += 1000;
            break;
        case "ILoveSpring":
            autoclicker += 10000;
            break;
        default:
            alert("Invalid code!");
            return;
    }

    usedCodes[code] = true;
    updateUI();
    updateProgressBar();
    alert("Code activated!");
}


// === SAVE / LOAD GAME ===
// Загружаем данные с сервера при загрузке страницы
function loadGame() {
    $.ajax({
        url: '/game/load/',
        type: 'GET',
        success: function (response) {
            console.log('📥 Данные при загрузке:', response);

            // Проверяем, чтобы значения были числами
            money = parseFloat(response.money) || 0;
            moneyForClick = parseFloat(response.money_per_click) || 1;
            autoclicker = parseInt(response.autoclicker_level) || 0;

        },
        error: function (xhr, status, error) {
            console.error('❌ Ошибка при загрузке:', error);
        }
    });
}

function saveGame() {
    const data = {
        money: money,
        money_per_click: moneyForClick,
        autoclicker_level: autoclicker
    };

    console.log('Saving data:', data);

    $.ajax({
        url: '/game/save/',
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            console.log('✅ Game saved:', response);
            alert("Game saved!");
        },
        error: function (xhr, status, error) {
            console.error('❌ Save failed:', error, xhr.responseText);
        }
    });
}



function newGame() {
    const csrfToken = getCookie('csrftoken');
    if (!confirm("Are you sure you want to start a new game? Your progress will be lost!")) {
        return;
    }

    $.post({
        url: '/game/new/',
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            console.log(response.message);
            // Сбрасываем переменные в JS
            money = 0;
            moneyForClick = 1;
            autoclicker = 0;
            updateUI();
            changeHamster(0);
            imageIndex = 0;
            alert("New game started!");
        },
        error: function() {
            alert("Error resetting game!");
        }
    });
}

// === SHOP ===
function openShop() {
    document.getElementById("shop-modal").style.display = "block";
}

function closeShop() {
    document.getElementById("shop-modal").style.display = "none";
}


// === HELP ===
function Help() {
    alert("Tap the hamster to earn money! Use the shop to buy upgrades.");
}


function sum(a, b) {
    return a + b;
}

const alexey = {
    name: "Alexey",
    lastName: "Shubnikov",
    age: 41
}

const ilia = {
    name: "Ilia",
    age: 11
}


class Person {
    name;
    age;

    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
}


const alexey2 = new Person("Alexey2", 21);

// === STARTUP ===
window.onload = function () {
    console.log(sum(alexey2.age, ilia.age));
    loadGame();
    updateUI();
    updateProgressBar();
    changeHamster(0)

    setInterval(Autoclicker, 1000);
};
