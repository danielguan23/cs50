document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here

    var video = document.getElementById("myVideo");


    var btn = document.getElementById("btn");
    var mute = document.getElementById("mute");


    btn.addEventListener('click', function() {
    if (video.paused) {
        video.play();
        btn.innerHTML = "Pause";
    }
    else {
        video.pause();
        btn.innerHTML = "Play";
    }
    });

    mute.addEventListener('click', function() {
    if (video.muted) {
        video.muted=false
        mute.innerHTML = "Mute";
    }
    else {
        video.muted=true;
        mute.innerHTML = "Unmute";
    }
    });
});