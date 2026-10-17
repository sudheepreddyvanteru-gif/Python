
const $ = id => document.getElementById(id);

const STORAGE_KEY = "fintrack_swipe_shop_v2";
const THEME_KEY = "fintrack_theme_v1";

const currency = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 2
});

const products = [
  {
    id: "p1", name: "Wireless Headphones",
    category: "Electronics", icon: "🎧",
    description: "Wireless audio for everyday use.",
    price: 1200, suggestedPrice: 1600
  },
  {
    id: "p2", name: "Smart Watch",
    category: "Electronics", icon: "⌚",
    description: "A stylish everyday smartwatch.",
    price: 1800, suggestedPrice: 2300
  },
  {
    id: "p3", name: "Running Shoes",
    category: "Fashion", icon: "👟",
    description: "Comfortable shoes for daily wear.",
    price: 1500, suggestedPrice: 2000
  },
  {
    id: "p4", name: "Travel Backpack",
    category: "Fashion", icon: "🎒",
    description: "A practical bag for daily travel.",
    price: 900, suggestedPrice: 1250
  },
  {
    id: "p5", name: "Desk Lamp",
    category: "Home", icon: "💡",
    description: "A modern lamp for your workspace.",
    price: 650, suggestedPrice: 900
  },
  {
    id: "p6", name: "Coffee Maker",
    category: "Home", icon: "☕",
    description: "Make your favorite coffee at home.",
    price: 2200, suggestedPrice: 2800
  },
  {
    id: "p7", name: "Sunglasses",
    category: "Accessories", icon: "🕶️",
    description: "Complete your everyday look.",
    price: 500, suggestedPrice: 750
  },
  {
    id: "p8", name: "Leather Wallet",
    category: "Accessories", icon: "👛",
    description: "A compact everyday wallet.",
    price: 400, suggestedPrice: 600
  },
  {
    id: "p9", name: "Bluetooth Speaker",
    category: "Electronics", icon: "🔊",
    description: "Portable sound for your favorite music.",
    price: 1000, suggestedPrice: 1400
  }
];

function initialState() {
  return {
    balance: 10000,
    purchases: [],
    activity: [],
    skipped: []
  };
}

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));

    if (
      !saved ||
      !Number.isFinite(saved.balance) ||
      saved.balance < 0 ||
      !Array.isArray(saved.purchases) ||
      !Array.isArray(saved.activity) ||
      !Array.isArray(saved.skipped)
    ) {
      return initialState();
    }

    return {
      balance: saved.balance,
      purchases: saved.purchases.filter(item =>
        item &&
        typeof item.id === "string" &&
        typeof item.productId === "string" &&
        typeof item.name === "string" &&
        Number.isFinite(item.cost) &&
        item.cost > 0 &&
        Number.isFinite(item.suggestedPrice) &&
        item.suggestedPrice > 0 &&
        ["owned", "sold"].includes(item.status) &&
        (
          item.status !== "sold" ||
          (Number.isFinite(item.salePrice) && item.salePrice > 0)
        )
      ),
      activity: saved.activity.filter(item =>
        item &&
        typeof item.id === "string" &&
        typeof item.description === "string" &&
        Number.isFinite(item.amount) &&
        typeof item.type === "string" &&
        typeof item.date === "string"
      ).slice(0, 100),
      skipped: saved.skipped.filter(id =>
        typeof id === "string" &&
        products.some(product => product.id === id)
      )
    };
  } catch {
    return initialState();
  }
}

let state = loadState();
let theme = "light";
let gesture = null;
let busy = false;
let visibleProducts = [];
let cardGeneration = 0;

try {
  theme = localStorage.getItem(THEME_KEY) === "dark"
    ? "dark"
    : "light";
} catch {}

function money(amount) {
  return currency.format(amount);
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[char]);
}

