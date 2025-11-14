const list = document.getElementById('list');
const input = document.getElementById('user-input');
const addBtn = document.getElementById('add-btn');

// Load + show todos
async function loadTodos() {
  const response = await fetch('http://localhost:5000/api/todos', {
    method: 'GET',
    headers: { 'Accept': 'application/json' }
  });
  const todos = await response.json();

  list.innerHTML = '';
  todos.forEach(todo => {
    const li = document.createElement('li');

    // Checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = todo.completed;

    // Text
    const span = document.createElement('span');
    span.textContent = todo.text;
    if (todo.completed) span.classList.add('completed');

    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';

    // Toggle complete
    checkbox.addEventListener('change', async () => {
      await fetch(`http://localhost:5000/api/todos/${todo.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' }
      });
      loadTodos();
    });

    // Delete action
    deleteBtn.addEventListener('click', async () => {
      await fetch(`http://localhost:5000/api/todos/${todo.id}`, {
        method: 'DELETE'
      });
      loadTodos();
    });

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

// Add new todo
addBtn.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) return;

  await fetch('http://localhost:5000/api/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });

  input.value = '';
  loadTodos();
});

// Start the app
loadTodos();