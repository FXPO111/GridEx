// Параметры направления
const BASE_RATE = 0.0105;  // Пример: 1 RUB = 0.0105 USDT
const FEE_PCT = 0.01;      // 1% комиссия
const LOCK_MINUTES = 5;

let currentRate = BASE_RATE;
let lockUntil = null;
let timerId = null;

function fmt(x) {
  return Number(x).toFixed(2);
}

function updateRate() {
  document.getElementById("rate-label").textContent = fmt(currentRate) + " USDT";
}

function convert() {
  const rub = parseFloat(document.getElementById("rub-input").value || "0");
  if (rub <= 0) {
    document.getElementById("usdt-output").value = "";
    document.getElementById("fee-label").textContent = "—";
    return;
  }

  const usdtGross = rub * currentRate;
  const fee = usdtGross * FEE_PCT;
  const usdtNet = usdtGross - fee;

  document.getElementById("usdt-output").value = fmt(usdtNet);
  document.getElementById("fee-label").textContent = fmt(fee) + " USDT";
}

function startTimer() {
  const el = document.getElementById("lock-timer");

  if (timerId) clearInterval(timerId);

  function tick() {
    const diff = lockUntil - Date.now();
    if (diff <= 0) {
      el.textContent = "Истекло";
      clearInterval(timerId);
      return;
    }
    const m = Math.floor(diff / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    el.textContent = `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  }

  tick();
  timerId = setInterval(tick, 1000);
}

document.getElementById("rub-input").addEventListener("input", convert);

document.getElementById("lock-btn").addEventListener("click", () => {
  // Добавляем небольшой джиттер ±0.5%
  currentRate = BASE_RATE * (1 + (Math.random() - 0.5) * 0.01);

  updateRate();
  convert();

  lockUntil = Date.now() + LOCK_MINUTES * 60 * 1000;
  startTimer();

  document.getElementById("form-status").textContent =
    "Курс зафиксирован. Создайте заявку, пока таймер не истёк.";
});

// Создание заявки
document.getElementById("exchange-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const rub = parseFloat(document.getElementById("rub-input").value || "0");
  const wallet = document.getElementById("wallet-input").value.trim();
  const status = document.getElementById("form-status");

  if (rub < 1000) {
    status.textContent = "Минимальная сумма — 1000 RUB.";
    return;
  }

  if (!wallet.startsWith("T")) {
    status.textContent = "Введите корректный TRC20 адрес (начинается на T...).";
    return;
  }

  if (!lockUntil) {
    status.textContent = "Сначала зафиксируйте курс.";
    return;
  }

  // Пока backend не подключён — генерируем фейковый order_id
  const fakeOrderId = "GX" + Math.random().toString(36).substring(2, 8).toUpperCase();

  // Локально сохраняем заявку (временно)
  localStorage.setItem("order_" + fakeOrderId, JSON.stringify({
    id: fakeOrderId,
    rub: rub,
    usdt: document.getElementById("usdt-output").value,
    wallet: wallet,
    rate: currentRate,
    lock_until: lockUntil
  }));

  // Переходим на страницу заявки
  window.location.href = "../../order/index.html?id=" + fakeOrderId;
});

// Первичная отрисовка
updateRate();
