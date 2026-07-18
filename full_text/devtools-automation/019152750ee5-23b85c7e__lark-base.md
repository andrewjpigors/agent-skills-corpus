---
name: lark-base
description: Use when operating Feishu/Lark Base through lark-cli for table, field, record, view, formula, lookup, and data-query workflows.
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli base --help"
---

# base

> **闁告挸绉堕悿鍡涘级閳ュ弶顐介柨?* 闁稿繐鐗撳Σ鍕嫚?[`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)闁?
> **闁圭瑳鍡╂斀闁告挸绉寸换鈧柛瀣啲缁?* 闁圭瑳鍡╂斀濞寸姾顔婄紞?`base` 闁告稒鍨濋幎銈夊礈瀹ュ繒绀夐煫鍥ф嚇閵嗗繘宕楅崼銉︻潐閻犲洩顕ч顔芥償閺傛寧鍤掑ù鐘€楀▓?reference 闁哄倸娲﹂妴鍌炴晬鐏炶棄鏅欓悹瀣暟閺併倝宕ㄩ幋鎺撳Б闁?
> **闁告稖妫勯幃鏇犵棯閿曗偓閻ｉ箖鏁?* 濞寸姴鎳嶆繛鍥偨?`lark-cli base +...` 鐟滆埇鍨圭槐锟犳儍閸曨偅鍤掑ù鐘€戦埀?


## Execution-Focused Rule

For `base` workflows, optimize for correct operation selection and parameter accuracy. The AI should choose the right command family before trying to solve the business problem.

When guiding execution, make sure the result clearly states:
- whether the task is schema, records, formula, lookup, view, or query work
- which command should be used first
- which table, field, or record identifier must be confirmed before writing
- which reference doc or structure query must be read before the next mutation

## Agent 闊浂鍋婇埀顒傚枑婢х晫鎮板畝鍕┾偓搴㈡償?

1. **闁稿繐鐗嗛崹浠嬪棘椤撴繃宕查柛鏃撶磿鐞氼偊宕?*
   - 濞戞挸鐡ㄥ鍌滅磼閻旀椿鍚€ / 闁艰鲸鑹鹃幃搴ㄥ礆閸℃鈧?闁?`+data-query`
   - 閻熸洑鐒︽俊鍝ョ磼閹惧浜梻鈧幐搴㈠焸闁哄嫬澧介妵姘跺捶閵娿劊鈧啴鏌?闁?formula 閻庢稒顨嗛?
   - 闁活潿鍔嶉崺娑㈠及鎼达絺鈧鎲?lookup闁挎稑鏈崹銊ф兜椤旇偐鏉介柡鍥ㄦ尦閳ь剙鍊搁幃?`from/select/where/aggregate` 闁?lookup 閻庢稒顨嗛?
   - 闁哄嫬娴风划蹇曟嫚鐠囨彃绲?/ 閻庣數鍘ч崵?闁?`+record-list / +record-get`
2. **闁稿繐鐗婄€ｄ胶绱掗幘瀵糕偓顖炴晬鐏炶棄鏅欓柛鎰懃閹斥剝绂?*
   - 闁煎嘲鍟块惃顖炲礂閸喎鐟忕憸鐗堟尭婢х姷鎮伴妸褏娉㈤柡瀣缁辩櫗+field-list` 闁?`+table-get`
   - 閻犳亽鍔忛妴鍐捶閻戞ɑ鐝煫鍥ф嚇閵嗗繘宕樺鍡欏弨**闁烩晩鍠楅悥锝囨偘?*闁汇劌瀚划銊╁几?
3. **formula / lookup 闁哄牆顦遍垾鏍⒒閵婏富娼?*
   - 闁稿繐鐗愰鎵偓鐢垫嚀缁?guide
   - 閻犲洩顕ч悾?guide 闁告艾鍑界槐婵嬪礃瀹ュ懎鐏＄€点倕鎼顔芥償閺傝法鎽熸繛?
4. **闁告劖鐟ㄩ鍥亹閺囩偛顤呴柛蹇撶墕閸ㄤ粙寮鐐垫憻婵炲牓娼цぐ鏌ュ礃濞嗘劏鍋?*
   - 闁告瑯浜滈崯鎾垛偓娑櫭崑宥団偓娑欘殕椤?
   - 缂侇垵宕电划铏光偓娑欘殕椤?/ formula / lookup 濮掓稒顭堥濠氬矗椤忓浂鍤?

## Agent 缂佸倷鐒﹂娑氭偘鐏炶壈绀?

- 濞戞挸绉烽々锕傚箮?`+record-list` 鐟滅増鎹佹禒娑㈠触閸繂鐎婚柡瀣姇缁扁晠骞?
- 濞戞挸绉烽々锕€鈻介檱椤?guide 閻忓繗浜ú鍧楀箳閵夈儱鐏＄€?formula / lookup 閻庢稒顨嗛?
- 濞戞挸绉烽々锕傚礄椤撯€虫闁绘帗鍎奸銏㈡嚊閳ь剟鎮鍡愨偓鍐触瀹ュ啠鍋撴担鍝ユ憻婵炲牓娼ч幃鏇㈠Υ娴ｇ褰嗙€殿喖绻楅妴鍐╂綇閹呯闂佹彃鐬煎▓鎴犫偓娑欘殕椤斿苯顕ｉ弴鐘虫殢
- 濞戞挸绉烽々锕傚箮婵犲嫰鍏囩紓浣哄枎閻⊙冣枔閻愬厜鍋撴稊鐜眗mula 閻庢稒顨嗛宀勫Υ娑旂okup 閻庢稒顨嗛宀冦亹閹炬潙鐏?`+record-upsert` 闁汇劌瀚崯鎾诲礂閵壯勭獥闁?
- 濞戞挸绉烽々锕傚捶?Base 闁革妇鍎ゅ▍娆撳绩绾懓娉?`lark-cli api GET /open-apis/bitable/v1/...`
- 濞戞挸绉烽々锕傚炊閻樿精绀?wiki 閻熸瑱绲鹃悗鐣岀磼閹惧浜梺鎻掔灱濞?`obj_type=bitable` 閻忓繐宕獮鎾诲箥?`bitable.*`闁挎稒绋戝﹢顏堝嫉?CLI 闂佹彃鑻花鑼磼瑜忛悽缁樻媴鐠恒劍鏆?`lark-cli base +...`

## Base 闁糕晝鍎ゅ﹢鎷岀疀閸愨晜顏℃俊顖椻偓宕団偓?

1. **Base 閻庢稒顨嗛宀勫礆閸℃洜鐟忕紒?*
   - **閻庢稒锚閸嬪秶鈧稒顨嗛?*闁挎稒姘ㄥ﹢锛勨偓鍦仜閻°劑鎮介妸锕€鐓曢弶鍫熸尭閸欏棝鎯冮崟顒佹闁硅鍣槐婵嬫焻濮橆剛鍩楅梺顐㈠€搁幃?`+record-upsert` 闁告劖鐟ラ崣鍡涙晬鐏炶偐浼愬┑鈥冲€归弸鍐嫉椤戦敮鍋撴担瑙勬閻庢稒銇滈埀顑跨劍濡晠寮甸悢绮瑰亾娴ｇ绀嬮梺顐㈩槶閳ь兛绀侀ˇ鍧楁焻婢跺牃鍋撴担閿嬬溄闁告稒菧閳ь兛绀侀崣褔鎳曢弬鐑╁亾?*闂傚嫬瀚▎銏⑩偓娑欘殕椤斿本绗熺€ｎ亶妯?*闁挎稒鑹鹃?agent 闁兼澘鐭侀埢鍫ユ晬鐏炵偓鐎ù鐘虫构缁楀倹瀵奸悩鑼畱濡炪倖妲掗摂?`+record-upload-attachment`闁?
   - **缂侇垵宕电划铏光偓娑欘殕椤?*闁挎稒鑹鹃柦鈺呭矗閹峰苯娈伴柛鏂诲妿濞ｎ噣骞庨妶蹇曠闁告瑯浜ｉ浼存晬鐏炶棄鎮侀柛銊ヮ儏鐎垫﹢骞忛鈧崹鍗烆嚈閻戞ɑ顦ч梻鍌涚暘閳ь兛鐒﹀〒鍫曞触鎼淬垺绾柡鍌滃濡炲倿姊诲ǎ顑藉亾娴ｇ鐏＄€点倛妗ㄥЧ澶愬Υ娴ｉ攱鍙忛柡鈧柅娑欑溄闁靛棔娴囬崵婊堝礉閵娧呮そ闁告瑦鐏氶埀?
   - **閻犱緤绱曢悾鑽も偓娑欘殕椤?*闁挎稒宀搁埀顒佷亢缁诲啰鎮伴妸銊﹀涧鐎殿喖绻戦崹銊ф崉閵娿劊鈧啰鎲撮崟顐㈢仧闁规亽鍔岄閬嶆晬鐏炶棄娑ч悹鍥︾串缁辨繈宕楃粙璺ㄢ偓鐑藉礌閸涱喖顏?**闁稿浚鍓欑槐锛勨偓娑欘殕椤斿矂鏁嶉崸鎶﹔mula闁?* 闁?**闁哄被鍎叉竟妯侯嚕閺囩姵鏆忛悗娑欘殕椤斿矂鏁嶉崸妾昽kup闁?*闁?
2. **闁告劖鐟ㄩ鍥亹閺囩偛顤呴柛蹇撶墕閸ㄤ粙寮鐐垫憻婵炲牏鏁哥悮顐﹀礆?* 闁?闁告瑯浜濆﹢浣衡偓娑櫭崑宥団偓娑欘殕椤斿矂宕ｉ婊勭函闁规亽鍎遍崯鎾绘晬濞戞ê褰嗙€?/ lookup / 闁告帗绋戠紓鎾诲籍閸洘锛?/ 闁哄洤鐡ㄩ弻濠囧籍閸洘锛?/ 闁告帗绋戠紓鎾寸?/ 濞ｅ浂鍠楅弫鍏肩?/ 闁煎浜滄慨鈺冪磽閺嵮冨▏闂侇喛妫勭花鑼喆閸℃洝绀嬮柛娆樹海椤曠増娼忛幘鍐叉瘔閻庢稒顨嗛宀勬晬鐏炶偐鐟濋柤瀹犲Г鐎ｄ線寮堕妷銉ょ驳 `+record-upsert` 闁稿繈鍎卞顒勫Υ?
3. **Base 濞戞挸绉磋ぐ褔寮伴姘辨憼閻炴稏鍔嶉弳鐔煎箲椤曞棛绀夊☉鏃傚枙閸忔﹢宕橀崨顓犵处閻犱緤绱曢悾?* 闁?闁活潿鍔嶉崺娑㈠箵閹邦剙姣夐柍銉︾矌缁櫣鎷嬫幊閳ь兛鐒﹂惁顔芥綇閸愶腹鍋撴担鐟扮瑩闁告艾绉查埀顑跨劍閺嬪啴寮甸浣割伝闁规亽鍎埀顑跨劍濡晠寮甸悢閿嬧枙闁靛棔娴囧▔鏇犳偘閵婏妇婀介柟顒佺湽閳ь兛鑳舵慨鎼佸箑娴ｇ鐏查柡鍌ゅ幐閳ь剚绻勯悺鎴︽閳ь剙效閸屾稒顦ч柨娑樺缁楀鎳楁禒瀣笡閻犱降鍊曢閬嶅礄閻戞ɑ娈堕柟璇″枛閹骞嶇€ｎ剛鏆柨娑欑椤╋箓宕楅崼婵嗙伈闁哄偆鍘藉Σ鎼佸触閿曗偓缁ㄦ煡鏌呭宕囩畺 `+data-query` 闁瑰瓨鐗曢崣鏇烆嚕韫囨挾鎽熸繛鍫ユ涧濠€?Base 闁告劕鎳庨悾顒勫箣閹扳斁鍋?

## 闁告帒妫欓悗鐣屾崉椤栨氨绐為柛鎰－閻?

1. **濞戞挴鍋撴繛鍡忓墲閳ь儸鍐ㄧ€婚柡?/ 濞戞挸鐡ㄥ鍌炲蓟閵夘煈鍤?* 闁?濞村吋锚閸?`+data-query`
   - 闂侇偄鍊搁幃搴ㄦ晬濮橆剙鐎荤紓浣稿缁櫣鎷嬫幊閳ь兛璁M / AVG / COUNT / MAX / MIN闁靛棔鐒﹀顖涚閸撲胶鎽ｉ梺顐㈩槸閹鎳曞顒佸€ら柕?
   - 闁绘鎳撶欢娑㈡晬濮樻剚娲ｉ柣銊ュ濡叉悂鍨惧鍡欑婵炲棴绱曢悾濠氬礄閻戞ɑ闄嶉柣銊ュ缁劑寮稿┃閿亾濠垫挾绀夊☉鎾崇У濡叉悂骞庢繝鍕尝闁哄绮嶉惌鍥庨埀顒勫箣閹邦垬鈧啴宕橀崨顓犳憻婵炲牏鍋ｉ埀?
2. **闂傗偓閹稿孩鍩傚璺虹Ф閺併倝鎯冮崟顒佺儲闁汇垻鍠愮€垫岸寮?/ 閻炴稑鐬兼鍥╂媼閿涘嫮鏆紓浣规尰閻?* 闁?濞村吋锚閸樻盯宕楅鈧槐锛勨偓娑欘殕椤?
   - 闂侇偄鍊搁幃搴ㄦ晬濮橆剙鐒烘繛鎴瀹稿ジ濡存担瑙勑﹂柛姘剧畱濞嗐垽寮甸悢绮瑰亾娴ｇ鈷栧ù锝嗙懃閵囧寮懜顑藉亾娴ｇ鐎绘俊妤嬬稻閻栵絿绮垫穱鎵佸亾娴ｈ姤纭堕悶娑栧妽閻綊骞€鐠囧弶鍊甸柣銊ュ濞ｆ娊鎮介悢铏规尝闁哄鍤庨埀?
   - 闁绘鎳撶欢娑㈡晬濮樻剚娲ｉ柟璺猴功缁劑寮稿鍫熸瘣闁哄牏鍠愬Ο澶岀矆閸濆嫭韬?Base 闂佹彃鐭夌槐婵堟崉閻斿吋顓归悹浣规緲缂嶅秹鎳涢鍕楅柡鍥х摠閺屽﹪濡?
3. **闁哄嫭鍎崇槐锛勬啺娴ｅ湱婀?Lookup闁挎稑鏈崹銊ф兜椤旇偐鏉介悷鏇氱劍鐎?source/select/where/aggregate 鐎点倗鍎よ啯** 闁?闁?lookup 閻庢稒顨嗛?
   - 濮掓稒顭堥缁樼瀹ュ嫮鍠橀柛蹇撶墣閳ь剙鍟冲?formula闁靛棔搴穙okup 闁告瑯浜滃﹢顏堟偨閵婏箑鐓曢柡鍕捣閳ユ鎲版担鍦勾闁靛棔鐒﹂崹銊╁即鐎靛壊鍎婇柛姘墕濞存劗鈧纰嶉悡锟犲箥妤ｅ啫甯崇紓鍐惧枟濡炲倹鎷呯捄銊︽殢闁?
4. **闁告鍠庨～鎰媼閺夎法绉块悹鍥嚙瑜?/ 闁哄嫬娴风划蹇曗偓鐢靛帶閸?* 闁?`+record-list / +record-get`
   - 濞戞挸绉烽々锕傚箮?`+record-list` 鐟滅増鎸搁崹搴ㄥ几閹邦剛绌块柟鍨嚱缁辫京鈧懓鍟崇粈瀣嫻閿濆懎绲块柡鍕捣缁繘鏁嶇仦鑲╃憹閻犳劗鍠曢惌妤呮嚂濮橆剚鍊ら悹渚婄磿閻ｅ濡?

## 闁稿浚鍓欑槐?/ Lookup 濞戞挻鎹囬妴宥囨喆閸曨偄鐏?

1. **婵炴垵顦?formula / lookup 闁哄啳顔愮槐婵嬪礂閸綆鍤?guide闁挎稑鑻崯鈧柛鎴濇惈閹斥剝绂?*
   - formula闁挎稒鐡焋formula-field-guide.md`](references/formula-field-guide.md)
   - lookup闁挎稒鐡焋lookup-field-guide.md`](references/lookup-field-guide.md)
