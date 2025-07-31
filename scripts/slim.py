# 生成されたデータをスリムに要約するスクリプト
import os
import json
import ollama
import time

MODEL = "phi4:14b"  # 使用するモデルを指定
# path
DIR_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
DIR_CORPUS = os.path.join(DIR_SCRIPTS, '..', 'corpus')
DIR_INPUT = os.path.join(DIR_CORPUS, 'anime_corpus-phi4.json')
DIR_OUTPUT = os.path.join(DIR_CORPUS, 'anime_corpus-phi4-slim.json')
# template
TEMPLATE = """\
要約の主軸: {instruction}
入力:
```
{input}
```
"""

def generate_summary(text, size=400, model=MODEL):
    """テキストの要約を生成する関数"""
    start_time = time.time()
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": f"あなたは要約の専門家です。{size}文字以下で要約してください。"},
            {"role": "user", "content": text}
        ]
    )
    print(f" - 時間: {time.time() - start_time:.2f}秒")
    return response['message']['content']

def slim_corpus(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    slimmed_data = []
    for row in data["train"]:
        instruction = row.get("instruction", "")
        input = row.get("input", "")
        output = row.get("output", "")
        if len(output) > 400:
            print(f"=" * 60)
            print(f" - スリム化対象: {input} / {instruction}")
            # 要約
            prompt = TEMPLATE.format(instruction=instruction, input=output)
            # print("--- 要約生成のためのプロンプト ---", prompt)
            output = generate_summary(prompt, size=400, model=MODEL)
            print("--- 要約生成 ---")
            print(output)
        row["output"] = output.strip()
        slimmed_data.append(row)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump({"train": slimmed_data}, outfile, ensure_ascii=False, indent=2)

def main():
    print("入力ファイル:", DIR_INPUT)
    print("出力ファイル:", DIR_OUTPUT)
    slim_corpus(DIR_INPUT, DIR_OUTPUT)
    print("スリム化が完了しました。")

if __name__ == "__main__":
    main()
