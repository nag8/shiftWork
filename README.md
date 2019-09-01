# shiftWork

## 仕様
- 朝、昼、夜に窓口が必要
    - 基本3人
- 第3日曜日は休館
    - ただし職員は研修で出勤
- 基本シフトから案を作成する

## in_out
### in
- 事業予定（会議や主催イベントの予定）
- 基本シフト
- でれないリスト

### out
- シフト表
- 事業予定表

## how
### 環境構築

- 基本シフト
shiftWork/IN/basic.csv
- 出勤可能日リスト
shiftWork/IN/canShift.csv
- ニックネーム表
shiftWork/IN/nickName.csv

### 各メンバー作業
1. 以下を実施する

 種別 | 内容 
 :--------: | -------- 
作業|[サイボウズofficeのスケジュール](https://npo-seeds.cybozu.com/o/ag.cgi?page=ScheduleIndex)に以下を記入する
内容|来月の休みたい日・時間。予定のカテゴリは「出れない」
期限|19日まで

### シフト担当者作業
1. 各ファイルが前月より変わらないか確認
    - 基本シフト
    - ニックネーム表
2. 事業予定をサイボウズから取得
3. 実行
    python3 shiftWork.py > OUT/log.txt


