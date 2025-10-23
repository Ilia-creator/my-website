// === BASE VARIABLES ===
let score = 0;
let moneyForClick = 1;
let autoclicker = 0;

const $hamster = $("#hamster-img");
let currentImageIndex = 0;


// === THRESHOLDS & IMAGES ===
const thresholds = [1000, 100000, 1000000, 10000000, 100000000];
let thresholdIndex = 0;

const images = [
    "images/hamster1.jpg",
    "images/hamster2.jpg",
    "images/hamster3.jpg",
    "images/hamster4.png",
    "images/hamster5.png",
    "images/hamster6.png",
];

// === DOM ELEMENTS ===
const scoreText = document.getElementById("score-text");
const clickPowerText = document.getElementById("show-money-for-click");

// === UPDATE UI ===
function updateUI() {
    $("#score-text").text("Moneys: " + score);
    $("#show-money-for-click").text("+" + moneyForClick + " moneys for click");
    $("#show-autoclicker").text(autoclicker + " money per second");
}

// === CHANGE IMAGE ===
function changeImage(index) {
    index = Math.min(index, images.length - 1);
    if (currentImageIndex === index) return;
    $("#hamster-img").attr("src", images[index]);
    currentImageIndex = index;
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
    const pct = Math.min(((score - prev) / (next - prev)) * 100, 100);
    progressBar.css("width", pct + "%");

    if (score >= next) {
        thresholdIndex++;
        changeImage(thresholdIndex);
    }
}

// === CLICK ON HAMSTER ===
$hamster.on("click", function (event) {
    score += moneyForClick;
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
    score += autoclicker;
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
    if (score >= price) {
        moneyForClick += moneyUp;
        score -= price;
        updateUI();
    } else {
        alert("Not enough money!");
    }
}

function UpgradeAutoclickerCustom(price, up) {
    if (score >= price) {
        autoclicker += up;
        score -= price;
        updateUI();
    } else {
        alert("Not enough money!");
    }
}

// === CODES ===
const codes = ["Steve_Shuba", "FREE_moneys", "FREE_moneys_and_upgrades", "NewYear25", "ILoveSpring"];
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
            score += 1000;
            break;
        case "FREE_moneys_and_upgrades":
            score += 1000;
            moneyForClick += 10;
            autoclicker += 10;
            break;
        case "Steve_Shuba":
            score += 100000;
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
function saveGame() {
    const gameState = {
        score,
        moneyForClick,
        autoclicker,
        thresholdIndex,
        currentImageIndex,
    };
    localStorage.setItem("hamsterClickerSave", JSON.stringify(gameState));
}

function loadGame() {
    const saved = localStorage.getItem("hamsterClickerSave");
    if (!saved) return;
    const data = JSON.parse(saved);

    score = data.score || 0;
    moneyForClick = data.moneyForClick || 1;
    autoclicker = data.autoclicker || 0;
    thresholdIndex = data.thresholdIndex || 0;
    currentImageIndex = data.currentImageIndex || 0;

    changeImage(currentImageIndex);
    updateUI();
    updateProgressBar();
}

function newGame() {
    if (confirm("Are you sure you want to start a new game?")) {
        localStorage.removeItem("hamsterClickerSave");
        score = 0;
        moneyForClick = 1;
        autoclicker = 0;
        thresholdIndex = 0;
        changeImage(0);
        updateUI();
        updateProgressBar();
    }
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
    loadGame();
    updateUI();
    updateProgressBar();

    setInterval(Autoclicker, 1000);
    setInterval(saveGame, 5000);
};
