---
name: opensea-nft
description: Search, buy, sell, and analyze NFTs on OpenSea with natural-language trading strategies. Supports strategy-driven trading for Pokémon cards (ポケカ) on Courtyard.io — define your own strategy or use the built-in momentum preset.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(export OPENSEA_API_KEY*)", "Bash(curl *)", "Bash(for *)", "Bash(LISTINGS=*)", "Bash(TOKEN_IDS=*)", "Bash(echo *)", "Bash(python3 *)", "Bash(kova sign *)", "Bash(kova wallet *)", "Bash(kova balance *)", "Bash(kova send *)"]
---

# OpenSea NFT Marketplace

OpenSea API v2 と `kova sign` を組み合わせて、NFT の検索・リスティング取得・購入・出品・分析を行う。

**Prerequisites:**
- 環境変数 `OPENSEA_API_KEY` を設定（https://docs.opensea.io/reference/api-keys で取得）
- kova ウォレットを作成済み（`kova wallet create --name <name>`）
- Polygon で USDC.e を使う場合は事前にトークン登録が必要:
  ```bash
  kova token add --chain polygon --symbol USDC.e --address 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --decimals 6
  ```

> **APIキー期限切れ時:** `KEY_EXPIRED` エラーが出た場合は `kova key rotate --name <key-name>` でローテートする。キー名は `kova status` の出力またはエラーメッセージの `hint` に表示される。

### API キーの読み込み

プロジェクトルートの `.env` から API キーを読み込む。**API キーの値を直接コマンドに埋め込まないこと。**

```bash
export OPENSEA_API_KEY=$(grep OPENSEA_API_KEY .env | cut -d'=' -f2)
```

以降の全コマンドは `$OPENSEA_API_KEY` 環境変数を参照する。キーが空の場合はスキル実行前にユーザーに `.env` への設定を促すこと。

---

## API Base

```
https://api.opensea.io/api/v2
```

全リクエストに `x-api-key: $OPENSEA_API_KEY` ヘッダーが必要。

---

## Known Collections (ショートカット)

よく検索されるコレクションのスラッグ一覧。スラッグが分かっている場合は Search をスキップして直接 Listings 取得に進める。

| カテゴリ | コレクション | スラッグ | チェーン | 備考 |
|---------|------------|---------|---------|------|
| ポケモンカード | Courtyard.io | `courtyard-nft` | polygon | 実物カードをトークン化。Category トレイトが `Pokémon` |

> **ポケカ検索のヒント:** Courtyard.io はポケカ以外（スポーツカード等）も含む混合コレクション。リスティング取得後に NFT Detail（セクション 2-b）で `Category == "Pokémon"` をフィルタすること。`Title/Subject` トレイトでカード名、`Set` トレイトでセット名が取れる。

---

## 1. Search Collections

OpenSea API v2 にはサーバーサイドのコレクション検索がない。以下の優先順で探す。

### 1-a. スラッグ直接指定（推奨・最速）

コレクション名が分かっている場合、スラッグを推測して直接取得する。スラッグは通常 `ブランド名-nft`、`ブランド名-io`、`ブランド名` のいずれか。

```bash
# 候補スラッグを順に試す（200 が返ればヒット）
for SLUG in "BRAND-nft" "BRAND-io" "BRAND"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "x-api-key: $OPENSEA_API_KEY" \
    "https://api.opensea.io/api/v2/collections/$SLUG")
  if [ "$STATUS" = "200" ]; then
    curl -s -H "x-api-key: $OPENSEA_API_KEY" \
      "https://api.opensea.io/api/v2/collections/$SLUG" \
      | jq '{slug: .collection, name, description: (.description[:120]), chain: .contracts[0].chain}'
    break
  fi
done
```

`BRAND` を検索したいブランド名（小文字、スペースは `-`）に置き換える。

### 1-b. 一覧取得 + フィルタ（スラッグ不明の場合）

```bash
# next カーソルでページネーション、最大 200 件ずつ取得
NEXT=""
for i in $(seq 1 3); do
  URL="https://api.opensea.io/api/v2/collections?limit=200${NEXT:+&next=$NEXT}"
  RESULT=$(curl -s -H "x-api-key: $OPENSEA_API_KEY" "$URL")
  echo "$RESULT" | jq -r '.collections[] | select(.name | test("QUERY"; "i")) | "\(.collection)\t\(.name)\t\(.contracts[0].chain)"'
  NEXT=$(echo "$RESULT" | jq -r '.next // empty')
  [ -z "$NEXT" ] && break
done
```

`QUERY` を検索したい文字列（正規表現可）に置き換える。ヒットしない場合はページを増やすか、1-a のスラッグ推測を併用する。

---

## 2. Get Listings

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/listings/collection/SLUG/all?limit=10" | jq '.listings[] | {orderHash: .order_hash, chain, price: (.price.current.value | tonumber / pow(10; .price.current.decimals)), currency: .price.current.currency, decimals: .price.current.decimals, maker: .protocol_data.parameters.offerer, protocolAddress: .protocol_address}'
```

`SLUG` をコレクションスラッグ（search で取得）に置き換える。

> **注意:** 価格は `decimals` フィールドを使って動的に計算している。ETH/WETH は 18、USDC は 6 など通貨により異なる。

---

## 2-b. Get NFT Detail (メタデータ・トレイト取得)

リスティングにはNFTの名前やトレイトが含まれない。カードの種類やカード名でフィルタするには、token ID から NFT 詳細を取得する。

> **注意:** OpenSea の NFT 詳細レスポンスには制御文字（U+0000〜U+001F）が含まれることがあり、`jq` がパースエラーになる。`python3` でパースすること。

```bash
# リスティングから token ID を取得済みとする
CONTRACT="<NFT_CONTRACT_ADDRESS>"
CHAIN_SLUG="<OPENSEA_CHAIN_SLUG>"  # matic, ethereum 等
TOKEN_ID="<TOKEN_ID_FROM_LISTING>"

curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/chain/$CHAIN_SLUG/contract/$CONTRACT/nfts/$TOKEN_ID" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
nft = d['nft']
traits = {t['trait_type']: t['value'] for t in nft.get('traits', [])}
print(json.dumps({
    'name': nft.get('name', ''),
    'category': traits.get('Category', ''),
    'subject': traits.get('Title/Subject', ''),
    'set': traits.get('Set', ''),
    'language': traits.get('Language', ''),
    'year': traits.get('Year', ''),
    'image_url': nft.get('image_url', '')
}, indent=2))
"
```

### バッチ取得（複数リスティングのフィルタリング）

リスティング一覧から安い順にNFTを特定するパターン:

> **重要: token ID ↔ order hash ↔ カード名の対応管理**
> 出力は必ず `{token_id, order_hash, name, price}` をセットで保持すること。分析フェーズと購入フェーズで対応が切れると、意図しないNFTを購入するリスクがある。

```bash
# 1. リスティング取得 → token ID + 価格を抽出
LISTINGS=$(curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/listings/collection/SLUG/all?limit=50")

# 2. 価格の安い順にソートして token ID を取得
TOKEN_IDS=$(echo "$LISTINGS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = []
for l in data['listings']:
    price_val = int(l['price']['current']['value'])
    decimals = l['price']['current']['decimals']
    tid = l['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
    oh = l['order_hash']
    items.append((price_val, decimals, tid, oh))
items.sort()
for price_val, decimals, tid, oh in items[:20]:
    print(f'{tid}\t{price_val / 10**decimals}\t{oh}')
")

# 3. 各 token の詳細を取得してフィルタ（例: ポケカのみ）
# NOTE: python3 + 制御文字除去を使うこと（jq はレスポンス内の制御文字でパース失敗する）
echo "$TOKEN_IDS" | while IFS=$'\t' read -r TID PRICE OH; do
  DETAIL=$(curl -s -H "x-api-key: $OPENSEA_API_KEY" \
    "https://api.opensea.io/api/v2/chain/CHAIN_SLUG/contract/CONTRACT/nfts/$TID" \
    | python3 -c "
import sys, json, re
raw = sys.stdin.read()
clean = re.sub(r'[\x00-\x1f]', '', raw)
d = json.loads(clean)
nft = d['nft']
traits = {t['trait_type']: t['value'] for t in nft.get('traits', [])}
cat = traits.get('Category', '')
if cat == 'Pokémon':
    print(json.dumps({'token_id': '$TID', 'order_hash': '$OH', 'name': nft.get('name',''), 'subject': traits.get('Title/Subject',''), 'set': traits.get('Set','')}))" 2>/dev/null)
  [ -n "$DETAIL" ] && echo -e "$PRICE USDC\t$DETAIL"
done
```

`SLUG`, `CHAIN_SLUG`, `CONTRACT` を対象コレクションに合わせて置き換える。

> **NFT 詳細取得時の注意:** OpenSea の NFT 詳細レスポンスには制御文字（U+0000〜U+001F）が含まれることがある。全ての NFT 詳細取得箇所で `python3` + `re.sub(r'[\x00-\x1f]', '', raw)` を使うこと。`jq` は使わない。

---

## 3. Buy an NFT

購入フローはリスティングの通貨によって異なる。

### Step 1: リスティングの確認

Get Listings（セクション2）で取得した情報から以下を確認する：
- `currency` — ETH（ネイティブ）か ERC20（WETH, USDC 等）か
- `protocolAddress` — Seaport の protocol address（fulfillment リクエストに必要、リスティングの `protocol_address` フィールド）

### Step 1.5: ERC20 残高の確認

`kova balance` は主要トークン（USDC ネイティブ等）のみ対応。USDC.e 等ブリッジトークンの残高は RPC の `eth_call` で直接確認する。

```bash
# balanceOf(address) — function selector: 0x70a08231
# RPC_URL は kova config list で確認（例: polygon → https://1rpc.io/matic）
curl -s -X POST -H "content-type: application/json" <RPC_URL> \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{
      "to": "<ERC20_TOKEN_ADDRESS>",
      "data": "0x70a08231000000000000000000000000<WALLET_ADDRESS_NO_0x>"
    }, "latest"],
    "id": 1
  }' | python3 -c "
import sys, json
r = json.load(sys.stdin)
bal = int(r['result'], 16)
print(f'{bal / 10**6} USDC.e (raw: {bal})')
"
```

> **RPC URL の確認:** `kova config list` で `rpc.<chain>` を取得する。未設定の場合はパブリック RPC を使用する。

### Step 1.6: ネイティブトークン（ガス代）残高の確認

> **このステップは省略禁止。** ガス代不足は "execution reverted for unknown reason" としか表示されず、原因特定が困難なため事前に必ず確認する。

購入トランザクションにはガス代（Polygon なら POL、Ethereum なら ETH）が必要。Seaport の fulfillment は約 350,000〜400,000 gas を消費するため、十分なネイティブトークンがあることを確認する。

```bash
# ネイティブトークン残高確認
curl -s -X POST -H "content-type: application/json" <RPC_URL> \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": ["<WALLET_ADDRESS>", "latest"],
    "id": 1
  }' | python3 -c "
import sys, json
r = json.load(sys.stdin)
bal = int(r['result'], 16)
# Polygon: 400000 gas * 300 gwei = 0.12 POL 目安
min_required = 400000 * 300 * 10**9
print(f'Native balance: {bal / 10**18:.4f}')
print(f'Min required for gas: ~{min_required / 10**18:.4f}')
if bal < min_required:
    print('⚠️  ガス代不足! ネイティブトークンを補充してください')
else:
    print('✅ ガス代十分')
"
```

> **ガス代不足時の症状:** `kova sign transaction --broadcast` で "Execution reverted for an unknown reason" エラーが出る。ERC20 残高や allowance に問題がなくてもこのエラーになるため、先にネイティブトークン残高を確認すること。

### Step 2: ERC20 リスティングの場合 — Approve

ERC20（WETH, USDC 等）で価格設定されたリスティングを購入する場合、事前に OpenSea Conduit への approve が必要。

**OpenSea Conduit アドレス（全チェーン共通）:**
```
0x1E0049783F008A0085193E00003D00cd54003c71
```

```bash
# approve 金額の hex 変換は手動でやらない（変換ミスで失敗する）。python3 で calldata を生成する。
APPROVE_AMOUNT=<PRICE_RAW>  # リスティングの price.current.value（例: 3960000）
APPROVE_DATA=$(python3 -c "
amount = $APPROVE_AMOUNT
hex_amount = f'{amount:064x}'
print(f'0x095ea7b30000000000000000000000001E0049783F008A0085193E00003D00cd54003c71{hex_amount}')
")

# ERC20 approve トランザクション
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to <ERC20_TOKEN_ADDRESS> \
  --data "$APPROVE_DATA" \
  --broadcast
```

> **手動 hex 変換禁止:** 金額の hex 変換は必ず `python3 -c "print(f'{amount:064x}')"` 等でプログラム的に行うこと。手動変換は桁ミスの原因になる。

> **USDC vs USDC.e に注意:** Polygon 等では USDC（ネイティブ）と USDC.e（ブリッジ版）のコントラクトアドレスが異なる。リスティングの `currency` フィールドに含まれるアドレスを正確に使うこと。間違えると approve しても購入に失敗する。

ETH/ネイティブトークンで価格設定されたリスティングの場合、approve は不要。Step 2.5 へ進む。

### Step 2.5: 購入対象NFTの確認（必須）

> **このステップは省略禁止。** リスティングの order hash / token ID とカード名の取り違えを防ぐため、購入直前に必ず NFT 詳細を取得してユーザーに確認する。

購入予定のリスティングから `token ID` を使って NFT 詳細を取得し、**意図したカードであることをユーザーに明示的に確認する**。

```bash
# リスティングの offer[0].identifierOrCriteria から token ID を取得済みとする
TOKEN_ID="<TOKEN_ID_FROM_LISTING>"
CONTRACT="<NFT_CONTRACT_ADDRESS>"
CHAIN_SLUG="<OPENSEA_CHAIN_SLUG>"  # matic, ethereum 等

curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/chain/$CHAIN_SLUG/contract/$CONTRACT/nfts/$TOKEN_ID" \
  | python3 -c "
import sys, json, re
raw = sys.stdin.read()
clean = re.sub(r'[\x00-\x1f]', '', raw)
d = json.loads(clean)
nft = d['nft']
traits = {t['trait_type']: t['value'] for t in nft.get('traits', [])}
print(f\"Name:     {nft.get('name', '')}\")
print(f\"Category: {traits.get('Category', '')}\")
print(f\"Subject:  {traits.get('Title/Subject', '')}\")
print(f\"Set:      {traits.get('Set', '')}\")
print(f\"Token ID: {nft.get('identifier', '')}\")
"
```

**確認事項:**
1. 表示された NFT 名・カード名が、ユーザーが購入を希望したものと一致すること
2. token ID がリスティングの `offer[0].identifierOrCriteria` と一致すること
3. ユーザーに「このカードを購入してよいか？」と明示的に確認を取ること

> **なぜ必要か:** 同じ価格帯に複数リスティングが存在する場合、order hash と NFT 名の対応を誤るリスクがある。分析フェーズと購入フェーズで token ID の紐付けが切れると、意図しない NFT を購入してしまう。このステップでそれを防ぐ。

確認が取れたら Step 3 へ進む。

### Step 3: Get Fulfillment Data

```bash
curl -s -X POST -H "x-api-key: $OPENSEA_API_KEY" -H "content-type: application/json" \
  "https://api.opensea.io/api/v2/listings/fulfillment_data" \
  -d '{
    "listing": {
      "chain": "CHAIN",
      "hash": "ORDER_HASH",
      "protocol_address": "PROTOCOL_ADDRESS"
    },
    "fulfiller": {
      "address": "BUYER_ADDRESS"
    }
  }'
```

- `CHAIN`: OpenSea チェーンスラッグ（下記マッピング参照）
- `ORDER_HASH`: listings から取得した order hash
- `PROTOCOL_ADDRESS`: listings の `protocol_address` フィールドから取得（**ハードコードしない**）
- `BUYER_ADDRESS`: `kova wallet info --name <wallet>` で確認

> **重要: `input_data` のフォーマットについて**
> レスポンスの `fulfillment_data.transaction` には `function`, `chain`, `to`, `value`, `input_data` が含まれる。
> `input_data` は **hex calldata ではなく構造化 JSON**（`parameters` オブジェクト）で返される。
> `kova sign transaction --data` に渡すには、次の Step 3.5 で ABI エンコードして hex calldata に変換する必要がある。

レスポンス例:
```json
{
  "fulfillment_data": {
    "transaction": {
      "function": "fulfillBasicOrder_efficient_6GL6yc(...)",
      "chain": 137,
      "to": "0x0000000000000068f116a894984e2db1123eb395",
      "value": "0",
      "input_data": {
        "parameters": {
          "considerationToken": "0x...",
          "considerationIdentifier": "0",
          "considerationAmount": "3906000",
          "offerer": "0x...",
          "zone": "0x...",
          "offerToken": "0x...",
          "offerIdentifier": "123...",
          "offerAmount": "1",
          "basicOrderType": 8,
          "startTime": "...",
          "endTime": "...",
          "zoneHash": "0x...",
          "salt": "...",
          "offererConduitKey": "0x...",
          "fulfillerConduitKey": "0x...",
          "totalOriginalAdditionalRecipients": "2",
          "additionalRecipients": [
            { "amount": "42000", "recipient": "0x..." }
          ],
          "signature": "0x..."
        }
      }
    }
  }
}
```

### Step 3.5: ABI エンコード（input_data → hex calldata）

`fulfillment_data.transaction.input_data.parameters` を ethers.js（v5）でエンコードする。

> **ethers.js v5 vs v6:** v5 は `new ethers.utils.Interface()`、v6 は `new ethers.Interface()`。環境に合わせて使い分けること。

```bash
# fulfillment レスポンスの input_data.parameters を JSON ファイルに保存済みとする
# PARAMS_JSON に parameters オブジェクトの JSON 文字列をセット

CALLDATA=$(node -e "
const { ethers } = require('ethers');

// ethers v5: ethers.utils.Interface / ethers v6: ethers.Interface
const InterfaceClass = ethers.utils ? ethers.utils.Interface : ethers.Interface;
const iface = new InterfaceClass([
  'function fulfillBasicOrder_efficient_6GL6yc(tuple(address considerationToken, uint256 considerationIdentifier, uint256 considerationAmount, address offerer, address zone, address offerToken, uint256 offerIdentifier, uint256 offerAmount, uint8 basicOrderType, uint256 startTime, uint256 endTime, bytes32 zoneHash, uint256 salt, bytes32 offererConduitKey, bytes32 fulfillerConduitKey, uint256 totalOriginalAdditionalRecipients, tuple(uint256 amount, address recipient)[] additionalRecipients, bytes signature) parameters) payable returns (bool fulfilled)'
]);

const params = $PARAMS_JSON;
const calldata = iface.encodeFunctionData('fulfillBasicOrder_efficient_6GL6yc', [params]);
process.stdout.write(calldata);
")
```

`PARAMS_JSON` は fulfillment レスポンスの `input_data.parameters` をそのまま展開する。ethers.js が自動的に Seaport の `fulfillBasicOrder_efficient_6GL6yc` 関数セレクタ（`0x00000000`）付きの hex calldata を生成する。

### Step 4: Sign and Broadcast

Step 3.5 でエンコードした `CALLDATA` を `kova sign transaction` に渡す。

```bash
# Dry-run（まず確認）
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to <fulfillment.transaction.to> \
  --value <fulfillment.transaction.value> \
  --data "$CALLDATA"

# 本番実行
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to <fulfillment.transaction.to> \
  --value <fulfillment.transaction.value> \
  --data "$CALLDATA" \
  --broadcast
```

**Important:** `--broadcast` なしで dry-run して内容を確認してから `--broadcast` で実行すること。

### Step 5: 購入後の確認

broadcast 後、トランザクションの成否を確認し、NFT がウォレットに入っていることを検証する。

```bash
# 1. トランザクションの成否確認
curl -s -X POST -H "content-type: application/json" <RPC_URL> \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getTransactionReceipt",
    "params": ["TX_HASH"],
    "id": 1
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
r = data.get('result')
if r:
    status = int(r['status'], 16)
    print(f'Status: {\"SUCCESS\" if status == 1 else \"FAILED\"} ({r[\"status\"]})')
else:
    print('Transaction not yet mined')
"

# 2. NFT の所有権確認（ownerOf）
# OpenSea API のインデックスは遅延するため、RPC 直接で確認する
TOKEN_ID_HEX=$(python3 -c "print(f'{TOKEN_ID:064x}')")
curl -s -X POST -H "content-type: application/json" <RPC_URL> \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"eth_call\",
    \"params\": [{
      \"to\": \"NFT_CONTRACT_ADDRESS\",
      \"data\": \"0x6352211e${TOKEN_ID_HEX}\"
    }, \"latest\"],
    \"id\": 1
  }" | python3 -c "
import sys, json
r = json.load(sys.stdin)
owner = '0x' + r['result'][-40:]
print(f'Owner: {owner}')
"
```

- `TOKEN_ID`: リスティングから取得した token ID（10進数）
- `0x6352211e`: `ownerOf(uint256)` の function selector
- 返り値の owner がウォレットアドレスと一致すれば購入成功

> **OpenSea API vs RPC:** OpenSea の NFT 一覧 API（`/account/.../nfts`）はインデックス反映に遅延がある。購入直後の確認は必ず RPC の `ownerOf` で行うこと。

**3. OpenSea URL の生成**

購入後にユーザーへ NFT の OpenSea ページを提示する:

```
https://opensea.io/assets/{CHAIN_SLUG}/{CONTRACT}/{TOKEN_ID}
```

| kova チェーン名 | OpenSea URL の CHAIN_SLUG |
|---------------|--------------------------|
| ethereum | ethereum |
| base | base |
| polygon | matic |
| arbitrum | arbitrum |
| optimism | optimism |

例: `https://opensea.io/assets/matic/0x251be3a17af4892035c37ebf5890f4a4d889dcad/12345`

### Chain Name Mapping

| kova / 一般名 | OpenSea API スラッグ |
|--------------|-------------------|
| ethereum | ethereum |
| base | base |
| polygon | matic |
| arbitrum | arbitrum |
| optimism | optimism |
| polygon-amoy | mumbai |

---

## 4. Collection Stats

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/collections/SLUG/stats" | jq '.total | {floorPrice: .floor_price, currency: .floor_price_symbol, volume: .volume, sales: .sales, owners: .num_owners}'
```

---

## 5. List an NFT (出品・売却)

出品は5ステップ：NFT approve → コレクション情報取得 → counter 取得 → EIP-712 署名 → API に POST。

### 定数

| Name | Value |
|------|-------|
| Seaport v1.6 | `0x0000000000000068F116a894984e2DB1123eB395` |
| OpenSea Conduit | `0x1E0049783F008A0085193E00003D00cd54003c71` |
| Conduit Key | `0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000` |
| OpenSea Fee Recipient | `0x0000a26b00c1F0DF003000390027140000fAa719` |
| OpenSea SignedZone v2 | `0x000056f7000000ece9003ca63978907a00ffd100` |
| OpenSea Fee | コレクションにより異なる（Step 2 の fees で確認） |
| Polygon RPC | `https://polygon-bor-rpc.publicnode.com` |
| USDC.e (Polygon bridged) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` (6 decimals) |
| USDC (Polygon native) | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` (6 decimals) |

> **通貨の注意:** Courtyard.io のリスティングは主に **USDC.e (bridged)** で建てられている。USDC native とはアドレスが異なるため混同しないこと。

### ItemType

| Value | Type |
|-------|------|
| 0 | NATIVE (ETH) |
| 1 | ERC20 |
| 2 | ERC721 |
| 3 | ERC1155 |

### Step 1: NFT を Conduit に Approve

NFT コントラクトの `setApprovalForAll(operator, true)` で OpenSea Conduit に転送権限を付与する。

**事前確認（approve 済みならスキップ）:**

```bash
# isApprovedForAll(owner, operator) - selector: 0xe985e9c5
curl -s -X POST -H "content-type: application/json" "https://polygon-bor-rpc.publicnode.com" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{
      "to": "<NFT_CONTRACT_ADDRESS>",
      "data": "0xe985e9c5000000000000000000000000<OWNER_ADDRESS_NO_0x>0000000000000000000000001e0049783f008a0085193e00003d00cd54003c71"
    }, "latest"],
    "id": 1
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print('approved:', int(r['result'], 16) == 1)"
```

結果が `approved: True` なら Step 2 へスキップ。`False` なら以下を実行:

```bash
# setApprovalForAll(0x1E0049783F008A0085193E00003D00cd54003c71, true)
# function selector: 0xa22cb465
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to <NFT_CONTRACT_ADDRESS> \
  --data "0xa22cb4650000000000000000000000001E0049783F008A0085193E00003D00cd54003c710000000000000000000000000000000000000000000000000000000000000001" \
  --broadcast
```

### Step 2: コレクション情報取得（creator fee）

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/collections/SLUG" | jq '{fees: .fees, editors: .editors}'
```

レスポンスの `fees` からクリエイターフィー（basis points とrecipient）を取得する。

### Step 3: Seaport counter 取得

seller の現在の counter を `eth_call` で取得する。

```bash
# getCounter(address) - function selector: 0xf07ec373
# address を 32 byte にパディングして連結
curl -s -X POST -H "content-type: application/json" "https://polygon-bor-rpc.publicnode.com" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{
      "to": "0x0000000000000068F116a894984e2DB1123eB395",
      "data": "0xf07ec373000000000000000000000000<SELLER_ADDRESS_NO_0x>"
    }, "latest"],
    "id": 1
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print('counter_hex:', r['result']); print('counter_dec:', int(r['result'], 16))"
```

返り値は hex エンコードされた uint256。10進数に変換して使用。counter は u128 を超えることがあるため、必ず python3 等で変換する。

### Step 4: Order パラメータ構築 + EIP-712 署名

以下の EIP-712 typed data を構築し、`kova sign typed-data` で署名する。

> **uint256 値の hex 変換が必要:** `kova sign typed-data` は u128 を超える数値を10進数文字列で受け付けない。
> `identifierOrCriteria`（token ID）、`salt`、`counter` は python3 で hex に変換してから渡すこと。
>
> ```bash
> # 大きな数値を hex に変換
> python3 -c "
> token_id = <TOKEN_ID_DECIMAL>
> counter = <COUNTER_DECIMAL>
> print(f'token_id hex: 0x{token_id:064x}')
> print(f'counter hex: 0x{counter:064x}')
> "
> ```

**価格計算（consideration 配列の構築）:**

Step 2 で取得した fees からコレクションの手数料率を確認する：
- OpenSea fee = `PRICE * OPENSEA_BPS / 10000`
- Creator fee = `PRICE * CREATOR_BPS / 10000`
- Seller proceeds = `PRICE - OpenSea fee - Creator fee`

> **Courtyard.io の手数料例（$5.00 USDC.e の場合）:**
> - OpenSea fee 1% = `50000` (= 5000000 * 100 / 10000)
> - Creator fee 6% = `300000` (= 5000000 * 600 / 10000)
> - Seller proceeds = `4650000` (= 5000000 - 50000 - 300000)
> - recipient (creator): `0x732134d7f99b90c704d736b360db45425073380f`

**通貨の選択:**
- ETH/ネイティブ建て: consideration の `itemType: 0`, `token: 0x0000...0000`
- ERC20 建て（USDC, WETH 等）: consideration の `itemType: 1`, `token: ERC20_CONTRACT_ADDRESS`
  - 金額は最小単位（USDC なら 6 decimals: 5 USDC = `5000000`）

```bash
kova sign typed-data \
  --name <wallet> \
  --chain <chain> \
  --data '{
    "types": {
      "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"}
      ],
      "OrderComponents": [
        {"name": "offerer", "type": "address"},
        {"name": "zone", "type": "address"},
        {"name": "offer", "type": "OfferItem[]"},
        {"name": "consideration", "type": "ConsiderationItem[]"},
        {"name": "orderType", "type": "uint8"},
        {"name": "startTime", "type": "uint256"},
        {"name": "endTime", "type": "uint256"},
        {"name": "zoneHash", "type": "bytes32"},
        {"name": "salt", "type": "uint256"},
        {"name": "conduitKey", "type": "bytes32"},
        {"name": "counter", "type": "uint256"}
      ],
      "OfferItem": [
        {"name": "itemType", "type": "uint8"},
        {"name": "token", "type": "address"},
        {"name": "identifierOrCriteria", "type": "uint256"},
        {"name": "startAmount", "type": "uint256"},
        {"name": "endAmount", "type": "uint256"}
      ],
      "ConsiderationItem": [
        {"name": "itemType", "type": "uint8"},
        {"name": "token", "type": "address"},
        {"name": "identifierOrCriteria", "type": "uint256"},
        {"name": "startAmount", "type": "uint256"},
        {"name": "endAmount", "type": "uint256"},
        {"name": "recipient", "type": "address"}
      ]
    },
    "primaryType": "OrderComponents",
    "domain": {
      "name": "Seaport",
      "version": "1.6",
      "chainId": CHAIN_ID,
      "verifyingContract": "0x0000000000000068F116a894984e2DB1123eB395"
    },
    "message": {
      "offerer": "SELLER_ADDRESS",
      "zone": "0x000056f7000000ece9003ca63978907a00ffd100",
      "offer": [
        {
          "itemType": 2,
          "token": "NFT_CONTRACT",
          "identifierOrCriteria": "TOKEN_ID_HEX",
          "startAmount": "1",
          "endAmount": "1"
        }
      ],
      "consideration": [
        {
          "itemType": 0,
          "token": "PAYMENT_TOKEN",
          "identifierOrCriteria": "0",
          "startAmount": "SELLER_PROCEEDS",
          "endAmount": "SELLER_PROCEEDS",
          "recipient": "SELLER_ADDRESS"
        },
        {
          "itemType": 0,
          "token": "PAYMENT_TOKEN",
          "identifierOrCriteria": "0",
          "startAmount": "OPENSEA_FEE",
          "endAmount": "OPENSEA_FEE",
          "recipient": "0x0000a26b00c1F0DF003000390027140000fAa719"
        },
        {
          "itemType": 0,
          "token": "PAYMENT_TOKEN",
          "identifierOrCriteria": "0",
          "startAmount": "CREATOR_FEE",
          "endAmount": "CREATOR_FEE",
          "recipient": "CREATOR_FEE_RECIPIENT"
        }
      ],
      "orderType": 2,
      "startTime": "START_UNIX_TIMESTAMP",
      "endTime": "END_UNIX_TIMESTAMP",
      "zoneHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "salt": "0x360c6ebe<RANDOM_56_HEX_CHARS>",
      "conduitKey": "0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
      "counter": "COUNTER_HEX_FROM_STEP3"
    }
  }'
```

> **署名 vs API POST の数値フォーマット:**
> | フィールド | `kova sign typed-data`（署名） | OpenSea API POST |
> |-----------|-------------------------------|-----------------|
> | `identifierOrCriteria` (token ID) | **hex** (`0x3b78...`) — u128超は10進不可 | **10進数文字列** — hex を送ると "Must be a valid integer" エラー |
> | `salt` | **hex** (`0x360c6ebe...`) | **10進数文字列** |
> | `counter` | **hex** (`0x4f3f...`) — u128超は10進不可 | **10進数文字列** |
> | 金額 (`startAmount` 等) | 10進数文字列 OK | 10進数文字列 |

> **salt のプレフィックス:** OpenSea ドメインのオーダーは salt の先頭4バイトを `360c6ebe` にする必要がある。API POST では10進数に変換して送る。

> **creator fee が 0% の場合:** consideration 配列は2要素（seller + OpenSea fee）のみ。`totalOriginalConsiderationItems` も 2 にする。

### Step 5: OpenSea API に POST

署名結果を Seaport order として OpenSea API に送信する。

```bash
curl -s -X POST \
  -H "x-api-key: $OPENSEA_API_KEY" \
  -H "content-type: application/json" \
  "https://api.opensea.io/api/v2/orders/CHAIN_SLUG/seaport/listings" \
  -d '{
    "parameters": {
      "offerer": "SELLER_ADDRESS",
      "zone": "0x000056f7000000ece9003ca63978907a00ffd100",
      "offer": [ ... ],
      "consideration": [ ... ],
      "orderType": 2,
      "startTime": "START_UNIX_TIMESTAMP",
      "endTime": "END_UNIX_TIMESTAMP",
      "zoneHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "salt": "SALT_AS_DECIMAL_STRING",
      "conduitKey": "0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
      "totalOriginalConsiderationItems": 3,
      "counter": "COUNTER"
    },
    "protocol_address": "0x0000000000000068F116a894984e2DB1123eB395",
    "signature": "SIGNATURE_FROM_STEP4"
  }'
