// === Ensure script runs after DOM is ready ===
window.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas");
    if (!canvas) {
        console.error("Canvas element not found!");
        return;
    }

    const ctx = canvas.getContext("2d");
    let isMousePressed = false;

    class CanvasState {
        constructor(color, shape, height, width, pencilHeight, pencilWidth) {
            this.color = color;
            this.shape = shape;
            this.height = height;
            this.width = width;
            this.pencilHeight = pencilHeight;
            this.pencilWidth = pencilWidth;
        }
    }

    // Default settings
    let canvasState = new CanvasState("black", "square", 400, 400, 10, 10);

    // === Utility functions ===
    function getCanvasCoords(clientX, clientY) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY,
        };
    }

    // === Drawing logic ===
    function draw(x, y) {
        ctx.fillStyle = canvasState.color;
        ctx.strokeStyle = canvasState.color;

        if (canvasState.shape === "square") {
            ctx.fillRect(
                x,
                y,
                canvasState.pencilWidth,
                canvasState.pencilHeight
            );
        } else {
            ctx.beginPath();
            ctx.arc(
                x,
                y,
                Math.max(1, canvasState.pencilWidth / 2),
                0,
                Math.PI * 2
            );
            ctx.fill();
            ctx.closePath();
        }
    }

    // === Save as image ===
    window.Save = function () {
        const image = canvas.toDataURL("image/jpeg");
        const link = document.createElement("a");
        link.href = image;
        link.download = "art-game-image.jpg";
        link.click();
    };

    // === Clear canvas ===
    window.Clear = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    // === Toggle shape ===
    window.Shape = function () {
        canvasState.shape =
            canvasState.shape === "square" ? "circle" : "square";
    };

    // === Change color ===
    window.setColor = function () {
        const colorInput = document.querySelector("#pencil-color");
        if (colorInput) {
            canvasState.color = colorInput.value;
        }
    };

    // === Change width ===
    window.Width = function () {
        const value = parseInt(document.getElementById("pixel-width").value, 10);
        if (value < 1 || isNaN(value)) {
            $("#error-width").text("Width must be greater than 0");
        } else {
            $("#error-width").text("");
            canvasState.pencilWidth = value;
        }
    };

    // === Change height ===
    window.Height = function () {
        const value = parseInt(document.getElementById("pixel-height").value, 10);
        if (value < 1 || isNaN(value)) {
            $("#error-height").text("Height must be greater than 0");
        } else {
            $("#error-height").text("");
            canvasState.pencilHeight = value;
        }
    };

    // === Mouse events ===
    $("#canvas")
        .on("mousedown", (e) => {
            isMousePressed = true;
            const pos = getCanvasCoords(e.clientX, e.clientY);
            draw(pos.x, pos.y);
        })
        .on("mouseup mouseleave", () => {
            isMousePressed = false;
        })
        .on("mousemove", (e) => {
            if (isMousePressed) {
                const pos = getCanvasCoords(e.clientX, e.clientY);
                draw(pos.x, pos.y);
            }
        });

    // === Touch events (for phones/tablets) ===
    canvas.addEventListener(
        "touchstart",
        (e) => {
            e.preventDefault();
            isMousePressed = true;
            const t = e.changedTouches[0];
            const pos = getCanvasCoords(t.clientX, t.clientY);
            draw(pos.x, pos.y);
        },
        { passive: false }
    );

    canvas.addEventListener(
        "touchmove",
        (e) => {
            e.preventDefault();
            if (!isMousePressed) return;
            const t = e.changedTouches[0];
            const pos = getCanvasCoords(t.clientX, t.clientY);
            draw(pos.x, pos.y);
        },
        { passive: false }
    );

    canvas.addEventListener("touchend", () => {
        isMousePressed = false;
    });

    // === Mobile redirect (optional) ===
    if (
        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Windows Phone/i.test(
            navigator.userAgent
        )
    ) {
        window.location.href = "https://shubnikov.me/error-page.html";
    }

    console.log("✅ Canvas drawing initialized successfully!");
});

