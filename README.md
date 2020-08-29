# experiment-EasyOCR

[EasyOCR](https://github.com/JaidedAI/EasyOCR)を使ってみた結果

| Detected | Recognized |
| --- | --- |
| ![img1](https://github.com/youichiro/experiment-EasyOCR/blob/master/out/test2.detect.jpg) | ![img2](https://github.com/youichiro/experiment-EasyOCR/blob/master/out/test2.text.jpg) |

## jupyter notebook

[https://github.com/youichiro/experiment-EasyOCR/blob/master/experiment_easyocr.ipynb](https://github.com/youichiro/experiment-EasyOCR/blob/master/experiment_easyocr.ipynb)

## CLIで試す

### 環境

python 3.8.3

### セットアップ

```bash
git clone https://github.com/youichiro/experiment-EasyOCR.git
cd experiment-EasyOCR
pip install -r requirements.txt
```

### 実行コマンド

```bash
python cli.py -l [langage, ...] -f <image file> -o <output dir>
```

