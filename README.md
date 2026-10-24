# 柴烧 CHAISHAO · 手工陶艺品欧洲独立站

柴烧杯子与手工陶艺品的全球销售网站。V1.0 目标：英语主线、SEO 友好、多语言可扩展、孤品销售。

## 架构（已锁定）

- **主线**：静态站 `site/`（内容 + SEO）
- **交易**：Shopify 结账（店铺 `40pdrr-d1.myshopify.com`，4 产品已建，作结账后端）
- **语言**：英语主线，结构预留多语言扩展
- **托管**（上线时定）：Cloudflare Pages / GitHub Pages

## 目录

```
site/            本地静态站（HTML/CSS/JS，零依赖）
shopify-theme/   Shopify OS 2.0 主题（交易后端）
audit/           Phase 0-1 审计与规划文档
photos-src/      201 张原始照片（源素材，不入库）
```

## 本地预览

```bash
cd site && python3 -m http.server 8321
# 打开 http://127.0.0.1:8321
```

## 产品数据铁律

- 产品真实性数据（窑炉/温度/产地/认证）缺失时一律标「待确认」，不编造。
- 容量/尺寸/价格必须来自实据。

## 阶段进度

见 `audit/04-项目文件结构与阶段任务.md`（Phase 0→13）。
