# ひじきLABO / HIJIKI LABO 公式サイト

日本の個人事業としてソフトウェアの企画・設計・開発に取り組む、ひじきLABOの公式Webサイト。静的HTML・CSSで構成し、外部フォント、JavaScript、解析タグ、広告、お問い合わせフォームは使用しません。

## 状態

- 目標本番URL：`https://hijikilabo.com/`（公開・接続・証明書は未確認）
- GitHubアカウント：`hijikiogan-sudo`（接続済みGitHubツールで確認）
- 専用リポジトリ：`https://github.com/hijikiogan-sudo/hijikilabo-site`（新規publicリポジトリを作成済み）
- 外部プレビューURL：未発行
- GitHub Pages：設定・デプロイ未実施
- DNS／ドメイン設定：変更なし。公開DNS照会でXServer系NS、メール用MX・SPF・DMARCを確認。管理画面の全レコードは未確認
- メール：設定変更なし。今回の作業での実送受信テストは未実施

制作依頼の基準日：2026年11月15日。開発環境からの外部通信には制限がありますが、後続の外部取得経路から公開DNSを照会できました。照会時点でルートのA/AAAAには回答がなく、wwwはNXDOMAINでした。Webページ取得も失敗しており、本番HTTPS表示は確認できていません。本人のブラウザ認証後、公式サイト専用の新規リポジトリを作成済みです。公開後は、この状態欄を実測結果に更新してください。

## ファイル

| パス | 用途 |
| --- | --- |
| `index.html` | 事業紹介・取り組み・開発姿勢・連絡先 |
| `privacy.html` | 当サイトの情報取り扱い方針 |
| `404.html` | 存在しないURLからの復帰ページ |
| `assets/css/style.css` | レスポンシブ表示・フォーカス・動きを減らす設定 |
| `assets/og.png` | 当サイト向けに作成したブランド共有画像 |
| `favicon.svg` | 当サイト向けに作成したアイコン |
| `.nojekyll` | Jekyll処理を行わない指定 |
| `scripts/build.py` | 公開対象だけを `dist/` に出力 |
| `.github/workflows/pages.yml` | 手動実行のGitHub Pages公開ワークフロー |

## ローカルで確認

Python 3以外のインストールは不要です。

```sh
python3 -m http.server 4173 --directory .
```

同じコンピューターのブラウザで `http://localhost:4173/` を開きます。クラウド環境のlocalhostは利用者のコンピューターとは別です。外部へのプレビューには環境が提供する正式なポート転送が必要です。

公開ファイルだけを確認する場合：

```sh
python3 scripts/build.py
python3 -m http.server 4173 --directory dist
```

`dist/` は再生成物です。直接編集しないでください。

## 新しいGitHub Pagesでの暫定公開

**既存サイト・Pages・ドメインの利用状況を先に確認してください。既存サイトを置き換える操作は、差分を提示して所有者の承認を得た後に行います。**

1. `hijikiogan-sudo` 配下に新しい **public** リポジトリ `hijikilabo-site` を作成。既存アプリのリポジトリは転用しません。
2. 認証済みの環境で、当ディレクトリだけをpush。添付引き継ぎ書・調査記録・ほかの作業ディレクトリを混ぜません。
3. `Settings > Pages > Build and deployment > Source` で `GitHub Actions` を選択。
4. `Actions > Publish website (manual) > Run workflow` で `base_path` を `/hijikilabo-site/` として実行。
5. ワークフローが返した実際のURLで、トップ・プライバシー・存在しない階層の404を確認。予定URLは `https://hijikiogan-sudo.github.io/hijikilabo-site/` ですが、デプロイ成功までは公開済みと扱いません。

このワークフローはpushでは発火しません。公開前の確認を終えたタイミングで手動実行します。公開アーティファクトはHTML3枚、CSS、共有画像、favicon、`.nojekyll`だけで、READMEや調査資料をサイトに配信しません。リポジトリ自体の内容はpublicになるため、すべてのコミットにも非公開情報を含めません。

新規リポジトリが存在しないことを確認し、GitHub CLIで `hijikiogan-sudo` として認証できる環境なら、当ディレクトリで以下を実行できます（今回は未実行）。既存リポジトリがある場合はこの作成コマンドを実行せず、先に内容を調査します。

```sh
gh repo create hijikiogan-sudo/hijikilabo-site --public --source . --remote origin --push
gh api --method POST repos/hijikiogan-sudo/hijikilabo-site/pages -f build_type=workflow
gh workflow run pages.yml --repo hijikiogan-sudo/hijikilabo-site -f base_path=/hijikilabo-site/
```

ソースZIPから始める場合は、その中だけで `git init -b main`、`git add .`、`git commit -m "Create official HIJIKI LABO website"` を先に行います。Gitの作者情報は自身で確認して設定してください。

SEOのcanonicalとOGPは最終ドメイン `https://hijikilabo.com/` を指しています。暫定URLでリンク先は動作しますが、OGP画像の外部取得・検索向けの検証完了は独自ドメイン接続後です。

## DNSと独自ドメイン：現時点では適用禁止

