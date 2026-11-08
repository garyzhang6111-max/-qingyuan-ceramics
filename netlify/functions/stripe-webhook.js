// Netlify Function：Stripe Webhook —— 支付成功后收单 + 落库
// 监听 checkout.session.completed，把订单（含收货地址）写入 Netlify Blobs
// 环境变量：STRIPE_SECRET_KEY、STRIPE_WEBHOOK_SECRET（都在 Netlify 后台配置）
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// 不在模块顶层初始化 store：本地/构建环境没有 Netlify Blobs 上下文会直接崩溃。
// 优先用运行时自动注入的上下文；CLI 部署无上下文时，用环境变量手动注入。
const { getStore } = require('@netlify/blobs');

function getOrdersStore() {
  const siteID = process.env.NETLIFY_SITE_ID;
  const token = process.env.NETLIFY_BLOBS_TOKEN;
  if (siteID && token) {
    return getStore({ name: 'orders', siteID, token });
  }
  return getStore('orders');
}

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
  };

  // 只接受 POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  const sig = event.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let stripeEvent;
  try {
    // 验签：用原始 body + signature 校验，确保请求真的来自 Stripe
    const rawBody = event.isBase64Encoded
      ? Buffer.from(event.body, 'base64').toString('utf8')
      : event.body;
    stripeEvent = stripe.webhooks.constructEvent(rawBody, sig, webhookSecret);
  } catch (err) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: `Webhook signature verification failed: ${err.message}` }) };
  }

  // 只处理支付成功事件
  if (stripeEvent.type !== 'checkout.session.completed') {
    return { statusCode: 200, headers, body: JSON.stringify({ received: true }) };
  }

  const session = stripeEvent.data.object;

  try {
    // 拉取完整 session（两层 expand：line_items 及其产品名）
    const full = await stripe.checkout.sessions.retrieve(session.id, {
      expand: ['line_items', 'line_items.data.price.product'],
    });

    // 收货地址优先级：站内表单填的（metadata.shipping_json）> Stripe 页收集的（shipping_details）
    var shipping = null;
    if (full.metadata && full.metadata.shipping_json) {
      try {
        var sj = JSON.parse(full.metadata.shipping_json);
        shipping = { name: sj.name || '', phone: sj.phone || '', address: sj };
      } catch (e) { shipping = null; }
    }
    if (!shipping && full.shipping_details) {
      shipping = {
        name: full.shipping_details.name,
        phone: full.shipping_details.phone,
        address: full.shipping_details.address,
      };
    }

    // 组装订单记录
    const record = {
      order_no: full.metadata && full.metadata.order ? full.metadata.order : '',
      session_id: full.id,
      created_at: new Date(full.created * 1000).toISOString(),
      amount_total: full.amount_total,          // 单位：分
      currency: full.currency,
      payment_status: full.payment_status,
      customer_email: full.customer_details ? full.customer_details.email : (full.customer_email || ''),
      customer_name: full.customer_details ? full.customer_details.name : '',
      shipping: shipping,
      items: (full.line_items && full.line_items.data || []).map(function (li) {
        return {
          name: li.description
            || (li.price && li.price.product && li.price.product.name)
            || 'Item',
          quantity: li.quantity,
          amount_total: li.amount_total,
        };
      }),
    };

    // 落库：以 session_id 为 key（CLI 部署无自动上下文时用环境变量手动注入）
    const orders = getOrdersStore();
    await orders.setJSON(full.id, record);

    return { statusCode: 200, headers, body: JSON.stringify({ received: true, order: record.order_no }) };
  } catch (err) {
    // 注意：这里即使落库失败也返回 200，避免 Stripe 无限重试；错误记到日志
    console.error('webhook order save failed:', err);
    return { statusCode: 200, headers, body: JSON.stringify({ received: true, warning: 'save failed' }) };
  }
};
