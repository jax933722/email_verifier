document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('emailForm');
  const output = document.getElementById('output');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const first_name = document.getElementById('first').value.trim();
    const last_name = document.getElementById('last').value.trim();
    const domain = document.getElementById('domain').value.trim();

    if (!first_name || !last_name || !domain) {
      output.textContent = '❌ Please fill in all fields.';
      return;
    }

    output.textContent = '🔄 Checking emails, please wait...';

    try {
      const response = await fetch('/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ first_name, last_name, domain })
      });

      const data = await response.json();

      if (data.error) {
        output.textContent = '❌ ' + data.error;
      } else {
        output.textContent = JSON.stringify(data, null, 2);
      }
    } catch (err) {
      output.textContent = '❌ An error occurred while checking emails.';
      console.error(err);
    }
  });
});