2. **guide 闁稿繐鐗呯花顒勫礆濞戞绱﹂柛娑欏灊閹?*
   - 婵炲眲銈庡殺閻庣數鎳撶花?guide 闁告挸绋勭槐婵囩▔瀹ュ牜娲ｉ柣鈺佺摠鐢挳宕氬☉妯肩处 formula / lookup 閻庢稒顨嗛?
   - 閻犲洩顕ч悾?guide 闁告艾鍑界槐婵嬪礃瀹ュ煻澶嬵瀲閹邦剦鍤犻幖?JSON 妤犵偠娉涢崹鍗烆嚈閸濆嫮鎽熸繛?
   - `type=formula` 闊洤鎳橀妴蹇涘箵閹邦亞杩?`expression`
   - `type=lookup` 闊洤鎳橀妴蹇涘箵閹邦亞杩?`from / select / where`闁挎稑鑻换鈧悷鏇氱劍濡炲倻鎮?`aggregate`
3. **闁稿浚鍓欑槐锛勨偓娑欘殕椤斿本瀵煎Ο鍝勫弗濞?lookup 閻庢稒顨嗛?*
   - 闁告瑯浜ｉ々锕傛偨閵婏箑鐓曢柣銊ュ閻︽柨效閸屾稒笑闁炽儲绮忛鍝ョ不?/ 闁哄鈧弶顐介柛鎺嬪€栭弻?/ 闁哄倸娲﹀﹢鐗堝緞閸曨厽鍊?/ 闁哄啨鍎插﹢鈥愁啅?/ 閻犳亽鍔忛妴鍐嚂濮橆剚鍊?/ 閻犳亽鍔忛妴鍐驳濞戔懇鍋撴径濠冨€甸柛娆愮墪閳ь剙鐨烽埀顒佺箰缁辨繃顪€濡鍚囧ù鍏济崢娑氫焊濠靛﹦妲?formula闁?
   - 闁告瑯浜濆﹢渚€鎮介妸锕€鐓曢柡鍕捣閳ユ鎷犵壕瀣垫矗 lookup闁挎稑鏈崹銊╂煀瀹ュ洨鏋傚鍨涙櫇閸斞囧即閹绢喒鍋撻崒姘€?lookup 闁搞儲绋戦崢鎾剁磼閸曨剚顦ч柨娑樿嫰閸熲偓閻?lookup闁?
4. **閻炴稏鍔岄幃?/ 閻庢稒顨嗛宀勫触瀹ュ懐绠戝銈堝吹缁ㄨ法娑甸鐓庣埍闂?*
   - 闁稿浚鍓欑槐锟犲Υ娑旂okup闁靛棔榫歛ta-query 濞戞搩鍘奸崵顓㈡偝閹殿喗鐣遍悶娑栧妼閹?/ 閻庢稒顨嗛宀勫触瀹ュ繒绀夐煫鍥ф嚇閵嗗繘寮堕妷銊ユ `+table-list` / `+table-get` / `+field-list` 闁汇劌瀚﹢锛勨偓鍦仩缁绘垿宕堕悜鍥╃缂佸倷鐒﹂娑㈠礄椤撯槅鍤斿☉鏂款槺鐎佃棄霉鐎ｎ偅鏆柛鎰懀閳?
5. **闁稿繐鐗婄€ｄ胶绱掗幘瀵糕偓顖炲礃瀹ュ懎鏅搁悶娑栧姀閹活亜顕?*
   - 闁稿浚鍓欑槐锟犲箣?lookup 濞戞挴鍋撶€垫澘顑呴崢娑㈡嚔瀹勬澘绲块柣鈺冾焾閸櫻呮偘閵娧呮尝闁哄瀚哥槐婵嬪礃瀹ュ洦鏅搁柟瀛樺姌閵嗗啯娼忛幆褏纭€ / 闂佹澘绉堕悿鍡涙晬濞戞鐟濋悷鏇氳兌濞插潡骞掗妷銉ユ闁活潿鍔嶉崺娑㈠矗閿濆牆鐗氶柟椋庡帶閻⊙冣枔闂堟稒鍊抽柕?

