<template>
    <div class="solara-sun-spinner-container">
        <!-- <img id="sun-spinner" height="100px" src="static/assets/favicon.svg" /> -->
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:svgjs="http://svgjs.com/svgjs" :width="size" :height="size" viewBox="0 0 65 65" fill="none">
            <path id="sun-spinner1" style="transform-origin: center;"
                d="M57.11 30.64L61.47 17.87L48.7 13.51L42.76 1.39999L30.65 7.34999L17.87 2.97999L13.51 15.75L1.40002 21.7L7.35002 33.81L2.99002 46.58L15.76 50.94L21.71 63.06L33.82 57.11L46.59 61.47L50.95 48.7L63.06 42.75L57.11 30.64ZM54.26 34.39L34.39 54.26C33.19 55.46 31.25 55.46 30.05 54.26L10.2 34.4C9.00002 33.2 9.00002 31.26 10.2 30.07L30.06 10.2C31.26 8.99999 33.2 8.99999 34.4 10.2L54.27 30.07C55.47 31.27 55.47 33.21 54.27 34.4L54.26 34.39Z"
                fill="#FFCF64"></path>
            <path id="sun-spinner2" style="transform-origin: center;"
                d="M53.62 19.42L51.65 6.07L38.3 8.04L27.46 0L19.42 10.84L6.07 12.82L8.04 26.17L0 37L10.84 45.04L12.81 58.39L26.16 56.42L37 64.46L45.04 53.62L58.39 51.64L56.42 38.29L64.46 27.45L53.62 19.4V19.42ZM52.8 24.06L44.24 50.82C43.72 52.43 42 53.32 40.39 52.81L13.63 44.25C12.02 43.74 11.13 42.01 11.64 40.4L20.21 13.64C20.72 12.03 22.45 11.14 24.06 11.65L50.82 20.21C52.43 20.72 53.32 22.45 52.81 24.06H52.8Z"
                fill="#FF8C3E"></path>
        </svg>
    </div>
</template>

<style id="solara-spinner">
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(359deg);
    }
}

@keyframes oscillate {
    0% {
        transform: scale(0.8);
    }

    50% {
        transform: scale(1.0);
    }

    100% {
        transform: scale(0.8);
    }
}

#sun-spinner1 {
    animation: spin 6s linear infinite;
    padding: 10px;
}

#sun-spinner2 {
    animation: spin 2s cubic-bezier(.79, .14, .15, .86) infinite;
    padding: 10px;
}

.solara-sun-spinner-container {
    animation: oscillate 2s linear infinite;
    display: inline-block;
}

@keyframes bounce-in {
    0% {
        transform: scale(0);
    }

    100% {
        transform: scale(1);
    }
}

@keyframes bounce-out {
    0% {
        transform: translateZ(0) scale(1);
    }

    100% {
        transform: translateZ(0) scale(50);
    }
}

.solara-transition-enter-active {
    transition: opacity 0.5s ease;
    /* animation: bounce-in 0.5s ease; */
}

.solara-transition-leave-active {
    transition: opacity 0.5s ease;
}

.solara-transition-leave-active .solara-loader {
    animation: bounce-out 0.5s ease;
}

.solara-transition-leave-active .solara-sun-spinner-container {
    animation: unset;
}

.solara-transition-leave-active h1 {
    visibility: hidden;
}

.solara-transition-enter,
.solara-transition-leave-to {
    opacity: 0;
}

.solara-sun-spinner-container {
    overflow: hidden;
}
</style>
