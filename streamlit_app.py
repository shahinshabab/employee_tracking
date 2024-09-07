import streamlit as st
import streamlit.components.v1 as components
from st_bridge import bridge

# Create a bridge for communication between HTML and Streamlit
data = bridge("my-bridge", default={"response": ""})

# Display the response from the server
st.subheader(f"Server Response: {data['response']}")

# Inject JavaScript into the Streamlit app
components.html("""
<script>
    async function sendHttpRequest() {
        try {
            // Define the server URL and request options
            const serverUrl = 'http://192.168.1.14:5000/';  // Update to your server's URL
            const response = await fetch(serverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ key1: 'value1', key2: 'value2' })
            });
            
            // Check if the response is ok
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            // Parse the JSON response
            const data = await response.json();
            
            // Send the response data back to Streamlit
            window.parent.stBridges.send('my-bridge', { response: data });
        } catch (error) {
            console.error('Error:', error);
            window.parent.stBridges.send('my-bridge', { response: 'Error: ' + error.message });
        }
    }

    // Call the function to send the request
    sendHttpRequest();
</script>
""", height=0)  # Set height to 0 to avoid extra space in the layout
