/* mobile.js —— 手机版（方案 A 土陶）交互与下单 */
(function () {
  'use strict';

  var PRODUCTS = window.MOBILE_PRODUCTS || [];
  var CATS = window.MOBILE_CATS || [];
  var CART_KEY = 'qingyuan-cart';
  var ADDR_KEY = 'qingyuan-addresses';
  var LANG_KEY = 'qingyuan-lang';
  var DESKTOP_FLAG = 'qy-desktop';

  var lang = localStorage.getItem(LANG_KEY) || 'en';
  var cart = [];
  var addrs = [];
  var curCat = 'all';
  var curItem = null;
  var qty = 1;
  var payAmt = 0;
  var paymentSuccess = new URLSearchParams(location.search).get('payment');

  /* ---------- 工具 ---------- */
  function $(id) { return document.getElementById(id); }
  function money(n) { return '€' + Number(n).toFixed(2).replace(/\.00$/, ''); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function toast(msg) {
    var t = $('toast');
    t.textContent = msg;
    t.classList.add('on');
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.classList.remove('on'); }, 1800);
  }
  function loadJSON(key) { try { return JSON.parse(localStorage.getItem(key)) || []; } catch (e) { return []; } }

  function getCart() { return loadJSON(CART_KEY); }
  function saveCart(c) { localStorage.setItem(CART_KEY, JSON.stringify(c)); }
  function getAddrs() { return loadJSON(ADDR_KEY); }
  function saveAddrs(a) { localStorage.setItem(ADDR_KEY, JSON.stringify(a)); }

  function t(zh, en) { return lang === 'zh' ? zh : en; }

  /* ---------- 语言 ---------- */
  function applyLang(l) {
    lang = l;
    document.documentElement.setAttribute('lang', l === 'zh' ? 'zh' : 'en');
    document.documentElement.classList.remove('early-zh');
    var els = document.querySelectorAll('[data-zh]');
    Array.prototype.forEach.call(els, function (el) {
      var v = l === 'zh' ? el.getAttribute('data-zh') : el.getAttribute('data-en');
      if (!v) return;
      var tag = el.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA') { el.setAttribute('placeholder', v); return; }
      if (v.indexOf('<') === 0) { el.innerHTML = v; } else { el.textContent = v; }
    });
    localStorage.setItem(LANG_KEY, l);
    var lb = $('btn-lang'), lb2 = $('btn-lang2');
    if (lb) lb.textContent = l === 'zh' ? 'EN' : '中';
    if (lb2) lb2.textContent = l === 'zh' ? 'EN' : '中';
    renderGrid();
    renderCart();
    renderAddrs();
    renderSheetAddr();
    if (curItem) fillDetailTexts();
  }
  $('btn-lang').addEventListener('click', function () { applyLang(lang === 'zh' ? 'en' : 'zh'); });
  $('btn-lang2').addEventListener('click', function () { applyLang(lang === 'zh' ? 'en' : 'zh'); });

  /* ---------- 屏幕切换 ---------- */
  var tabs = document.querySelectorAll('.tabbar .tab');
  function showScr(id) {
    var s = $(id);
    if (!s) return;
    var all = document.querySelectorAll('.scr');
    Array.prototype.forEach.call(all, function (x) { x.classList.remove('on'); });
    s.classList.add('on');
    if (id === 'scr-detail') { s.classList.add('fixed'); } else { s.classList.remove('fixed'); }
    Array.prototype.forEach.call(tabs, function (tb) { tb.classList.toggle('on', tb.getAttribute('data-scr') === id); });
  }
  Array.prototype.forEach.call(tabs, function (tb) {
    tb.addEventListener('click', function () { showScr('scr-' + tb.getAttribute('data-scr')); });
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-back]');
    if (b) showScr('scr-' + b.getAttribute('data-back'));
  });
  $('btn-brand').addEventListener('click', function () { showScr('scr-home'); });

  /* ---------- 首页网格 ---------- */
  function renderChips() {
    var chips = $('chips');
    chips.innerHTML = CATS.map(function (c) {
      return '<button class="chip' + (c[0] === curCat ? ' on' : '') + '" data-cat="' + c[0] + '">' + esc(t(c[1], c[2])) + '</button>';
    }).join('');
    Array.prototype.forEach.call(chips.children, function (chip) {
      chip.addEventListener('click', function () {
        curCat = chip.getAttribute('data-cat');
        Array.prototype.forEach.call(chips.children, function (c) { c.classList.remove('on'); });
        chip.classList.add('on');
        renderGrid();
      });
    });
  }

  function renderGrid() {
    var grid = $('grid');
    var list = PRODUCTS.filter(function (p) { return curCat === 'all' || p.cat === curCat; });
    grid.innerHTML = list.map(function (p) {
      return '<div class="card" data-id="' + esc(p.id) + '">' +
        '<div class="ph"><img src="' + esc(p.img) + '" alt="' + esc(p.name) + '" loading="lazy"></div>' +
        '<div class="info"><h3>' + esc(t(p.name, p.nameEn)) + '</h3>' +
        '<div class="price">' + money(p.price) + '</div></div></div>';
    }).join('');
    Array.prototype.forEach.call(grid.querySelectorAll('.card'), function (card) {
      card.addEventListener('click', function () {
        openDetail(card.getAttribute('data-id'));
      });
    });
  }

  /* ---------- 详情 ---------- */
  function openDetail(id) {
    var p = PRODUCTS.filter(function (x) { return x.id === id; })[0];
    if (!p) return;
    curItem = p;
    qty = 1;
    $('det-main-img').src = p.imgs[0];
    var th = $('det-thumbs');
    th.innerHTML = p.imgs.map(function (im, i) {
      return '<img src="' + esc(im) + '" class="' + (i === 0 ? 'on' : '') + '" data-i="' + i + '" alt="">';
    }).join('');
    Array.prototype.forEach.call(th.children, function (im) {
      im.addEventListener('click', function () {
        $('det-main-img').src = p.imgs[im.getAttribute('data-i')];
        Array.prototype.forEach.call(th.children, function (x) { x.classList.remove('on'); });
        im.classList.add('on');
      });
    });
    fillDetailTexts();
    showScr('scr-detail');
  }

  function fillDetailTexts() {
    var p = curItem;
    $('det-name').textContent = t(p.name, p.nameEn);
    $('det-price').textContent = money(p.price);
    $('det-desc').textContent = t(p.desc, p.descEn);
    $('det-tag') ? null : null;
    var tagEl = document.querySelector('#scr-detail .det-tag');
    if (tagEl) tagEl.textContent = t('世间唯一 · 售出即无', 'One of a kind · Once sold, gone');
  }

  $('btn-add-cart').addEventListener('click', function () {
    if (!curItem) return;
    cart = getCart();
    var found = cart.filter(function (it) { return it.id === curItem.id; })[0];
    if (found) { found.qty = (found.qty || 1) + 1; } else {
      cart.push({ id: curItem.id, name: curItem.name, nameEn: curItem.nameEn, price: curItem.price, qty: 1 });
    }
    saveCart(cart);
    renderCartBadge();
    toast(t('已加入购物袋', 'Added to bag'));
  });

  $('btn-buy').addEventListener('click', function () { openSheet(); });

  /* ---------- 购物袋 ---------- */
  function renderCartBadge() {
    cart = getCart();
    var n = cart.reduce(function (s, it) { return s + (it.qty || 1); }, 0);
    var b = $('cart-badge');
    b.hidden = n === 0;
    b.textContent = n;
  }
  function cartTotal() {
    return cart.reduce(function (s, it) { return s + Number(it.price) * (it.qty || 1); }, 0);
  }

  function renderCart() {
    cart = getCart();
    var list = $('cart-list');
    if (!list) return;
    if (!cart.length) {
      list.innerHTML = '<div class="cart-empty">' + esc(t('购物袋是空的，去挑一件孤品吧。', 'Your bag is empty — go find a one-off.')) + '</div>';
      $('cart-foot').hidden = true;
      return;
    }
    list.innerHTML = cart.map(function (it, i) {
      var p = PRODUCTS.filter(function (x) { return x.id === it.id; })[0];
      var img = p ? p.img : '';
      return '<div class="cart-item" data-i="' + i + '">' +
        '<img src="' + esc(img) + '" alt="">' +
        '<div class="t"><h4>' + esc(t(it.name, it.nameEn)) + '</h4>' +
        '<div class="p">' + money(it.price) + '</div>' +
        '<div class="q"><button data-act="minus">−</button><b>' + (it.qty || 1) + '</b><button data-act="plus">+</button></div></div>' +
        '<button class="rm" data-act="rm" aria-label="remove">✕</button></div>';
    }).join('');
    $('cart-foot').hidden = false;
    $('cart-total').textContent = money(cartTotal());
    Array.prototype.forEach.call(list.querySelectorAll('.cart-item'), function (row) {
      var i = Number(row.getAttribute('data-i'));
      row.querySelector('[data-act="minus"]').addEventListener('click', function () {
        if (cart[i].qty > 1) { cart[i].qty--; } else { cart.splice(i, 1); }
        saveCart(cart); renderCart(); renderCartBadge();
      });
      row.querySelector('[data-act="plus"]').addEventListener('click', function () {
        cart[i].qty++; saveCart(cart); renderCart(); renderCartBadge();
      });
      row.querySelector('[data-act="rm"]').addEventListener('click', function () {
        cart.splice(i, 1); saveCart(cart); renderCart(); renderCartBadge();
      });
    });
  }

  $('btn-cart').addEventListener('click', function () { renderCart(); showScr('scr-cart'); });
  $('btn-cart-clear').addEventListener('click', function () {
    saveCart([]); renderCart(); renderCartBadge();
    toast(t('购物袋已清空', 'Bag cleared'));
  });
  $('btn-cart-checkout').addEventListener('click', function () {
    cart = getCart();
    if (!cart.length) return;
    curItem = null;
    openSheet();
  });

  /* ---------- 地址簿 ---------- */
  function renderAddrs() {
    addrs = getAddrs();
    var box = $('addr-list');
    if (!box) return;
    if (!addrs.length) {
      box.innerHTML = '<div class="addr-none">' + esc(t('暂无保存的地址。下单时勾选「保存此地址」即可自动记住。', 'No saved addresses yet. Check "save this address" at checkout and it will be remembered.')) + '</div>';
      return;
    }
    box.innerHTML = addrs.map(function (a, i) {
      return '<div class="addr-item" data-i="' + i + '"><div>' + esc(a.name) +
        '<small>' + esc([a.line1, a.line2, a.city, a.postal, a.country].filter(Boolean).join(', ')) + '</small></div>' +
        '<button class="del" data-i="' + i + '" aria-label="delete">✕</button></div>';
    }).join('');
    Array.prototype.forEach.call(box.querySelectorAll('.del'), function (d) {
      d.addEventListener('click', function () {
        addrs.splice(Number(d.getAttribute('data-i')), 1);
        saveAddrs(addrs); renderAddrs(); renderSheetAddr();
        toast(t('已删除', 'Deleted'));
      });
    });
  }

  /* ---------- 下单抽屉 ---------- */
  function renderSheetAddr() {
    addrs = getAddrs();
    var pick = document.querySelector('.addr-pick');
    var empty = document.querySelector('.addr-empty');
    if (addrs.length) {
      var a = addrs[0];
      $('sheet-addr-text').textContent = a.name + ' · ' + [a.line1, a.city, a.country].filter(Boolean).join(' · ');
      pick.hidden = false; empty.hidden = true;
    } else {
      pick.hidden = true; empty.hidden = false;
    }
  }

  function openSheet() {
    if (curItem) {
      $('sheet-name').textContent = t(curItem.name, curItem.nameEn);
      payAmt = Number(curItem.price);
    } else {
      cart = getCart();
      $('sheet-name').textContent = t('购物袋结算 · 共 ' + cart.length + ' 件', 'Bag checkout · ' + cart.length + ' items');
      payAmt = cartTotal();
    }
    qty = 1;
    $('q-val').textContent = 1;
    $('sheet-total').textContent = money(payAmt);
    $('pay-amt').textContent = money(payAmt);
    $('addr-form').hidden = true;
    $('email-row').hidden = true;
    renderSheetAddr();
    $('mask').classList.add('on');
    $('sheet').classList.add('on');
  }

  function closeSheet() {
    $('mask').classList.remove('on');
    $('sheet').classList.remove('on');
    $('addr-form').hidden = true;
    $('email-row').hidden = true;
  }
  $('mask').addEventListener('click', closeSheet);
  $('q-minus').addEventListener('click', function () {
    if (curItem) { qty = Math.max(1, qty - 1); $('q-val').textContent = qty; payAmt = Number(curItem.price) * qty; }
    $('sheet-total').textContent = money(payAmt);
    $('pay-amt').textContent = money(payAmt);
  });
  $('q-plus').addEventListener('click', function () {
    if (curItem) { qty++; $('q-val').textContent = qty; payAmt = Number(curItem.price) * qty; }
    $('sheet-total').textContent = money(payAmt);
    $('pay-amt').textContent = money(payAmt);
  });

  $('sheet-addr').addEventListener('click', function () {
    addrs = getAddrs();
    if (addrs.length) {
      // 有地址时点击：展开表单可编辑，默认填入第一个地址
      var a = addrs[0];
      $('f-name').value = a.name || '';
      $('f-phone').value = a.phone || '';
      $('f-line1').value = a.line1 || '';
      $('f-line2').value = a.line2 || '';
      $('f-city').value = a.city || '';
      $('f-postal').value = a.postal || '';
      $('f-country').value = a.country || 'PT';
    }
    $('addr-form').hidden = false;
    $('email-row').hidden = false;
  });

  /* ---------- 下单 ---------- */
  $('btn-pay').addEventListener('click', function () {
    var btn = $('btn-pay');
    btn.disabled = true;
    btn.style.opacity = '.6';

    var shipping = null;
    if (!$('addr-form').hidden) {
      shipping = {
        name: $('f-name').value.trim(),
        phone: $('f-phone').value.trim(),
        line1: $('f-line1').value.trim(),
        line2: $('f-line2').value.trim(),
        city: $('f-city').value.trim(),
        postal: $('f-postal').value.trim(),
        country: $('f-country').value,
      };
      if (!shipping.name || !shipping.line1 || !shipping.city || !shipping.country) {
        toast(t('请填写姓名、地址和城市', 'Please fill name, address and city'));
        btn.disabled = false; btn.style.opacity = '';
        return;
      }
      if ($('f-save').checked) {
        addrs = getAddrs();
        var dup = addrs.filter(function (a) {
          return a.name === shipping.name && a.line1 === shipping.line1 && a.city === shipping.city && a.country === shipping.country;
        });
        if (!dup.length) {
          addrs.unshift(shipping);
          saveAddrs(addrs.slice(0, 8));
          renderAddrs();
          toast(t('地址已保存', 'Address saved'));
        }
      }
    } else {
      addrs = getAddrs();
      if (addrs.length) {
        shipping = {
          name: addrs[0].name, phone: addrs[0].phone || '',
          line1: addrs[0].line1, line2: addrs[0].line2 || '',
          city: addrs[0].city, postal: addrs[0].postal || '', country: addrs[0].country,
        };
      }
    }

    var items, orderNo;
    if (curItem) {
      items = [{ id: curItem.id, name: curItem.name, nameEn: curItem.nameEn, price: curItem.price, qty: qty }];
    } else {
      cart = getCart();
      items = cart.map(function (it) { return { id: it.id, name: it.name, nameEn: it.nameEn, price: it.price, qty: it.qty || 1 }; });
    }
    orderNo = 'M' + Date.now().toString(36).toUpperCase();

    fetch('/.netlify/functions/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: items,
        shipping: shipping,
        email: $('sheet-email') && $('sheet-email').value ? $('sheet-email').value : undefined,
        orderNo: orderNo,
        origin: location.origin,
        returnPath: '/mobile.html',
      }),
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (d.url) { location.href = d.url; } else { throw new Error(d.error || 'unknown'); }
    }).catch(function (err) {
      toast(t('下单失败：' + err.message, 'Order failed: ' + err.message));
      btn.disabled = false; btn.style.opacity = '';
    });
  });

  /* ---------- 桌面版切换 ---------- */
  $('btn-desktop').addEventListener('click', function () {
    localStorage.setItem(DESKTOP_FLAG, '1');
    location.href = '/index.html';
  });

  /* ---------- 支付回跳 ---------- */
  function handlePaymentReturn() {
    if (paymentSuccess === 'success') {
      saveCart([]);
      renderCartBadge();
      toast(t('支付成功！我们会确认库存并与你联系发货。', 'Payment successful! We will confirm stock and contact you about shipping.'));
      history.replaceState(null, '', location.pathname);
    } else if (paymentSuccess === 'cancel') {
      toast(t('支付已取消，购物袋仍为你保留。', 'Payment cancelled — your bag is kept.'));
      history.replaceState(null, '', location.pathname);
    }
  }

  /* ---------- 初始化 ---------- */
  function init() {
    renderChips();
    renderGrid();
    renderCartBadge();
    renderCart();
    renderAddrs();
    renderSheetAddr();
    applyLang(lang);
    handlePaymentReturn();
    showScr('scr-home');
  }
  init();
})();
