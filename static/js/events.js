document.addEventListener("DOMContentLoaded", function () {

    const countdown = document.getElementById("countdown");

    if (!countdown) {
        return;
    }

    const eventDate = countdown.dataset.date;
    const eventTime = countdown.dataset.time;

    const targetDate = new Date(
        `${eventDate}T${eventTime}:00`
    ).getTime();


    function updateCountdown() {

        const now = new Date().getTime();

        const difference = targetDate - now;


        if (difference <= 0) {

            document.getElementById("days").innerText = "00";
            document.getElementById("hours").innerText = "00";
            document.getElementById("minutes").innerText = "00";
            document.getElementById("seconds").innerText = "00";

            return;
        }


        const days = Math.floor(
            difference / (1000 * 60 * 60 * 24)
        );

        const hours = Math.floor(
            (difference / (1000 * 60 * 60)) % 24
        );

        const minutes = Math.floor(
            (difference / (1000 * 60)) % 60
        );

        const seconds = Math.floor(
            (difference / 1000) % 60
        );


        document.getElementById("days").innerText =
            String(days).padStart(2, "0");

        document.getElementById("hours").innerText =
            String(hours).padStart(2, "0");

        document.getElementById("minutes").innerText =
            String(minutes).padStart(2, "0");

        document.getElementById("seconds").innerText =
            String(seconds).padStart(2, "0");
    }


    updateCountdown();

    setInterval(updateCountdown, 1000);

});