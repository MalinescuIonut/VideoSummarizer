::conda activate tensorflow-mkl
::set PATH="C:\Users\jmmm\Google Drive\SW\GnuWin32\lib";"C:\Users\jmmm\Google Drive\SW\GnuWin32\bin";%PATH%
::conda activate tf-gpu
::conda activate tf
::pause
::python.exe --version
::pause
::pip uninstall tensorboard
::pause
::pip uninstall tensorflow
::pause
::pip install tensorflow-cpu==1.15.0
::pause
::pip install tensorflow-1.9.0-cp36-cp36m-win_amd64.whl
:: pause
::python.exe -m pip install --upgrade pip
::pause
::pip install torch==1.5.0 -f https://download.pytorch.org/whl/torch_stable.html
::pause
::python -c "print('hola')"
::pause
::python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
set USER=jmmm
set NAME=TheVastOfNight2020Patterson
set EXTENS=mkv
set "FOLDERSW=C:\Users\%USER%\Google Drive\SW"
set FILE=%NAME%.%EXTENS%
set TRACKAUDIO=1
::"%FOLDERSW%\ffmpeg.exe" -i "%FILE%" -map "0:a:%TRACKAUDIO%" -y "%NAME%.mp3"
::pause
::python ina_speech_segmenter.py -i "%NAME%.mp3" -o . -g false -b "%FOLDERSW%\ffmpeg.exe"
::python ina_speech_segmenter.py -i "%NAME%.mp3" -o . -g true -b "%FOLDERSW%\ffmpeg.exe"
::pause

::python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([2, 2])))"
::pause
::conda install -c pytorch pytorch
::pause
::pip install inaSpeechSegmenter-0.6.2-py3-none-any.whl
::pause 
::conda install keras
::conda install pandas
::conda install scikit-image
::conda install opencv
::pip install -q https://github.com/pyannote/pyannote-audio/tarball/develop
::conda install torchvision
::pip install s4d
::https://github.com/Jamiroquai88/VBDiarization
::pip install bert-extractive-summarizer
::pip install spacy
::pip install transformers
::pip install neuralcoref
::python -m spacy download en_core_web_md
::python -m spacy download es_core_news_lg
::python textSummary.py
pause