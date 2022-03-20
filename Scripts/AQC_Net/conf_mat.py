def create_conf_mat():
    from sklearn import metrics
    actual = open("actual_res.txt" , mode = "r")
    pred = open("predict_res.txt", mode = "r")
    actual_list = [int(line[0]) for line in actual ]
    pred_list = [int(line[0]) for line in pred]
    actual_list = actual_list[1:]
    pred_list = pred_list[1:]
    print(metrics.confusion_matrix(actual_list,pred_list))
    print(metrics.classification_report(actual_list,pred_list, digits = 2))
    actual.close()
    pred.close()


#{'p0a0': 22, 'p1a1': 4, 'p1a0': 2, 'p0a1': 7}
