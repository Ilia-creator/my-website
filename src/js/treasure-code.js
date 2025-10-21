let getRandomNumber = function (size) {
    return Math.floor(Math.random() * size);
};
let getDistance = function (event, target) {
    var diffX = event.offsetX - target.x;
    var diffY = event.offsetY - target.y;
    return Math.sqrt((diffX * diffX) + (diffY * diffY));
};

let getDistanceHit = function (distance) {
    if (distance < 10) {
        return "Very very hot!";
    } else if (distance < 20) {
        return "Very hot!";
    } else if (distance < 80) {
        return "Hot!";
    } else if (distance < 160) {
        return "Cold!";
    } else if (distance < 320) {
        return "Very cold!";
    } else {
        return "Very very cold!";
    }
};

const width = 400;
const height = 400;
let clicks = 0;

let target = {
    x: getRandomNumber(width),
    y: getRandomNumber(height)
};

$("#map").click(function (event) {
    clicks++;

    let distance = getDistance(event, target);

    let distanceHit = getDistanceHit(distance);

    $("#distance").text(distanceHit);

    if (distance < 8) {
        $("body").append("<b>YOU FOUND TREASURE! You made "+ clicks +" clicks.<b/>");
    }
});