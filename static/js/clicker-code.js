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
let images = []; // filled from server
let imageIndex = 0;
let thresholds = [1000, 100000, 1000000, 10000000, 100000000];
let thresholdIndex = 0;
let money_goal = 1000;

// Sync image/goal to loaded money
function syncImageToMoney() {
    if (!Array.isArray(images) || images.length === 0) return;

    // Find which threshold we've passed
    for (let i = thresholds.length - 1; i >= 0; i--) {
        if (money >= thresholds[i]) {
            thresholdIndex = i;
            imageIndex = Math.min(i + 1, images.length - 1);
            money_goal = thresholds[i + 1] || thresholds[i] * 10;
            changeHamster(imageIndex);
            break;
        }
    }

    // If below first threshold
    if (money < thresholds[0]) {
        thresholdIndex = 0;
        imageIndex = 0;
        money_goal = thresholds[0];
        changeHamster(0);
    }
}

// Check if we need to upgrade hamster image
function checkImageUpgrade() {
    if (thresholdIndex < thresholds.length && money >= thresholds[thresholdIndex]) {
        thresholdIndex++;
        imageIndex = Math.min(thresholdIndex, images.length - 1);
        money_goal = thresholds[thresholdIndex] || thresholds[thresholdIndex - 1] * 10;
        changeHamster(imageIndex);
    }
}

function loadHamsterImages() {
    fetch('/game/hamster-images/')
        .then(response => {
            if (!response.ok) throw new Error('Failed to load images');
            return response.json();
        })
        .then(data => {
            images = Array.isArray(data.images) ? data.images : [];
            imageIndex = 0;
            thresholdIndex = 0;

            // set initial image only if we have at least one
            if (images.length > 0) {
                changeHamster(0);
            }
            try {
                updateUI();
                updateProgressBar();
            } catch (e) {
                // ignore if other functions not defined yet
            }
        })
        .catch(err => console.error('Error loading hamster images:', err));
}

// === UPDATE UI ===
function updateUI() {
    $("#score-text").text("Moneys: " + money);
    $("#show-money-for-click").text("+" + moneyForClick + " moneys for click");
    $("#show-autoclicker").text(autoclicker + " money per second");
}

// === CHANGE IMAGE ===
function changeHamster(index) {
    if (!Array.isArray(images) || images.length === 0) {
        // no images loaded yet – do nothing
        return;
    }

    // clamp index into valid range
    index = Math.max(0, Math.min(index, images.length - 1));
    imageIndex = index;

    // images[] contains absolute URLs returned by the server
    const el = document.getElementById("hamster-img");
    if (el) {
        el.src = images[imageIndex];
    }
}

// === PROGRESS BAR ===
function updateProgressBar() {
    const progressBar = $("#progress-bar");
    const currentGoal = money_goal || 1000;
    const prevGoal = thresholdIndex > 0 ? thresholds[thresholdIndex - 1] : 0;

    if (money >= currentGoal) {
        progressBar.css("width", "100%");
    } else {
        const pct = Math.min(((money - prevGoal) / (currentGoal - prevGoal)) * 100, 100);
        progressBar.css("width", Math.max(0, pct) + "%");
    }
}

// === CLICK ON HAMSTER ===
$hamster.on("click", function (event) {
    money += moneyForClick;
    checkImageUpgrade();
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
    checkImageUpgrade();
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
    checkImageUpgrade();
    updateUI();
    updateProgressBar();
    alert("Code activated!");
}

// === SAVE / LOAD GAME ===
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

            // Sync image after loading
            syncImageToMoney();
            updateUI();
            updateProgressBar();
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
            money = 0;
            moneyForClick = 1;
            autoclicker = 0;
            imageIndex = 0;
            thresholdIndex = 0;
            money_goal = 1000;
            updateUI();
            changeHamster(0);
            updateProgressBar();
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

// === STARTUP ===
window.onload = function () {
    loadHamsterImages();
    loadGame();
    updateUI();
    updateProgressBar();
    setInterval(Autoclicker, 1000);
};