```

- `CHAIN_SLUG`: OpenSea チェーンスラッグ（Chain Name Mapping 参照）
- `totalOriginalConsiderationItems`: consideration 配列の要素数（creator fee なしなら 2、ありなら 3）
- **重要**: `identifierOrCriteria` と `salt` は**10進数文字列**で送ること（hex 不可）
- `offer`/`consideration` は Step 4 の署名で使ったものと同じ内容（ただし数値フォーマットを10進数に変換）
- レスポンスに `listing.order_hash` と `listing.status: "ACTIVE"` が返れば出品成功

### バッチ出品（複数 NFT を同時出品）

複数 NFT を同一価格・同一期間で出品する場合、以下を共通化して効率的に処理する:

1. **1回だけ実行:** Step 1 (approve確認)、Step 2 (fees取得)、Step 3 (counter取得)
2. **NFT ごとに変える:** `offer[0].identifierOrCriteria` (token ID) と `salt` のみ
3. **署名は NFT ごと** — token ID が異なるため EIP-712 ハッシュも異なる
4. **POST は並行可** — 署名済み order は互いに独立

```bash
# salt 生成（NFTごとに一意にする）
python3 -c "
import secrets
TOKEN_IDS = [<TOKEN_ID_1>, <TOKEN_ID_2>, <TOKEN_ID_3>]
for tid in TOKEN_IDS:
    salt = '0x360c6ebe' + secrets.token_hex(28)
    print(f'token_id: {tid}')
    print(f'  token_id_hex: 0x{tid:064x}')
    print(f'  salt_hex: {salt}')
    print(f'  salt_dec: {int(salt, 16)}')
