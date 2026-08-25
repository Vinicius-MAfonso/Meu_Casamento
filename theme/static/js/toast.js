if (typeof toastr !== "undefined") {
  toastr.options = {
    closeButton: true,
    debug: false,
    newestOnTop: false,
    progressBar: true,
    positionClass: "toast-top-right",
    preventDuplicates: false,
    onclick: null,
    showDuration: "300",
    hideDuration: "1000",
    timeOut: "3000",
    extendedTimeOut: "1000",
    showEasing: "swing",
    hideEasing: "linear",
    showMethod: "fadeIn",
    hideMethod: "fadeOut",
  };
}

function showToast(message, type = "info", duration = 3000) {
  const typeMap = {
    success: "success",
    error: "error",
    warning: "warning",
    info: "info",
  };

  const toastrType = typeMap[type] || "info";

  if (typeof toastr !== "undefined") {
    toastr.options.timeOut = duration;
    toastr[toastrType](message);
  } else {
    console.log(`[Toast ${type}]: ${message}`);
  }
}