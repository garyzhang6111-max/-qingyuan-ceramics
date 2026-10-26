// 清原 QINGYUAN · 交互脚本
(function () {
  var LANG_KEY = 'qingyuan-lang';
  var CART_KEY = 'qingyuan-cart';
  var lang = localStorage.getItem(LANG_KEY) || 'en';
  var langBtns = document.querySelectorAll('.lang-btn');

  /* ============ 购物车 ============ */
  function getCart() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
    catch (e) { return []; }
  }
  function saveCart(cart) { localStorage.setItem(CART_KEY, JSON.stringify(cart)); }
  function cartCount() {
    return getCart().reduce(function (n, it) { return n + it.qty; }, 0);
  }
  function cartTotal() {
    return getCart().reduce(function (s, it) { return s + it.qty * it.price; }, 0);
  }
  function money(n) { return '€' + Number(n).toFixed(2); }

  // 注入购物车按钮 + 抽屉（全站共享，无需改各页 header）
  function injectCartUI() {
    var navRight = document.querySelector('.nav-right');
    if (navRight && !document.getElementById('cart-btn')) {
      var btn = document.createElement('button');
      btn.className = 'cart-btn';
      btn.id = 'cart-btn';
      btn.setAttribute('data-zh', '购物车');
      btn.setAttribute('data-en', 'Cart');
      btn.innerHTML = '<span class="cart-ic">🛒</span><span class="cart-count" id="cart-count">0</span>';
      // 插到语言切换之前
      var langSwitch = navRight.querySelector('.lang-switch');
      navRight.insertBefore(btn, langSwitch || navRight.firstChild);
    }
    if (!document.getElementById('cart-drawer')) {
      var drawer = document.createElement('div');
      drawer.id = 'cart-drawer';
      drawer.className = 'cart-drawer';
      drawer.innerHTML =
        '<div class="cart-backdrop" id="cart-backdrop"></div>' +
        '<aside class="cart-panel" role="dialog" aria-label="cart">' +
          '<div class="cart-head">' +
            '<h3 data-zh="购物车" data-en="Cart">购物车</h3>' +
            '<button class="cart-close" id="cart-close" aria-label="close">×</button>' +
          '</div>' +
          '<div class="cart-items" id="cart-items"></div>' +
          '<div class="cart-foot" id="cart-foot"></div>' +
        '</aside>';
      document.body.appendChild(drawer);
    }
  }

  function renderCart() {
    var count = document.getElementById('cart-count');
    if (count) count.textContent = cartCount();
    var items = document.getElementById('cart-items');
    var foot = document.getElementById('cart-foot');
    if (!items || !foot) return;
    var cart = getCart();
    if (!cart.length) {
      items.innerHTML = '<p class="cart-empty" data-zh="购物车还是空的。" data-en="Your cart is empty.">购物车还是空的。</p>';
      foot.innerHTML = '';
      return;
    }
    items.innerHTML = cart.map(function (it, i) {
      var name = lang === 'zh' ? it.name : it.nameEn;
      return '<div class="cart-item">' +
        '<div class="cart-item-ph ' + (it.ph || 'ph-bowl') + '"></div>' +
        '<div class="cart-item-info">' +
          '<div class="cart-item-name">' + name + '</div>' +
          '<div class="cart-item-price">' + money(it.price) + '</div>' +
          '<div class="cart-qty">' +
            '<button data-cart-minus="' + i + '" aria-label="minus">−</button>' +
            '<span>' + it.qty + '</span>' +
            '<button data-cart-plus="' + i + '" aria-label="plus">＋</button>' +
          '</div>' +
        '</div>' +
        '<button class="cart-remove" data-cart-remove="' + i + '" aria-label="remove">×</button>' +
      '</div>';
    }).join('');
    foot.innerHTML =
      '<div class="cart-subtotal"><span data-zh="小计" data-en="Subtotal">小计</span><strong>' + money(cartTotal()) + '</strong></div>' +
      '<a class="btn solid cart-checkout" href="checkout.html" data-zh="去结算" data-en="Checkout">去结算</a>' +
      '<p class="cart-note" data-zh="孤品售出即无，付款后锁定库存。" data-en="One-offs are unique — payment reserves yours.">孤品售出即无，付款后锁定库存。</p>';
  }

  function openCart() { var d = document.getElementById('cart-drawer'); if (d) d.classList.add('open'); }
  function closeCart() { var d = document.getElementById('cart-drawer'); if (d) d.classList.remove('open'); }

  function addToCart(item) {
    var cart = getCart();
    var found = cart.find(function (it) { return it.id === item.id; });
    if (found) { found.qty += 1; }
    else { cart.push(item); }
    saveCart(cart);
    renderCart();
    openCart();
  }

  function initCartEvents() {
    document.addEventListener('click', function (e) {
      // 加入购物车按钮（产品卡上的 data-add-cart）
      var addBtn = e.target.closest('[data-add-cart]');
      if (addBtn) {
        e.preventDefault();
        var card = addBtn.closest('[data-item]');
        if (card) {
          addToCart({
            id: card.getAttribute('data-id'),
            name: card.getAttribute('data-name'),
            nameEn: card.getAttribute('data-name-en'),
            price: parseFloat(card.getAttribute('data-price')),
            ph: card.getAttribute('data-ph') || '',
            qty: 1
          });
        }
        return;
      }
      // 抽屉操作
      if (e.target.closest('#cart-btn')) { openCart(); return; }
      if (e.target.closest('#cart-close') || e.target.closest('#cart-backdrop')) { closeCart(); return; }
      var minus = e.target.closest('[data-cart-minus]');
      if (minus) {
        var i = parseInt(minus.getAttribute('data-cart-minus'), 10);
        var cart = getCart();
        if (cart[i]) { cart[i].qty -= 1; if (cart[i].qty <= 0) cart.splice(i, 1); }
        saveCart(cart); renderCart(); return;
      }
      var plus = e.target.closest('[data-cart-plus]');
      if (plus) {
        var j = parseInt(plus.getAttribute('data-cart-plus'), 10);
        var c2 = getCart();
        if (c2[j]) { c2[j].qty += 1; }
        saveCart(c2); renderCart(); return;
      }
      var rm = e.target.closest('[data-cart-remove]');
      if (rm) {
        var k = parseInt(rm.getAttribute('data-cart-remove'), 10);
        var c3 = getCart();
        c3.splice(k, 1);
        saveCart(c3); renderCart(); return;
      }
    });
  }

  /* ============ 语言切换 ============ */
  function setText(el, l) {
    var tag = el.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') {
      if (l === 'en' && el.hasAttribute('data-en')) {
        el.setAttribute('placeholder', el.getAttribute('data-en'));
      } else if (el.hasAttribute('data-zh')) {
        el.setAttribute('placeholder', el.getAttribute('data-zh'));
      }
      return;
    }
    if (l === 'en') {
      if (el.hasAttribute('data-en')) {
        if (!el.hasAttribute('data-zh')) el.setAttribute('data-zh', el.textContent);
        el.textContent = el.getAttribute('data-en');
      }
    } else if (el.hasAttribute('data-zh')) {
      el.textContent = el.getAttribute('data-zh');
    }
  }

  function applyLang(l) {
    lang = l;
    document.documentElement.setAttribute('lang', l === 'zh' ? 'zh' : 'en');
    document.body.setAttribute('data-lang', l);
    document.querySelectorAll('[data-en]').forEach(function (el) {
      setText(el, l);
    });
    var meta = document.querySelector('meta[name="description"][data-en]');
    if (meta) meta.setAttribute('content', l === 'en' ? meta.getAttribute('data-en') : meta.getAttribute('data-zh'));
    langBtns.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-lang') === l);
    });
    localStorage.setItem(LANG_KEY, l);
    renderCart();
  }

  langBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      applyLang(b.getAttribute('data-lang'));
    });
  });

  /* ============ 初始化顺序 ============ */
  injectCartUI();
  initCartEvents();
  applyLang(lang);
  renderCart();

  // 移动端菜单
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  // 首页精选：横向无缝滚动（requestAnimationFrame + scrollLeft，像素级精确）
  var featMarquee = document.querySelector('.featured-marquee');
  var featTrack = document.querySelector('.featured-track[data-marquee-track]');
  if (featMarquee && featTrack) {
    // 复制一份实现无缝循环
    featTrack.innerHTML += featTrack.innerHTML;
    var half = featTrack.scrollWidth / 2; // 单份内容宽度（复制后总宽的一半）
    var x = 0;
    var speed = 55; // px/秒
    var lastTime = null;
    var rafId = null;
    function step(now) {
      if (lastTime === null) lastTime = now;
      var dt = (now - lastTime) / 1000;
      lastTime = now;
      x += speed * dt;
      if (x >= half) x -= half;
      featMarquee.scrollLeft = x;
      rafId = requestAnimationFrame(step);
    }
    rafId = requestAnimationFrame(step);
    // 悬停暂停
    featMarquee.addEventListener('mouseenter', function () { cancelAnimationFrame(rafId); });
    featMarquee.addEventListener('mouseleave', function () { lastTime = null; rafId = requestAnimationFrame(step); });
    // 点击卡片跳转到商店页对应分类（内链）
    featMarquee.addEventListener('click', function (e) {
      var card = e.target.closest('.card[data-id]');
      if (!card) return;
      if (e.target.closest('a')) return; // 已经是链接，交给浏览器默认行为
      var cat = card.getAttribute('data-cat') || 'all';
      window.location.href = 'shop.html?filter=' + cat;
    });
  }

  // 详情页相关推荐：点击卡片跳转到对应详情页（内链）
  var relGrid = document.querySelector('.featured .grid');
  if (relGrid) {
    relGrid.addEventListener('click', function (e) {
      if (e.target.closest('button')) return;
      var card = e.target.closest('.card[data-id]');
      if (!card) return;
      var slug = card.getAttribute('data-id');
      if (slug) window.location.href = slug + '.html';
    });
  }

  // 商店筛选（三列静态 grid，无滚动）
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('[data-cat]');
  if (chips.length && cards.length) {
    function applyFilter(filter) {
      chips.forEach(function (c) {
        c.classList.toggle('active', c.getAttribute('data-filter') === filter);
      });
      cards.forEach(function (card) {
        var show = filter === 'all' || card.getAttribute('data-cat') === filter;
        card.style.display = show ? '' : 'none';
      });
    }
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        applyFilter(chip.getAttribute('data-filter'));
      });
    });
    // 读取 URL 参数 ?filter=xxx，自动定位到对应分类
    var urlParams = new URLSearchParams(window.location.search);
    var initFilter = urlParams.get('filter');
    if (initFilter && document.querySelector('.chip[data-filter="' + initFilter + '"]')) {
      applyFilter(initFilter);
      var shopSection = document.querySelector('.shop');
      if (shopSection) shopSection.scrollIntoView({ behavior: 'smooth' });
    }

    // 商店页：点击卡片图片进入详情页（排除「加入购物车」按钮）
    var shopGridEl = document.querySelector('.shop .grid');
    if (shopGridEl) {
      shopGridEl.addEventListener('click', function (e) {
        if (e.target.closest('button')) return; // 加购按钮交给购物车逻辑
        var card = e.target.closest('.card[data-id]');
        if (!card) return;
        var slug = card.getAttribute('data-id');
        if (slug) window.location.href = slug + '.html';
      });
    }
  }

  // 结算页：渲染订单摘要（checkout.html）
  var orderEl = document.getElementById('checkout-summary');
  if (orderEl) {
    var cart = getCart();
    if (!cart.length) {
      orderEl.innerHTML = '<p class="cart-empty" data-zh="购物车是空的，先去看看作品吧。" data-en="Your cart is empty — browse the collection first.">购物车是空的，先去看看作品吧。</p>';
    } else {
      var rows = cart.map(function (it) {
        return '<div class="co-row"><span>' + (lang === 'zh' ? it.name : it.nameEn) + ' × ' + it.qty + '</span><strong>' + money(it.price * it.qty) + '</strong></div>';
      }).join('');
      orderEl.innerHTML = rows +
        '<div class="co-total"><span data-zh="合计" data-en="Total">合计</span><strong>' + money(cartTotal()) + '</strong></div>';
    }
  }

  // 结算提交：调用 Netlify Function 创建 Stripe Checkout Session 并跳转
  var checkoutForm = document.getElementById('checkout-form');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var cart = getCart();
      if (!cart.length) { alert(lang === 'zh' ? '购物车是空的' : 'Cart is empty'); return; }

      var done = document.getElementById('checkout-done');
      var btn = checkoutForm.querySelector('button[type="submit"]');
      var orderNo = 'CS' + Date.now().toString().slice(-8);

      // 价格有效性检查：任一商品无有效价格则提示，不发起支付
      var invalid = cart.filter(function (it) { return !Number.isFinite(Number(it.price)) || Number(it.price) <= 0; });
      if (invalid.length) {
        if (done) {
          done.style.display = 'block';
          done.textContent = (lang === 'zh'
            ? '部分孤品价格待确认，暂无法在线支付。请通过联系页咨询定价。'
            : 'Some pieces are awaiting pricing and cannot be paid online yet. Please contact us for a quote.');
        }
        return;
      }

      if (btn) { btn.disabled = true; btn.textContent = (lang === 'zh' ? '正在跳转支付…' : 'Redirecting to payment…'); }

      var payload = {
        items: cart.map(function (it) {
          return { id: it.id, name: it.name, nameEn: it.nameEn, price: it.price, qty: it.qty };
        }),
        orderNo: orderNo,
        origin: window.location.origin
      };

      fetch('/.netlify/functions/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && data.url) {
          window.location.href = data.url;
        } else {
          throw new Error(data && data.error ? data.error : 'Checkout failed');
        }
      })
      .catch(function (err) {
        if (btn) { btn.disabled = false; btn.textContent = (lang === 'zh' ? '提交订单并支付' : 'Place Order & Pay'); }
        if (done) {
          done.style.display = 'block';
          done.textContent = (lang === 'zh'
            ? '支付通道暂未接入，请联系我们完成下单。'
            : 'Payment is not available yet. Please contact us to complete your order.');
        }
        console.error('checkout error:', err);
      });
    });

    // 支付回跳状态提示（success / cancel）
    var payParam = new URLSearchParams(window.location.search).get('payment');
    var doneEl = document.getElementById('checkout-done');
    if (doneEl && payParam) {
      doneEl.style.display = 'block';
      if (payParam === 'success') {
        doneEl.textContent = (lang === 'zh'
          ? '支付成功！我们会确认库存并与你联系发货。'
          : 'Payment successful! We will confirm stock and contact you about shipping.');
      } else if (payParam === 'cancel') {
        doneEl.textContent = (lang === 'zh'
          ? '支付已取消，购物车仍为你保留。'
          : 'Payment cancelled — your cart is still saved.');
      }
    }
  }

  // 滚动显现（轻量）
  var reveal = document.querySelectorAll('.val, .card, .step, .quote, .master');
  reveal = Array.prototype.filter.call(reveal, function (el) { return !el.closest('.shop'); });
  if ('IntersectionObserver' in window && reveal.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'none';
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    reveal.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity .6s ease, transform .6s ease';
      io.observe(el);
    });
  }

  /* ============ 图片放大 Lightbox（滚轮缩放 / 拖动 / 双击全屏）============ */
  function initLightbox() {
    var mainImg = document.querySelector('.pd-gallery .ph.main img');
    if (!mainImg) return;

    // 创建 lightbox DOM
    var lb = document.createElement('div');
    lb.className = 'lb';
    lb.innerHTML = '';
    var lbImg = document.createElement('img');
    lbImg.src = mainImg.src;
    lbImg.alt = mainImg.alt || '';
    var closeBtn = document.createElement('button');
    closeBtn.className = 'lb-close';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.innerHTML = '&times;';
    var zoomWrap = document.createElement('div');
    zoomWrap.className = 'lb-zoom';
    var btnOut = document.createElement('button');
    btnOut.innerHTML = '&minus;';
    btnOut.setAttribute('aria-label', 'Zoom out');
    var btnFit = document.createElement('button');
    btnFit.textContent = 'Fit';
    var btnIn = document.createElement('button');
    btnIn.innerHTML = '&plus;';
    btnIn.setAttribute('aria-label', 'Zoom in');
    var btnFs = document.createElement('button');
    btnFs.textContent = 'Full';
    zoomWrap.appendChild(btnOut);
    zoomWrap.appendChild(btnFit);
    zoomWrap.appendChild(btnIn);
    zoomWrap.appendChild(btnFs);
    var hint = document.createElement('div');
    hint.className = 'lb-hint';
    hint.textContent = 'Scroll to zoom · Drag to move · Double-click for fullscreen';
    lb.appendChild(lbImg);
    lb.appendChild(closeBtn);
    lb.appendChild(zoomWrap);
    lb.appendChild(hint);
    document.body.appendChild(lb);

    var scale = 1, minScale = 0.5, maxScale = 6;
    var tx = 0, ty = 0;

    function apply() {
      lbImg.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
    }

    // 图片由 flex 居中定位，图片中心默认在容器中心；translate 是相对该中心的偏移
    function fit() {
      var vw = lb.clientWidth, vh = lb.clientHeight;
      var iw = lbImg.naturalWidth || lbImg.width || 1;
      var ih = lbImg.naturalHeight || lbImg.height || 1;
      scale = Math.min(vw / iw, vh / ih, 1);
      tx = 0; ty = 0;
      apply();
    }

    function open() {
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      fit();
    }

    function close() {
      lb.classList.remove('open');
      document.body.style.overflow = '';
    }

    function setScale(ns, cx, cy) {
      // 以容器坐标 (cx,cy) 为焦点缩放，焦点在屏幕上保持不动
      var oldScale = scale;
      scale = Math.min(maxScale, Math.max(minScale, ns));
      var vw = lb.clientWidth, vh = lb.clientHeight;
      var cx0 = vw / 2 + tx;  // 当前图片中心屏幕坐标
      var cy0 = vh / 2 + ty;
      var ox = cx - cx0;      // 焦点相对图片中心的偏移
      var oy = cy - cy0;
      var k = scale / oldScale;
      var newCx = cx - ox * k;  // 缩放后新图片中心
      var newCy = cy - oy * k;
      tx = newCx - vw / 2;
      ty = newCy - vh / 2;
      apply();
    }

    // 打开
    mainImg.addEventListener('click', open);
    // 关闭
    closeBtn.addEventListener('click', function (e) { e.stopPropagation(); close(); });
    lb.addEventListener('click', function (e) {
      if (e.target === lb) close();
    });
    // 键盘
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === '+' || e.key === '=') setScale(scale * 1.12, lb.clientWidth / 2, lb.clientHeight / 2);
      if (e.key === '-') setScale(scale / 1.12, lb.clientWidth / 2, lb.clientHeight / 2);
      if (e.key === '0') fit();
    });
    // 滚轮缩放（慢速）
    lb.addEventListener('wheel', function (e) {
      if (!lb.classList.contains('open')) return;
      e.preventDefault();
      var lr = lb.getBoundingClientRect();
      var cx = e.clientX - lr.left;
      var cy = e.clientY - lr.top;
      var factor = e.deltaY < 0 ? 1.06 : 1 / 1.06;
      setScale(scale * factor, cx, cy);
    }, { passive: false });
    // 按钮缩放（慢速）
    btnIn.addEventListener('click', function (e) { e.stopPropagation(); setScale(scale * 1.18, lb.clientWidth / 2, lb.clientHeight / 2); });
    btnOut.addEventListener('click', function (e) { e.stopPropagation(); setScale(scale / 1.18, lb.clientWidth / 2, lb.clientHeight / 2); });
    btnFit.addEventListener('click', function (e) { e.stopPropagation(); fit(); });
    // 全屏（双击 或 Full 按钮）
    function toggleFullscreen() {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else if (lb.requestFullscreen) {
        lb.requestFullscreen();
      }
    }
    btnFs.addEventListener('click', function (e) { e.stopPropagation(); toggleFullscreen(); });
    lbImg.addEventListener('dblclick', function (e) { e.stopPropagation(); toggleFullscreen(); });

    // 拖动平移
    var dragging = false, sx = 0, sy = 0, otx = 0, oty = 0;
    lbImg.addEventListener('dragstart', function (e) { e.preventDefault(); });
    lbImg.addEventListener('mousedown', function (e) {
      dragging = true;
      sx = e.clientX; sy = e.clientY;
      otx = tx; oty = ty;
      lbImg.classList.add('dragging');
      e.preventDefault();
    });
    window.addEventListener('mousemove', function (e) {
      if (!dragging) return;
      tx = otx + (e.clientX - sx);
      ty = oty + (e.clientY - sy);
      apply();
    });
    window.addEventListener('mouseup', function () {
      dragging = false;
      lbImg.classList.remove('dragging');
    });
    // 触摸拖动
    var touchStart = null;
    lbImg.addEventListener('touchstart', function (e) {
      if (e.touches.length === 1) {
        touchStart = { x: e.touches[0].clientX, y: e.touches[0].clientY, tx: tx, ty: ty };
        dragging = true;
      }
    }, { passive: true });
    lbImg.addEventListener('touchmove', function (e) {
      if (dragging && touchStart && e.touches.length === 1) {
        tx = touchStart.tx + (e.touches[0].clientX - touchStart.x);
        ty = touchStart.ty + (e.touches[0].clientY - touchStart.y);
        apply();
      }
    }, { passive: true });
    lbImg.addEventListener('touchend', function () { dragging = false; });
  }

  initLightbox();
})();