"
```

counter、startTime、endTime、consideration は全 NFT 共通で使い回せる。

---

## 6. Sale Events (売買履歴)

### 基本取得

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/events/collection/SLUG?event_type=sale&limit=50" | jq '.asset_events[] | {tokenId: .nft.identifier, name: .nft.name, price: (.payment.quantity | tonumber / pow(10; .payment.decimals)), currency: .payment.symbol, timestamp: .event_timestamp}'
```

### 時間窓指定（戦略で使用）

`after` パラメータで取得開始時刻（UNIX秒）を指定できる。

```bash
# 直近6時間の売買を取得
AFTER=$(python3 -c "import time; print(int(time.time()) - 6*3600)")
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/events/collection/courtyard-nft?event_type=sale&limit=50&after=$AFTER"
```

### ページネーションで全件取得

```bash
python3 << 'PYEOF'
import json, subprocess, os, time

api_key = os.environ['OPENSEA_API_KEY']
after = int(time.time()) - 6 * 3600  # 時間窓（秒）を調整

sales = []
next_cursor = ""
for page in range(100):
    url = f"https://api.opensea.io/api/v2/events/collection/courtyard-nft?event_type=sale&limit=50&after={after}"
    if next_cursor:
        url += f"&next={next_cursor}"
    r = subprocess.run(
        ["curl", "-s", "-H", f"x-api-key: {api_key}", url],
        capture_output=True, text=True
    )
    clean = ''.join(c if ord(c) >= 32 or c in '\n\r\t' else ' ' for c in r.stdout)
    try:
        data = json.loads(clean)
    except Exception:
        break
    events = data.get('asset_events', [])
    if not events:
        break
    for e in events:
        name = e.get('nft', {}).get('name', '')
        payment = e.get('payment', {})
        price = int(payment.get('quantity', '0')) / 10**int(payment.get('decimals', 6))
        if price <= 0:
            continue
        ts = e.get('event_timestamp', 0)
        token_id = e.get('nft', {}).get('identifier', '')
        sales.append({'name': name, 'price': price, 'ts': ts, 'token_id': token_id})
    next_cursor = data.get('next', '')
    if not next_cursor:
        break

print(f"Total sales: {len(sales)}")
PYEOF
```

