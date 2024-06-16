
document.addEventListener("DOMContentLoaded", function() {
    function updateLastActivity() {
        fetch("/api/update-last-activity/", {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
        })
        .then(response => response.json())
        .then(data => {
                // console.log("Received data:", data);
                data.forEach(user => {
                    const userElement = document.getElementById(`user-${user.user}`);
                    if (userElement) {
                        // console.log(`Updating status for user ${user.user}: ${user.is_online ? 'online' : 'offline'}`);
                        userElement.className = user.is_online ? 'online-user' : 'offline-user';
                    } else {
                        console.warn(`No element found for user ${user.user}`);
                    }
                    });
    })}

    // Оновлювати статус кожні 5 хвилин (300000 мс)
    setInterval(updateLastActivity, 30000);

    // Відразу оновити статус після завантаження сторінки
    updateLastActivity();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}