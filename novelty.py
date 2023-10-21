import sys
from genalgorithm import GenAlgorithm


# python novelty.py apply AbIPP-Combined-1.xlsx GA-Output2.xlsx 100 400 0.6 2 False 0-4 5-7
# python novelty.py merge AbIPP-Combined-1.xlsx GtIPP-Combined-1.xlsx
if __name__=="__main__":
    options = sys.argv[1:]
    print(options)

    if options[0] == "apply":
        try:
            if options[7] == 'True':
                options[7] = True
            else:
                options[7] = False

            if len(options) == 11:
                ga = GenAlgorithm(options[1], options[2], options[3],
                            options[4], options[5], options[6],
                            '0-10', options[7],
                            options[8], options[9], options[10])
            else:
                ga = GenAlgorithm(options[1], options[2], options[3],
                            options[4], options[5], options[6],
                            '0-10', options[7],
                            options[8], options[9])
            ga.apply_gen_algorithm()

            sys.exit(1)
        except SystemExit:
            print "Algorithm Successfully Applied"
        except:
            sys.exit(9)

        sys.exit(1)

    elif options[0] == "merge":
        all_inputs = []
        all_inputs2 = []
        uniq_inputs = []
        all_labels = []
        all_files = []
        for i, opt in enumerate(options[2:]):
            if i % 2 != 0:
                ga = GenAlgorithm(opt)
                ip = ga.get_inputs(True)
                all_inputs.append(ip)
                uniq_inputs.extend(ip)
                print ip[0]
                all_files.append(opt)
                # ga.merge_files(options[1:])
            else:
                all_labels.append(opt[2:])


        # print len(uniq_inputs)
        uniq_indices = [list(x) for x in set(tuple(x) for x in uniq_inputs)]
        # print len(uniq_indices)

        # common_indices = [i for c in common for (i,f) in enumerate(final_small) if c==f]
        # common_indices.sort()
        print "======"
        all_inputs2 = [[x[:-1] for x in y] for y in all_inputs]
        print all_inputs2[0][0]

        for i, lbl in enumerate(all_labels):
            for q, qinputs in enumerate(uniq_inputs):
                if qinputs[:7] in all_inputs2[i]:
                    uniq_inputs[q].append(1)
                else:
                    uniq_inputs[q].append(0)

        sorted_indices = [b[0] for b in sorted(enumerate([u[-(len(all_labels)+1)] for u in uniq_inputs]),key=lambda x:-float(x[1]))]
        # uniq_inputs.sort(key=lambda x: -float(x[-3]))
        # print [i[-2:] for i in uniq_inputs]
        # print all_labels
	# print sorted_indices

	ext_inputs = [u[-len(all_labels):] for u in uniq_inputs]
        # print [x for x in ext_inputs if x[0]==x[1]]

        common_indices = []
        common_indices2 = []
        for i, elem in enumerate(uniq_inputs):
            for j, elem2 in enumerate(uniq_inputs):
                if (elem[:7] == elem2[:7]) and j>i:
                    common_indices.append(j)
                    common_indices2.append({i:j})

        # print common_indices
        # print common_indices2
        print len(common_indices)
        common_indices = list(set(common_indices))
        print len(sorted_indices)
        sorted_indices = [n for n in sorted_indices if n not in common_indices]
        # print uniq_inputs[common_indices2[0].keys()[0]]
        # print uniq_inputs[common_indices2[0].values()[0]]


	ga.merge_files(sorted_indices, ext_inputs, all_labels, all_files, all_inputs, uniq_inputs, options[1:])

        try:
            print "Sadsa"
        except SystemExit:
            print "Files Successfully Merged"
        except:
            sys.exit(9)

        sys.exit(1)