## Workflow 濞戞挻鎹囬妴宥囨喆閸曨偄鐏?

1. **闁圭瑳鍡╂斀濞寸姾顔婄紞?workflow 闁告稒鍨濋幎銈夊礈瀹ュ繒绀夐煫鍥ф嚇閵嗗繘宕楅崼锝庡殺濞戞挶鍊撻崬銈夊棘閸ャ劊鈧倿鏁嶅顒夊殸閹煎瓨姊诲▓鎴﹀川閹存帗濮㈤柡鍌氭处閵?+ [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md)**
   - `+workflow-create` 闁?闁稿繐鐗愰?[lark-base-workflow-create.md](references/lark-base-workflow-create.md) + schema
   - `+workflow-update` 闁?闁稿繐鐗愰?[lark-base-workflow-update.md](references/lark-base-workflow-update.md) + schema
   - `+workflow-list` 闁?闁稿繐鐗愰?[lark-base-workflow-list.md](references/lark-base-workflow-list.md) + schema
   - `+workflow-get` 闁?闁稿繐鐗愰?[lark-base-workflow-get.md](references/lark-base-workflow-get.md) + schema
   - `+workflow-enable` 闁?闁稿繐鐗愰?[lark-base-workflow-enable.md](references/lark-base-workflow-enable.md) + schema
   - `+workflow-disable` 闁?闁稿繐鐗愰?[lark-base-workflow-disable.md](references/lark-base-workflow-disable.md) + schema
   - schema 濞戞搩鍘奸悾鐐▕婢跺鍟婇柟纰樺亾闁?StepType 闁哄鐭俊鍥Υ娴ｈ鍔勫Δ鐘€楃划銊╁几閸曗斁鍋撴稊鈧瑀igger/Action/Branch/Loop 闁?data 闁哄秶鍘х槐锟犲Υ娴ｇ硶鍋撻悡搴ｇ┛闁活潿鍔忛銏犫枖閺囩姷鎼?
   - 缂佸倷鐒﹂娑㈠礄椤撯€虫闁绘帗鍎奸銏㈡嚊閳ь剟鎮鍕偞 `type` 闁稿﹦銆嬬槐娆愪繆閸屾稑惟"闁哄倹婢橀·鍐媼閺夎法绉?闁绘碍绮嶉崹?`CreateTrigger`闁挎稑顧€缁辨繆绠涢崨娣偓蹇旂?schema 闁?StepType 闁哄鐭俊鍥ㄧ▔椤撶儐妲婚柛鎺曟硾閸ｎ垳娑甸鐐暠缂侇偉顕ч悗鐑藉触瀹ュ泦?

2. **闁告帗绋戠紓鎾诲礈瀹ュ洠鈧鎷嬮妶鍕穿閻犙勭墧娣囧﹪骞?*
   - 闁稿繐鐗撻埀顒佷亢缁?`+table-list` / `+field-list` 闁兼儳鍢茶ぐ鍥儑閻旈鏉介柣銊ュ閵嗗啴宕ュ鍐ｅ亾娴ｅ摜鎽熸繛鍫ユ涧閹?
   - 缂佸倷鐒﹂娑㈠礄椤撯€虫闁绘帗鍎奸銏㈡嚊閳ь剟鎮鍕偞閻炴稏鍔岄幃?閻庢稒顨嗛宀勫触瀹ュ拑缍栭柛?workflow 闂佹澘绉堕悿?

## 闁哄秶顭堢缓鍓ф喆閸曨偄鐏?

1. **闁告瑯浜欐繛鍥偨閵娿儱鏂ч悗娑欏姇閹斥剝绂?* 闁?濞达綀娉曢弫?`+table-list / +table-get / +field-create / +record-upsert / +view-set-filter / +record-history-list / +base-get` 閺夆晜鐟х悮顐ｇ▔閳ь剟宕ㄩ幋鎺撳Б濞戞挴鍋撻柛鏂诲妺缂嶆棃鎯冮崟顐㈡櫢婵炲娲╃槐婵囩▔瀹ュ嫬鈻忛柣顫妽濡偊鎳曞顒佸€ょ€?`+table / +field / +record / +view / +history / +workspace`
2. **闁告劖鐟ㄩ鍥亹閺囩偛顤呴柛蹇撶墣椤曟壆鈧稒顨嗛宀€绱掗幘瀵糕偓?* 闁?闁稿繐鐗愰惃鐔兼偨?`+field-list` 闁兼儳鍢茶ぐ鍥┾偓娑欘殕椤斿瞼绱掗幘瀵糕偓顖炴晬鐏炶棄鏅欓悹?[lark-base-shortcut-record-value.md](references/lark-base-shortcut-record-value.md) 缁绢収鍠涢濠氬触閸曨偆鎽熸繛鍫㈡暩鐞氼偊宕圭€ｎ剚鐣遍柛鎰懃閸欏棝宕愰崗鑲╁鐎?
3. **闁告劖鐟ラ悺褍鈻撻棃娑橆枀闁稿繐鐗忓﹢鍛偓娑欘殕椤斿瞼浠﹂悙绮瑰亾瑜戦～澶愭嚑?* 闁?闁稿繐鐗愰?[lark-base-shortcut-field-properties.md](references/lark-base-shortcut-field-properties.md) 缁绢収鍠涢?`+field-create/+field-update` 闁?JSON 缂備焦鎸婚悗?
4. **缂佹稒鐩埀顒€顦伴悡锛勬嫚閵忊€崇樆閻熸瑥妫楀ù姗€鎳楅挊澶婎潝闁圭瑳鍡╂斀** 闁?闁稿繐鐗愰?[lark-base-view-set-filter.md](references/lark-base-view-set-filter.md) 闁?[lark-base-record-list.md](references/lark-base-record-list.md)闁挎稑鐭傞埀顒佷亢缁?`+view-set-filter` + `+record-list` 缂備礁瀚幃搴ｂ偓鐟版湰閸ㄦ氨绮靛☉鈶╁亾婢跺寒鍤㈤柛?
5. **閻庣數顢婇鍥亹閺囷紕绠婚悶娑樿嫰閸ㄥ酣寮搁幇鍓佺婵炴垵顦?闁哄牃鍋撳Δ?闁哄牃鍋撳ù?闁诡剚妲掗?妤犵偛鍟垮?闁圭儤甯掗幃?婵絾妫佺欢?闁轰椒鍗抽崳?缂佹稑顦崹搴ㄥ几閹邦厼澹堥柛銉︽嫕缁?* 闁?闁稿繐鐗愰?[lark-base-data-query.md](references/lark-base-data-query.md)闁挎稑鐭傞埀顒佷亢缁?`+data-query` 閺夆晜绋栭、鎴﹀极閻楀牆绁︾紒娑欑洴閳ь剙顦虫禒娑㈠触閸垺鐣遍柡鍫濈Т婵喓绮╅婵愬悁缂?
6. **闁艰鲸鑹鹃幃搴ㄥ礆閸℃鈧姤绋夋惔鈥崇悼闁轰線顣︾花浼村棘?* 闁?闂傚洠鍋撻悷鏇氱閸ㄥ海绱掗崟顓犲煚閻?/ SUM / MAX / AVG / COUNT 闁哄啳顔愮槐婵婄疀閸涙番鈧繑鎷呯捄銊︽殢 `+data-query`闁挎稑鐗婂﹢鍥礉閿涘嫷浼傞悹渚婄磿閻ｅ鏁嶆径娑氱缂佸倷鐒﹂娑㈡偨?`+record-list` 闁瑰嘲顦崣蹇涙煂韫囨凹鍞剁憸鐗堟礀閸熲偓闁归潧顑呮慨鈺冩媼閿涘嫮鏆柨娑欑☉瀵姤绋婄€ｅ墎绀塦+data-query` 濞戞挸绉风换鎴﹀炊閻愭彃鏂у┑顔碱儓椤斿洩銇愰弴顏嗙闁告瑦鐗楅弳鐔煎捶閻戞ɑ鐝ù鐘茬Х閾?`+record-list / +record-get`
7. **闁圭鍋撻柡?`+xxx-list` 缂佸倷鐒﹂娑㈢嵁鐠哄搫绲洪悹瀣暟閺?* 闁?`+table-list / +field-list / +record-list / +view-list / +record-history-list / +role-list` 闁告瑯浜ｉ崗妯荤▔閼奸鏀介柟绗涘棭鏀?
8. **闁归潧缍婇崳鐑樼▔婵犲洦顎?500 闁?婵?* 闁?闁告艾濂旂粩瀵告偘閵娿儳绱﹂悹渚囧枙鐟曞棛鎮扮仦钘夋櫢闁稿繈鍎荤槐婵嬬嵁鐠虹儤韬柟浣冾潐椤愬ジ姊婚弶鎴烆偨閺?0.5闁? 缂?
9. **缂備胶鍠嶇粩鎾矗閸屾稒娈堕柛?* 闁?濞戞挴鍋撶€垫澘顑勬繛鍥偨?`--base-token`闁挎稑濂旂粭澶嬫媴鐠恒劍鏆忛柡?`--app-token`
10. **闂侇剙娲ら崺宀勫灳濠婂啫褰嗙€?/ 闁哄被鍎叉竟妯侯嚕閺囩姵鏆?/ 婵炴彃澧介弫鎾诲箰閸ャ劎鍨?/ 閻犳亽鍔忛妴鍐媼閿涘嫮鏆柍銉︾箞濞撹泛效閸岋妇绀夊ù鍏济崢娑氭導閺夎法鎽熸繛鍫濈仛閺岀喎顩奸崼婵嗙伈闁?* 闁?闁稿繐鐗嗛崹浠嬪棘椤撶偟瀹夌€?formula / lookup 閻庢稒顨嗛宀勬晬瀹€鍐闁哄嫷鍨拌ぐ褔宕戝顐ゎ伇婵炲棌鍓濋埀?`+data-query`
11. **闁稿浚鍓欑槐锟犲Υ娑旂okup闁靛棔鑳堕柈瀵哥磼閻旈鎽熸繛鍫㈡暬缁垳鎷嬮妶鍫綊濞戞挸鎼ぐ褏鎷?* 闁?闂?`+field-create / +field-update` 缂備礁鐡ㄦ慨銏⑩偓娑欘殕椤斿瞼鈧鐭粻鐔稿緞閺嶇數绀夊☉鎾崇Х椤╋箓骞庢繝鍛濞存粍绋戦悺褍鈻撻崗鍝ョ▕濞戞捇缂氶鍥亹閺囩偛鏅搁柛蹇嬪劤濞蹭即寮?
12. **闁衡偓閻熺増鍊抽柛婊冭嫰閸ㄥ綊姊介妶鍡楃樆闁哄嫬娴烽垾姗€骞囪箛鎾寸闁圭瑳鍡╂斀** 闁?`+view-rename` 闁革负鍔庡ú浼村冀閸ヮ亶娼掗柛銉﹀劤閹蜂即寮弶鎸庡€崇紒澶夊嵆閸忔﹢寮版惔锝傗偓姗€寮捄鍝勮闁烩晛鐡ㄧ敮鎾箥瑜戦、鎴︽晬濞?record-delete / +field-delete / +table-delete` 闁革负鍔庨弫銈夊箣瀹勬澘鍤掔紓浣哥箲濡叉垹娑甸娆炬矗婵懓鍊搁崹褰掓⒔閵堝嫮鐟柣鈺婂枟閻栵綁寮版惔锝傗偓姗€寮張鐢电槏闁告瑯鍨冲ú鍧楀箳閵夛箑鈷旈悶娑樼焿缁辨繃绋夊澶嬩粯閻熸洑绀侀崯鈧悶娑栧劙缁旀潙鈻庨敍鍕ㄢ偓妯兼媼閵堝繒绀夋鐐存构缁楁牠骞嶈椤㈡垿宕氶悩缁樼彑闁告稒鍨濋幎銈夊籍閹偊娲ｅ☉鎾诡嚙婵晝鎮伴妷銈囩憪 `--yes`闁挎稒绋戣ぐ褔寮垫径灞剧獥闁哄秴娲ｇ粭澶愬及鎼达絺鈧﹢寮懜闈涱枀缂備綀鍛暰閺夆晙绮欏Λ?

