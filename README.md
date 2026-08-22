# BCFIP 优选IP

在线地址：https://bcfip.pages.dev

## 项目简介

本项目参照 [wanwushequ/cfyxip](https://github.com/wanwushequ/cfyxip) 的思路搭建，把各大公开渠道的 Cloudflare 优选 IP 数据整理为统一格式的 txt 订阅，并提供集中导航页面。数据由 GitHub Actions 定时抓取、有变化才提交，部署于 Cloudflare Pages，完全免费、开箱即用。

**提供内容：**

- 优选 IP txt 订阅，统一格式 `IP:端口#来源 | 归属地 | IPv4/IPv6 | 运营商`
- 多个来源的优选 IP 列表：CFYes、vvHan、WeTest、UOUIN、LuoLi、CM 1/2、Mia、天诚 1/3、S5公益、Gslege、NiREvil、VPS789 优选域名等
- 按地区 / 运营商 / 网段随机优选、SUB 订阅合集、EDT/WARP 相关链接
- 数据管道说明页：https://bcfip.pages.dev/pipeline

## 数据格式

数据文件每行一条订阅，统一格式：

```
IP:端口#来源 | 归属地 | IPv4/IPv6 | 运营商
```

文件首行为头广告（携带刷新时间），尾行为尾广告，例如：

```
162.159.198.1:443#CFYes优选IPv4 | 08-20 08:43
104.16.0.1:443#CFYes | 未知 | IPv4 | 移动
162.159.197.1:443#CFYes优选IPv4
```

## 目录结构

```
BestCF-IP/
├── index.html              # 首页：优选IP导航
├── pipeline.html           # 数据管道说明页
├── parse_sub.py            # 订阅解析脚本（生成统一格式）
├── _headers                # 禁止 txt/html 缓存
├── favicon.svg
├── .github/workflows/      # 24 个定时抓取工作流（每6小时，错峰执行）
│
├── cfyes/                  # CFYes 优选（IPv4 / IPv6）
├── cmliu/                  # CM 1 优选
├── cmliu2/                 # CM 2 优选（镜像参考站）
├── gslege/                 # Gslege 优选（Cfxyz/JP/NL/US/DE/SG）
├── ircf/                   # IRCF 优选
├── kristi/                 # Kristi 优选
├── lajiao/                 # 辣椒优选（已停更，保留初始数据）
├── luoli/                  # 洛璃 优选
├── lzj/                    # 辣子鸡 优选
├── mingyu/                 # MingYu 优选（静态数据）
├── moistr/                 # Moist_R 优选
├── nirevil/                # NiREvil 优选（IPv4 / IPv6）
├── random-region/          # 按地区随机优选（mix/mix2 + 81 个地区目录）
├── s5gy/                   # S5公益 优选（all/mini/分地区 + old/ 备份）
├── tiancheng/              # 天诚1 优选（all/mini/分地区 + old/ 备份）
├── tiancheng2/             # 天诚2 优选（已停更，保留初始数据）
├── tiancheng3/             # 天诚3 优选（all/mini/分地区 + old/ 备份）
├── uouin/                  # 麒麟（UOUIN）优选
├── vps789/                 # VPS789 优选域名（TOP10/20/50/100，443/8443，镜像参考站）
├── vvhan/                  # vvHan 优选（IPv4 / IPv6）
├── wetest/                 # WeTest 优选
├── xinyitang3/             # Mia 优选（镜像参考站）
├── yutian/                 # 雨田（YuTian）优选
├── zhixuanwang/            # 智选（ZhiXuan）优选
│
├── entryip/                # Anycast Entry IP（静态维护）
├── WARP/                   # WARP 通用线路（静态维护）
├── CIDR/                   # CF 网段库（静态维护）
└── tools/                  # 工具（cidr / cidr2ip / colo）
```

## 部署方式

1. **上传到 GitHub**：新建仓库并推送本项目，确认 `.github/workflows/` 下的工作流已在 Actions 页面生效。
2. **连接 Pages**：Cloudflare 控制台 → Workers 和 Pages → Create → Pages → Connect to Git → 选择该仓库。
3. **构建设置**（纯静态，无构建步骤）：
   - Framework preset：**None**
   - Build command：留空
   - Build output directory：留空（或 `/`）
4. 保存后首次自动部署，页面和订阅链接立即可用。

## 定时更新说明

- 每个来源对应一个 workflow，触发方式为 `schedule` cron（每 6 小时，分钟错峰避免冲突）+ `workflow_dispatch`（可手动触发）。
- 工作流流程：抓取上游 → 与仓库旧文件比对（排除头尾广告行）→ 有实质变化才 commit + push → Pages 自动重新部署。
- 也可在 Actions 页面手动点 **Run workflow** 立即刷新。
- `entryip/`、`WARP/`、`CIDR/`、`mingyu/` 为手工维护数据，无对应工作流。
- 注意：GitHub 会暂停 60 天无活动的仓库定时任务，保持仓库活跃即可。

## 需要的 Secrets

以下来源的上游订阅地址为私有链接，工作流通过 GitHub Secrets 读取。**未配置时对应工作流会自动跳过（不污染数据），仓库内的初始数据仍然可用；配置后即恢复自动更新。**

| Secret | 对应来源 |
| --- | --- |
| `CMLIU_URL` | cmliu |
| `KRISTI_URL` | kristi |
| `LAJIAO_URL` | lajiao |
| `LUOLI_URL` | luoli |
| `LZJ_URL` | lzj |
| `MOISTR_URL` | moistr |
| `PROXY_URL` | random-region（按地区随机优选） |
| `S5GY_URL` | s5gy-cf |
| `YUTIAN_URL` | yutian |

配置方法：仓库 Settings → Secrets and variables → Actions → New repository secret，名称与上表一致，值为对应订阅链接。

无需 Secrets 即可自动更新的来源：cfyes、gslege、ircf、nirevil、s5gy、tiancheng1/2/3、uouin、vvhan、wetest、zhixuanwang、cmliu2、xinyitang3、vps789。其中 **Mia（xinyitang3）、CM 2（cmliu2）、VPS789** 直接镜像参考站 [wanwushequ/cfyxip](https://github.com/wanwushequ/cfyxip) 的公开数据文件。

## 数据源说明

上游数据均来自公开渠道，本项目参照 [wanwushequ/cfyxip](https://github.com/wanwushequ/cfyxip) 的栏目与工作流思路搭建，页面与数据文件仅供学习研究，请遵守相关服务条款与当地法律。