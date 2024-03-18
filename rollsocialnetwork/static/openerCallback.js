const qs = new URLSearchParams(window.location.search);
window.opener.postMessage(qs.get("message"), qs.get("origin"));
