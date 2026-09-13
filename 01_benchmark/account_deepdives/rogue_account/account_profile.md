# Account Deep Dive: rogue

**Target User ID**: 2598837511262019
**Share UID**: MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis
**Target URL**: https://profile.zjurl.cn/rogue/ugc/profile/?app=news_article&category_new=profile&module_name=Android_tt_others&share_uid=MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis&user_id=2598837511262019

**采集时间**: 2026-09-06
**状态**: ACCESS_LIMITED (需要登录)

---

## 账号基本信息

| 字段 | 值 | 来源 |
|------|-----|------|
| 账号ID | 2598837511262019 | 用户提供 |
| Share UID | MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis | 用户提供 |
| 平台 | 今日头条 | 用户提供 |

---

## 访问情况

### 尝试的访问方式

1. **直接用户主页 URL**
   - URL: `https://www.toutiao.com/user/2598837511262019/`
   - 结果: 404 Not Found

2. **Token格式URL**
   - URL: `https://www.toutiao.com/c/user/token/MS4wLjABAAAAQb9J_4uoC8eStPqgMOl47A1aleGvzA757_EhHnBgnis/`
   - 结果: 空页面 (需要登录)

3. **用户信息API**
   - API: `https://www.toutiao.com/api/pc/user/info/?user_id=2598837511262019`
   - 结果: `"reason": "login_required"`

4. **Share链接**
   - URL: `https://profile.zjurl.cn/rogue/ugc/profile/...`
   - 结果: 安全验证页面 (captcha/anti-bot)

---

## 搜索发现

在头条搜索"rogue"时，找到以下用户：

| 用户名 | 粉丝数 | 简介 |
|--------|--------|------|
| rogue·超 | 3,958 | 开始修仙...画过仙缘.打发时间... |
| RoGue | 0 | - |
| Rogue | 0 | - |
| Roguee | 135 | 关注我！爱你们哦 |
| Rogue | 28 | - |
| Rogue | 0 | - |
| Rogue | 0 | - |
| Rogue陈 | 24 | - |

**注意**: 以上搜索结果中的用户是否为目标用户需要进一步确认。

---

## 阻塞原因

1. **需要登录**: 头条用户主页和API都需要已登录会话
2. **安全验证**: Share链接触发反爬虫验证
3. **无Cookie**: Hermes浏览器会话未登录头条账号

---

## 下一步操作

需要Lan协助完成以下任一操作：

### 方案A: 浏览器登录
1. 在当前浏览器窗口中登录今日头条账号
2. 然后访问目标用户主页
3. 截图或提供页面内容

### 方案B: 提供Cookie
1. 从已登录的Chrome浏览器导出头条Cookie
2. 提供Cookie字符串给Hermes使用

### 方案C: 手动复制内容
1. 手动打开目标用户主页
2. 复制用户信息和前50条内容
3. 提供给我进行后续分析

---

## 数据记录规则

**严格执行REAL-ONLY原则**:
- ❌ 禁止模拟数据
- ❌ 禁止使用模型记忆填充
- ❌ 禁止根据"这类账号通常"猜测
- ✅ 真实数据: 标注 evidence_url + evidence_type
- ✅ NULL数据: 明确标记为NULL
- ✅ 无证据: performance_verified = False

---

*等待Lan完成登录或提供Cookie后继续采集*
