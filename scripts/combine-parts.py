# 生成されたデータをスリムに要約するスクリプト
import os
import json
import ollama
import time
import glob

# path
DIR_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
DIR_CORPUS = os.path.join(DIR_SCRIPTS, '..', 'corpus')
DIR_CORPUS_PARTS = os.path.join(DIR_CORPUS, 'parts')
FILE_OUTPUT = os.path.join(DIR_CORPUS, 'anime_corpus.json')

def enum_files():
    """指定ディレクトリ内のすべてのJSONファイルを列挙する"""
    return glob.glob(os.path.join(DIR_CORPUS_PARTS, '*.json'))

def main():
    result = []
    for file in enum_files():
        print(f"Processing {file}...")
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # ファイルを結合する
        for item in data["train"]:
            result.append(item)
    result.sort(key=lambda x: x['input'])  # inputでソート
    # 出力ファイルに書き込む
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as out_file:
        json.dump({
            "train": result
            },
            out_file, ensure_ascii=False, indent=2)

    print(f"Finished: {FILE_OUTPUT}")

if __name__ == "__main__":
    main()
