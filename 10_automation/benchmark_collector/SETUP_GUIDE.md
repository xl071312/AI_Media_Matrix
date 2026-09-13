# Hermes Benchmark Collector - MediaCrawler Setup Guide

## 环境准备步骤

### 第一步：启动带Debug端口的Chrome

1. **关闭所有Chrome窗口**（完全退出）
2. **创建新的Chrome快捷方式**，目标改为：
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark"
   ```
3. **双击新快捷方式启动Chrome**

### 第二步：登录抖音

1. 在打开的Chrome中访问：`https://www.douyin.com`
2. 完成登录（手机号/扫码）
3. 如果有验证码，**手动完成**
4. 登录成功后**不要关闭这个Chrome窗口**

### 第三步：验证CDP连接

打开新的命令行，运行：
```powershell
curl.exe http://127.0.0.1:9222/json/version
```

如果返回Chrome版本信息，说明CDP已就绪。

### 第四步：运行MediaCrawler

```bash
cd C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler
uv run main.py --platform dy --type search --keywords "赚钱逻辑" --headless false --get_comment no --save_data_option jsonl
```

---

## 配置文件位置

- `config/base_config.py` - 主配置
- `config/platform_config.py` - 平台配置

---

## 输出位置

- 原始数据：`01_benchmark/shards/hermes_real/mediacrawler_raw/`
- 报告：`01_benchmark/shards/hermes_real/smoke_test_report.md`

---

*Hermes Benchmark Collector v3.0*
