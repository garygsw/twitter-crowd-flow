#/bin/bash

#PBS -q normal
#PBS -l select=1:ncpus=16:mem=64GB
#PBS -l walltime=24:00:00

#PBS -N "filter_set4"
#PBS -P Personal

cd /home/users/sutd/1002045/traffic/tagger
source venv/bin/activate 

python stanford_tagger.py VDLset2 tweets_20151130.csv &> log/tweets_20151130.txt &
python stanford_tagger.py VDLset2 tweets_20151201.csv &> log/tweets_20151201.txt &
python stanford_tagger.py VDLset2 tweets_20151202.csv &> log/tweets_20151202.txt &
python stanford_tagger.py VDLset2 tweets_20151203.csv &> log/tweets_20151203.txt &
python stanford_tagger.py VDLset2 tweets_20151204.csv &> log/tweets_20151204.txt &
python stanford_tagger.py VDLset2 tweets_20151205.csv &> log/tweets_20151205.txt &
python stanford_tagger.py VDLset2 tweets_20151206.csv &> log/tweets_20151206.txt &
python stanford_tagger.py VDLset2 tweets_20151207.csv &> log/tweets_20151207.txt &
python stanford_tagger.py VDLset2 tweets_20151208.csv &> log/tweets_20151208.txt &
python stanford_tagger.py VDLset2 tweets_20151209.csv &> log/tweets_20151209.txt &
python stanford_tagger.py VDLset2 tweets_20151210.csv &> log/tweets_20151210.txt &
python stanford_tagger.py VDLset2 tweets_20151211.csv &> log/tweets_20151211.txt &
python stanford_tagger.py VDLset2 tweets_20151212.csv &> log/tweets_20151212.txt &
python stanford_tagger.py VDLset2 tweets_20151213.csv &> log/tweets_20151213.txt &
python stanford_tagger.py VDLset2 tweets_20151214.csv &> log/tweets_20151214.txt &
python stanford_tagger.py VDLset2 tweets_20151215.csv &> log/tweets_20151215.txt &
python stanford_tagger.py VDLset2 tweets_20151216.csv &> log/tweets_20151216.txt &
python stanford_tagger.py VDLset2 tweets_20151217.csv &> log/tweets_20151217.txt &
python stanford_tagger.py VDLset2 tweets_20151218.csv &> log/tweets_20151218.txt &
python stanford_tagger.py VDLset2 tweets_20151219.csv &> log/tweets_20151219.txt &
python stanford_tagger.py VDLset2 tweets_20151220.csv &> log/tweets_20151220.txt &
python stanford_tagger.py VDLset2 tweets_20151221.csv &> log/tweets_20151221.txt &
python stanford_tagger.py VDLset2 tweets_20151222.csv &> log/tweets_20151222.txt &
python stanford_tagger.py VDLset2 tweets_20151223.csv &> log/tweets_20151223.txt &
python stanford_tagger.py VDLset2 tweets_20151224.csv &> log/tweets_20151224.txt &
python stanford_tagger.py VDLset2 tweets_20151225.csv &> log/tweets_20151225.txt &
python stanford_tagger.py VDLset2 tweets_20151226.csv &> log/tweets_20151226.txt &
python stanford_tagger.py VDLset2 tweets_20151227.csv &> log/tweets_20151227.txt &
python stanford_tagger.py VDLset2 tweets_20151228.csv &> log/tweets_20151228.txt &
python stanford_tagger.py VDLset2 tweets_20151229.csv &> log/tweets_20151229.txt &
python stanford_tagger.py VDLset2 tweets_20151230.csv &> log/tweets_20151230.txt &
python stanford_tagger.py VDLset2 tweets_20151231.csv &> log/tweets_20151231.txt &
python stanford_tagger.py VDLset2 tweets_20160101.csv &> log/tweets_20160101.txt &
python stanford_tagger.py VDLset2 tweets_20160102.csv &> log/tweets_20160102.txt &
python stanford_tagger.py VDLset2 tweets_20160103.csv &> log/tweets_20160103.txt &
python stanford_tagger.py VDLset2 tweets_20160104.csv &> log/tweets_20160104.txt &
python stanford_tagger.py VDLset2 tweets_20160105.csv &> log/tweets_20160105.txt &
python stanford_tagger.py VDLset2 tweets_20160106.csv &> log/tweets_20160106.txt &
python stanford_tagger.py VDLset2 tweets_20160107.csv &> log/tweets_20160107.txt &
python stanford_tagger.py VDLset2 tweets_20160108.csv &> log/tweets_20160108.txt &
python stanford_tagger.py VDLset2 tweets_20160109.csv &> log/tweets_20160109.txt &
python stanford_tagger.py VDLset2 tweets_20160110.csv &> log/tweets_20160110.txt &
python stanford_tagger.py VDLset2 tweets_20160111.csv &> log/tweets_20160111.txt &
python stanford_tagger.py VDLset2 tweets_20160112.csv &> log/tweets_20160112.txt &
python stanford_tagger.py VDLset2 tweets_20160113.csv &> log/tweets_20160113.txt &
python stanford_tagger.py VDLset2 tweets_20160114.csv &> log/tweets_20160114.txt &
python stanford_tagger.py VDLset2 tweets_20160115.csv &> log/tweets_20160115.txt &
python stanford_tagger.py VDLset2 tweets_20160116.csv &> log/tweets_20160116.txt &
python stanford_tagger.py VDLset2 tweets_20160117.csv &> log/tweets_20160117.txt &
python stanford_tagger.py VDLset2 tweets_20160118.csv &> log/tweets_20160118.txt &
python stanford_tagger.py VDLset2 tweets_20160119.csv &> log/tweets_20160119.txt &
python stanford_tagger.py VDLset2 tweets_20160120.csv &> log/tweets_20160120.txt &
python stanford_tagger.py VDLset2 tweets_20160121.csv &> log/tweets_20160121.txt &
python stanford_tagger.py VDLset2 tweets_20160122.csv &> log/tweets_20160122.txt &
python stanford_tagger.py VDLset2 tweets_20160123.csv &> log/tweets_20160123.txt &
python stanford_tagger.py VDLset2 tweets_20160124.csv &> log/tweets_20160124.txt &
python stanford_tagger.py VDLset2 tweets_20160125.csv &> log/tweets_20160125.txt &
python stanford_tagger.py VDLset2 tweets_20160126.csv &> log/tweets_20160126.txt &
python stanford_tagger.py VDLset2 tweets_20160127.csv &> log/tweets_20160127.txt &
python stanford_tagger.py VDLset2 tweets_20160128.csv &> log/tweets_20160128.txt &
python stanford_tagger.py VDLset2 tweets_20160129.csv &> log/tweets_20160129.txt &
python stanford_tagger.py VDLset2 tweets_20160130.csv &> log/tweets_20160130.txt &
python stanford_tagger.py VDLset2 tweets_20160131.csv &> log/tweets_20160131.txt &
python stanford_tagger.py VDLset2 tweets_20160201.csv &> log/tweets_20160201.txt &
python stanford_tagger.py VDLset2 tweets_20160202.csv &> log/tweets_20160202.txt &
python stanford_tagger.py VDLset2 tweets_20160203.csv &> log/tweets_20160203.txt &
python stanford_tagger.py VDLset2 tweets_20160204.csv &> log/tweets_20160204.txt &
python stanford_tagger.py VDLset2 tweets_20160205.csv &> log/tweets_20160205.txt &
python stanford_tagger.py VDLset2 tweets_20160206.csv &> log/tweets_20160206.txt &
python stanford_tagger.py VDLset2 tweets_20160207.csv &> log/tweets_20160207.txt &
python stanford_tagger.py VDLset2 tweets_20160208.csv &> log/tweets_20160208.txt &
python stanford_tagger.py VDLset2 tweets_20160209.csv &> log/tweets_20160209.txt &
python stanford_tagger.py VDLset2 tweets_20160210.csv &> log/tweets_20160210.txt &
python stanford_tagger.py VDLset2 tweets_20160211.csv &> log/tweets_20160211.txt &
python stanford_tagger.py VDLset2 tweets_20160212.csv &> log/tweets_20160212.txt &
python stanford_tagger.py VDLset2 tweets_20160213.csv &> log/tweets_20160213.txt &
python stanford_tagger.py VDLset2 tweets_20160214.csv &> log/tweets_20160214.txt &
python stanford_tagger.py VDLset2 tweets_20160215.csv &> log/tweets_20160215.txt &
python stanford_tagger.py VDLset2 tweets_20160216.csv &> log/tweets_20160216.txt &
python stanford_tagger.py VDLset2 tweets_20160217.csv &> log/tweets_20160217.txt &
python stanford_tagger.py VDLset2 tweets_20160218.csv &> log/tweets_20160218.txt &
python stanford_tagger.py VDLset2 tweets_20160219.csv &> log/tweets_20160219.txt &
python stanford_tagger.py VDLset2 tweets_20160220.csv &> log/tweets_20160220.txt &
python stanford_tagger.py VDLset2 tweets_20160221.csv &> log/tweets_20160221.txt &
python stanford_tagger.py VDLset2 tweets_20160222.csv &> log/tweets_20160222.txt &
python stanford_tagger.py VDLset2 tweets_20160223.csv &> log/tweets_20160223.txt &
python stanford_tagger.py VDLset2 tweets_20160224.csv &> log/tweets_20160224.txt &
python stanford_tagger.py VDLset2 tweets_20160225.csv &> log/tweets_20160225.txt &
python stanford_tagger.py VDLset2 tweets_20160226.csv &> log/tweets_20160226.txt &
python stanford_tagger.py VDLset2 tweets_20160227.csv &> log/tweets_20160227.txt &
python stanford_tagger.py VDLset2 tweets_20160228.csv &> log/tweets_20160228.txt &
python stanford_tagger.py VDLset2 tweets_20160229.csv &> log/tweets_20160229.txt &
python stanford_tagger.py VDLset2 tweets_20160301.csv &> log/tweets_20160301.txt &
python stanford_tagger.py VDLset2 tweets_20160302.csv &> log/tweets_20160302.txt &
python stanford_tagger.py VDLset2 tweets_20160303.csv &> log/tweets_20160303.txt &
python stanford_tagger.py VDLset2 tweets_20160304.csv &> log/tweets_20160304.txt &
python stanford_tagger.py VDLset2 tweets_20160305.csv &> log/tweets_20160305.txt &
python stanford_tagger.py VDLset2 tweets_20160306.csv &> log/tweets_20160306.txt &
python stanford_tagger.py VDLset2 tweets_20160307.csv &> log/tweets_20160307.txt &
python stanford_tagger.py VDLset2 tweets_20160308.csv &> log/tweets_20160308.txt &
python stanford_tagger.py VDLset2 tweets_20160309.csv &> log/tweets_20160309.txt &
python stanford_tagger.py VDLset2 tweets_20160310.csv &> log/tweets_20160310.txt &
python stanford_tagger.py VDLset2 tweets_20160311.csv &> log/tweets_20160311.txt &
python stanford_tagger.py VDLset2 tweets_20160312.csv &> log/tweets_20160312.txt &
python stanford_tagger.py VDLset2 tweets_20160313.csv &> log/tweets_20160313.txt &
python stanford_tagger.py VDLset2 tweets_20160314.csv &> log/tweets_20160314.txt &
python stanford_tagger.py VDLset2 tweets_20160315.csv &> log/tweets_20160315.txt &
python stanford_tagger.py VDLset2 tweets_20160316.csv &> log/tweets_20160316.txt &
python stanford_tagger.py VDLset2 tweets_20160317.csv &> log/tweets_20160317.txt &
python stanford_tagger.py VDLset2 tweets_20160318.csv &> log/tweets_20160318.txt &
python stanford_tagger.py VDLset2 tweets_20160319.csv &> log/tweets_20160319.txt &
python stanford_tagger.py VDLset2 tweets_20160320.csv &> log/tweets_20160320.txt &
python stanford_tagger.py VDLset2 tweets_20160321.csv &> log/tweets_20160321.txt &
python stanford_tagger.py VDLset2 tweets_20160322.csv &> log/tweets_20160322.txt &
python stanford_tagger.py VDLset2 tweets_20160323.csv &> log/tweets_20160323.txt &
python stanford_tagger.py VDLset2 tweets_20160324.csv &> log/tweets_20160324.txt &
python stanford_tagger.py VDLset2 tweets_20160325.csv &> log/tweets_20160325.txt &
python stanford_tagger.py VDLset2 tweets_20160326.csv &> log/tweets_20160326.txt &
python stanford_tagger.py VDLset2 tweets_20160327.csv &> log/tweets_20160327.txt &
python stanford_tagger.py VDLset2 tweets_20160328.csv &> log/tweets_20160328.txt &
python stanford_tagger.py VDLset2 tweets_20160329.csv &> log/tweets_20160329.txt &
python stanford_tagger.py VDLset2 tweets_20160330.csv &> log/tweets_20160330.txt &
python stanford_tagger.py VDLset2 tweets_20160331.csv &> log/tweets_20160331.txt &

wait
