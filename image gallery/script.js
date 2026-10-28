
const images = document.querySelectorAll(".gallery img");
const slideshow = document.getElementById("slideshow");
const slideImage = document.getElementById("slideImage");
const caption = document.getElementById("caption");
const playBtn = document.getElementById("playBtn");

let currentIndex = 0;
let timer = null;

// Open the selected image
function openSlide(index) {
    currentIndex = index;
    slideshow.style.display = "block";
    showSlide();
}

// Display the current image
function showSlide() {
    slideImage.src = images[currentIndex].src;
    caption.textContent =
        images[currentIndex].alt +
        " (" + (currentIndex + 1) + " of " + images.length + ")";
}

// Next and Previous navigation
function changeSlide(step) {
    currentIndex =
        (currentIndex + step + images.length) % images.length;

    showSlide();
}

// Close the slideshow
function closeSlide() {
    slideshow.style.display = "none";
    stopAutoPlay();
}

// Start or stop automatic slideshow
function toggleAutoPlay() {
    if (timer !== null) {
        stopAutoPlay();
    } else {
        timer = setInterval(function () {
            changeSlide(1);
        }, 2000);

        playBtn.textContent = "Stop Auto Play";
    }
}

// Stop automatic slideshow
function stopAutoPlay() {
    clearInterval(timer);
    timer = null;
    playBtn.textContent = "Start Auto Play";
}