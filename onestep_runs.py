import subprocess

datadir = './data/'
#datasets = ['sklearn-digits', 'dna','satimage','svmguide1']
datasets = ['dna']
#datasets = ['svmguide1']
#datasets = ['ijcnn1']
#datasets = ['letter']
#datasets = ['usps']
#datasets = ['connect_4']
#datasets = ['shuttle']
fracs =[0.3,0.5]#0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#fracs =[ 0.4,0.5,0.6,0.7,0.8,0.9]
num_epochs = 200
select_every = [20]#,35,50]
warm_method = [0]   # 0 = online, 1 = onestep warmstart
num_runs = 10
feature = ['dss']#,'noise']#,'classimb']
#feature = ['noise']
#feature = ['classimb']#,'noise']
for dset in datasets:
    for sel in select_every:
        for f in fracs:
            for feat in feature:
                for isOneStepWarm in warm_method:
                    args = ['python3']
                    if feat == 'classimb':
                        args.append('run_onestep_classimb.py')
                    else:
                        args.append('run_onestep_clean.py')
                    
                    if dset in ['mnist', "fashion-mnist"]:
                        args.append(datadir + dset.upper())
                    else:
                        args.append(datadir + dset)
                    args.append(dset)
                    args.append(str(f))
                    args.append(str(num_epochs))
                    args.append(str(sel))
                    args.append(feat)
                    args.append(str(isOneStepWarm))
                    args.append(str(num_runs))
                    print(args)
                    subprocess.run(args)




