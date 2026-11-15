# ひじきLABO / HIJIKI LABO 公式サイト

日本の個人事業としてソフトウェアの企画・設計・開発に取り組む、ひじきLABOの公式Webサイト。静的HTML・CSSで構成し、外部フォント、JavaScript、解析タグ、広告、お問い合わせフォームは使用しません。

## 状態

- 本番URL：`https://hijikilabo.com/`（外部ネットワークからHTTP 200・TLS検証成功、Enforce HTTPS有効）
- GitHubアカウント：`hijikiogan-sudo`（接続済みGitHubツールで確認）
- 専用リポジトリ：`https://github.com/hijikiogan-sudo/hijikilabo-site`（新規publicリポジトリを作成済み）
- 初回暫定URL：`https://hijikiogan-sudo.github.io/hijikilabo-site/`（初回外部表示確認済み。Custom domain登録後は独自ドメインへの接続を利用）
- GitHub Pages：公開元GitHub Actions。独自ドメイン用の `base_path: /` で再公開成功
- DNS：所有者の明示承認後、所有者がWeb用A4件とwwwのCNAME1件を追加。管理画面画像と権威DNS3台で確認済み。一部の端末・回線で古いキャッシュが残る可能性があります
- メール：既存のMX・SPF・DKIM・DMARCとNSの値が公開DNS上で変更前と一致。実送受信テストは未実施

制作依頼の基準日：2026年11月15日。管理画面の一覧全体（NS3件、SOA、MX、SPF、DKIM、DMARCの8件）を所有者の画像で確認し、公開DNS値の控えと照合済みです。A/AAAA/wwwがない初期状態から、承認されたWeb用5件だけを追加しました。ネームサーバーと既存メール設定は変更していません。変更前後の控えは公開リポジトリの外に保存しています。

初回配信ソースcommit：`4cdedfa7126dfc7de1700e9fdc6b37e857fccad3`。初回ワークフロー：`https://github.com/hijikiogan-sudo/hijikilabo-site/actions/runs/43692897614`（success）。暫定URLのトップ・プライバシーを外部から取得し、深い階層のカスタム404、CSS、トップへの復帰とプライバシーへの遷移も確認済みです。

独自ドメイン登録後の配信ソースcommit：`2a31de4e3378a947f427779f18628fe18ababff4`。ワークフロー：`https://github.com/hijikiogan-sudo/hijikilabo-site/actions/runs/43694708494`（success、base `/`）。Custom domainは `hijikilabo.com`。GitHub公式の証明書更新手順を実施し、Enforce HTTPSの保存とDNSチェック成功を確認済みです。

外部のGitHub Actions実行環境から、権威DNS3台すべてがA4件とwwwの正しいCNAMEを返すことを確認。最終検証 `https://github.com/hijikiogan-sudo/hijikilabo-site/actions/runs/43698844889` の実ログでは、トップ・プライバシーがHTTP 200、カスタム404がHTTP 404、HTTP→HTTPSとwww→正規ドメインが301後に200でした。通常DNS経由とPagesの各IPv4への接続で、apex/www双方のTLS検証も成功しました。証明書のSANは両方のホスト名を含み、有効期限は2027年2月13日08:21:03 UTC（17:21:03 JST）です。証明書はホスティング側で更新されるため、将来の有効期限は再確認してください。

証明書更新後、外部ブラウザでも警告を回避せずにトップ・プライバシー・wwwからの正規URLへの遷移・カスタム404を確認済みです。

所有者の端末では `ERR_NAME_NOT_RESOLVED` が残るとの報告があり、その回線での表示は別途確認が必要です。外部の正常な接続確認と区別して記録しています。古いDNS応答が残っていることを理由に、登録をやり直したり既存のメール用レコードを削除したりしないでください。

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
| `scripts/check_domain.py` | DNS・HTTP・TLSの読み取り専用診断 |
| `.github/workflows/check-domain.yml` | 手動実行の接続診断ワークフロー |

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

