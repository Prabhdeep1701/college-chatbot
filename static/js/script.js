function showTab(tabName) {
    // Hide all form contents
    document.querySelectorAll('.form-content').forEach(content => {
        content.style.display = 'none';
    });
    
    // Show the selected form content
    document.getElementById(`${tabName}-form`).style.display = 'block';
    
    // Update active tab button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}