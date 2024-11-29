document.addEventListener('DOMContentLoaded', () => {
    // Check for access token
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        alert('You are not logged in. Redirecting to login page.');
        window.location.href = '/';
        return; // Stop further execution if not authenticated
    }

    console.log('Authenticated! Token:', accessToken);

    // Set Authorization header for all fetch requests
    const defaultHeaders = {
        'Authorization': `Bearer ${accessToken}`
    };

    // Fetch and update game state
    const fetchGameState = async () => {
        try {
            // Fetch player stats
            const playerResponse = await fetch('/game/player/state', {
                headers: defaultHeaders
            });
            const playerData = await playerResponse.json();
            document.getElementById('health').textContent = playerData.health || 'N/A';
            document.getElementById('hunger').textContent = playerData.hunger || 'N/A';
            document.getElementById('sanity').textContent = playerData.sanity || 'N/A';

            // Fetch room state
            const roomResponse = await fetch('/game/room/state', {
                headers: defaultHeaders
            });
            const roomData = await roomResponse.json();
            document.getElementById('time-of-day').textContent = roomData.time_of_day || 'N/A';
            document.getElementById('weather').textContent = roomData.weather || 'N/A';

            // Fetch inventory
            const inventoryResponse = await fetch('/inventory', {
                headers: defaultHeaders
            });
            const inventoryData = await inventoryResponse.json();
            const inventoryList = document.getElementById('inventory-list');
            inventoryList.innerHTML = '';
            inventoryData.inventory.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.item_name} (x${item.quantity})`;
                inventoryList.appendChild(li);
            });

            // Fetch resources
            const resourcesResponse = await fetch('/resource/room', {
                headers: defaultHeaders
            });
            const resourcesData = await resourcesResponse.json();
            const resourceList = document.getElementById('resource-list');
            resourceList.innerHTML = '';
            resourcesData.resources.forEach(resource => {
                const li = document.createElement('li');
                li.textContent = `${resource.type} (${resource.quantity})`;
                resourceList.appendChild(li);
            });

        } catch (err) {
            console.error('Error fetching game state:', err);
        }
    };

    // Save game event
    document.getElementById('save-game').addEventListener('click', async () => {
        try {
            const response = await fetch('/game/save', {
                method: 'POST',
                headers: defaultHeaders
            });
            const result = await response.json();
            alert(result.msg || 'Game saved successfully');
        } catch (err) {
            console.error('Error saving game:', err);
        }
    });

    // Exit game event
    document.getElementById('exit-game').addEventListener('click', () => {
        window.location.href = '/';
    });

    // Periodically fetch game state
    setInterval(fetchGameState, 5000);
    fetchGameState(); // Initial fetch
});
