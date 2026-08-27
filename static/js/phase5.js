/* ==========================================
   GALLERY LIGHTBOX
========================================== */

function openLightbox(image, title, description) {

    const lightbox =
        document.getElementById(
            "galleryLightbox"
        );

    const imageElement =
        document.getElementById(
            "lightboxImage"
        );

    const titleElement =
        document.getElementById(
            "lightboxTitle"
        );

    const descriptionElement =
        document.getElementById(
            "lightboxDescription"
        );


    if (!lightbox) {
        return;
    }


    imageElement.src = image;

    imageElement.alt = title;

    titleElement.textContent = title;

    descriptionElement.textContent =
        description;


    lightbox.classList.add(
        "active"
    );


    document.body.style.overflow =
        "hidden";
}


function closeLightbox() {

    const lightbox =
        document.getElementById(
            "galleryLightbox"
        );


    if (!lightbox) {
        return;
    }


    lightbox.classList.remove(
        "active"
    );


    document.body.style.overflow =
        "";
}


/* Close by clicking outside */

document.addEventListener(
    "click",
    function(event) {

        const lightbox =
            document.getElementById(
                "galleryLightbox"
            );


        if (
            event.target === lightbox
        ) {

            closeLightbox();

        }

    }
);


/* Close using Escape */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Escape"
        ) {

            closeLightbox();

        }

    }
);