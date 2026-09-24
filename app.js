let database = [];
let dependencies = {};
let userProgress = JSON.parse(localStorage.getItem('wf_mr_tracker_data')) || {};
let currentGroup = 'equipment';
let currentSub = 'All';
let statusFilter = 'all';

const MR_RANKS = [
  "Initiate", "Silver Initiate", "Gold Initiate",
  "Novice", "Silver Novice", "Gold Novice",
  "Disciple", "Silver Disciple", "Gold Disciple",
  "Seeker", "Silver Seeker", "Gold Seeker",
  "Hunter", "Silver Hunter", "Gold Hunter",
  "Eagle", "Silver Eagle", "Gold Eagle",
  "Tiger", "Silver Tiger", "Gold Tiger",
  "Dragon", "Silver Dragon", "Gold Dragon",
  "Sage", "Silver Sage", "Gold Sage",
  "Master", "Middle Master", "True Master",
  "Legend 1", "Legend 2", "Legend 3", "Legend 4"
];

async function init() {
  const [itemsRes, depRes] = await Promise.all([
    fetch('items.json'),
    fetch('dependencies.json')
  ]);
  database = await itemsRes.json();
  dependencies = await depRes.json();

  renderSubTabs();
  renderTable();
  calculateMR();
}

function calculateMR() {
  let totalXp = 0;
  for (let i = 0; i < database.length; i++) {
    if (userProgress[database[i].id]) {
      totalXp += database[i].xp;
    }
  }

  const rank = Math.floor(Math.sqrt(totalXp / 2500));
  const nextRank = rank + 1;
  const nextTargetXp = 2500 * (nextRank * nextRank);
  const xpNeeded = Math.max(0, nextTargetXp - totalXp);

  document.getElementById('current-mr').innerText = `MR ${rank}`;
  document.getElementById('mr-title').innerText = MR_RANKS[rank] || "Legend";
  document.getElementById('total-xp').innerText = totalXp.toLocaleString('en-US');
  document.getElementById('next-rank-xp').innerText = nextTargetXp.toLocaleString('en-US');
  document.getElementById('xp-remaining').innerText = xpNeeded.toLocaleString('en-US');
}

function toggleItem(id) {
  const isChecking = !userProgress[id];
  userProgress[id] = isChecking;

  // Interceptador Lógico para Intrínsecos (Efeito Cascata)
  if (id.startsWith('int_')) {
    // Separa a string do ID. Exemplo: 'int_rj_tactical_6' vira ['int', 'rj', 'tactical', '6']
    const parts = id.split('_');
    const clickedLevel = parseInt(parts.pop(), 10);
    const basePrefix = parts.join('_'); // Reconstrói o prefixo base, ex: 'int_rj_tactical'

    if (isChecking) {
      // Se marcou o nível N, garante que todos de 1 até N-1 também fiquem marcados
      for (let i = 1; i < clickedLevel; i++) {
        userProgress[`${basePrefix}_${i}`] = true;
      }
    } else {
      // Se desmarcou o nível N, garante que todos de N+1 até 10 também sejam desmarcados
      for (let i = clickedLevel + 1; i <= 10; i++) {
        userProgress[`${basePrefix}_${i}`] = false;
      }
    }
  }

  // Salva no armazenamento local, recalcula a matemática do MR e redesenha a tabela
  localStorage.setItem('wf_mr_tracker_data', JSON.stringify(userProgress));
  calculateMR();
  renderTable();
}

function markCurrentView(status) {
  const visibleItems = getFilteredItems();
  visibleItems.forEach(item => {
    userProgress[item.id] = status;
  });
  localStorage.setItem('wf_mr_tracker_data', JSON.stringify(userProgress));
  calculateMR();
  renderTable();
}

function switchTab(group) {
  currentGroup = group;
  currentSub = 'All';
  document.querySelectorAll('#main-tabs .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.group === group);
  });
  renderSubTabs();
  renderTable();
}

function switchSubTab(sub) {
  currentSub = sub;
  document.querySelectorAll('#sub-tabs .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.sub === sub);
  });
  renderTable();
}

function renderSubTabs() {
  const subContainer = document.getElementById('sub-tabs');
  subContainer.innerHTML = '';
  const subs = ['All', ...new Set(database.filter(i => i.group === currentGroup).map(i => i.sub))];
  
  subs.forEach(s => {
    const btn = document.createElement('button');
    btn.className = `tab-btn ${s === currentSub ? 'active' : ''}`;
    btn.innerText = s;
    btn.dataset.sub = s;
    btn.onclick = () => switchSubTab(s);
    subContainer.appendChild(btn);
  });
}

function setStatusFilter(type) {
  statusFilter = type;
  renderTable();
}

function getFilteredItems() {
  return database.filter(item => {
    const matchGroup = item.group === currentGroup;
    const matchSub = currentSub === 'All' || item.sub === currentSub;
    const isMastered = !!userProgress[item.id];
    const matchStatus = statusFilter === 'all' || 
                        (statusFilter === 'unmastered' && !isMastered) || 
                        (statusFilter === 'mastered' && isMastered);
    return matchGroup && matchSub && matchStatus;
  });
}

function renderTable() {
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';
  const filtered = getFilteredItems();

  filtered.forEach(item => {
    const isMastered = !!userProgress[item.id];
    const row = document.createElement('tr');

    let ingredientWarning = '';
    if (dependencies[item.name]) {
      const details = dependencies[item.name].map(d => `${d.count > 1 ? d.count + 'x ' : ''}${d.target}`).join(' & ');
      ingredientWarning = `<span class="ingredient-alert">⚠️ Do not sell: Required for ${details}</span>`;
    }

    row.innerHTML = `
      <td class="checkbox-col">
        <input type="checkbox" ${isMastered ? 'checked' : ''} onchange="toggleItem('${item.id}')">
      </td>
      <td>
        <strong>${item.name}</strong>
        ${ingredientWarning}
      </td>
      <td>${item.sub}</td>
      <td>+${item.xp.toLocaleString('en-US')} XP</td>
      <td><span class="tier-badge">T${item.tier}</span></td>
    `;
    tbody.appendChild(row);
  });
}

function exportData() {
  const blob = new Blob([JSON.stringify(userProgress, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `warframe_save_${new Date().toISOString().slice(0,10)}.json`;
  a.click();
}

function importData(event) {
  const reader = new FileReader();
  reader.onload = function() {
    try {
      userProgress = JSON.parse(reader.result);
      localStorage.setItem('wf_mr_tracker_data', JSON.stringify(userProgress));
      calculateMR();
      renderTable();
    } catch (err) {
      alert('Invalid save file.');
    }
  };
  reader.readAsText(event.target.files[0]);
}

window.onload = init;