function dateNow() {
  return new Date().toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

function createId() {
  return globalThis.crypto?.randomUUID?.() ||
    `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    return true;
  } catch {
    showMessage("Unable to save. Check your browser storage.", true);
    return false;
  }
}

function showMessage(text, error = false) {
  $("message").textContent = text;
  $("message").style.color = error ? "var(--red)" : "var(--primary)";
}

function showShopMessage(text) {
  $("shop-message").textContent = text;
}

function applyTheme() {
  document.documentElement.dataset.theme = theme;
  $("theme-toggle").textContent =
    theme === "dark" ? "☀ Light mode" : "☾ Dark mode";
}

function addActivity(description, amount, type) {
  state.activity.unshift({
    id: createId(),
    description,
    amount,
    type,
    date: dateNow()
  });

  state.activity = state.activity.slice(0, 100);
}

function totals() {
  const spent = state.purchases.reduce(
    (sum, item) => sum + item.cost, 0
  );

  const sold = state.purchases.filter(
    item => item.status === "sold"
  );

  const revenue = sold.reduce(
    (sum, item) => sum + item.salePrice, 0
  );

  const profit = sold.reduce(
    (sum, item) => sum + item.salePrice - item.cost, 0
  );

  return { spent, revenue, profit };
}

function renderSummary() {
  const summary = totals();

  $("balance").textContent = money(state.balance);
  $("wallet-balance").textContent = money(state.balance);
  $("spent").textContent = money(summary.spent);
  $("revenue").textContent = money(summary.revenue);
  $("profit").textContent = money(summary.profit);

  $("profit").className =
    summary.profit > 0 ? "positive" :
    summary.profit < 0 ? "negative" : "";

  $("purchase-count").textContent =
    `${state.purchases.length} ${
      state.purchases.length === 1 ? "product" : "products"
    } bought`;

  const owned = state.purchases.filter(
    item => item.status === "owned"
  );

  $("inventory-count").textContent =
    `${owned.length} ${owned.length === 1 ? "item" : "items"}`;
}

function getFilteredProducts() {
  const search = $("product-search").value.trim().toLowerCase();
  const category = $("category-filter").value;

  return products.filter(product =>
    (category === "All" || product.category === category) &&
    `${product.name} ${product.category} ${product.description}`
      .toLowerCase().includes(search)
  );
}

function currentDeckProducts() {
  return getFilteredProducts().filter(product =>
    !state.skipped.includes(product.id) &&
    !state.purchases.some(item =>
      item.productId === product.id && item.status === "owned"
    )
  );
}

function renderDeck() {
  const allFiltered = getFilteredProducts();
  visibleProducts = currentDeckProducts();

  $("deck-count").textContent =
    visibleProducts.length
      ? `1 / ${visibleProducts.length}`
      : "0 / 0";

  $("deck-empty").hidden = visibleProducts.length > 0;
  $("product-deck").innerHTML = "";

  if (!visibleProducts.length) {
    showShopMessage(
      allFiltered.length
        ? "You've viewed all matching products. Start again to revisit them."
        : "No products match your search."
    );
    return;
  }

  showShopMessage("Swipe right to buy, or left to skip.");

  // Render a top card and a small preview of the next card.
  const top = visibleProducts[0];
  const next = visibleProducts[1];

  if (next) {
    const preview = document.createElement("div");
    preview.className = "swipe-card";
    preview.style.transform = "scale(.94) translateY(12px)";
    preview.style.pointerEvents = "none";
    preview.style.opacity = ".45";
    preview.setAttribute("aria-hidden", "true");
    preview.innerHTML = `
      <div class="product-art">${next.icon}</div>
      <div class="product-details">
        <span class="product-category">${escapeHTML(next.category)}</span>
        <h3>${escapeHTML(next.name)}</h3>
        <div class="product-price">${money(next.price)}</div>
      </div>`;
    $("product-deck").appendChild(preview);
  }

  const card = document.createElement("article");
  card.className = "swipe-card";
  card.dataset.product = top.id;
  card.setAttribute("aria-label", `${top.name}. Swipe right to buy or left to skip.`);

  card.innerHTML = `
    <div class="swipe-stamp stamp-buy">BUY ♥</div>
    <div class="swipe-stamp stamp-skip">SKIP ✕</div>
    <div class="product-art">${top.icon}</div>
    <div class="product-details">
      <span class="product-category">${escapeHTML(top.category)}</span>
      <h3>${escapeHTML(top.name)}</h3>
      <p class="product-description">${escapeHTML(top.description)}</p>
      <div class="product-price">${money(top.price)}</div>
      <div class="suggested-price">
        Suggested selling price: ${money(top.suggestedPrice)}
      </div>
      <div class="potential-profit">
        Potential profit: ${money(top.suggestedPrice - top.price)}
      </div>
    </div>`;

  $("product-deck").appendChild(card);
  cardGeneration++;
}

function animateCard(direction, onComplete) {
  const card = $("product-deck").querySelector(
    `.swipe-card[data-product="${CSS.escape(visibleProducts[0]?.id || "")}"]`
  );

  if (!card) {
    onComplete();
    return;
  }

  busy = true;
  card.style.transition = "transform .24s ease, opacity .24s ease";
  card.style.transform =
    `translate(${direction * 700}px, -40px) rotate(${direction * 25}deg)`;
  card.style.opacity = "0";

  setTimeout(() => {
    onComplete();
    busy = false;
  }, 240);
}

function skipProduct() {
  if (busy || !visibleProducts.length) return;

  const product = visibleProducts[0];

  animateCard(-1, () => {
    const oldState = JSON.stringify(state);

    if (!state.skipped.includes(product.id)) {
      state.skipped.push(product.id);
    }

    if (!saveState()) {
      state = JSON.parse(oldState);
      renderDeck();
      return;
    }

    renderDeck();
  });
}

function buyProduct(productId) {
  if (busy) return;

  const product = products.find(item => item.id === productId);
  if (!product) return;

  if (state.balance < product.price) {
    showMessage("Insufficient balance. Add funds before buying.", true);
    showShopMessage("Not enough money to buy this product.");
    return;
  }

  const confirmed = confirm(
    `Purchase ${product.name} for ${money(product.price)}?\n\n` +
    `Balance after purchase: ${money(state.balance - product.price)}\n` +
    `Suggested resale price: ${money(product.suggestedPrice)}`
  );

  if (!confirmed) return;

  // Animate first; only complete the purchase after confirmation.
  animateCard(1, () => {
    const oldState = JSON.stringify(state);

    state.balance -= product.price;

    state.purchases.push({
      id: createId(),
      productId: product.id,
      name: product.name,
      icon: product.icon,
      cost: product.price,
      suggestedPrice: product.suggestedPrice,
      status: "owned",
      purchaseDate: dateNow()
    });

    state.skipped = state.skipped.filter(id => id !== product.id);

    addActivity(`Bought ${product.name}`, -product.price, "purchase");

    if (!saveState()) {
      state = JSON.parse(oldState);
      render();
      return;
    }

    render();
    showMessage(`${product.name} purchased successfully!`);
    showShopMessage("Purchased! Here's your next product.");
  });
}

function renderInventory() {
  const owned = state.purchases.filter(
    item => item.status === "owned"
  );

  $("inventory-empty").hidden = owned.length > 0;

  $("inventory-list").innerHTML = owned.map(item => `
    <article class="inventory-item">
      <div class="item-icon">${item.icon}</div>
      <div class="item-info">
        <h3>${escapeHTML(item.name)}</h3>
        <p>Cost: ${money(item.cost)} · Bought ${escapeHTML(item.purchaseDate)}</p>
        <p class="positive">
          Suggested profit: ${money(item.suggestedPrice - item.cost)}
        </p>
      </div>
      <div class="item-right">
        <strong>${money(item.cost)}</strong>
        <button class="sell-button"
          data-sell="${escapeHTML(item.id)}"
          type="button">Sell product</button>
      </div>
    </article>
  `).join("");
}

function sellProduct(purchaseId) {
  const item = state.purchases.find(
    purchase => purchase.id === purchaseId
  );

  if (!item || item.status !== "owned") return;

  const answer = prompt(
    `Sell ${item.name}\nPurchase cost: ${money(item.cost)}\n` +
    `Suggested price: ${money(item.suggestedPrice)}\n\n` +
    `Enter the actual selling price:`,
    String(item.suggestedPrice)
  );

  if (answer === null) return;

  const salePrice = Number(answer.trim());

  if (
    answer.trim() === "" ||
    !Number.isFinite(salePrice) ||
    salePrice <= 0 ||
    salePrice > 1000000000
  ) {
    showMessage("Enter a valid selling price greater than zero.", true);
    return;
  }

  const profit = salePrice - item.cost;

  if (!confirm(
    `Confirm sale for ${money(salePrice)}?\n` +
    `${profit >= 0 ? "Profit" : "Loss"}: ${money(Math.abs(profit))}\n` +
    `Balance after sale: ${money(state.balance + salePrice)}`
  )) return;

  const oldState = JSON.stringify(state);

  item.status = "sold";
  item.salePrice = salePrice;
  item.saleDate = dateNow();

  state.balance += salePrice;

  addActivity(`Sold ${item.name}`, salePrice, "sale");

  if (!saveState()) {
    state = JSON.parse(oldState);
    return;
  }

  render();

  showMessage(
    profit >= 0
      ? `Sold successfully! Profit: ${money(profit)}`
      : `Sold at a loss of ${money(Math.abs(profit))}.`,
    profit < 0
  );
}

function renderActivity() {
  $("activity-empty").hidden = state.activity.length > 0;

  $("activity-list").innerHTML = state.activity.map(item => `
    <article class="activity-item">
      <div class="item-icon">
        ${item.type === "purchase" ? "🛒" :
          item.type === "sale" ? "💸" : "💰"}
      </div>
      <div class="item-info">
        <strong>${escapeHTML(item.description)}</strong>
        <p>${escapeHTML(item.date)}</p>
      </div>
      <div class="activity-amount ${
        item.amount < 0 ? "negative" : "positive"
      }">
        ${item.amount > 0 ? "+" : ""}${money(item.amount)}
      </div>
    </article>
  `).join("");
}

function render() {
  renderSummary();
  renderDeck();
  renderInventory();
  renderActivity();
}

function handlePointerDown(event) {
  if (busy || event.target.closest("button")) return;

  const card = event.target.closest(".swipe-card[data-product]");
  if (!card) return;

  gesture = {
    card,
    startX: event.clientX,
    startY: event.clientY,
    pointerId: event.pointerId,
    moved: false
  };

  card.style.transition = "none";
}

function handlePointerMove(event) {
  if (!gesture || gesture.pointerId !== event.pointerId || busy) return;

  const dx = event.clientX - gesture.startX;
  const dy = event.clientY - gesture.startY;

  // Keep vertical movement available for page scrolling.
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 12) return;

  if (Math.abs(dx) > 5) gesture.moved = true;

  gesture.card.style.transform =
    `translate(${dx}px, ${dy * .15}px) rotate(${dx * .045}deg)`;

  const buyStamp = gesture.card.querySelector(".stamp-buy");
  const skipStamp = gesture.card.querySelector(".stamp-skip");

  buyStamp.style.opacity = dx > 0
    ? String(Math.min(dx / 100, 1)) : "0";

  skipStamp.style.opacity = dx < 0
    ? String(Math.min(Math.abs(dx) / 100, 1)) : "0";
}

function handlePointerUp(event) {
  if (!gesture || gesture.pointerId !== event.pointerId || busy) return;

  const current = gesture;
  const dx = event.clientX - current.startX;
  const dy = event.clientY - current.startY;

  gesture = null;

  if (
    Math.abs(dx) >= 90 &&
    Math.abs(dx) > Math.abs(dy) * 1.2
  ) {
    const productId = current.card.dataset.product;

    if (dx > 0) {
      buyProduct(productId);
    } else {
      skipProduct();
    }
    return;
  }

  current.card.style.transition = "transform .2s ease";
  current.card.style.transform = "";
  current.card.querySelector(".stamp-buy").style.opacity = "0";
  current.card.querySelector(".stamp-skip").style.opacity = "0";
}

function resetDeck() {
  const oldState = JSON.stringify(state);
  state.skipped = [];

  if (!saveState()) {
    state = JSON.parse(oldState);
    return;
  }

  renderDeck();
  showShopMessage("All products are available again. Start swiping!");
}

$("product-deck").addEventListener("pointerdown", handlePointerDown);
$("product-deck").addEventListener("pointermove", handlePointerMove);
$("product-deck").addEventListener("pointerup", handlePointerUp);

$("product-deck").addEventListener("pointercancel", () => {
  if (!gesture) return;

  gesture.card.style.transition = "transform .2s ease";
  gesture.card.style.transform = "";
  gesture.card.querySelector(".stamp-buy").style.opacity = "0";
  gesture.card.querySelector(".stamp-skip").style.opacity = "0";
  gesture = null;
});

$("skip-button").addEventListener("click", skipProduct);

$("buy-button").addEventListener("click", () => {
  if (visibleProducts.length) {
    buyProduct(visibleProducts[0].id);
  }
});

$("reset-deck").addEventListener("click", resetDeck);

$("product-search").addEventListener("input", renderDeck);
$("category-filter").addEventListener("change", renderDeck);

$("inventory-list").addEventListener("click", event => {
  const button = event.target.closest("[data-sell]");
  if (button) sellProduct(button.dataset.sell);
});

$("add-funds").addEventListener("click", () => {
  const answer = prompt("Enter the amount to add to your virtual wallet:");

  if (answer === null) return;

  const amount = Number(answer.trim());

  if (
    answer.trim() === "" ||
    !Number.isFinite(amount) ||
    amount <= 0 ||
    amount > 1000000000
  ) {
    showMessage("Enter a valid amount greater than zero.", true);
    return;
  }

  const oldState = JSON.stringify(state);

  state.balance += amount;
  addActivity("Added funds", amount, "funds");

  if (!saveState()) {
    state = JSON.parse(oldState);
    return;
  }

  render();
  showMessage(`${money(amount)} added to your virtual wallet.`);
});

$("theme-toggle").addEventListener("click", () => {
  theme = theme === "dark" ? "light" : "dark";
  applyTheme();

  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    showMessage("Theme changed but could not be saved.", true);
  }
});

applyTheme();
render();
