document.getElementById('emailForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const data = {
    first: document.getElementById('first').value,
    last: document.getElementById('last').value,
    domain: document.getElementById('domain').value
  };

  const res = await fetch('/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById('output').textContent = JSON.stringify(result, null, 2);
});

document.getElementById('bulkForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const formData = new FormData();
  formData.append('csv', document.getElementById('csvFile').files[0]);

  const res = await fetch('/bulk', {
    method: 'POST',
    body: formData
  });

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = "email_verification_results.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
});
