document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('emailForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const first_name = document.getElementById('first').value.trim();
    const last_name = document.getElementById('last').value.trim();
    const domain = document.getElementById('domain').value.trim();

    console.log("First:", first_name);
    console.log("Last:", last_name);
    console.log("Domain:", domain);

    if (!first_name || !last_name || !domain) {
      document.getElementById('output').textContent = '❌ Please fill in all fields.';
      return;
    }

    document.getElementById('output').textContent = '🔄 Checking...';

    const response = await fetch('/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ first_name, last_name, domain })
    });

    const result = await response.json();
    document.getElementById('output').textContent = JSON.stringify(result, null, 2);
  });
});
