// constants 
const modal = $('#viz-modal');
const openModalBtn = $('#open-viz-modal');
const closeModalBtn = $('#close-viz-modal');

$(document).ready(function() { 
  openModal();
  closeModal();

  
});

function openModal() {
  openModalBtn.on("click", function() {
  modal.css("display", "block");
  })
}

function closeModal() {
  closeModalBtn.on("click", function() {
    modal.css("display", "none");
  })
}