### 分析パターン

Stats と Sale Events を組み合わせて分析する：
- **floorPrice / 平均売買価格 < 0.9** → 割安の可能性
- **floorPrice / 平均売買価格 > 1.1** → 割高の可能性
- 直近半分 vs 古い半分の平均を比較して **trend**（rising/declining/stable）を判定

---

## 7. My Listings (自分の出品一覧)

自分のウォレットが出品中のオーダーを取得する。

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/orders/CHAIN_SLUG/seaport/listings?maker=SELLER_ADDRESS&limit=20" \
  | jq '.orders[] | {
    orderHash: .order_hash,
    nft: .protocol_data.parameters.offer[0].token,
    tokenId: .protocol_data.parameters.offer[0].identifierOrCriteria,
    price: ((.protocol_data.parameters.consideration | map(.startAmount | tonumber) | add) / 1e6),
    expiration: .expiration_time,
    params: .protocol_data.parameters
  }'
```

- `CHAIN_SLUG`: OpenSea チェーンスラッグ（Chain Name Mapping 参照）
- `SELLER_ADDRESS`: 自分のウォレットアドレス（小文字）
- レスポンスの `params` にキャンセルに必要な order parameters が含まれる

> **price の計算:** 上記は USDC (6 decimals) 前提。ETH の場合は `/ 1e18` に変更すること。

---

## 8. Cancel a Listing (出品取り消し)

Seaport v1.6 でオンチェーンにキャンセルを記録する。3つの方法がある。

### 方法 A: 個別キャンセル（推奨）

Seaport の `cancel(OrderComponents[])` を呼び出す。Section 7 で取得した order parameters を使う。

```
function cancel(OrderComponents[] calldata orders) external returns (bool cancelled)
```

**function selector:** `0xfd9f1e10`

cancel の calldata は OrderComponents 構造体の ABI エンコードが必要。以下の手順でエンコードする：

**Step 1: Section 7 で order parameters を取得**

キャンセルしたいオーダーの `params` を確認する。必要なフィールド：
`offerer`, `zone`, `offer[]`, `consideration[]`, `orderType`, `startTime`, `endTime`, `zoneHash`, `salt`, `conduitKey`, `counter`

**Step 2: ABI エンコードして calldata を構築**

`cancel` は `OrderComponents[]`（構造体の配列）を引数に取る。ABI エンコードのルール：

1. function selector: `0xfd9f1e10`
2. offset to array: `0x0000...0020` (32 bytes)
3. array length: `0x0000...0001` (1 order)
4. offset to first OrderComponents: `0x0000...0020`
5. 各フィールドを順に 32 bytes にパディング（offer/consideration は動的配列なのでさらに offset が入る）

**エンコードは複雑なため、以下の方法で生成することを推奨:**

```bash
# ethers.js でエンコード（v5/v6 両対応）
CANCEL_DATA=$(node -e "
const { ethers } = require('ethers');
const InterfaceClass = ethers.utils ? ethers.utils.Interface : ethers.Interface;
const iface = new InterfaceClass([
  'function cancel(tuple(address offerer, address zone, tuple(uint8 itemType, address token, uint256 identifierOrCriteria, uint256 startAmount, uint256 endAmount)[] offer, tuple(uint8 itemType, address token, uint256 identifierOrCriteria, uint256 startAmount, uint256 endAmount, address recipient)[] consideration, uint8 orderType, uint256 startTime, uint256 endTime, bytes32 zoneHash, uint256 salt, bytes32 conduitKey, uint256 counter)[] orders) external returns (bool cancelled)'
]);
const params = \$ORDER_PARAMS_JSON;  // Section 7 で取得した params + counter
process.stdout.write(iface.encodeFunctionData('cancel', [[params]]));
")
```

> **counter フィールド:** Section 7 のレスポンスの `params` には `counter` が含まれていない場合がある。その場合は Section 5 Step 3 と同様に `getCounter` で取得して追加すること。

**Step 3: トランザクション送信**

```bash
# Dry-run
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to 0x0000000000000068F116a894984e2DB1123eB395 \
  --data "$CANCEL_DATA"

# Broadcast
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to 0x0000000000000068F116a894984e2DB1123eB395 \
  --data "$CANCEL_DATA" \
  --broadcast
```

### 方法 B: 全オーダー一括無効化

Seaport の `incrementCounter()` を呼び出すと、現在の counter 以下で作成した**全オーダー**が無効になる。

```
function incrementCounter() external returns (uint256 newCounter)
```

**function selector:** `0x5b34b966`

```bash
# Dry-run
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to 0x0000000000000068F116a894984e2DB1123eB395 \
  --data "0x5b34b966"

# Broadcast
kova sign transaction \
  --name <wallet> \
  --chain <chain> \
  --to 0x0000000000000068F116a894984e2DB1123eB395 \
  --data "0x5b34b966" \
  --broadcast
```

> **注意:** `incrementCounter` は出品だけでなくオファーも含め**全ての未約定オーダー**を無効化する。残したいオーダーがある場合は方法 A を使うこと。

### 方法の選び方

| 状況 | 推奨 |
|------|------|
| 特定の1件だけ取り消したい | 方法 A（個別 cancel） |
| 全オーダーを取り消したい | 方法 B（incrementCounter） |
| foundry がなく calldata 構築が面倒 | 方法 B（incrementCounter） → 残したいオーダーを再出品 |

> **ガス代:** キャンセルはオンチェーントランザクションなのでガス代がかかる。Polygon なら数セント程度。

### キャンセル後の確認

```bash
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/orders/CHAIN_SLUG/seaport/listings?maker=SELLER_ADDRESS&limit=20" \
  | jq '.orders | length'
```

トランザクションが確定すると、OpenSea 側でもリスティングが自動的に削除される（反映に数分かかる場合がある）。0 件になればキャンセル完了。

---

## Typical Workflow

```bash
# 0. API キー読み込み
export OPENSEA_API_KEY=$(grep OPENSEA_API_KEY .env | cut -d'=' -f2)

# 1. Search for a collection（スラッグ直接指定）
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/collections/azuki" | jq '{slug: .collection, name, chain: .contracts[0].chain}'

# 2. Check stats
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/collections/azuki/stats" | jq '.total'

# 3. Browse listings
curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/listings/collection/azuki/all?limit=5" | jq '.listings[] | {orderHash: .order_hash, price: (.price.current.value | tonumber / pow(10; .price.current.decimals)), currency: .price.current.currency}'

# 4. Get fulfillment data for a listing (protocol_address はリスティングから取得)
FULFILLMENT=$(curl -s -X POST -H "x-api-key: $OPENSEA_API_KEY" -H "content-type: application/json" \
  "https://api.opensea.io/api/v2/listings/fulfillment_data" \
  -d '{"listing":{"chain":"ethereum","hash":"0xORDER","protocol_address":"0xPROTOCOL_FROM_LISTING"},"fulfiller":{"address":"0xBUYER"}}')

# 5. (ERC20の場合のみ) Approve — 金額は python3 で hex 変換（手動変換禁止）
APPROVE_AMOUNT=3960000  # price.current.value
APPROVE_DATA=$(python3 -c "print(f'0x095ea7b30000000000000000000000001E0049783F008A0085193E00003D00cd54003c71{$APPROVE_AMOUNT:064x}')")
kova sign transaction --name my-wallet --chain ethereum \
  --to 0xTOKEN_ADDRESS --data "$APPROVE_DATA" --broadcast

# 6. ABI エンコード（input_data は構造化 JSON なので hex calldata に変換が必要）
PARAMS_JSON=$(echo "$FULFILLMENT" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['fulfillment_data']['transaction']['input_data']['parameters']))")
CALLDATA=$(node -e "
const { ethers } = require('ethers');
const InterfaceClass = ethers.utils ? ethers.utils.Interface : ethers.Interface;
const iface = new InterfaceClass([
  'function fulfillBasicOrder_efficient_6GL6yc(tuple(address considerationToken, uint256 considerationIdentifier, uint256 considerationAmount, address offerer, address zone, address offerToken, uint256 offerIdentifier, uint256 offerAmount, uint8 basicOrderType, uint256 startTime, uint256 endTime, bytes32 zoneHash, uint256 salt, bytes32 offererConduitKey, bytes32 fulfillerConduitKey, uint256 totalOriginalAdditionalRecipients, tuple(uint256 amount, address recipient)[] additionalRecipients, bytes signature) parameters) payable returns (bool fulfilled)'
]);
const params = $PARAMS_JSON;
process.stdout.write(iface.encodeFunctionData('fulfillBasicOrder_efficient_6GL6yc', [params]));
")

# 7. Dry-run
kova sign transaction --name my-wallet --chain ethereum \
  --to 0xSEAPORT --value 0 --data "$CALLDATA"

# 8. Broadcast
kova sign transaction --name my-wallet --chain ethereum \
  --to 0xSEAPORT --value 0 --data "$CALLDATA" --broadcast

# 9. 購入確認（RPC で ownerOf を確認 — OpenSea API は遅延あり）
TOKEN_ID_HEX=$(python3 -c "print(f'{TOKEN_ID:064x}')")
curl -s -X POST -H "content-type: application/json" <RPC_URL> \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_call\",\"params\":[{\"to\":\"NFT_CONTRACT\",\"data\":\"0x6352211e${TOKEN_ID_HEX}\"},\"latest\"],\"id\":1}" \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'Owner: 0x{r[\"result\"][-40:]}')"
```

### Pokémon Card Workflow（ポケカ検索 → 購入）

```bash
# 0. API キー読み込み
export OPENSEA_API_KEY=$(grep OPENSEA_API_KEY .env | cut -d'=' -f2)

