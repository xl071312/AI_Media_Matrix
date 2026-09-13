# Phase 3 Benchmark Chrome v3 - 手动启动指南

## 步骤1: 打开PowerShell管理员模式

右键点击PowerShell → 以管理员身份运行

## 步骤2: 复制粘贴以下命令执行

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profile = "C:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark_v3"

Start-Process $chrome -ArgumentList @(
    "--remote-debugging-port=9223",
    "--remote-debugging-address=127.0.0.1",
    "--user-data-dir=$profile",
    "--no-first-run",
    "--no-default-browser-check",
    "--remote-allow-origins=*",
    "https://www.douyin.com"
)
```

## 步骤3: 在新Chrome中完成登录

- 访问抖音页面
- 完成登录（二维码或手机号）
- 如有验证码/拼图，**手动完成**
- **保持窗口打开**

## 步骤4: 验证CDP

新PowerShell窗口运行：
```powershell
Invoke-RestMethod "http://127.0.0.1:9223/json/version"
```

应返回JSON包含Browser版本信息。

## 步骤5: 通知我

完成后回复 **"Chrome v3 ready"**

---

**注意**: 
- 此操作只启动独立的Benchmark Chrome
- 不影响您日常使用的Chrome
- 新Chrome使用独立Profile: `douyin_benchmark_v3`
- 端口: 9223 (不是9222)
