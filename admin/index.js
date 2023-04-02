function formatDuration(seconds) {
    if (seconds === 0) {
        return '0 seconds';
    }
  
    const units = [
        { label: 'month', secs: 30 * 24 * 60 * 60 },
        { label: 'day', secs: 24 * 60 * 60 },
        { label: 'hour', secs: 60 * 60 },
        { label: 'minute', secs: 60 },
        { label: 'second', secs: 1 },
    ];
  
    const parts = [];
    for (const { label, secs } of units) {
        if (seconds >= secs) {
            const count = Math.floor(seconds / secs);
            parts.push(`${count} ${label}${count > 1 ? 's' : ''}`);
            seconds %= secs;
        }
    }
  
    if (parts.length === 1) {
        return parts[0];
    }
  
    return parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
}

var server_stats_up = null;

function dashboard_changer(type) {
    var contents_div = document.getElementById('contents');
    switch(type) {
        case 'dashboard':
            server_stats_up = document.getElementById('server_stats-up-time');
            contents_div.innerHTML = `
            <!-- <div>
                <canvas id="myChart"></canvas>
            </div> -->
            <div id="server_stats">
                <i class="bi bi-link-45deg"></i>
                <a 
                    id="server_stats-link" 
                    style="color: #fff; text-decoration: none; padding: 5px;"
                    target="_blank"></a><br>
                <br>

                <i class="bi bi-clock-history"></i>
                <span id="server_stats-up-for" style="padding: 5px;">
                    <span>Up for</span>
                    <span id="server_stats-up-time" style="color: #00ff00;"></span>
                </span><br>
                <span id="server_stats-datetime" style="padding: 25px;"></span><br>
                <br>

                <i class="bi bi-folder"></i>
                <span id="server_stats-size" style="padding: 5px;">
                    <span style="color: gray">Loading ...</span>
                </span><br>
                <br>

            </div>
            
            <!-- <script>
                const ctx = document.getElementById('myChart');
            
                var chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                    datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                    y: {
                        beginAtZero: true
                    }
                    }
                }
                });
            </script> -->
            `;

            const date = new Date(server_time);

            const options = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                // timeZone: 'local'
            };
            
            const user_locale = navigator.language;
            const formatter = new Intl.DateTimeFormat(user_locale, options);
            const date_string = formatter.format(date);

            var server_stats_datetime = document.getElementById('server_stats-datetime');

            server_stats_datetime.innerHTML = '(' + date_string + ')';

            var server_stats_link = document.getElementById('server_stats-link');

            server_stats_link.href = loadCookieAsType('server_public_address');
            server_stats_link.innerHTML = loadCookieAsType('server_public_address');

            var server_stats_size = document.getElementById('server_stats-size');
            var xhr = new XMLHttpRequest();

            xhr.open('GET', '/admin/get_used_space.py');

            xhr.responseType = 'text';

            xhr.onload = function() {
                if (xhr.status === 200) {
                    server_stats_size.innerHTML = xhr.responseText;
                }
            };

            xhr.send();

            break;

        case 'pages':
            contents_div.innerHTML = ``;
            break;
        
        case 'shell':
            contents_div.innerHTML = ``;
            break;
        
        case 'configuration':
            contents_div.innerHTML = ``;
            break;
        
        case 'manage':
            contents_div.innerHTML = ``;
            break;
    }
}

function loadCookieAsType(name) {
    let value = "";
    const cookies = document.cookie.split(";");
    cookies.forEach(cookie => {
        const [cookieName, cookieValue] = cookie.trim().split("=");
        if (cookieName === name) {
            value = decodeURIComponent(cookieValue);
        }
    });
  
    if (!value) {
        return value;
    }
  
    // Try to parse the value as a number
    const numberValue = Number(value);
    if (!isNaN(numberValue)) {
        return numberValue;
    }
  
    // Try to parse the value as a boolean
    if (value === "true" || value === "false") {
        return value === "true";
    }
  
    // Try to parse the value as an object or array
    try {
        return JSON.parse(value);
    } catch (error) {
        // If parsing fails, return the value as a string
        return value;
    }
}

function createAndSaveLastCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
  
    const oldCookie = document.cookie.split(";").find(cookie => cookie.trim().startsWith(name + "="));
    if (oldCookie) {
        document.cookie = name + "=" + oldCookie.split("=")[1] + "; expires=Thu, 01 Jan 1970 00:00:00 UTC" + expires + "; path=/";
    }
  
    document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/";
}

async function startTimer(callback) {
    let count = 0;
    while (true) {
        callback(count++);
        await new Promise(resolve => setTimeout(resolve, 10));
    }
}

var server_time = loadCookieAsType('server_time') * 1000;

startTimer(count => {
    // console.log(`${formatDuration(count)} have passed`);
    var server_stats_up = document.getElementById('server_stats-up-time');
    page_time = Math.floor(Date.now());
    try {
        server_stats_up.innerHTML = formatDuration(((page_time) - server_time) / 1000);
    } catch(error) {
        var server_stats_up = document.getElementById('server_stats-up-time');
    }
});
