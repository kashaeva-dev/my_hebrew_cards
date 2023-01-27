let translation_color = document.querySelector('.learn-word-translation');
let change_translation_color = document.querySelector('.show-translation');
change_translation_color.onclick = function() {
    translation_color.classList.toggle('color-white');
};
let pronunciation_color = document.querySelector('.learn-word-pronunciation');
let change_pronunciation_color = document.querySelector('.show-pronunciation');
change_pronunciation_color.onclick = function() {
    pronunciation_color.classList.toggle('color-white');
};