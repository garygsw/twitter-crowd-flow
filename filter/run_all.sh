source venv/bin/activate

python rule_tagger.py VLDset1 &
python rule_tagger.py VLDset2 &
python rule_tagger.py VLDset3 &

wait

