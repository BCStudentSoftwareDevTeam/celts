
$('.accordion-button').on('click', (evt) => {
    $(this).hide(); // does not run a DOM query
    $('.accordion-collapse').hide() // runs a DOM query
});
