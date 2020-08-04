# ETroboSimController

新が趣味で作ったUnityETroboSim環境(ETロボコンシミュレータ)のPython用クライアントライブラリです。
Athrillから置き換えることで、比較的軽量で快適な走行体制御が可能となります。 

# API

https://www.toppers.jp/ev3pf/EV3RT_CXX_API_Reference/files.html に準拠しています。
ev3apiの下にあるクラスを見ればだいたいわかるでしょう。  
https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/ に準拠させたいと思う人は勝手にやってください。  

# 動作確認

git cloneした後、python test_Motor.pyを実行してみてください。シナリオトレーサーっぽい動きをします。  
その他、サンプルプログラムtest_*.pyを参考にして遊んでみてください。  

# 確認環境

Python 3.7.6 (tags/v3.7.6:43364a7ae0, Dec 19 2019, 00:42:30) [MSC v.1916 64 bit (AMD64)] on win32  
ETロボコンシミュレータver2.1  

# 技術情報

一応、Unityとは10ms周期で通信できているようです。test_LineTrace.pyのライントレースはめちゃ簡単に走ります。
遅いPCでは動かないかも。Unityを待って止まる機能は今のところつけてませんが、Controllerの runCyclicあたりをいじればできるのかも？
LED、操作キーなど、C++ APIに入っていない機能の実装はこれからやります。
