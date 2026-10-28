// Netlify Function：Stripe Webhook —— 支付成功后收单 + 落库
// 监听 checkout.session.completed，把订单（含收货地址）写入 Netlify Blobs
// 环境变量：STRIPE_SECRET_KEY、STRIPE_WEBHOOK_SECRET（都在 Netlify 后台配置）
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { getStore } = require('@netlify/blobs');

const orders = getStore('orders');

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
    // 拉取完整 session（含 line_items 明细）
    const full = await stripe.checkout.sessions.retrieve(session.id, {
      expand: ['line_items'],
    });

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
      shipping: full.shipping_details ? {
        name: full.shipping_details.name,
        phone: full.shipping_details.phone,
        address: full.shipping_details.address,
      } : null,
      items: (full.line_items && full.line_items.data || []).map(function (li) {
        return {
          name: li.description || (li.price && li.price.product ? '' : ''),
          quantity: li.quantity,
          amount_total: li.amount_total,
        };
      }),
    };

    // 落库：以 session_id 为 key
    await orders.setJSON(full.id, record);

    return { statusCode: 200, headers, body: JSON.stringify({ received: true, order: record.order_no }) };
  } catch (err) {
    // 注意：这里即使落库失败也返回 200，避免 Stripe 无限重试；错误记到日志
    console.error('webhook order save failed:', err);
    return { statusCode: 200, headers, body: JSON.stringify({ received: true, warning: 'save failed' }) };
  }
};