# 1. Courtyard.io のリスティング取得（Polygon, USDC 建て）
LISTINGS=$(curl -s -H "x-api-key: $OPENSEA_API_KEY" \
  "https://api.opensea.io/api/v2/listings/collection/courtyard-nft/all?limit=50")

# 2. 安い順にソート → token ID 抽出
TOKEN_IDS=$(echo "$LISTINGS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = []
for l in data['listings']:
    pv = int(l['price']['current']['value'])
    dec = l['price']['current']['decimals']
    tid = l['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
    oh = l['order_hash']
    items.append((pv, dec, tid, oh))
items.sort()
for pv, dec, tid, oh in items[:20]:
    print(f'{tid}\t{pv / 10**dec}\t{oh}')
")

# 3. NFT 詳細取得 + ポケカフィルタ（python3 必須: API レスポンスに制御文字あり）
echo "$TOKEN_IDS" | while IFS=$'\t' read -r TID PRICE OH; do
  curl -s -H "x-api-key: $OPENSEA_API_KEY" \
    "https://api.opensea.io/api/v2/chain/matic/contract/0x251be3a17af4892035c37ebf5890f4a4d889dcad/nfts/$TID" \
    | python3 -c "
import sys, json
d = json.load(sys.stdin)
nft = d['nft']
traits = {t['trait_type']: t['value'] for t in nft.get('traits', [])}
if traits.get('Category') == 'Pokémon':
    print(json.dumps({'name': nft.get('name',''), 'subject': traits.get('Title/Subject',''), 'set': traits.get('Set',''), 'lang': traits.get('Language','')}))" 2>/dev/null \
    | while read -r DETAIL; do echo -e "\$${PRICE}\t${OH}\t${DETAIL}"; done
done

# 4. 気に入ったカードを Buy
# 4-a. ERC20 残高確認（USDC.e は kova balance で取れないので RPC 直接）
#   RPC_URL=$(kova config list | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['config']['rpc'].get('polygon','https://1rpc.io/matic'))")
#   curl ... eth_call balanceOf（セクション 3 Step 1.5 参照）
# 4-b. Approve → Fulfillment → ABI エンコード → Dry-run → Broadcast（セクション 3 参照）
```

---

## Pokémon Card Traits Reference

Courtyard.io NFT の traits 構造。戦略でフィルタリングする際に使用する。

| Trait | 用途 | 例 |
|-------|------|-----|
| Category | カテゴリフィルタ | `Pokémon` |
| Title/Subject | カード名（ポケモン名） | `Charizard ex`, `Pikachu` |
| Set | セット名 | `Pokémon Pre EN-Prismatic Evolutions` |
| Grade | グレード数値 | `10 GEM MINT`, `9 MINT`, `8 NM-MT` |
| Grader | グレーディング会社 | `PSA`, `CGC`, `BGS` |
| Year | 発行年 | `2025` |
| Language | 言語 | `English`, `Japanese` |
| Card Number | カード番号 | `75` |

**グレード間の価格差目安:**

| グレード | 価格倍率（PSA 9 を 1x とした場合） |
|---------|--------------------------------|
| PSA 10 GEM MINT / CGC 10 PRISTINE | 2x - 10x |
| PSA 9 MINT / CGC 9 MINT | 1x（基準） |
| PSA 8 NM-MT / CGC 8.5 | 0.3x - 0.7x |
| PSA 7 以下 | 0.1x - 0.3x |

> **重要:** 同一カード名でもグレードが異なると適正価格が大きく変わる。戦略で価格比較する際は必ずグレードを考慮すること。

---

## Error Handling

| HTTP Status | Cause | Fix |
|------------|-------|-----|
| 401 | Invalid API key | `$OPENSEA_API_KEY` を確認 |
| 429 | Rate limited | 数秒待ってリトライ |
| 400 | Invalid request | リクエストパラメータを確認 |

## Supported Chains

Mainnet: `ethereum`, `base`, `polygon`, `arbitrum`, `optimism`
Testnet: `sepolia`, `base-sepolia`, `polygon-amoy`

---

# Part 2: 戦略フレームワーク

ユーザーが自然言語で取引戦略を伝え、エージェントが解釈・実行するフレームワーク。

## Overview

使用例:
- 「モメンタム戦略で探して」→ Part 3 のプリセットを実行
- 「ポケカのPSA 10で、直近1日に2回以上売買されて値上がり中のカードがあれば、相場より20%安い出品を見つけて購入提案して」→ カスタム戦略
- 「CGC 10のカードで$50以下、最近売れたやつを探して」→ カスタム戦略

## Execution Flow

```
[1. Parse]  ユーザーの自然言語から条件を抽出
     │
     ▼
[2. Scan]   OpenSea events/listings API でデータ取得
     │
     ▼
[3. Score]  条件に合致するカードをスコアリング
     │
     ▼
[4. Propose] 購入候補を提示 → ユーザー承認 → Part 1 の購入フローで実行
```

## Parse: 戦略パラメータ抽出

ユーザーの指示から以下のパラメータを抽出する:

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| grade | 対象グレード（PSA 10, CGC 9 等） | 全グレード |
| price_range | 価格帯（$20-100 等） | 制限なし |
| time_window | 分析対象の時間窓 | 直近6時間 |
| trigger | 購入候補に入れる条件 | 戦略依存 |
| action_threshold | アクション実行の閾値 | 相場比-15% |
| budget_limit | 1件あたり/合計の予算上限 | **必ず確認** |

**ルール:**
- `budget_limit` が未指定の場合、実行前に必ずユーザーに確認する
- 曖昧な条件は確認せず、ベストエフォートで解釈する（結果を見てユーザーが調整）
- カテゴリは Pokémon 固定（Category == "Pokémon" でフィルタ）
- ブースターパック/シールド品は常に除外（name に "Booster Pack", "Draft Booster" を含むもの）

## Scan: データ取得

戦略の種類に応じて Part 1 の API を使い分ける:

| データ | 使用するセクション | 用途 |
|--------|-----------------|------|
| 直近売買 | Section 6 (Sale Events) with `after` param | 相場算出、トレンド検出 |
| 現在出品 | Section 2 (Get Listings) | 購入候補の特定 |
| NFT詳細 | Section 2-b (Get NFT Detail) | カード名・グレード照合 |

**Pokémon フィルタ:**

events API のレスポンスでは `nft.name` にカード情報が含まれる。以下でフィルタ:
- `name` に "Pok" または "Pokemon" を含むもののみ対象
- "Booster Pack", "Draft Booster" を含むものを除外

正確なカテゴリ判定が必要な場合は NFT Detail (Section 2-b) で `Category` trait を確認する。

## Score: スコアリング

トリガー条件に応じてスコアを算出する。基本式:

```
score = signal_strength × confidence × recency
```

| 要素 | 説明 | 計算例 |
|------|------|--------|
| signal_strength | トリガー条件の強度 | 価格上昇率 (%) |
| confidence | データの信頼性 | log(売買回数 + 1) |
| recency | 直近性の重み | 直近1hなら1.0, 6h前なら0.5 |

スコア上位のカードから順に出品スキャンを行う。

## Propose: 購入提案

提案フォーマット:

```
🔥 購入候補 #1
  カード: [カード名] ([Grade])
  シグナル: [トリガー条件の具体的内容]
  出品価格: $XX.XX
  相場（直近中央値）: $XX.XX
  割安率: -XX%
  潜在利益: $XX.XX ~ $XX.XX

  購入しますか？ (order_hash: 0x...)
```

ユーザーが承認した場合、Part 1 Section 3 (Buy an NFT) のフローに進む:
1. ERC20 残高確認 (Step 1.5)
2. Approve (Step 2)
3. Fulfillment data 取得 (Step 3)
4. ABI エンコード (Step 3.5)
5. Dry-run → ユーザー確認 → Broadcast (Step 4)
6. 購入確認 (Step 5)

## Safety Rules

- 購入前に必ず dry-run (`--broadcast` なし) を実行し内容を表示する
- `budget_limit` を超える購入は提案しない
- 同一カードを重複購入しない（ウォレット内の保有確認は ownerOf で可能）
- events API が 500 エラーの場合、3秒待ってリトライ（最大3回）。回復しなければユーザーに通知して中止
- レートリミット (429) の場合、5秒待ってリトライ

---

# Part 3: プリセット戦略

## モメンタム戦略

直近の売買で価格上昇中のカードを検出し、同名カードの安い出品を特定する。

**呼び出し方:** 「モメンタム戦略で探して」

### 条件

```
strategy: momentum
time_window: 6h
trigger: 同一カード名で2回以上売買 AND 最新価格 > 最初の価格
action_threshold: 直近売買の中央値より15%以上安い出品
exclude: ブースターパック/シールド品
grade_match: 同一グレードでの比較を優先（不一致時は閾値を30%に引き上げ）
```

### バックテスト結果

| 指標 | 値 |
|------|-----|
| 分析期間 | 8.8時間 |
| 同一token ID転売 | 40件 |
| 利益転売の勝率 | 78% (31/40) |
| 平均利益率 | +20.5% |
| 最大利益 | +109.3% |

### Step 1: モメンタム検出

```bash
python3 << 'PYEOF'
import json, subprocess, os, time, math
from collections import defaultdict

api_key = os.environ['OPENSEA_API_KEY']
now = int(time.time())
window = now - 6 * 3600

# 売買データ取得
sales = []
next_cursor = ""
for page in range(100):
    url = f"https://api.opensea.io/api/v2/events/collection/courtyard-nft?event_type=sale&limit=50&after={window}"
    if next_cursor:
        url += f"&next={next_cursor}"
    r = subprocess.run(
        ["curl", "-s", "-H", f"x-api-key: {api_key}", url],
        capture_output=True, text=True
    )
    clean = ''.join(c if ord(c) >= 32 or c in '\n\r\t' else ' ' for c in r.stdout)
    try:
        data = json.loads(clean)
    except Exception:
        break
    events = data.get('asset_events', [])
    if not events:
        break
    for e in events:
        name = e.get('nft', {}).get('name', '')
        if 'Booster Pack' in name or 'Draft Booster' in name:
            continue
        if 'Pok' not in name and 'Pokemon' not in name:
            continue
        payment = e.get('payment', {})
        price = int(payment.get('quantity', '0')) / 10**int(payment.get('decimals', 6))
        if price <= 0:
            continue
        ts = e.get('event_timestamp', 0)
        token_id = e.get('nft', {}).get('identifier', '')
        sales.append({'name': name, 'price': price, 'ts': ts, 'token_id': token_id})
    next_cursor = data.get('next', '')
    if not next_cursor:
        break

print(f"Pokémon sales (last 6h): {len(sales)}")

# モメンタム検出
name_sales = defaultdict(list)
for s in sales:
    name_sales[s['name']].append(s)

momentum = []
for name, card_sales in name_sales.items():
    if len(card_sales) < 2:
        continue
    card_sales.sort(key=lambda x: x['ts'])
    first_price = card_sales[0]['price']
    last_price = card_sales[-1]['price']
    if first_price > 0 and last_price > first_price:
        pct = (last_price - first_price) / first_price * 100
        median = sorted(s['price'] for s in card_sales)[len(card_sales) // 2]
        score = pct * math.log(len(card_sales) + 1)
        momentum.append({
            'name': name,
            'score': score,
            'pct_change': pct,
            'median': median,
            'num_sales': len(card_sales),
            'last_price': last_price,
        })

momentum.sort(key=lambda x: -x['score'])
top_targets = momentum[:10]

print(f"\n=== MOMENTUM TARGETS (Top {len(top_targets)}) ===\n")
for i, m in enumerate(top_targets, 1):
    print(f"#{i} [score={m['score']:.1f}] {m['name'][:60]}")
    print(f"   +{m['pct_change']:.1f}%, {m['num_sales']}回売買, 中央値=${m['median']:.2f}")

# 後続の出品スキャンで使うカード名を出力
print(f"\n=== TARGET NAMES ===")
for m in top_targets:
    print(f"  {m['name']}")
PYEOF
```

### Step 2: 出品スキャン（割安出品の検出）

Step 1 で検出したモメンタム上位カードと同名の出品を検索し、相場より安い出品を購入候補として提示する。

```bash
python3 << 'PYEOF'
import json, subprocess, os

api_key = os.environ['OPENSEA_API_KEY']

# Step 1 の結果からターゲットカード名と中央値をセット
# (エージェントが Step 1 の出力から手動でセットする)
targets = {
    # "カード名": median_price,
}

# 出品を取得
listings = []
next_cursor = ""
for page in range(5):
    url = f"https://api.opensea.io/api/v2/listings/collection/courtyard-nft/all?limit=100"
    if next_cursor:
        url += f"&next={next_cursor}"
    r = subprocess.run(
        ["curl", "-s", "-H", f"x-api-key: {api_key}", url],
        capture_output=True, text=True
    )
    data = json.loads(r.stdout)
    for l in data.get('listings', []):
        pv = int(l['price']['current']['value'])
        dec = l['price']['current']['decimals']
        tid = l['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
        oh = l['order_hash']
        listings.append({'price': pv / 10**dec, 'tid': tid, 'order_hash': oh})
    next_cursor = data.get('next', '')
    if not next_cursor:
        break

print(f"Scanning {len(listings)} listings...\n")

# NFT詳細取得 + マッチング
found = []
for item in listings:
    r = subprocess.run(
        ["curl", "-s", "-H", f"x-api-key: {api_key}",
         f"https://api.opensea.io/api/v2/chain/matic/contract/0x251be3a17af4892035c37ebf5890f4a4d889dcad/nfts/{item['tid']}"],
        capture_output=True, text=True
    )
    clean = ''.join(c if ord(c) >= 32 or c in '\n\r\t' else ' ' for c in r.stdout)
    try:
        nft = json.loads(clean)['nft']
        name = nft.get('name', '')
        traits = {t['trait_type']: t['value'] for t in nft.get('traits', [])}
        if traits.get('Category') != 'Pokémon':
            continue
        if name in targets:
            median = targets[name]
            discount = (median - item['price']) / median * 100
            if discount >= 15:
                found.append({
                    'name': name[:70],
                    'price': item['price'],
                    'median': median,
                    'discount': discount,
                    'grade': traits.get('Grade', '?'),
                    'order_hash': item['order_hash'],
                })
                print(f"  🔥 ${item['price']:.2f} (相場${median:.2f}, -{discount:.0f}%) | {traits.get('Grade','?')} | {name[:50]}")
    except Exception:
        pass

if not found:
    print("  ターゲットカードの割安出品は見つかりませんでした")
else:
    print(f"\n=== {len(found)} 件の購入候補 ===")
    for i, f in enumerate(found, 1):
        potential = f['median'] - f['price']
        print(f"\n🔥 購入候補 #{i}")
        print(f"  カード: {f['name']} ({f['grade']})")
        print(f"  出品価格: ${f['price']:.2f}")
        print(f"  相場（中央値）: ${f['median']:.2f}")
        print(f"  割安率: -{f['discount']:.1f}%")
        print(f"  潜在利益: ${potential:.2f}")
        print(f"  order_hash: {f['order_hash']}")
PYEOF
```

### Step 3: 購入実行

ユーザーが購入を承認した場合、Part 1 Section 3 (Buy an NFT) のフローに従って実行する。

1. `order_hash` と出品の `protocol_address` を使って Fulfillment Data を取得
2. ERC20 (USDC) の approve を実行
3. ABI エンコード → dry-run → broadcast
4. 購入確認 (ownerOf)