## 闂傚偆鍠栧畵?/ 閻炴稏鍔屽畷鐔煎箵閹邦喓浠?

- **闁兼儳鍢茶ぐ鍥⒒椤旂厧绁归柛鎺擃殙閵?*闁挎稒鐭繛鍥偨?`+form-list`闁挎稑鐗嗛崢娑㈠箯?`form-id`闁?
- **闁兼儳鍢茶ぐ鍥础閺囨岸鍤嬮梻鍌ゅ枛瀹?*闁挎稒鐭繛鍥偨?`+form-get`
- **闁兼儳鍢茶ぐ鍥╂偘閵娿儱绀?/ 闂傚偆鍠栧畵搴ㄦ⒒椤曗偓椤?*闁挎稒鐭繛鍥偨?`+form-questions-list`
- **闁告帞濞€濞呭酣姊婚鐓庣ス / 閻炴稏鍔屽畷鐔兼⒒椤曗偓椤?*闁挎稒鐭繛鍥偨?`+form-questions-delete`
- **闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻濠囨⒒椤曗偓椤?*闁挎稒鐭繛鍥偨?`+form-questions-create / +form-questions-update`

## 闁规澘绻愬ù?闁?闁告稒鍨濋幎銈囨閵忕姷绌?

| 闁规澘绻愬ù?| 闁规亽鍔忓畷姗€宕ㄩ幋鎺撳Б | 濠㈣泛娲﹂弫?|
|------|---------|------|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥极閻楀牆绁﹂悶?| `lark-cli base +table-list` / `+table-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭酣寮悧鍫濈ウ閻?| `lark-cli base +table-create` / `+table-update` / `+table-delete` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥┾偓娑欘殕椤?| `lark-cli base +field-list` / `+field-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻濠勨偓娑欘殕椤?| `lark-cli base +field-create` / `+field-update` | 濞达綀娉曢弫?`--json` |
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻濠囧礂椤掆偓缁憋紕鈧稒顨嗛?| `lark-cli base +field-create` / `+field-update` | `type=formula`闁挎稒绋戦崢娑氭嫚?formula guide闁挎稑鑻崯鈧柛鎺撶☉缂?/ 闁哄洤鐡ㄩ弻?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?lookup 閻庢稒顨嗛?| `lark-cli base +field-create` / `+field-update` | `type=lookup`闁挎稒绋戦崢娑氭嫚?lookup guide闁挎稑鑻崯鈧柛鎺撶☉缂?/ 闁哄洤鐡ㄩ弻濠囨晬瀹€鍕笡閻犱降鍊曢崢娑㈠礆閵堝棙鐒?formula 闁哄嫷鍨伴幆渚€寮撮弶鎴炲€ら梺?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥╂媼閺夎法绉?| `lark-cli base +record-list` / `+record-get` | 闁告鍠庨悺娆撳川閹存帗濮㈤柨娑樿嫰椤┭囧几濠婂牊浠橀悷鏇氭闁艰鲸鑹鹃幃搴ｆ媼閿涘嫮鏆琡闁挎稑鐣柛鎺戞缁秶绱掗悢娲诲悁` 闁规亽鍔忓畷妯兼導?`+data-query` |
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻濠勬媼閺夎法绉?| `lark-cli base +record-upsert` | `--table-id [--record-id] --json` |
| 闁艰鲸鑹鹃幃搴ㄥ礆閸℃鈧?/ 婵絾妫佺欢婵嬪箳閹烘垹纰?/ 婵懓鍊瑰〒鍫曞磹?/ 缂佹稒鐩埀顒€顦辩划铏规媼?| `lark-cli base +data-query` | 濞戞挸绉烽々锕傛偨?`+record-list` 闁瑰嘲顦崣蹇涙煂韫囨梹娈堕柟璇″枛閸熲偓闁归潧顑呮慨鈺冩媼閿涘嫮鏆柨娑樼焸濞撹埖鎷呯捄銊︽殢 `+data-query` 閻犙呭濠€鍥礉閿涘嫷浼傞悹渚婄磿閻?|
| 闂佹澘绉堕悿?/ 闁哄被鍎撮妤冩喆閸℃绂?| `lark-cli base +view-*` | `list/get/create/delete/get-*/set-*/rename` |
| 闁哄被鍎冲﹢鍛媼閺夎法绉块柛妯烘瑜?| `lark-cli base +record-history-list` | 闁圭顦抽妴鍐椽瀹€鍐惧敹鐟滅増娲橀悡锛勬嫚閵忕姴缍侀柡鍥ㄦ綑瀹稿宕?|
| 闁圭顦抽～瀣炊閸撗呮懀闂侇偄顦伴悡锛勬嫚?| `lark-cli base +view-set-filter` + `lark-cli base +record-list` | 缂備礁瀚幃搴ｆ嫬閸愵亝鏆?|
| 闁告帗绋戠紓?/ 闁兼儳鍢茶ぐ?/ 濠㈣泛绉撮崺?Base | `lark-cli base +base-create` / `+base-get` / `+base-copy` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥ь啅閵夈倗绋婃繛?| `lark-cli base +workflow-list` / `+workflow-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻濠傤啅閵夈倗绋婃繛?| `lark-cli base +workflow-create` / `+workflow-update` | 濞达綀娉曢弫?`--json`闁挎稑鑻换鈧銈咁煼濡插嫮鎷?schema |
| 闁告凹鍨抽弫?/ 闁稿绮庨弫銈咁啅閵夈倗绋婃繛?| `lark-cli base +workflow-enable` / `+workflow-disable` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|
| 闁告凹鍨抽弫?/ 闁稿绮庨弫銈嗩殗濡ジ鐛撻柡澶婂暣濡?| `lark-cli base +advperm-enable` / `+advperm-disable` | 闁告凹鍨抽弫銈夊触鎼淬垹顤呴柤铏灊婵炲洭鎮介妸銊ユ閻庤鐭粻鐔烘喆閹烘洖顥忛柨娑欑☉娴犵娀鎮介妸銈囩獥濞达絽鐏濋崙锟犲嫉婢跺寒娼￠柤瑙勫絻閵囨垿寮?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥╂喆閹烘洖顥?| `lark-cli base +role-list / +role-get` | 闁哄被鍎冲﹢鍛喆閹烘洖顥忛柟鑺ヮ焾椤╋箓骞嬮弽褏鏆氶柡浣规尦閸樸倗绱?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭海鎲撮幒鏇烆棌 | `lark-cli base +role-create / +role-update / +role-delete` | 缂佺媴绱曢幃濠囨嚊椤忓嫮鏆板☉鏂款槼椤鎳濋崣澶嬬秬闂?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥╂偘閵娿儱绀?| `lark-cli base +form-list` / `+form-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭海鎮伴妸銉ョ | `lark-cli base +form-create` / `+form-update` / `+form-delete` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|
| 闁告帗顨夐妴?/ 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭海鎮伴妸銉ョ闂傚偆鍣ｉ。?| `lark-cli base +form-questions-list` / `+form-questions-create` / `+form-questions-update` / `+form-questions-delete` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥ㄧ椤忓洢鈧啴鎯?| `lark-cli base +dashboard-list` / `+dashboard-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭孩绂掗鍥モ偓鍐儎?| `lark-cli base +dashboard-create` / `+dashboard-update` / `+dashboard-delete` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|
| 闁告帗顨夐妴?/ 闁兼儳鍢茶ぐ鍥ㄧ椤忓洢鈧啴鎯?Block | `lark-cli base +dashboard-block-list` / `+dashboard-block-get` | 闁告鍠庨悺娆撳川閹存帗濮?|
| 闁告帗绋戠紓?/ 闁哄洤鐡ㄩ弻?/ 闁告帞濞€濞呭孩绂掗鍥モ偓鍐儎?Block | `lark-cli base +dashboard-block-create` / `+dashboard-block-update` / `+dashboard-block-delete` | 濞戞挴鍋撻柛娑欏灊閹躲倖绋夐埀顒勫礉閵娿倗绋?|


## 闁瑰灝绉崇紞鏂库枖閵婏箑澹堝ù婊冾儔閵?

