const tbody = document.querySelector("#orders-table tbody");

function loadOrders() {
  tbody.innerHTML = "";

  Object.keys(localStorage).forEach(key => {
    if (!key.startsWith("order_")) return;

    const o = JSON.parse(localStorage.getItem(key));

    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${o.id}</td>
      <td>${o.rub}</td>
      <td>${o.usdt}</td>
      <td>${o.status || "waiting"}</td>
      <td>
        <button class="btn-ok" data-id="${o.id}" data-action="approve">Оплата ок</button>
        <button class="btn-send" data-id="${o.id}" data-action="send">Отправил крипту</button>
        <button class="btn-cancel" data-id="${o.id}" data-action="cancel">Отмена</button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

document.addEventListener("click", e => {
  if (!e.target.dataset.action) return;

  const id = e.target.dataset.id;
  const action = e.target.dataset.action;

  const key = "order_" + id;
  const o = JSON.parse(localStorage.getItem(key));

  if (action === "approve") o.status = "confirmed";
  if (action === "send") o.status = "completed";
  if (action === "cancel") o.status = "canceled";

  localStorage.setItem(key, JSON.stringify(o));
  loadOrders();
});

loadOrders();