GitHub公式資料のソースを取得してPages用の候補値を確認済みです。**現行DNSのバックアップと差分の承認がまだないため、以下は変更指示ではありません。**

| 対象 | 現在値 | GitHub Pages接続時の候補 |
| --- | --- | --- |
| `@` A | 公開DNS照会はNOERROR、Answerなし | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| `@` AAAA | 公開DNS照会はNOERROR、Answerなし | IPv6を追加するかは承認時に確定。採用時は `2606:50c0:8000::153` ～ `2606:50c0:8003::153` |
| `www` CNAME等 | 公開DNS照会はNXDOMAIN（A/AAAA/CNAME） | `hijikiogan-sudo.github.io.` へのCNAME（リポジトリ名は付けない） |
| MX・TXT・SPF・DMARC・NS | 公開DNS応答を別途保存済み | 既存の値を維持。変更対象に含めない |
| DKIM | セレクタ・レコード未確認 | 管理画面等で確認し、既存値を維持 |

観測されたNSは `ns1.xdomain.ne.jp.` / `ns2.xdomain.ne.jp.` / `ns3.xdomain.ne.jp.`。MXはWebのルート名ではなく外部のメール用ホストを参照し、そのホストのA応答とSPFのa機構の参照先も確認しました。DNSの参照関係と公開応答を確認した段階であり、管理画面のゾーン全体のバックアップ・送受信テストの代わりにはなりません。生の調査資料は公開リポジトリの外に保管しています。

メールサーバー名やMXの参照先がWeb用A/AAAAと共用されていないかも確認します。ルートのAを変更するとメールに影響する構成もあるため、MX/TXTをそのまま残すだけでは安全の確認になりません。DKIMセレクタは推測せず、管理画面または有効なメールヘッダーから確認します。公開DNS照会だけでは全レコードのバックアップにはなりません。

承認前に：

1. 権威NS、実際のDNS管理先、現在のWebサイト／公開元を確認。
2. DNS管理画面からゾーン全体を保存し、MX・TXT・SPF・DKIM・DMARC・CAA・メール関連ホストとその参照先を記録。設定バックアップは公開リポジトリに入れず別途保管。
3. Web用レコードの変更前／変更後、TTL、競合するAAAA・CNAME等、復旧手順を一覧化して所有者に提示し、明示承認を得る。
4. ドメイン所有権の検証用TXTがGitHubから発行された場合、その実値も承認対象に加える。既存TXTを置き換えず別レコードとして追加。

承認後に：

1. 他のサイトで使われていないことを確認してから、GitHub PagesのCustom domainに `hijikilabo.com` を設定。DNSより先にGitHub側へ登録。
2. 承認されたWeb用DNS差分だけを適用。ネームサーバーは切り替えない。
3. ワークフローを `base_path: /` で実行。Actions公開ではCNAMEファイルは不要です。
4. DNS反映、GitHubの証明書発行を確認してEnforce HTTPSを有効化。
5. `https://hijikilabo.com/`、`https://www.hijikilabo.com/`、HTTP→HTTPS、www→正規ドメイン、プライバシー、深い階層の404、TLSのホスト名と期限を外部から検証。
6. DNSのメール関連レコードをバックアップと比較し、利用者が `contact@hijikilabo.com` の送信・受信を実テスト。メール送信は自動実行しません。

公式資料：

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

## 更新と復旧

制作時のローカル検証では、Chromiumで幅320・375・390・640・768・1024・1440pxの3ページ、計21条件を確認。横方向のはみ出しはなく、axeのWCAG 2 A/AA・2.1 AA対象自動検査の指摘は0件でした。リンク、本文スキップのフォーカス移動、動きを減らす設定も確認済みです。通常閲覧で外部リクエスト、Cookie、localStorage/sessionStorageへの保存は観測されませんでした。自動検査はアクセシビリティ全体や実機・本番動作を保証するものではありません。

HTML/CSSを編集し、ローカルでPC・スマートフォン幅、メールリンク、ページ間リンク、キーボード、文字コントラストを確認してからcommit/pushし、手動ワークフローを実行します。製品紹介は作品ごとに所有者が掲載を承認した後にだけ追加します。

表示変更の復旧は、既知の正常なcommitへ変更をrevertしてpushし、同じ公開設定でワークフローを再実行します。DNSの復旧は、承認した変更対象だけを保存済みの値へ戻して検証します。初期値が未記録のままDNS変更を行わないでください。

## 公開前の残確認

- 所有者による掲載文、プライバシーポリシーの運用適合性・保持期間の確認。
- GitHub Pagesで配信することと、GitHubのプライバシー声明へのリンクを本文に記載済み。未確認のログ保持日数や配信サービス全体のCookieの不存在は断定していません。
- 本番DNS、HTTPS、www挙動、外部プレビューとメール実送受信の検証。
- 実機iPhoneのSafariでの確認（開発環境ではChromiumによる画面幅の検証）。

Appleへの移行開始を依頼する前に、①2ファクタ認証が有効か、②受取銀行口座を変更する必要がないか／変更するなら完了したか、必ず確認してください。サイト公開だけで組織登録の承認が保証されるものではありません。