## DNSと独自ドメイン：承認済みの変更記録

GitHub公式資料を確認し、既存値の控えを保存して差分を提示した後、所有者の「進めて」という明示承認を受けました。以下のWeb用5件だけを所有者が追加し、追加後の管理画面画像を確認済みです。**既存8件の編集・削除は行っていません。**

| 対象 | 変更前 | 承認・追加された値 |
| --- | --- | --- |
| `@` A | 未登録、公開DNSでAnswerなし | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`（各TTL 3600） |
| `www` CNAME | 未登録、公開DNSでNXDOMAIN | `hijikiogan-sudo.github.io`（TTL 3600） |
| `@` AAAA | 未登録 | 追加・変更なし |
| MX・SPF・DMARC・NS | 管理画面と公開DNSで確認・保存済み | 値を維持。変更後の公開応答でも一致 |
| DKIM TXT | `rs20261101._domainkey.hijikilabo.com` | 公開鍵を含め既存値と一致。変更なし |

NSは `ns1.xdomain.ne.jp.` / `ns2.xdomain.ne.jp.` / `ns3.xdomain.ne.jp.`。MXはWebのルート名とは別の外部ホストを参照し、そのA応答とSPFのa機構の参照先も確認しました。管理画面の設定TTL 3600と公開リゾルバーの残存TTLは区別して記録しています。DNS値の維持確認はメールの実送受信テストの代わりにはなりません。生の控えは公開リポジトリの外に保管しています。

今回の追加5件以外のDNS変更は改めて差分を提示し、所有者の承認を得てから行います。ドメイン所有権検証用TXTはまだ追加していません。

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

接続の再確認は `Actions > Check website connection (manual) > Run workflow` から実行できます。公開やDNS変更は行わず、権威DNSの応答、HTTPステータス・遷移先、TLSのホスト名検証・証明書情報をログに出力します。ジョブの完了表示だけでなく、各診断の `exit_code`・`http_code`・`ssl_verify_result` 等を確認してください。

制作時のローカル検証では、Chromiumで幅320・375・390・640・768・1024・1440pxの3ページ、計21条件を確認。横方向のはみ出しはなく、axeのWCAG 2 A/AA・2.1 AA対象自動検査の指摘は0件でした。リンク、本文スキップのフォーカス移動、動きを減らす設定も確認済みです。通常閲覧で外部リクエスト、Cookie、localStorage/sessionStorageへの保存は観測されませんでした。自動検査はアクセシビリティ全体や実機・本番動作を保証するものではありません。

HTML/CSSを編集し、ローカルでPC・スマートフォン幅、メールリンク、ページ間リンク、キーボード、文字コントラストを確認してからcommit/pushし、手動ワークフローを実行します。製品紹介は作品ごとに所有者が掲載を承認した後にだけ追加します。

表示変更の復旧は、既知の正常なcommitへ変更をrevertしてpushし、同じ公開設定でワークフローを再実行します。DNSの復旧は、承認した変更対象だけを保存済みの値へ戻して検証します。初期値が未記録のままDNS変更を行わないでください。

## 公開前の残確認

- 所有者による掲載文、プライバシーポリシーの運用適合性・保持期間の確認。
- GitHub Pagesで配信することと、GitHubのプライバシー声明へのリンクを本文に記載済み。未確認のログ保持日数や配信サービス全体のCookieの不存在は断定していません。
- 本番DNS・HTTPS・www/HTTP遷移は外部環境で検証済み。所有者の端末・回線での表示確認と、メール実送受信は未完了。
- 実機iPhoneのSafariでの確認（開発環境ではChromiumによる画面幅の検証）。

Appleへの移行開始を依頼する前に、①2ファクタ認証が有効か、②受取銀行口座を変更する必要がないか／変更するなら完了したか、必ず確認してください。サイト公開だけで組織登録の承認が保証されるものではありません。
