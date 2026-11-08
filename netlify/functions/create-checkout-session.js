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

    // 站内表单已收集完整收货地址 → 不再让 Stripe 页重复收集（避免双重填写）
    // Stripe Checkout 不支持直接预填收货表单，因此地址走两条正规通道：
    //   1) payment_intent_data.shipping —— 地址挂在 PaymentIntent 上，Stripe Dashboard 可见
    //   2) metadata.shipping_json —— 订单元数据，webhook 落库时解析
    const shipping = body.shipping || null;
    const hasFullShipping = shipping && shipping.name && shipping.line1 && shipping.city && shipping.country;

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items,
      payment_method_types: PAYMENT_METHODS,
      payment_method_options: {
        wechat_pay: { client: 'web' },
      },
      // 地址已由站内表单收集：关闭 Stripe 页地址收集（客户只付款不重填）
      // 地址缺失时才退回 Stripe 收集，保证实体发货总有地址
      shipping_address_collection: hasFullShipping ? undefined : {
        allowed_countries: [
          'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
          'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
          'SI', 'ES', 'SE', 'GB', 'CH', 'NO', 'IS', 'LI', 'MC', 'US', 'CA', 'CN',
          'JP', 'KR', 'AU', 'NZ', 'SG', 'HK', 'TW', 'MO',
        ],
      },
      payment_intent_data: hasFullShipping ? {
        shipping: {
          name: shipping.name,
          phone: shipping.phone || undefined,
          address: {
            line1: shipping.line1,
            line2: shipping.line2 || undefined,
            city: shipping.city,
            postal_code: shipping.postal || undefined,
            country: shipping.country,
          },
        },
      } : undefined,
      // 同时要求客户填邮箱（用于发收据 + 联系）
      customer_email: body.email || undefined,
      success_url: `${origin}/checkout.html?payment=success`,
      cancel_url: `${origin}/checkout.html?payment=cancel`,
      metadata: {
        order: body.orderNo || '',
        shipping_json: hasFullShipping ? JSON.stringify({
          name: shipping.name,
          phone: shipping.phone || '',
          line1: shipping.line1,
          line2: shipping.line2 || '',
          city: shipping.city,
          postal: shipping.postal || '',
          country: shipping.country,
        }) : '',
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
