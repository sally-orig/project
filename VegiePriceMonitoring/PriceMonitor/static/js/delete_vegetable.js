document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        
        const vegetableId = button.getAttribute('data-id');
        const userConfirmed = confirm("Are you sure you want to delete this vegetable?");
        
        if (userConfirmed) {
          window.location.href = "/vegetable/delete/" + vegetableId + "/";
        }
      });
    });
  });
  