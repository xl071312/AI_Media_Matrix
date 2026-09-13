# 【HERMES MediaCrawler Smoke Test - READY】

**时间**: 2026-09-07 05:20 GMT+8
**状态**: 配置验证通过，等待CDP连接

---

## ✅ 已完成

| 项目 | 状态 |
|------|------|
| MediaCrawler克隆 | ✅ 已安装 |
| dy_config配置 | ✅ PLATFORM=dy, KEYWORDS=赚钱逻辑 |
| CDP配置 | ✅ ENABLE_CDP_MODE=True, PORT=9222 |
| 配置验证 | ✅ 所有参数正确 |

---

## ⏸️ 等待中

### 需要你执行：

**第一步：关闭Chrome**
完全退出所有Chrome窗口

**第二步：启动带Debug的Chrome**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark"
```

**第三步：登录抖音**
1. Chrome打开后访问 `https://www.douyin.com`
2. 完成登录
3. 如有验证码，手动完成
4. **保持窗口打开**

**第四步：验证CDP**
```powershell
curl.exe http://127.0.0.1:9222/json/version
```

**第五步：告诉我"CDP已就绪"**

---

## 📋 运行命令（CDP就绪后自动执行）

```bash
cd C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler
uv run main.py --platform dy --type search --keywords "赚钱逻辑"
```

---

## 📊 预期输出

```
C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\mediacrawler_raw\
├── smoke_赚钱逻辑.jsonl          # 原始数据
└── smoke_test_report.md          # 测试报告
```

---

*Hermes Benchmark Collector v3.0*
*等待Lan完成Chrome CDP配置*
