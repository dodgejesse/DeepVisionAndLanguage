%to run the evaluation:
%start matlab (using $matlab)
%use:

path_to_stored_variables = '/home/jessed/data_storage/deep_vision_and_language/baseline/dataset_info.mat'


path_to_output_train = '/home/jessed/data_storage/deep_vision_and_language/baseline/caffe_train_fthn_fea8.mat'
path_to_save_train_results = '/home/jessed/data_storage/deep_vision_and_language/baseline/train_results.mat'
path_to_write_train_progress = '/home/jessed/data_storage/deep_vision_and_language/baseline/train_progress.txt'

path_to_output_val = '/home/jessed/data_storage/deep_vision_and_language/baseline/caffe_valid_fthn_fea8.mat'
path_to_save_val_results = '/home/jessed/data_storage/deep_vision_and_language/baseline/val_results.mat'
path_to_write_val_progress = '/home/jessed/data_storage/deep_vision_and_language/baseline/val_progress.txt'


%[recallOne,recallFive,recallTen,medianRecall] = evaluation_of_baseline(path_to_output_train, path_to_stored_variables)
%evaluation_of_baseline(path_to_output_val, path_to_stored_variables, path_to_save_val_results, path_to_write_val_progress)
evaluation_of_baseline(path_to_output_train, path_to_stored_variables, path_to_save_train_results, path_to_write_train_progress)