- **Base token 闁告瑱绲界欢鐐电磼閻斿墎顏?*闁挎稒姘ㄧ划鐑樼▔閳ь剚鎷呯捄銊︽殢 `--base-token`
- **`+xxx-list` 閻犲鍟伴弫銈囩棯椤忓嫮浼?*闁挎稒鐡?table-list / +field-list / +record-list / +view-list / +record-history-list / +role-list / +dashboard-list / +dashboard-block-list / +workflow-list` 缂佸倷鐒﹂娑㈢嵁鐠哄搫绲洪悹瀣暟閺併倝鏁嶅☉娆忣棗闂佹彃绻戞晶鐣屾偘鐏炵偓顦ч柛娆樹海閸忔ɑ绋夐懠棰濇斀
- **`+record-list` limit 濞戞挸锕?*闁挎稒鐡?-limit` 闁哄牃鍋撳?`200`闁靛棗鍊垮〒鍓佹啺娴ｈ绾鑸电閺嗙喖骞戦鑺ヮ槯闊洤鎳橀妴蹇涙偨閵娿儱鐎诲銈囶暜缁辨獋offset` 闂侇偅甯掗·鍐晬婢跺﹤鐎婚柟浣冾潐婵椽宕ｉ弽鐢电缂佸倷鐒﹂娑㈠础閺囩噥鍋уù鑲╁Ь缁夊瓨娼?`200`
- **閻庢稒顨嗛宀勫矗椤栨艾鏅搁柟顑啫甯ラ柛鎺嬪€栭弻?*闁挎稒鑹鹃悺銊╁磼閵娿儳鎽熸繛鍫濈仛婢х娀宕ｉ姘櫢闁挎稒绋戦崣鏇烆嚕?/ lookup / 缂侇垵宕电划铏光偓娑欘殕椤斿本顪€濡鍚囬柛娆樹海椤曚即鏁嶇仦钘夋櫢閻犱焦婢樼紞宥夊籍鐠鸿櫣瀹夐悹鍝勭枃缁?
- **闁稿浚鍓欑槐锟犳嚄閽樺顫旈悷鏇氭鐎靛矂宕濋妸锕€鍘掗柛?*闁挎稒姘ㄩ弫銈夊箣閻ゎ垼鍤涢柍銉︾矌閻ｇ粯绋夐埀顒佺▔鐎Ｑ€鍋撳┑鍐ｅ亾濠婂懏鏅搁柟瀛樺姈閻栵絿绮甸柨顖楀亾濠靛啠鍋撳鍐ㄧ伈闁哄偆鍘藉Σ鎼佸触閿曗偓缁辨挾鏁化鏇楀亾濠靛啠鍋撳鍡樼《閻炴稏鍔嶉惇褰掑箑閻戔斁鍋撳┑鍐ｅ亾濠婂嫬鐦婚柡鍐﹀劜濠€鈥愁啅椤曗偓椤ｂ晝鎷冮敂鍏夊亾濠靛洦顦ч柨娑樼焷椤╋箓宕楅崼婵嗙伈闁哄偆鍘藉Σ鎼佸触閿曗偓缁ㄨ尙鎷犻妷銉х处闁稿浚鍓欑槐锛勨偓娑欘殕椤斿矂鏁嶅畝鍐ｅ亾鐏炶偐鐟濋柡鍕靛灠瑜把勬交閺傛寧绀€闁归潧顑呮导鎰板礆閸℃鈧粙寮憴鍕垫敵
- **lookup 濞戞挸绉靛Σ鍛婎渶濡鍚囧Λ锝嗙墵閳?*闁挎稒顒okup 闁告瑯浜滃﹢顏堟偨閵婏箑鐓曢柡鍕捣閳ユ鎲版担鍦勾闁瑰瓨鐗滈垾妯尖偓鍦仦濞插潡鏌呴崒姘€ら柛銉ユ惈閻ｉ箖寮婚妷锕€顥濇俊顖椻偓宕団偓鐑藉籍閺堥潧鈻忛柣銏╃厜缁辫京鏁宀婃綈閻犱緤绱曢悾濠氬Υ娴ｈ姤纭堕悶娑栧姀娴犳盯宕ラ崼婵囧闁哄鈧弶顐介柛鎺嬪€栭弻鍥ㄥ濡搫甯?formula
- **闂傚嫬瀚▎銏⑩偓娑欘殕椤?*闁挎稒鑹鹃々褔寮稿鍛殢闁瑰鏌夐々锕傚灳濠娾偓缁楀倹瀵奸悩缁橆€嶅ù?/ 缂備焦鐟ㄩ鍥亹閺囩偛顫ｉ柡鍌氭矗濞嗐垽鍨惧┑鎾剁闁告瑯浜ｉ崗妯兼導?`+record-upload-attachment` 閺夆晜鐟﹀顖炴煣閹规劗鐔呴柨娑樼墣椤曟壆鈧稒顨嗛?闁?閻犲洦妲掗鍥亹?闁?濞戞挸锕ｇ槐鍓佹閻樿櫕缍?闁?闁搞儳鍋涢崯鎾舵媼閺夎法绉块柨?
- **濞存粌鎼幉宕団偓娑欘殕椤?/ 闁活潿鍔嶉崺娑氣偓娑欘殕椤?*闁挎稒淇洪惃鐔烘嫚閺囩喐顦ф繛澶堝妽閸?`user_id_type` 濞戞挸瀛╂晶鐣屾偘瀹€鍐叐濞寸姵鏋荤槐妾渟er / bot闁挎稑顦Ο濠傤嚕?
- **history 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鐡?record-history-list` 闁?`table-id + record-id` 闁哄被鍎撮妤冩媼閺夎法绉块柛妯烘瑜板爼鏁嶇仦鑲╃憹闁衡偓椤栨稑鐦柡浣侯棎閵嗗啴宕㈤崱妤€钑夐柟娈垮亝瀵?
- **workspace 闁绘鍩栭埀?*闁挎稒鑹鹃崙锟犲箳閵夈儱寮?`+base-create / +base-get / +base-copy`
- **`+base-create / +base-copy` 缂備焦鎸婚悘澶嬫交閺傛寧绀€閻熸瑥瀚€?*闁挎稒鑹鹃崹鍗烆嚈閻戞ê鐏楀璺虹Т閸╂骞嬮幇顒€顫犻柛姘嚱缁辨繈宕堕悙宸Щ濞戞搩鍘肩换鈧銈堫唺鐎靛矂宕濋妸銊х闁搞儳鍋為弻?Base 闁汇劌瀚悥锝囨嫚閸℃洑绻嗛柟顓у灛閳ь剙鍊界€氥垺娼婚弬鎸庣缂備焦鎸婚悘澶愭煂鐏炵晫鏁ㄩ柛娆樺灥椤旀牠姊婚鈧幗濂稿箳閵夘垳绀勫┑?`base.url`闁挎稑顧€缁辨繄鎲版担椋庮伇妤犵偞鍎肩换鎴﹀炊?
- **`+base-create / +base-copy` 闁告瑥顑呴妶浠嬪箑瑜戦～澶愬礆?*闁挎稒鐡?-folder-token`闁靛棔姊?-time-zone`闁靛棔绀侀ˇ鏌ュ礆閼稿灚顦ч柣?`--name` 闂侇喛濮ゅΣ鎼佸矗椤栫偐鍋撴径鎰┾偓宥夊Υ閸屾粍鏆忛柟鎾敱閻ュ懘寮垫径灞筋棗闁告帩鍋夐々锕€效閸屾稒顦ч柨娑樺缁楀鎲版担鐤濞存粌妫滅换鏍ㄧ濞戞ê璁查梺顐㈩槸瀵剟寮导鎼澓濠㈣埖鐗楁晶锕傚棘椤撱劎骞㈤柤宕囨櫕濞插潡骞掗妷銉ョ仭鐎?濠㈣泛绉撮崺妤冧焊鏉堚晜绾柟鎭掑劜婢х晫鎮?
- **`+base-create / +base-copy` 闁哄鍟村鐑樺緞閸曨厽鍊為柨娑樻綄ot 闁告帗绋戠紓鎾绘晬?*闁挎稒淇虹€?Base 闁汇垹宕花鏌ユ偨閵娿劑鐓╁ù鐘虫灮缁辨獏ot闁挎稑顦崹鍗烆嚈閻氬绀夐柛鎺撶☉缂傛捇骞嬮弽褜妲婚柛鎺曞煐閸ㄦ岸宕濋悢閿嬪€靛娑欘焾椤撹崵绱掕閻㈢粯鎷呯捄銊︽殢 bot 闂婎剦鍋傞崬銈嗙▔閸濆嫮绉奸柛鎾崇Т瑜版煡鎮?user闁挎稑鐗婄€垫俺銇愰幘鍐差枀 CLI 濞?auth 婵☆垪鈧櫕鍋ョ€规瓕灏欏▍銉ㄣ亹閺囨氨鐟柛娆樺灣閺併倝鎯冮崟顓熸殢闁瑰鏌夐棅鈺傜閺傘倗绀嗘繛锝堫嚙婵?`full_access`闁挎稑鐗忛鎼佹偠閸℃鍠呴柨娑橆槹濞煎牓姊介幇鍓佺妤犵偠娉涘﹢顏堝炊閻愬樊妲诲☉鎿冨幗濡叉垹娑甸钘夋埧闁哄鍟扮划銊╁几濠婃劗绀勯柟瀛樺姇婵?/ 闁哄啰濮磋ぐ鏌ユ偨?user / 闁瑰搫鐗婂鍫熷緞鏉堫偉袝闁告瑥锕ょ敮顐﹀炊閻欏懐绀嗛柕鍡楀€界€氥垽骞掗崼鐔哥秬闁哄牜浜滈悾顒勫箣閹板墎绀夐悷鏇氳兌閹撮绱掗鐘佃埗闁告垵鎼幃妤冪磼椤撶偟绌块悗鐢点€嬬槐娆戠矙瀹ュ懏鍊甸梺鎻掔Х閻︻垶骞掗崼鐔哥秬闁瑰瓨鐗滈幋椋庣磼椤撶姵鏆?bot闁挎稑顧€缁辩湐wner 閺夌儐鍓涗簺闊洤鎳橀妴蹇涘础閺囩姴顏痪顓у枦椤撳鏁嶅畝鈧々锕€顫㈤姀鈩冩儘闁煎浜濇晶鐣屾偘?
- **dashboard 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鐡?dashboard-create` 闁告帗绋戠紓鎾诲触鎼淬倗绠查柛?`dashboard_id`闁挎稒闆筶ock 闁?`data_config` 闂侇偅淇虹换?JSON 閻庢稒顨堥浣圭▔闊厾鐐婇柛蹇嬪劵缁辨繈寮ㄩ娑樼槷 `@file.json` 閻犲洩顕цぐ鍥棘閸ワ附顐?
- **advperm 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鐡?advperm-enable` 闁告凹鍨抽弫銈嗩殗濡ジ鐛撻柡澶婂暣濡炬椽宕ユ惔銏狀枀闁煎磭鏅鎼佹偠閸℃凹娼￠柤纭咁嚋缁辨獋+role-*`闁挎稑顧€缁辩浗+advperm-disable` 闁哄嫷鍨堕悵顔筋槹鎼淬劍鐝﹂柟鍨С缂嶆棃鏁嶇仦鎴掔不闁活潿鍔岄幃妤€顔忛崣澶嬬畳闁煎浜滈悾鐐▕婢跺寒娼￠柤瑙勫絻閸欏繘鏌堥妸銉ｄ杭闁轰礁鐗炵槐閬嶅箼瀹ュ嫮绋婇柣顫妽閸╂稖绠涢崨娣偓蹇旂▔?Base 缂佺媴绱曢幃濠囧川濮楀牏骞㈤柛蹇撶墣椤?[lark-base-advperm-enable.md](references/lark-base-advperm-enable.md) / [lark-base-advperm-disable.md](references/lark-base-advperm-disable.md)
- **role 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鐡?role-create` 濞寸姴鎳忛弫顕€骞?`custom_role`闁挎稒鐭?role-update` 闂佹彃娲ㄩ弫?Delta Merge闁挎稑娼塺ole_name` 闁?`role_type` 闊洤鎳橀妴蹇旀叏鐎ｎ剛鐭掗柟缁樺姃缁剁敻鏁嶆径娑氬耿`+role-delete` 濞戞挸绉磋ぐ鏌ユ焻閸℃洜鐟ù鐘叉噺閺侇噣骞愭担钘夋閻庤鐭粻鐔烘喆閹烘洖顥忛柨娑欑椤鎳濋弻銉ュ赋缂傚喚鍠楅弫顕€骞?`base_rule_map`闁挎稑婀恆se 缂佺嫏鍐炬Щ闁?濞戞挸顑堝ù鍥晬婢跺牃鍋撴稊顤篴ble_rule_map`闁挎稑鐗愰妴鍐棯瑜庡鍫ユ⒔閹邦剚鍎撻悹浣规緲缂?閻庢稒顨嗛宀€鍒掗幒鎴濐唺闁挎稑顦埀顑挎dashboard_rule_map`闁挎稑鐗呴崡搴ｆ偘閵娧勭８闁哄鍟村娲晬婢跺牃鍋撴稊顤猳cx_rule_map`闁挎稑鐗婇弸鍐浖閿濆棙缍€闂傚嫭鍔х槐姘舵晬濞戞ê鏅搁悷娆愬笩婢瑰﹪宕滃鍛弗閻?[role-config.md](references/role-config.md)
- **閻炴稏鍔屽畷?form-id**闁挎稒宀搁埀顒佷亢缁?`+form-list` 闁兼儳鍢茶ぐ鍥晬濞?form-create` 閺夆晜鏌ㄥú鏍儍?`id` 闁?`form-id`闁挎稑鑻ぐ鏌ユ偨閵娿倗鑹?`+form-questions-*` 闁瑰灝绉崇紞?
- **workflow 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鑹惧﹢顏堝礆濞戞绱﹂柟瀛樼墬濞插潡寮?workflow 闁告挸绋勭槐婵婄疀閸涙番鈧繑绂掗弮鍌滅煄闂傚啫鎳撻?[lark-base-workflow-schema.md](references/lark-base-workflow-schema.md) 濞存粌妫滆闁告艾瀚闁告瑦鍨靛▍鎺楀椽瀹€鍐ㄎ濋柣鎰贡缁秵绂掗崜浣圭暠缂備焦鎸婚悗顖炴晬濞戞ɑ鍊遍柡?`+workflow-list` 閺夆晜鏌ㄥú鏍儍閸曨亞鐟濋柡鍕靛灠閻ｎ剟寮€涙鍩愰柣妯哄缁劑寮搁崟鍓佺闁兼眹鍎靛〒鍓佹嫚鐠囨彃绲块悗鐟版湰閺嗭絿绱掗幘瀵糕偓顖滄嫚閾氬倸鈻忛柣?`+workflow-get`闁?
- **data-query 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒鐭繛鍥偨?`+data-query` 闁告挸绉寸换鈧銈堫嚙閸樻盯姊奸崨閭﹀殺 [lark-base-data-query.md](references/lark-base-data-query.md) 濞存粌妫滆 DSL 缂備焦鎸婚悗顖炲Υ娴ｈ鏆滈柟闀愯兌濞堟垹鈧稒顨嗛宀€鐚剧拠鑼偓鐑藉Υ娴ｆ垝绮甸柛姘墕閸ら亶寮弶鎸庡闂傚嫭鍔曢崺妤呭级閳ュ弶顐介柨娑欓ケSL 濞戞搩鍘惧▓?`field_name` 闊洤鎳橀妴蹇旂▔鎼淬們鈧啰鈧稒顨嗛宀勫触瀹ュ洨缈辩痪顓у枛鐏忣噣鏌婂蹇曠闁哄瀚伴埀顒傚Т婢х娀宕楅崼銏℃殢 `+field-list` 闁兼儳鍢茶ぐ鍥儑閻旈鏉介悗娑欘殕椤斿矂宕?
- **闁稿浚鍓欑槐?/ lookup 濞达綀娉曢弫銈夊棘閻熸壆纭€**闁挎稒纰嶉悗顖炴焻閻樻亽鈧啯娼忛幆褏纭€闁?where 闁哄鈧弶顐介柛鎾崇▌缁辨繈鎳涢崘鑼瘜闁稿繐鐗婄€ｄ浇銇愰幘鍐差枀閻炴稏鍔庣划銊╁几閸曞墎骞㈤悹鎭掑姀閵嗗啴寮幆閭︽矗闁哄被鍎叉竟姗€鎯勯鐣屽灱閻炴稏鍔庡▓鎴犵磼閹惧鈧垶鏁嶇仦鑲╃憹闁稿繋娴囬蹇涘礄椤撯€虫闁绘帗鍎奸銏㈡嚊閳ь剟鎮鍐憻婵炲牓娼ч幃?
- **閻熸瑥妫楀ù姗€鏌屽鍛殥闁告艾绉堕垾妯兼媼閵堝牜娼愰柛?*闁挎稒姘ㄩ弫銈夊箣瀹勬澘鍤掔紓浣哥箲濡叉垹娑甸鍏夊亾濠婂嫬惟闁告繍浜欓柌婊呮喆閸℃绂堥柡鈧憴鍕亣濞寸姭鍋撳☉鏂跨墕閹洜鈧稒銇涢埀顒佺箖濡炲倿鏁嶇€?view-rename` 闁烩晛鐡ㄧ敮鎾箥瑜戦、鎴﹀础閸愭彃璁查柨娑樺缁楀妫侀埀顒傛啺娴ｇ鏅欓悶娑栧劙缁旀挳宕ｉ妷褉鈧鎷?
- **闁告帞濞€濞呭海娑甸娆惧悋閻熸瑥瀚崹顖炴晬閸綆鍞剁憸?/ 閻庢稒顨嗛?/ 閻炴侗鐓夌槐?*闁挎稒鑹鹃々褔寮稿鍛殢闁规潙鍢查崙锛勭磼韫囨梹顫栫痪顓у枦椤曗晝鎲版担绋跨仼闂傚嫨鍊х槐婵嬬嵁閺堢數鐟柣鈺婂枟閻栵絾绋婇悢鍛婎潠缁绢収鍣槐婕?record-delete / +field-delete / +table-delete` 闁告瑯鍨冲ú鍧楀箳閵夛箑鈷旈悶娑樼焿缁辨繃绋夊澶嬩粯閻熸洑绀侀崯鈧悶娑栧劙缁旀潙鈻庨敍鍕ㄢ偓妯兼媼閵堝繒骞㈤柟绗涘棭鏀介柡鍐ㄥ濞插潡骞掗妷銉ф暔 `--yes` 闂侇偅淇虹换?CLI 闁汇劌瀚伴悵顔筋槹鎼淬劍鐝﹂柛鎰懃閸欏棝寮介敓鐘靛矗闁靛棗鍊歌ぐ褔寮垫径灞剧獥闁哄秴娲ｇ划娑㈠嫉婢跺鍔嗗☉鏂款槹濡炲倿鏁嶇仦钘夋櫃闁稿繐鐗忛弫?`+record-get / +field-get / +table-get` 闁?list 闁告稒鍨濋幎銈囨兜椤旀鍚?

## Wiki 闂佸墽鍋撶敮鎾偋鐟欏嫮鏆曞璺哄閹﹪鏁嶉崼銏狀棗闁告帩鍋勯崣褔鏌ㄩ鍡欑＜闁?

闁活厹鍎撮惁鎴炴償閹剧粯鎳犻柟鎭掑劵缁辨獋/wiki/TOKEN`闁挎稑顦抽崕妤呭触鎼粹€宠闁煎疇濮ゅΣ鍛婄閹寸偞鐎俊妤嬬祷閳ь兛鑳堕弫鍝モ偓娑欏姌閵嗗啴寮界粭琛″亾娴ｅ壊妯嬬紓浣侯棎閵嗗啴寮介懖鈺冩惣濞戞挸绉撮幃鎾剁尵鐠囪尙鈧兘鎯冮崟顒佺€俊妤嬬祷閳?*濞戞挸绉烽崗姗€鎯勭€涙ê澶嶉柛瀣穿椤?URL 濞戞搩鍘惧▓?token 閻忓繗椴稿Σ?file_token**闁挎稑鑻换鈧銈堫嚙閸樻盯寮婚妷顭戝殑閻庡湱鍋ゅ顖滅尵鐠囪尙鈧兘宕畝鈧﹢锛勨偓?token闁?

