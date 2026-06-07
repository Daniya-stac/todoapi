const API = 'http://localhost:8000/todos';
let todos = [];
let currentFilter = 'all';

async function fetchTodos() {
  try {
    const res = await fetch(`${API}/`);
    if (!res.ok) throw new Error('Ошибка сервера');
    todos = await res.json();
    render();
  } catch (e) {
    document.getElementById('todo-list').innerHTML =
      `<div class="empty">Не удалось подключиться к API.<br>${e.message}</div>`;
    showToast('Ошибка подключения к ' + API, 'error');
  }
}

async function createTodo() {
  const desc = document.getElementById('new-desc').value.trim();
  const date = document.getElementById('new-date').value;
  if (!desc) { showToast('Введите описание задачи', 'error'); return; }

  const body = { description: desc, completed: false };
  if (date) body.date = new Date(date).toISOString();

  try {
    const res = await fetch(`${API}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(await res.text());
    document.getElementById('new-desc').value = '';
    document.getElementById('new-date').value = '';
    showToast('Задача добавлена', 'success');
    await fetchTodos();
  } catch (e) {
    showToast('Ошибка: ' + e.message, 'error');
  }
}

async function toggleTodo(id, current) {
  try {
    const res = await fetch(`${API}/${id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !current })
    });
    if (!res.ok) throw new Error(await res.text());
    await fetchTodos();
  } catch (e) {
    showToast('Ошибка обновления', 'error');
  }
}

async function deleteTodo(id) {
  try {
    const res = await fetch(`${API}/${id}/`, { method: 'DELETE' });
    if (!res.ok) throw new Error(await res.text());
    showToast('Задача удалена', 'success');
    await fetchTodos();
  } catch (e) {
    showToast('Ошибка удаления', 'error');
  }
}

async function saveEdit(id) {
  const descInput = document.getElementById(`edit-desc-${id}`);
  const dateInput = document.getElementById(`edit-date-${id}`);
  const desc = descInput.value.trim();
  if (!desc) { showToast('Описание не может быть пустым', 'error'); return; }

  const body = { description: desc };
  if (dateInput.value) body.date = new Date(dateInput.value).toISOString();
  else body.date = null;

  try {
    const res = await fetch(`${API}/${id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(await res.text());
    showToast('Сохранено', 'success');
    await fetchTodos();
  } catch (e) {
    showToast('Ошибка: ' + e.message, 'error');
  }
}

function toggleEdit(id) {
  const row = document.getElementById(`edit-row-${id}`);
  row.style.display = row.style.display === 'none' ? 'flex' : 'none';
}

function setFilter(f, btn) {
  currentFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

function formatDate(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  return d.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function toDatetimeLocal(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function escHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function render() {
  const list = document.getElementById('todo-list');
  let filtered = todos;
  if (currentFilter === 'active') filtered = todos.filter(t => !t.completed);
  if (currentFilter === 'done') filtered = todos.filter(t => t.completed);

  const total = filtered.length;
  document.getElementById('count-label').textContent =
    `${total} задач${total === 1 ? 'а' : total >= 2 && total <= 4 ? 'и' : ''}`;

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty">Задач нет ✓</div>`;
    return;
  }

  list.innerHTML = filtered.map(t => {
    const dateStr = formatDate(t.date);
    const dtLocal = toDatetimeLocal(t.date);
    return `
      <div class="todo-item ${t.completed ? 'completed' : ''}" id="todo-${t.id}">
        <div class="todo-checkbox ${t.completed ? 'checked' : ''}" onclick="toggleTodo(${t.id}, ${t.completed})" title="Отметить выполненным"></div>
        <div class="todo-body">
          <div class="todo-desc">${escHtml(t.description)}</div>
          <div class="todo-meta">
            <span class="todo-id">#${t.id}</span>
            ${dateStr ? `<span class="todo-date">📅 ${dateStr}</span>` : ''}
            ${t.completed ? `<span class="badge-done">выполнено</span>` : ''}
          </div>
          <div class="edit-row" id="edit-row-${t.id}" style="display:none;">
            <input type="text" id="edit-desc-${t.id}" value="${escHtml(t.description)}" maxlength="30" style="flex:1; min-width:150px;" />
            <input type="datetime-local" id="edit-date-${t.id}" value="${dtLocal}" />
            <button class="btn btn-primary btn-sm" onclick="saveEdit(${t.id})">сохранить</button>
            <button class="btn btn-sm" onclick="toggleEdit(${t.id})">отмена</button>
          </div>
          <div class="todo-actions">
            <button class="btn btn-sm" onclick="toggleEdit(${t.id})">✎ изменить</button>
            <button class="btn btn-danger" onclick="deleteTodo(${t.id})">✕ удалить</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

let toastTimer;
function showToast(msg, type = '') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show ' + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = ''; }, 2800);
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('new-desc').addEventListener('keydown', e => {
    if (e.key === 'Enter') createTodo();
  });
  fetchTodos();
});