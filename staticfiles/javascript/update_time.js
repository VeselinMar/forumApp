function updateTime() {
    const timeElement = document.getElementById("current-time");
    const currentTime = new Date().toLocaleString('en-US', {
        year: 'numeric', month: 'numeric', day: 'numeric',
        hour: 'numeric', minute: 'numeric', second: 'numeric',
        hour12: false
    });
    timeElement.innerHTML = currentTime;
}

window.onload = updateTime;