### 濠㈣泛瀚幃濠偯规担琛℃煠

1. **濞达綀娉曢弫?`wiki.spaces.get_node` 闁哄被鍎撮妤呮嚍閸屾粌浠ǎ鍥ｅ墲娴?*
   ```bash
   lark-cli wiki spaces get_node --params '{"token":"&lt;wiki_token&gt;"}'
   ```

2. **濞寸姴姘︾换鎴﹀炊閻愮數娉㈤柡瀣矆閼垫垿骞撻幇顒€绲块柛蹇斿▕閺侇厽绌遍埄鍐х礀**
   - `node.obj_type`闁挎稒纰嶉弸鍐浖閿濆洩顫﹂柛銊ヮ儜缁辨獓ocx/doc/sheet/bitable/slides/file/mindnote闁?
   - `node.obj_token`闁?*闁活亞鍠庨悿鍕儍閸曨剚鐎俊?token**闁挎稑鐗忛弫銈嗙鎼粹剝鍊电紓渚囧幗閹奸攱鎷呭鎰
   - `node.title`闁挎稒纰嶉弸鍐浖閿濆棛鍨煎Λ?

3. **闁哄秷顫夊畵?`obj_type` 闂侇偄顦扮€氥劑宕ユ惔锝囨暰闁告稒鍨濋幎?*

   | obj_type | 閻犲洤鐡ㄥΣ?| 闁告艾娴烽悽濠氬川閹存帗濮?|
         |----------|------|-----------|
   | `docx` | 闁哄倹澹嗘晶妤佺閹寸偞鐎俊?| `drive file.comments.*`闁靛棔姊梔ocx.*` |
   | `doc` | 闁哄唲鍛暭濞存粍鍨堕弸鍐浖?| `drive file.comments.*` |
   | `sheet` | 闁汇垽娼ч悺娆戞偘閵婏妇澹?| `sheets.*` |
   | `bitable` | 濠㈣埖姘ㄥǎ顔炬偘閵婏妇澹?| `lark-cli base +...`闁挎稑鐗呯槐顓㈠礂閸剛绀嗛柨娑欑☉椤┭囧几?shortcut 濞戞挸绉烽々顐︽儎閺嶇數绀夐柛鎰Ф閺?`lark-cli base <resource> <method>`闁?*濞戞挸绉烽々?*闁衡偓绾懓娉?`lark-cli api /open-apis/bitable/v1/...` |
   | `slides` | 妤犵偠宕垫导鍛存偋?| `drive.*` |
   | `file` | 闁哄倸娲ｅ▎?| `drive.*` |
   | `mindnote` | 闁诡剚绻勫ǎ顔锯偓鐢靛帶濞?| `drive.*` |

4. **闁?wiki 閻熸瑱绲鹃悗浠嬪礄閾忚鐣?`obj_token` 鐟滅増鎸婚崹?Base token 濞达綀娉曢弫?*
   - 鐟?`obj_type=bitable` 闁哄啳顔愮槐婕檔ode.obj_token` 閻忓繗椴稿Σ鎼佸触鎼达絿鏁?`base` 闁告稒鍨濋幎銈嗘償閺傛儳鈻忛柣顫妿濞堟垿鎯囬悢椋庢澖 token闁?
   - 濞戞梻鍠庡銊╁及椤栨繍鍤涢柨娑欒壘椤┭囧几濠婂啫鏂у┑顔碱儓缁额參宕楅妷锔叫?`/wiki/...` 闂佸墽鍋撶敮鎾晬鐏炶偐鐟濋悷鏇氱劍婵?`wiki_token` 闁烩晛鐡ㄧ敮瀛樼箙閻愮數鑸?`--base-token`闁?

