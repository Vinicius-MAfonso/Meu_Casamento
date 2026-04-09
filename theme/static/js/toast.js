// Wrapper function for showToast using Toastr library
function showToast(message, type = 'info', duration = 3000) {
    // Map our types to Toastr types
    const typeMap = {
        'success': 'success',
        'error': 'error',
        'warning': 'warning',
        'info': 'info'
    };
    
    const toastrType = typeMap[type] || 'info';
    
    // Update timeout
    toastr.options.timeOut = duration;
    
    // Show toast
    toastr[toastrType](message);
}