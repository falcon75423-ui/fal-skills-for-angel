# Mac 環境準備

> 適用於 macOS 12+（Intel 或 Apple Silicon）。

## 1. 裝 Homebrew（如果還沒有）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安裝完後依 Homebrew 提示把 `brew` 加到 PATH（Apple Silicon 通常會要你加 `/opt/homebrew/bin`）。

驗證：

```bash
brew --version
```

## 2. 裝 Node.js（≥ 18）

建議用 `nvm` 管理 Node 版本，方便日後升級：

```bash
brew install nvm
mkdir -p ~/.nvm
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$(brew --prefix)/opt/nvm/nvm.sh" ] && \. "$(brew --prefix)/opt/nvm/nvm.sh"' >> ~/.zshrc
source ~/.zshrc

nvm install --lts
nvm use --lts
```

驗證：

```bash
node --version    # 應 ≥ v18
npm --version
```

## 3. 裝 uv（Python 套件/工具管理器）

`skillful-mcp` 是 Python 寫的，用 `uv` 管理會比較乾淨：

```bash
brew install uv
```

驗證：

```bash
uv --version
```

## 4. 裝 playwright-cli（全域 npm 套件）

```bash
npm install -g @playwright/cli@latest
```

第一次跑會下載 Chromium / Firefox / WebKit 瀏覽器二進位（約 1-2GB），耐心等。

驗證：

```bash
playwright-cli --version
```

## 5. 建立 Chrome 小屋資料夾（給網頁抓取用）

深度研究跟法眼抓需要登入的網頁時，會用獨立的 Chrome user data dir
（避免跟你日常用的 Chrome 互相干擾）：

```bash
mkdir -p "$HOME/playwright-chrome"
```

之後第一次抓某個付費網站時，工具會跳出乾淨 Chrome 視窗讓你登入一次，cookie
會永久保留在這個資料夾裡。

## 6. 確認 Claude Code 是最新版

```bash
claude --version
```

如果版本太舊，先升級：

```bash
brew upgrade claude
```

或依官方文件升級。

## 下一步

環境就緒，繼續 → [docs/mcp-setup.md](mcp-setup.md) 裝 skillful-mcp + 設 API key。
