let currentSliderIndex = 0;
const sliders = document.querySelectorAll('.slider .slider-field');
const prevBtnSlider = document.querySelector('.slider .prevSlider');
const nextBtnSlider = document.querySelector('.slider .nextSlider');


function showSlider(index) {
    sliders.forEach( feedback => feedback.classList.remove('active'));
    sliders[index].classList.add('active');
    currentSliderIndex = index;
}

prevBtnSlider.addEventListener('click', () => {
    if (currentSliderIndex === 0) {
        showSlider(sliders.length - 1);
    } else {
        showSlider(currentSliderIndex - 1);
    }
});

nextBtnSlider.addEventListener('click', () => {
    if (currentSliderIndex === sliders.length - 1) {
        showSlider(0);
    } else {
        showSlider(currentSliderIndex + 1);
    }
});

showSlider(0);