function showToast(message, type = 'info', duration = 3000) {
    const typeMap = {
        'success': 'success',
        'error': 'error',
        'warning': 'warning',
        'info': 'info'
    };
    
    const toastrType = typeMap[type] || 'info';
    
    toastr.options.timeOut = duration;
    
    toastr[toastrType](message);
}