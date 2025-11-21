function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

const orderId = getParam("id");
const el = id => document.getElementById(id);

// отображаем ID
el("order-id").textContent = orderId || "—";

// загружаем данные
const data = JSON.parse(localStorage.getItem("order_" + orderId));

if (!data) {
  alert("Заявка не найдена");
}

// подставляем данные
el("rub-amount").textContent = data.rub + " RUB";
el("usdt-amount").textContent = data.usdt + " USDT";
el("wallet").textContent = data.wallet;
el("rate").textContent = data.rate.toFixed(4);

el("card-number").textContent = "{{CARD_NUMBER}}";

// таймер
function startTimer() {
  const t = el("timer");

  function tick() {
    const diff = data.lock_until - Date.now();
    if (diff <= 0) {
      t.textContent = "истекло";
      return;
    }
    const m = Math.floor(diff / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    t.textContent = `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
  }

  tick();
  setInterval(tick, 1000);
}
startTimer();

// кнопка "я оплатил"
el("btn-paid").addEventListener("click", () => {
  data.status = "paid";
  localStorage.setItem("order_" + orderId, JSON.stringify(data));
  el("status-text").textContent = "Ожидается подтверждение оператором";
});
