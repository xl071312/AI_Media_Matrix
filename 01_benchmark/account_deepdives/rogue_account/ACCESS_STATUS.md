# 今日头条账号 Deep Dive - rogue

**目标账号**: user_id=2598837511262019
**Share UID**: MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis
**采集时间**: 2026-09-06 19:30 GMT+8
**状态**: ACCESS_LIMITED (需要登录)

---

## 尝试的访问方式

### 1. 直接用户主页URL
- URL: `https://www.toutiao.com/user/2598837511262019/`
- 结果: **404 Not Found**

### 2. Token格式URL
- URL: `https://www.toutiao.com/c/user/token/MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis/`
- 结果: **空页面** (需要登录)

### 3. 用户信息API
- API: `https://www.toutiao.com/api/pc/user/info/?user_id=2598837511262019`
- 结果: `{"reason": "login_required", "message": "error"}`

### 4. Share链接
- URL: `https://profile.zjurl.cn/rogue/ugc/profile/?app=news_article&...`
- 结果: **安全验证页面** (captcha/anti-bot)

---

## 核心问题

1. **所有用户数据接口都需要登录Cookie**
2. **未登录状态下无法访问用户主页**
3. **Share链接触发反爬验证**

---

## 需要Lan协助

### 方案1: 浏览器登录 (推荐)
在当前浏览器中：
1. 访问 `https://www.toutiao.com`
2. 点击右上角"登录"
3. 完成手机号/二维码登录
4. 登录后访问目标用户主页

### 方案2: 提供Cookie
从已登录Chrome导出头条Cookie：
1. F12 → Application → Cookies → https://www.toutiao.com
2. 复制所有cookie值
3. 提供给我

### 方案3: 手动内容
1. 手动打开目标用户主页
2. 复制用户基本信息（名称、简介、粉丝数）
3. 复制前50条内容列表
4. 提供给我进行深拆分析

---

## 已建立的文件结构

```
C:\workspace\AI_Media_Matrix\01_benchmark\
├── shards\hermes\quarantine\          # 旧模拟数据
├── shards\hermes_real\
│   ├── collector_real.py              # REAL-ONLY采集器
│   ├── session_status.json            # Session状态
│   ├── douyin_cookies.txt             # 抖音Cookie
│   ├── douyin_real_batch_001.csv      # 抖音采集结果
│   └── CHECKPOINT_REPORT.md
└── account_deepdives\
    └── rogue_account\
        ├── account_profile.md
        └── ACCESS_STATUS.md
```

---

*等待Lan完成登录后继续采集*
