// Netlify Function：创建 Stripe Checkout Session
// 环境变量 STRIPE_SECRET_KEY 在 Netlify 后台配置
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// 欧洲常用支付方式（需在 Stripe Dashboard 激活；商户账号须欧洲注册）
// 默认只开 card（信用卡，始终可用）；其他方式需在 Stripe 后台逐个激活后，
// 通过环境变量 STRIPE_PAYMENT_METHODS（逗号分隔）追加，例如：
//   STRIPE_PAYMENT_METHODS=card,ideal,bancontact,klarna,sepa_debit
const DEFAULT_METHODS = ['card'];
const EXTRA_METHODS = (process.env.STRIPE_PAYMENT_METHODS || '')
  .split(',')
  .map(function (s) { return s.trim(); })
  .filter(Boolean);
const PAYMENT_METHODS = Array.from(new Set(DEFAULT_METHODS.concat(EXTRA_METHODS)));

exports.handler = async (event) => {
  // 只接受 POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method Not Allowed' }) };
  }

  // CORS（本地调试 / 跨域）
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const items = body.items || [];
    const origin = body.origin || 'https://www.qingyuan-ceramics.com';

    if (!items.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'No items in order' }) };
    }

    // 构建 line_items：金额单位为「分」，必须为正整数
    const line_items = items.map((it) => {
      const unitAmount = Math.round(Number(it.price) * 100);
      if (!Number.isFinite(unitAmount) || unitAmount <= 0) {
        throw new Error(`Invalid price for item: ${it.name || it.id}`);
      }
      return {
        quantity: Math.max(1, Math.round(it.qty || 1)),
        price_data: {
          currency: 'eur', // 欧洲站，欧元
          unit_amount: unitAmount,
          product_data: {
            name: it.nameEn || it.name || it.id || 'Item',
          },
        },
      };
    });

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items,
      payment_method_types: PAYMENT_METHODS,
      success_url: `${origin}/checkout.html?payment=success`,
      cancel_url: `${origin}/checkout.html?payment=cancel`,
      metadata: {
        order: body.orderNo || '',
      },
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ url: session.url }),
    };
  } catch (err) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: err.message }),
    };
  }
};