5. **濠碘€冲€归悘澶婎啅閼碱剛鐥呴柟韬插劙缁?token 闂佹寧鐟辩槐婵嬪礃瀹ュ懏绀€闂侇偀鍋撴俊顐熷亾闁?wiki**
   - 濠碘€冲€归悘澶愬川閹存帗濮㈤弶鈺傛煥濞?`param baseToken is invalid`闁靛棔姊梑ase_token invalid`闁靛棔姊梟ot found`闁挎稑鑻懟鐔哥▔閺冨倹鏆忛柟鎾敱濞撳爼宕氬┑鍫㈣埗闁汇劌瀚Σ?`/wiki/...` 闂佸墽鍋撶敮鎾箣?`wiki_token`闁挎稑濂旂槐顓㈠礂閸啿鍋撻埀顒勬偪閹存柡鍋撳鍕?wiki token 鐟滅増鎸婚崹姘?base token闁炽儲绺块埀?
   - 閺夆晜鐟﹀鍌涚▔瀹ュ牜娲ｉ柡鈧涵鍛版巢 `bitable/v1` API闁挎稒绋戠花鑼博鐎ｎ亜绁梺鎻掔У閺屽﹪骞嶈椤?`lark-cli wiki spaces get_node`闁挎稑鐬奸垾妯兼媼?`obj_type=bitable` 闁告艾鍑界槐婵嬪绩閸︻厽鏆?`node.obj_token` 闂佹彃绉甸弻濠囧箥瑜戦、?`lark-cli base +...`闁?

### 闁哄被鍎撮妤冪矆鏉炴壆浼?

```bash
# 闁哄被鍎撮?wiki 闁煎搫鍊婚崑?
lark-cli wiki spaces get_node --params '{"token":"Pgrr***************UnRb"}'
```

閺夆晜鏌ㄥú鏍磼閹惧浜紒鈧潪鎵紣闁?
```json
{
  "node": {
    "obj_type": "docx",
    "obj_token": "UAJ***************E9nic",
    "title": "ai friendly 婵炴潙顑堥惁?- 1 闁告搩鍨卞﹢?,
    "node_type": "origin",
    "space_id": "6946843325487906839"
  }
}
```

## Base 闂佸墽鍋撶敮瀵告喆閿濆棛鈧晫鎲撮崟顐㈢仧
| 闂佸墽鍋撶敮瀵哥尵鐠囪尙鈧?| 闁哄秶鍘х槐?| 濠㈣泛瀚幃濠囧棘閻熸壆纭€ |
|---------|------|---------|
| 闁烩晛鐡ㄧ敮?Base 闂佸墽鍋撶敮?| `/base/{token}` | 闁烩晛鐡ㄧ敮鎾箵閹邦剙绲垮ù锝嗙矆鐠?`--base-token` |
| Wiki 闁活厹鍎撮惁鎴炴償閹剧粯鎳犻柟?| `/wiki/{token}` | 闁稿繐鐗愰惃鐔兼偨?`wiki.spaces.get_node`闁挎稑鑻ぐ?`node.obj_token` |
### URL 闁告瑥鍊归弳鐔煎箵閹邦剙绲?
```
https://{domain}/base/{base-token}?table={table-id}&view={view-id}
```
- `/base/{token}` 闁?`--base-token`
- `?table={id}` 闁?`--table-id`
- `?view={id}` 闁?`--view-id`
### 缂佸倷鐒﹂娑欑鐎ｎ喓鈧?
- **缂佸倷鐒﹂?*閻忓繐妫楅悾顒勫极?URL 闁烩晛鐡ㄧ敮瀛樻媴濠娾偓鐠?`--base-token` 闁告瑥鍊归弳鐔稿閻樻彃寮?
- **缂佸倷鐒﹂?*閻?wiki_token 闁烩晛鐡ㄧ敮瀛樻媴濠娾偓鐠?`--base-token`

## 閻㈩垱鐡曢～鍡涙煥濞嗘帩鍤栭梺顐ゅ枑閻?

| 闂佹寧鐟ㄩ銈夋儘?| 闁告凹鍋傜粻?| 閻熸瑱绲介崰鍛村棘鐟欏嫷鏀?|
|--------|------|----------|
| 1254064 | 闁哄啨鍎插﹢锟犲冀閻撳海纭€闂佹寧鐟ㄩ?| 闁活潿鍔嶉鐘电矓閹烘挻顦ч梻鍌氱摠閸╂垿鏁嶅畝鍕閻庢稒顨堥浣圭▔?/ 缂佸甯炴?|
| 1254068 | 閻℃帒鎳橀幗濂稿箳閵夛妇澹愮€殿喖绻橀弫濠勬嫚?| 闁?`{text, link}` 閻庣數顢婇挅?|
| 1254066 | 濞存粌鎼幉宕団偓娑欘殕椤斿矂鏌ㄥ▎鎺濆殩 | 闁?`[{id:"ou_xxx"}]`闁挎稑鑻懟鐔烘兜椤旀鍚?`user_id_type` |
| 1254045 | 閻庢稒顨嗛宀勫触瀹ュ嫮鐟濋悗娑櫭﹢?| 婵☆偀鍋撻柡灞诲劚閻⊙冣枔闂堟稒鍊抽柨娑樼墕閹牏绮氶悜妯煎闁靛棔绀侀妵鍥╀焊韫囨挸鏅搁柨?|
| 1254015 | 閻庢稒顨嗛宀勫磹閼测晞顫﹂柛銊ヮ儎缁楀宕犺ぐ鎺戝赋 | 闁?`+field-list`闁挎稑鑻崯鈧柟绋款槺鐞氼偊宕圭€ｎ偆鈧垶鏌?|
| `param baseToken is invalid` / `base_token invalid` | 闁?wiki token闁靛棔绨歰rkspace token 闁瑰瓨鐗曢崣鐐?token 鐟滅増鎸婚崹姘?`base_token` | 濠碘€冲€归悘澶嬫綇閹惧啿寮抽柡澶堝劥閸?`/wiki/...`闁挎稑鑻崢娑㈡偨?`lark-cli wiki spaces get_node` 闁告瑦鐗滃﹢锛勨偓?`obj_token`闁挎稒绋戠紞?`obj_type=bitable` 闁哄啳顔愮槐婵嬫偨?`node.obj_token` 濞达絾绮堢拹?`--base-token` 闂佹彃绉烽惁顖炴晬鐏炶偐鐟濋悷鏇氱劍閺佽偐鎸?`bitable/v1` |
| formula / lookup 闁告帗绋戠紓鎾村緞鏉堫偉袝 | 闁圭娲ゅ畷锟犲嫉椤忓浂鍤㈤柟瀛樼墱缁劑寮搁崟顏嗙憹闁告艾鐗婄涵?| 闁稿繐鐗愰?`formula-field-guide.md` / `lookup-field-guide.md`闁挎稑鑻崯鈧柟?guide 闂佹彃绉寸紓鎾舵嫚闁垮婀?|
| 缂侇垵宕电划铏光偓娑欘殕椤?/ 闁稿浚鍓欑槐锛勨偓娑欘殕椤斿矂宕樺▎蹇撳汲濠㈡儼绮剧憴?| 闁告瑯浜ｉ鎵偓娑欘殕椤斿瞼鎮銏㈢Ъ闁瑰瓨鍔曡ぐ鏌ュ礃濞嗗繒鎽熸繛?| 闁衡偓闁稖绀嬮柛鎰懃閻°劑宕掗妸銉ф憻婵炲牏顣槐婵堟媼閿涘嫮鏆紓浣规尰閻忓绂嶉妶鍥╄埗 formula / lookup / 缂侇垵宕电划铏光偓娑欘殕椤斿矂鎳涢鍕楀ù婧犲啫姣?|
| 1254104 | 闁归潧缍婇崳铏规惥?500 闁?| 闁告帒妫欐竟鎺旀嫬閸愵亝鏆?|
| 1254291 | 妤犵偠娉涜ぐ鍌炲礃濞嗗繐鏆辩紒?| 濞戞捁灏、鎴﹀礃濞嗗繐寮?+ 闁逛絻顫夐濂告⒒閺夋垶顐介弶?|

