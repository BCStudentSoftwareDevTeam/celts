export function populateModal(programName, contactEmail, contactName, location) {
    // Update modal fields with program information
    document.getElementById('programName').value = programName;
    document.getElementById('contactEmail').value = contactEmail;
    document.getElementById('contactName').value = contactName;
    document.getElementById('location').value = location;
    
    // Optionally update the form action URL if needed - make changes here
    document.getElementById('updateProgramForm').action = "/admin/updateProgramInfo/" + programName;       
  }
  
  // Ensure all modals close when clicking outside of them (optional)
  document.addEventListener('click', function(event) {
    var isClickInside = document.getElementById('adminProgramManagement').contains(event.target);
    if (!isClickInside) {
       document.getElementById('adminProgramManagement').classList.remove('show');
    }
  });
  

 
  