## 闁告瑥鍊介埀顒€鍟弸鍐浖?

- [lark-base-shortcut-field-properties.md](references/lark-base-shortcut-field-properties.md) 闁?`+field-create/+field-update` JSON 閻熸瑥瀚€垫牠鏁嶉崼鐔疯吂闁艰姤鍔х槐?
- [role-config.md](references/role-config.md) 闁?閻熸瑦甯熸竟濠囧级閸愵喗顎欓梺鏉跨Ф閻ゅ棛鎷犻敃浣?
- [lark-base-shortcut-record-value.md](references/lark-base-shortcut-record-value.md) 闁?`+record-upsert` 闁稿﹤鍚嬮悧绋款嚕韫囨凹娼愰柤鐓庡枦缁辨瑩骞掗妸銊ョ闁?
- [formula-field-guide.md](references/formula-field-guide.md) 闁?formula 閻庢稒顨嗛宀勫礃濞嗘劗銆婇柕鍡曠閸ら亶寮幍顔碱唺闁哄鍠嗛埀顑跨urrentValue 閻熸瑥瀚崹顖炲Υ娴ｈ姤纭堕悶娑栧姀椤撳摜绮诲Δ浼充礁顕ｈ箛銉х鐎殿喛娅ｉ崕鎾诲箳閵娿劌绀冮柨?
- [lookup-field-guide.md](references/lookup-field-guide.md) 闁?lookup 閻庢稒顨嗛宀勬煀瀹ュ洨鏋傞悷娆忓閸垶濡存禍鈧琱ere/aggregate 缂佹拝闄勫顐﹀Υ娴ｉ鐟?formula 闁汇劌瀚ぐ鍥嚋?
- [lark-base-view-set-filter.md](references/lark-base-view-set-filter.md) 闁?閻熸瑥妫楀ù妯肩驳濞戔懇鍋撴径鎰赋缂?
- [lark-base-record-list.md](references/lark-base-record-list.md) 闁?閻犱焦婢樼紞宥夊礆濡ゅ嫨鈧啰鎷犵拠鎻掔悼濞戞挸楠搁崹搴亜?
- [lark-base-advperm-enable.md](references/lark-base-advperm-enable.md) 闁?`+advperm-enable` 闁告凹鍨抽弫銈嗩殗濡ジ鐛撻柡澶婂暣濡?
- [lark-base-advperm-disable.md](references/lark-base-advperm-disable.md) 闁?`+advperm-disable` 闁稿绮庨弫銈嗩殗濡ジ鐛撻柡澶婂暣濡?
- [lark-base-role-list.md](references/lark-base-role-list.md) 闁?`+role-list` 闁告帗顨呴崵顓犳喆閹烘洖顥?
- [lark-base-role-get.md](references/lark-base-role-get.md) 闁?`+role-get` 闁兼儳鍢茶ぐ鍥╂喆閹烘洖顥忛悹鍥烽檮閸?
- [lark-base-role-create.md](references/lark-base-role-create.md) 闁?`+role-create` 闁告帗绋戠紓鎾舵喆閹烘洖顥?
- [lark-base-role-update.md](references/lark-base-role-update.md) 闁?`+role-update` 闁哄洤鐡ㄩ弻濠勬喆閹烘洖顥?
- [lark-base-role-delete.md](references/lark-base-role-delete.md) 闁?`+role-delete` 闁告帞濞€濞呭海鎲撮幒鏇烆棌
- [lark-base-dashboard.md](references/lark-base-dashboard.md) 闁?dashboard 闁告稒鍨濋幎銈囨閵忕姷绌块柨娑樼墛閻︹剝绋夐鍕殥濞寸姰鍊曢崙锟犲箯閸℃鐓傞柣娆樺墰閻濇盯寮崶銊ｂ偓鍌炴晬?
- [lark-base-dashboard-block.md](references/lark-base-dashboard-block.md) 闁?dashboard block 闁告稒鍨濋幎銈囨閵忕姷绌块柨娑樼墛閻︹剝绋夐鍕殥濞寸姰鍊曢崙锟犲箯閸℃鐓傞柣娆樺墰閻濇盯寮崶銊ｂ偓鍌炴晬?
- [dashboard-block-data-config.md](references/dashboard-block-data-config.md) 闁?Block data_config 缂備焦鎸婚悗顖炲Υ娴ｅ憡绂堥悶娑栧妿鐞氼偊宕圭€ｃ劉鍋撴稊鐜ter 閻熸瑥瀚崹?
- [lark-base-workflow.md](references/lark-base-workflow.md) 闁?workflow 闁告稒鍨濋幎銈囨閵忕姷绌?
- [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md) 闁?`+workflow-create/+workflow-update` JSON body 闁轰胶澧楀畵浣虹磼閹惧鈧垳鎷犻敃浣囨帡鏁嶇仦钘夌樁闁告凹鍋夎闁告瑦鍨靛▍鎺楀矗婵犲倹鍊楃紒顐ｆ婵☆參鎮欓崷顓熺暠闂佹澘绉堕悿鍡欐喆閸曨偄鐏熼柨娑樼墕瀹搁亶鎮滈崼鐔疯吂闁艰姤鍔х槐?
- [lark-base-data-query.md](references/lark-base-data-query.md) 闁?`+data-query` 闁艰鲸鑹鹃幃搴ㄥ礆閸℃鈧粙鏁嶉崷鏈 缂備焦鎸婚悗顖炲Υ娴ｈ鏆滈柟闀愮閻⊙冣枔閻絻顫﹂柛銊ヮ儍閳ь兛娴囨禒娑㈠触閸繂姣愰柡浣稿簻缁?
- [examples.md](references/examples.md) 闁?閻庣懓鏈弳锝夊箼瀹ュ嫮绋婄紒鈧潪鎵紣闁挎稑鐗嗙紓鎾舵偘閵婏絺鍋撴担鍓插殼闁稿繈鍎埀顑胯兌閻☆偊鏌呮径鍫氬亾娴ｈ绾柡鍌氬簻缁?

## 闁告稒鍨濋幎銈夊礆閸℃瑧鐭?

> **闁圭瑳鍡╂斀闁告挸绉寸换鈧柛瀣啲缁?* 濞寸姴绨肩粭鍛偘閵娿儳鏆板ù锝呯Т閸╁矂宕ㄩ幋鎺撳Б闁告艾鍑界槐婵嬪礉閳ュ磭绠戦柛蹇撶墦濡插嫮鎷犵拠宸殸閹煎瓨鏌ㄩ幊鈩冪閵堝洦鐣?reference 闁哄倸娲﹂妴鍌炴晬鐏炶棄鏅欓悹瀣暟閺併倝宕ㄩ幋鎺撳Б闁?

| 闁告稒鍨濋幎銈夊礆閸℃瑧鐭?| 閻犲洤鐡ㄥΣ?|
|----------|------|
| [`table commands`](references/lark-base-table.md) | `+table-list / +table-get / +table-create / +table-update / +table-delete` |
| [`field commands`](references/lark-base-field.md) | `+field-list / +field-get / +field-create / +field-update / +field-delete / +field-search-options` |
| [`record commands`](references/lark-base-record.md) | `+record-list / +record-get / +record-upsert / +record-upload-attachment / +record-delete` |
| [`view commands`](references/lark-base-view.md) | `+view-list / +view-get / +view-create / +view-delete / +view-get-* / +view-set-* / +view-rename` |
| [`data-query commands`](references/lark-base-data-query.md) | `+data-query` |
| [`history commands`](references/lark-base-history.md) | `+record-history-list` |
| [`base / workspace commands`](references/lark-base-workspace.md) | `+base-create / +base-get / +base-copy` |
| [`advperm commands`](references/lark-base-advperm-enable.md) | `+advperm-enable / +advperm-disable` |
| [`role commands`](references/lark-base-role-list.md) | `+role-list / +role-get / +role-create / +role-update / +role-delete` |
| [`form commands`](references/lark-base-form-create.md) | `+form-list / +form-get / +form-create / +form-update / +form-delete` |
| [`form questions commands`](references/lark-base-form-questions-create.md) | `+form-questions-list / +form-questions-create / +form-questions-update / +form-questions-delete` |
| [`workflow commands`](references/lark-base-workflow.md) | `+workflow-list / +workflow-get / +workflow-create / +workflow-update / +workflow-enable / +workflow-disable` |
| [`dashboard commands`](references/lark-base-dashboard.md) | `+dashboard-list / +dashboard-get / +dashboard-create / +dashboard-update / +dashboard-delete` |
| [`dashboard block commands`](references/lark-base-dashboard-block.md) | `+dashboard-block-list / +dashboard-block-get / +dashboard-block-create / +dashboard-block-update / +dashboard-block-delete` |
